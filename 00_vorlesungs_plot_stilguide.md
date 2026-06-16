# Vorlesungs-Plot-Stilguide

Diese Datei fasst das aktuelle Erscheinungsbild der Vorlesungsplots zusammen. Sie soll für neue Vorlesungen als verbindliche Referenz dienen, damit Layout, Farben und Schriftgrößen konsistent bleiben.

## Ablageort

Die Datei liegt bewusst ganz oben im `Python`-Ordner. Das ist sinnvoll, weil sie damit nicht an einen einzelnen Themenblock gebunden ist und für `1_fourier_transformation`, `2_fensterung_und_faltung` und spätere Vorlesungen gleichermaßen als gemeinsame Stilreferenz dient.

## Exportstandard

- Backend: `matplotlib.use("Agg")`
- Export: `dpi = 200`
- Hintergrund: weiß
- Grundregel: keine überladenen Figuren, lieber mehrere kleine Bildschritte

## Standardformate

Diese Formate sind aktuell etabliert und sollten nach Möglichkeit wiederverwendet werden:

- Standard-Einzelplot: `figsize = (12.0, 4.4)`
- Standardspektrum: `figsize = (11.0, 4.8)`
- Diskrete Einzelfolge / Stem-Plot: `figsize = (10.5, 4.2)`
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

## Schriftgrößen

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

Für diskrete Folgen in Präsentationsfolien:

- Titel: `26`
- Achsenbeschriftung: `24`
- Tick-Labels: `18`
- Stem-Marker: `8`
- Stem-Linienstärke: `2.8`

## Farbpalette

Verbindliche Hauptfarben:

- neutrales Signal / Endergebnis: `SIGNAL_BLACK = "0.10"`
- aktive Standardsprache Blau: `SPECTRUM_BLUE = "#2b7bbb"`
- Vergleichsspur Orange: `COMPARE_ORANGE = "#d98c2f"`
- Modulationssignale und extrahierte Steuersignale: `MODULATION_VIOLET = "#7b4ab8"`
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
- Blau: Standardsignal, aktive Grundspur, ungefensterte IR, berechnetes Ausgangssignal einer Modulation
- Bei Systemabbildungen mit diskreten Folgen: Eingangssignale immer schwarz, Ausgangssignale immer blau
- Violett: Modulationssignale und aus Demodulation extrahierte Steuersignale, zum Beispiel LFOs, Hüllkurven und Parameterverläufe
- Grün: Systemantworten wie $h[n]$ und $H[k]$ beziehungsweise $H(e^{j\Omega})$; außerdem Rechteckfenster und Fensterspektrum in den früheren Fensterungsblöcken
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
- Zoomplots dürfen Achsentitel und Zahlen ausblenden, Ticks und Grid bleiben aber sichtbar

## Diskrete Folgen und GIFs

Für einfache Folgenplots, Systemantworten und spätere animierte GIFs gilt:

- Eingangssignale wie `x[n]` oder `\delta[n]`: schwarz
- Ausgangssignale wie `y[n]`: blau
- Systemantworten wie `h[n]`, `H[k]` und `H(e^{j\Omega})`: grün
- y-Bereich bei normalisierten Beispielen fest auf etwa `[-1.05, 1.05]`
- x-Achse als Sampleindex zeigen, bei englischen Abbildungen `Sample index n`
- diskrete Spektralbeispiele in frühen Systemfolien als Bin-Folgen zeigen, bei englischen Abbildungen `Frequency bin k`
- reine DFT-Bin-Darstellungen auf der x-Achse als `DFT bin k` beschriften; Übergangsbilder dürfen die $H(e^{j\Omega})$-Hüllkurve ebenfalls über `DFT bin k` zeigen, bevor die allgemeine Darstellung mit normierter Kreisfrequenz `Normalized frequency $\Omega/\pi$` folgt
- Grid zurückhaltend mit `alpha = 0.25`
- Nulllinie deutlich in Schwarz mit `lw = 1.2`
- oberer und rechter Rahmen werden ausgeblendet
- keine erklärenden Zusatztexte im Plot, wenn die Abbildung in der Folie kommentiert wird
- bei GIFs Achsenlimits, Titelposition, Grid und Ränder über alle Frames konstant halten
- GIF-Frames einzeln in derselben PNG-Qualität rendern und danach animieren, damit nichts springt

## Titelstil

- Titel kurz halten
- keine langen Erklärsätze im Plot
- Inhalt lieber über Bildfolge statt über Titel erklären
- bei datensatzbezogenen Serien Prefix verwenden:
  - `Hochtöner: ...`
  - `Tieftöner: ...`

## Sprachkonvention

- Sichtbare deutsche Texte werden mit Umlauten und `ß` geschrieben.
- Keine ASCII-Umschreibungen wie `fuer`, `ueber`, `groesser`, `weiss` oder `Anstoss` in Folientexten, Markdown-Konzepten und Plotlabels verwenden.
- Dateinamen, Pfade, Python-Bezeichner und technische IDs bleiben ASCII, wenn das für Stabilität oder Reproduzierbarkeit sinnvoll ist.

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
2. Schriftgrößen und Grundformat unverändert lassen
3. nur dann neue Farben einführen, wenn die bestehende Rollenlogik nicht ausreicht
4. neue Zoomfiguren wieder im breiten Rechteckformat anlegen
5. neue Blockkonzepte weiterhin im jeweiligen Themenordner dokumentieren

So bleibt der Gesamtauftritt über mehrere Vorlesungen hinweg stabil.
