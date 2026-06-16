# Block 5: z-Transformation als verallgemeinerte komplexe Schwingung

Diese Bildserie zeigt die Zeitfunktion

$$
x_z[n]=z^n=r^n e^{j\Omega n}
$$

fuer unterschiedliche Radien und Frequenzen.

- `05A_r_1_unit_circle`: stationaere Schwingungen auf dem Einheitskreis
- `05B_r_less_1_decay`: abklingende Schwingungen mit \(r<1\)
- `05C_r_greater_1_growth`: aufschwingende Schwingungen mit \(r>1\)
- `05D_r_pole_radius`: natuerlicher Biquad-Modus mit
  \(r=|p|\approx0.6911\)
- `05E_biquad_poles_zeros_2d`: reines Pol-Nullstellen-Diagramm des
  Biquad-Hochpasses in der 2D-z-Ebene, ohne Zeiger und ohne Helix

Die absolute Startamplitude ist in den Abbildungen \(A=1\). Der Radius \(r\)
beschreibt daher die Huelle pro Sample: \(r^n\). Die eigentliche
z-Transformationssumme nutzt den Kern \(z^{-n}\); fuer die Systemintuition ist
\(z^n\) die anschauliche Zeitfunktion, weil Pole und natuerliche Systemanteile
ebenfalls als \(p^n\) sichtbar werden.

In `05A_r_1_unit_circle` wird fuer jeden diskreten Analysekern die
Systemantwort des Biquad-Hochpasses aus Block 4D zunaechst als
2D-Frequenzgang wie in Block 4D gezeigt: vollstaendig grau, bis zur aktuellen
Zeigerposition gruen. Danach folgt fuer alle Radiusfaelle dieselbe Auswertung
als 3D-Kurve ohne Flaeche. Die Kurve liegt fuer \(r=1\) auf dem
Einheitskreis, fuer \(r=0.86\) innerhalb, fuer \(r=1.08\) ausserhalb und fuer
\(r=|p|\) auf dem Polradius. Beim Polwinkel \(\Omega\approx0.1234\pi\) trifft
die letzte Serie den Pol des Biquads.

Die z-Ebene markiert die doppelte Nullstelle des Biquad-Hochpasses bei
\(z=1\). In der \(r>1\)-Serie werden die konjugiert-komplexen Polstellen von
Anfang an mit gezeigt. In der Polradius-Serie werden sie erst eingeblendet,
sobald der aktive Zeiger den Polwinkel erreicht oder ueberschritten hat.
Dieselbe Logik gilt in der 2D-z-Ebene und unten in den 3D-Darstellungen.
