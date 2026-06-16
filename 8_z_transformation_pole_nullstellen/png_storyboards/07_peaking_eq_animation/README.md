# Block 7: Peaking-EQ Sweep

Der Block enthaelt drei framegenau synchrone Animationen desselben
Peaking-EQ-Verlaufs:

- `01_spectrum_motion.gif`: Spektrum mit logarithmischer Frequenzachse und
  Betrag in dB und aktuellen Biquad-Koeffizienten
- `02_z_plane_2d_motion.gif`: Pol-Nullstellen-Bewegung in der 2D-z-Ebene
- `03_z_plane_3d_motion.gif`: zugehoerige 3D-z-Ebenenflaeche

Alle drei GIFs nutzen dieselbe Parameterfolge, dieselbe Framezahl und dieselbe
Bildrate. Der Peaking-EQ wandert mit logarithmisch gebremstem
Frequenzfortschritt von tiefen zu hohen Frequenzen; Gain und Guete steigen in
der Mitte deutlich an und sinken danach wieder. Der Gain wechselt dabei von
Cut zu Boost und zurueck zu Cut.
