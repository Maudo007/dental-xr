# Dental XR Viewer – Prototype

A viewer for STL, PLY, OBJ and GLB models that runs in the browser of the **Meta Quest 3** (WebXR).
No app needs to be installed. **Files are only opened locally in the browser and are never uploaded.**

**Live:** https://maudo007.github.io/dental-xr/

The viewer is a single file: `index.html`.

---

## 1. Workflow: from case to headset

1. **Plan as usual** (R2Gate, coDiagnostiX, Diagnocat …): align and segment the CBCT and the intraoral scan.
2. **Export all segments of a case as STL**, e.g. maxilla, mandible, nerve canal, teeth, implant and surgical guide.
   Important: all files must come from **the same project** so they share the same coordinate system.
3. **Pseudonymize the file names** (e.g. `Case07_mandible.stl`), because the file name is shown in the headset.
4. Optional: **reduce very large files.** A maxilla with about 1.4 million triangles (≈ 70 MB) runs sluggishly on the Quest 3.
   Use Blender (“Decimate” modifier) or Meshmixer to reduce it to about 200,000–300,000 triangles.
   That is plenty for visualization.
5. Transfer the STLs to the Quest (see section 3) and load them in the viewer.

## 2. Hosting the viewer (one-time)

WebXR only works over **HTTPS**. The easiest option is **GitHub Pages** (free):

1. Create an account on github.com and a new repository, e.g. `dental-xr`.
2. Upload the file `index.html` (“Add file → Upload files”).
3. Under *Settings → Pages* select *Branch: main* and save.
4. After about 1 minute the viewer is available at `https://<name>.github.io/dental-xr/`.
   Give this link to your students.

The server only hosts the viewer itself and **no patient data**.
The headset needs an internet connection because the 3D library (three.js) is loaded when the page opens.

## 3. Getting STL files onto the Quest

- **Via USB cable:** connect the Quest to your Mac, confirm “Allow access to data” in the headset and copy the files
  into the `Download` folder using *OpenMTP* or *Android File Transfer*.
- **Via download:** download the file in the headset from an (institutional) cloud folder. Use pseudonymized data only.

Then tap **“Load files”** in the Quest browser and select the STLs. Selecting several files at once is possible.

## 4. Controls

**On screen (before entering the headset view, also on the Mac for preparation):**

- *Orientation:* DICOM-based STLs are usually Z-up. Clicking **“X 90°”** stands the model upright.
- *Opacity and color* per segment, e.g. make the bone semi-transparent so the nerve and implant become visible.
- *Clipping plane:* move the cut along the X, Y or Z axis.
- *Landmarks:* click 3 easily palpable points on the model, e.g. cusp tip 16, cusp tip 26 and incisal edge 31.

**In the headset (both controllers and hand tracking work):**

In the headset you see **only the model**, floating freely in the room. Menu, rays and controller models are hidden.

| Action | Controller | Hand |
|---|---|---|
| Show/hide menu | **B** or **Y** button | **Double pinch** in empty space |
| Start registration | **A** or **X** button | Open the menu, then “Register” |
| Grab, move, rotate the model | Grip button (side) or trigger | Pinch |
| Scale | Grab with both controllers and pull apart | Grab with both hands and pull apart |
| Press a menu button (only while the menu is open) | Point the ray at the button, trigger | Point at the button, pinch |

The menu also offers: segments on/off, opacity (100/60/30 %), clipping plane, size **1:1 / ×2 / ×4**, “In front of me”, Lock/Unlock and Register.
Short hints (e.g. “Tap point 2/3 on the patient”) briefly appear at the bottom of your view and then disappear.

## 5. Matching to the patient (3-point method, markerless)

1. Set 3 landmarks on the model on screen (see above). Alternatively, use “Landmarks” in the headset menu.
2. In the headset press **A/X** or choose **“Register”** in the menu. The menu then disappears.
3. Tap the same 3 points **in the same order** on the phantom or patient:
   - *Hand:* pinch exactly at the point. A small cyan dot between your fingertips shows where the point will be saved.
   - *Controller:* during registration a thin **virtual needle** (10 cm) sticks out of the controller. Touch the point with the **cyan needle tip** and pull the trigger. A short vibration confirms the point.
4. The model jumps onto the patient at original size (1:1) and is **locked**. Grabbing is then disabled
   so it cannot shift during treatment. The mean deviation of the 3 points is briefly shown in mm.
5. Unlock via the menu (“Locked – unlock”). You can re-register at any time with A/X.

**Limitations:** The model is anchored in the **room**, not to the head. If the head moves, you need to register again.
The accuracy of the Quest 3 is in the millimeter-to-centimeter range.
The viewer is therefore intended for **teaching, phantom courses and patient education**. It is not suitable for navigation,
and clinical use is subject to MDR requirements and ethics approval.

## 6. Testing on a Mac without a headset

The page can also be opened on a Mac (Chrome or Safari). Loading, orientation, clipping and landmarks work normally there.
The “Start AR/VR” buttons are only active in the headset.

## 7. Possible next steps

- Automatically reduce large scans inside the viewer
- Several cases as a list that students open via link
- Shared session: instructor and students see the same model
- Vision Pro: should run in principle (Safari, VR mode), not yet tested

---

© 2026 Marcus Engelschalk. All rights reserved.
The viewer may be used via the website above for teaching and research. Copying, modifying, redistributing or commercial use of the code requires written permission. See [LICENSE](LICENSE).
