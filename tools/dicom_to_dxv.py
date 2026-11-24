#!/usr/bin/env python3
"""Convert a DVT/CBCT DICOM folder into one compact, anonymized .dxv file for the Dental XR Viewer.

Usage:
    python3 dicom_to_dxv.py <dicom_folder> <output.dxv> [--factor 2]

Requires: pydicom, numpy  (pip install pydicom numpy)

Only voxel values and geometry are written. No DICOM header fields (patient name,
birth date, IDs, institution, physician, dates) end up in the output file.

File layout (.dxv, little endian):
    4 bytes   magic "DXV1"
    4 bytes   uint32 length of the JSON header
    N bytes   JSON header (UTF-8): dims [nx, ny, nz], spacing [sx, sy, sz] in mm,
              origin [x, y, z] = centre of voxel (0, 0, 0) in DICOM patient coordinates (mm),
              valueMin / valueMax = values mapped to byte 0 / 255
    nx*ny*nz  uint8 voxels, x fastest (column), then y (row), then z (slice)
"""
import argparse, glob, json, os, struct, sys
import numpy as np
import pydicom

VMIN, VMAX = -1000.0, 3000.0     # value range stored in 8 bit (≈ 16 units per step)
AIR = -500.0                     # everything below counts as air when cropping
MARGIN_MM = 3.0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('folder')
    ap.add_argument('out')
    ap.add_argument('--factor', type=int, default=2, help='downsampling factor (default 2: 0.16 mm → 0.32 mm)')
    a = ap.parse_args()
    f = max(1, a.factor)

    files = sorted(glob.glob(os.path.join(a.folder, '**', '*'), recursive=True))
    slices = []
    for p in files:
        if not os.path.isfile(p):
            continue
        try:
            h = pydicom.dcmread(p, stop_before_pixels=True)
        except Exception:
            continue
        if not hasattr(h, 'ImagePositionPatient') or not hasattr(h, 'PixelSpacing'):
            continue
        slices.append((float(h.ImagePositionPatient[2]), p, h))
    if not slices:
        sys.exit('No DICOM image slices found.')
    series = {s[2].SeriesInstanceUID for s in slices}
    if len(series) > 1:
        sys.exit(f'Folder contains {len(series)} series. Please export only the DVT volume.')
    slices.sort(key=lambda s: s[0])
    h0 = slices[0][2]
    iop = [round(float(v), 3) for v in h0.ImageOrientationPatient]
    if iop != [1, 0, 0, 0, 1, 0]:
        sys.exit(f'Unsupported slice orientation {iop} (expected axial 1,0,0,0,1,0).')
    rows, cols = int(h0.Rows), int(h0.Columns)
    sy, sx = (float(v) for v in h0.PixelSpacing)
    zs = np.array([s[0] for s in slices])
    sz = float(np.median(np.diff(zs))) if len(zs) > 1 else float(getattr(h0, 'SliceThickness', sx))
    x0, y0 = (float(v) for v in h0.ImagePositionPatient[:2])
    print(f'{len(slices)} slices, {cols}x{rows}, spacing {sx}/{sy}/{sz:.3f} mm')

    # read + downsample in blocks of f slices to keep memory low
    ny, nx = rows // f, cols // f
    out = []
    for k in range(0, len(slices) - f + 1, f):
        acc = np.zeros((ny, nx), np.float32)
        for _, p, _h in slices[k:k + f]:
            d = pydicom.dcmread(p)
            img = d.pixel_array.astype(np.float32) * float(getattr(d, 'RescaleSlope', 1)) + float(getattr(d, 'RescaleIntercept', 0))
            img = img[:ny * f, :nx * f].reshape(ny, f, nx, f).mean(axis=(1, 3))
            acc += img
        out.append(acc / f)
        if (k // f) % 40 == 0:
            print(f'  {k + f}/{len(slices)} slices')
    vol = np.stack(out)                      # (nz, ny, nx)

    # crop to non-air region
    mask = vol > AIR
    if mask.any():
        m = int(round(MARGIN_MM / (sx * f)))
        idx = [np.where(mask.any(axis=tuple(j for j in range(3) if j != ax)))[0] for ax in range(3)]
        lo = [max(0, int(i.min()) - m) for i in idx]
        hi = [min(vol.shape[ax], int(i.max()) + 1 + m) for ax, i in enumerate(idx)]
        vol = vol[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]]
    else:
        lo = [0, 0, 0]

    spacing = [sx * f, sy * f, sz * f]
    # centre of downsampled voxel (0,0,0) = mean of the f original voxel centres
    origin = [x0 + (f - 1) / 2 * sx + lo[2] * spacing[0],
              y0 + (f - 1) / 2 * sy + lo[1] * spacing[1],
              float(zs[0]) + (f - 1) / 2 * sz + lo[0] * spacing[2]]
    data = np.clip(np.round((vol - VMIN) / (VMAX - VMIN) * 255), 0, 255).astype(np.uint8)
    nz2, ny2, nx2 = data.shape
    header = json.dumps({'format': 'dxv', 'version': 1, 'dims': [nx2, ny2, nz2], 'spacing': spacing,
                         'origin': origin, 'valueMin': VMIN, 'valueMax': VMAX}).encode()
    with open(a.out, 'wb') as fh:
        fh.write(b'DXV1' + struct.pack('<I', len(header)) + header)
        fh.write(np.ascontiguousarray(data).tobytes())
    print(f'Wrote {a.out}: {nx2}x{ny2}x{nz2} voxels at {spacing[0]:.2f} mm, {os.path.getsize(a.out) / 1e6:.1f} MB')


if __name__ == '__main__':
    main()
