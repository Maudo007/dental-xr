# Dental XR Viewer – Prototyp

Ein Viewer für STL-, PLY-, OBJ- und GLB-Modelle, der im Browser der **Meta Quest 3** läuft (WebXR).
Es muss keine App installiert werden. **Die Dateien werden nur lokal im Browser geöffnet und nicht hochgeladen.**

Der Viewer besteht aus einer einzigen Datei: `index.html`.

---

## 1. Workflow: vom Fall zur Brille

1. **Planung wie bisher** (R2Gate, coDiagnoSiX, Diagnocat …): DVT und Intraoralscan ausrichten und segmentieren.
2. **Alle Segmente eines Falls als STL exportieren**, z. B. OK, UK, Nervkanal, Zähne, Implantat und Bohrschablone.
   Wichtig: Alle Dateien müssen aus **demselben Projekt** stammen, damit sie dasselbe Koordinatensystem haben.
3. **Dateinamen pseudonymisieren** (z. B. `Fall07_UK.stl`), denn der Dateiname wird in der Brille angezeigt.
4. Optional: **sehr große Dateien verkleinern.** Ein OK mit ca. 1,4 Mio. Dreiecken (≈ 70 MB) läuft auf der Quest 3 eher zäh.
   Mit Blender (Modifier „Decimate“) oder Meshmixer auf ca. 200.000–300.000 Dreiecke reduzieren.
   Für die Darstellung reicht das völlig.
5. STLs auf die Quest übertragen (siehe Abschnitt 3) und im Viewer laden.

## 2. Viewer bereitstellen (einmalig)

WebXR funktioniert nur über **HTTPS**. Am einfachsten geht das mit **GitHub Pages** (kostenlos):

1. Auf github.com ein Konto anlegen und ein neues Repository erstellen, z. B. `dental-xr`.
2. Die Datei `index.html` hochladen („Add file → Upload files“).
3. Unter *Settings → Pages* die Option *Branch: main* wählen und speichern.
4. Nach ca. 1 Minute ist der Viewer unter `https://<name>.github.io/dental-xr/` erreichbar.
   Diesen Link geben Sie den Studierenden.

Auf dem Server liegt nur der Viewer selbst und **keine Patientendaten**.
Die Brille braucht Internet, weil die 3D-Bibliothek (three.js) beim Öffnen geladen wird.

## 3. STL-Dateien auf die Quest bringen

- **Per USB-Kabel:** Quest an den Mac anschließen, in der Brille „Zugriff auf Daten erlauben“ bestätigen und die Dateien
  mit *OpenMTP* oder *Android File Transfer* in den Ordner `Download` kopieren.
- **Per Download:** die Datei in der Brille aus einem (institutionellen) Cloud-Ordner herunterladen. Dabei nur pseudonymisierte Daten verwenden.

Danach im Quest-Browser auf **„Dateien laden“** tippen und die STLs auswählen. Mehrere Dateien gleichzeitig wählen ist möglich.

## 4. Bedienung

**Am Bildschirm (vor dem Start in der Brille, auch am Mac zum Vorbereiten):**

- *Ausrichtung:* DICOM-basierte STLs liegen meist mit Z nach oben. Ein Klick auf **„X 90°“** stellt das Modell auf.
- *Deckkraft und Farbe* pro Segment einstellen, z. B. den Knochen halbtransparent machen, damit Nerv und Implantat sichtbar werden.
- *Schnittebene:* den Schnitt entlang der Achse X, Y oder Z verschieben.
- *Landmarken:* 3 gut tastbare Punkte am Modell anklicken, z. B. Höckerspitze 16, Höckerspitze 26 und Inzisalkante 31.

**In der Brille (Controller und Hand-Tracking funktionieren beide):**

In der Brille ist **nur das Modell** zu sehen, frei schwebend im Raum. Menü, Strahlen und Controller-Modelle sind ausgeblendet.

| Aktion | Controller | Hand |
|---|---|---|
| Menü ein-/ausblenden | Taste **B** oder **Y** | **Doppel-Pinch** ins Leere |
| Registrierung starten | Taste **A** oder **X** | Menü öffnen, dann „Registrieren“ |
| Modell greifen, bewegen, drehen | Grifftaste (seitlich) oder Trigger | Pinch |
| Skalieren | mit beiden Controllern greifen und auseinanderziehen | mit beiden Händen greifen und auseinanderziehen |
| Menü-Knopf drücken (nur bei offenem Menü) | Strahl auf den Knopf, Trigger | auf den Knopf zeigen, Pinch |

Im Menü stehen außerdem: Segmente ein/aus, Deckkraft (100/60/30 %), Schnittebene, Größe **1:1 / ×2 / ×4**, „Vor mich“, Fixieren/Lösen und Registrierung.
Kurze Hinweise (z. B. „Punkt 2/3 antippen“) erscheinen kurz unten im Blickfeld und verschwinden wieder.

## 5. Matching mit dem Patienten (3-Punkt-Verfahren, ohne Marker)

1. Am Bildschirm 3 Landmarken am Modell setzen (siehe oben). Alternativ geht das auch in der Brille über „Landmarken“.
2. In der Brille die Taste **A/X** drücken oder im Menü **„Registrieren“** wählen. Das Menü verschwindet daraufhin.
3. Dieselben 3 Punkte **in derselben Reihenfolge** am Phantom oder Patienten antippen:
   - *Hand:* genau am Punkt pinchen
   - *Controller:* mit der Spitze des Controllers an den Punkt gehen und den Trigger drücken
4. Das Modell springt in Originalgröße (1:1) auf den Patienten und wird **fixiert**. Greifen ist dann gesperrt,
   damit es sich während der Behandlung nicht verschiebt. Die mittlere Abweichung der 3 Punkte wird kurz in mm angezeigt.
5. Lösen geht über das Menü („Fixiert – lösen“). Neu registrieren geht jederzeit mit A/X.

**Grenzen:** Das Modell ist im **Raum** verankert, nicht am Kopf. Bewegt sich der Kopf, muss neu registriert werden.
Die Genauigkeit der Quest 3 liegt im Millimeter- bis Zentimeterbereich.
Der Viewer ist deshalb für **Lehre, Phantomkurs und Aufklärung** gedacht. Für Navigation ist er ungeeignet,
und für die klinische Anwendung gelten MDR-Vorgaben und ein Ethikvotum.

## 6. Testen am Mac ohne Brille

Die Seite lässt sich auch am Mac öffnen (Chrome oder Safari). Laden, Ausrichten, Schnittebene und Landmarken funktionieren dort normal.
Die Knöpfe „AR/VR starten“ sind nur in der Brille aktiv.

## 7. Mögliche nächste Schritte

- Große Scans automatisch im Viewer verkleinern
- Mehrere Fälle als Liste, die Studierenden per Link öffnen
- Gemeinsame Sitzung: Dozent und Studierende sehen dasselbe Modell
- Vision Pro: grundsätzlich lauffähig (Safari, VR-Modus), noch nicht getestet
