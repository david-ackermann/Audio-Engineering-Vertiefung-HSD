# Vorlesungs-Plot-Stilguide

Diese Datei fasst das aktuelle Erscheinungsbild der Vorlesungsplots zusammen. Sie soll für neue Vorlesungen als verbindliche Referenz dienen, damit Layout, Farben und Schriftgrössen konsistent bleiben.

## Ablageort

Die Datei liegt bewusst ganz oben im `Python`-Ordner. Das ist sinnvoll, weil sie damit nicht an einen einzelnen Themenblock gebunden ist und für `1_fourier_transformation`, `2_fensterung_und_faltung` und spätere Vorlesungen gleichermassen als gemeinsame Stilreferenz dient.

## Exportstandard

- Backend: `matplotlib.use("Agg")`
- Export: `dpi = 200`
- Hintergrund: weiss
- Grundregel: keine überladenen Figuren, lieber mehrere kleine Bildschritte

## Standardformate

Diese Formate sind aktuell etabliert und sollten nach Möglichkeit wiederverwendet werden:

- Standard-Einzelplot: `figsize = (12.0, 4.4)`
- Standardspektrum: `figsize = (11.0, 4.8)`
- Vertikale Dreierfigur: `figsize = (12.0, 11.2)`
- Referenz-Zweierfigur: `figsize = (12.0, 6.6)`
- Quadratische komplexe Ebene: `figsize = (6.8, 6.8)`
- Breiter Zoom-Plot: `figsize = (8.6, 3.0)`
- 3D-Helix: `figsize = (14.2, 8.8)`

## Standardränder

Für normale 2D-Plots:

- `left = 0.10`
- `right = 0.98`
- `bottom = 0.18`
- `top = 0.86`

Für Referenz-Zweier- und Dreierfiguren:

- `bottom = 0.10`
- `top = 0.92`

Für breite Zoomplots:

- `left = 0.08`
- `right = 0.98`
- `bottom = 0.18`
- `top = 0.95`

## Schriftgrössen

Für präsentationstaugliche Lesbarkeit:

- Titel: `24`
- Achsenbeschriftung: `20`
- Tick-Labels: `17`
- Legende: `14`

Für kleinere Vergleichs- oder Referenzplots:

- Titel: `22`
- Achsenbeschriftung: `18`
- Tick-Labels: `15`
- Legende: `13`

## Farbpalette

Verbindliche Hauptfarben:

- neutrales Signal / Endergebnis: `SIGNAL_BLACK = "0.10"`
- aktive Standardsprache Blau: `SPECTRUM_BLUE = "#2b7bbb"`
- Vergleichsspur Orange: `COMPARE_ORANGE = "#d98c2f"`
- Fenster-Grün: `WINDOW_GREEN = "#66b77a"`
- Blackman-Rotbraun: `BLACKMAN_RED = "#c45b4d"`
- aktive Markierung / Cursor / Probe: `ACTIVE_RED = "crimson"`

Hilfs- und Referenzfarben:

- Grid / Nulllinie: `GRID_GREY = "0.75"`
- Support- und Begrenzungslinien: `BOUNDARY_GREY = "0.72"`
- mittlere Vergleichsgrauwerte: `GREY_MEDIUM = "0.55"`
- sehr helle Referenz für kleinen Fensterfall: `SMALL_WINDOW_GREY = "0.90"`
- rechteckige Referenz im Hintergrund: `"0.87"`
- ungefensterte Referenz im IR-Block: `"#bddcf3"`
- helle Summenspur in 3D: `"#de8d8d"`

## Rollenlogik

- Schwarz: neutrales Signal, Produkt aus Signal und Fenster, finales beobachtetes Spektrum
- Blau: Standardsignal, aktive Grundspur, ungefensterte IR
- Grün: Rechteckfenster und Fensterspektrum
- Orange: Hammingfenster und zweite Vergleichsspur
- Rotbraun: Blackmanfenster
- Rot: aktive Frequenzmarkierung, aktueller Cursor, Probe, Summenvektor
- Hellgrau: Referenzfall im Hintergrund, bereits erklärte oder bewusst inaktive Spur

## Linienstärken

Bewährte Richtwerte:

- normale Kurven: `lw = 1.6` bis `2.4`
- hervorgehobene Endkurven: `lw = 2.6`
- Spektrallinien / Markerlinien: `lw = 2.5` bis `3.2`
- Support- und Hilfslinien: `lw = 1.2` bis `1.3`, meist gestrichelt

## Grid und Achsen

- Grid immer sichtbar, aber zurückhaltend: `alpha = 0.25`
- horizontale Nulllinie in Grau mit `lw = 0.9`
- bei zentrierten Zeitplots zusätzlich vertikale Nulllinie
- Zoomplots duerfen Achsentitel und Zahlen ausblenden, Ticks und Grid bleiben aber sichtbar

## Titelstil

- Titel kurz halten
- keine langen Erklärsätze im Plot
- Inhalt lieber über Bildfolge statt über Titel erklären
- bei datensatzbezogenen Serien Prefix verwenden:
  - `Hochtöner: ...`
  - `Tieftöner: ...`

## Legendenstil

- nur dann Legenden zeigen, wenn sie für den Bildschritt wirklich helfen
- wenn möglich nur in einem Teilplot der Figur
- Referenzlinien in sehr hellem Grau nicht zwangsläufig in die Legende aufnehmen
- bei ruhigen Einzelplots bevorzugt links mittig oder links oben platzieren

## Didaktische Bildlogik

- pro Abbildung nur ein neuer gedanklicher Schritt
- erst Zutaten, dann Produkt, dann Resultat
- Vergleich immer mit identischen Achsen, wenn inhaltlich möglich
- bei Serien das Layout nicht zwischen zwei direkt zu vergleichenden Abbildungen ändern
- für Zooms eigenes Format verwenden, damit sie wie ein echter Ausschnitt wirken

## Benennungskonvention

- Nummerierung immer mit führender Null: `01`, `02`, ...
- sprechende Dateinamen ohne Leerzeichen
- Unterserien mit `A`, `B`, ... nur auf Blockebene verwenden, nicht innerhalb eines einzelnen Plotnamens

## Empfehlung für neue Vorlesungen

Wenn ein neuer Vorlesungsblock entsteht:

1. zuerst eines der bestehenden Exportskripte als Stilvorlage kopieren
2. Schriftgrössen und Grundformat unverändert lassen
3. nur dann neue Farben einführen, wenn die bestehende Rollenlogik nicht ausreicht
4. neue Zoomfiguren wieder im breiten Rechteckformat anlegen
5. neue Blockkonzepte weiterhin im jeweiligen Themenordner dokumentieren

So bleibt der Gesamtauftritt über mehrere Vorlesungen hinweg stabil.
