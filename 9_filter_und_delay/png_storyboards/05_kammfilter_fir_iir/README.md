# Block 5: Kammfilter FIR und IIR

Ziel: Feedforward-Comb und Feedback-Comb ueber Delayzeit, Gain, Frequenzgang
und Stabilitaet unterscheiden.

Didaktische Einordnung: Der Comb-Filter wird aus einer Delayline gebaut, wird
hier aber zuerst als Filterwirkung durch Interferenz gezeigt.

Geplante Bildideen:

- FIR-Comb-Impulsantwort und Betrag
- IIR-Comb-Impulsantwort und Betrag
- Kammabstand \(\Delta f=f_s/M\)
- Einfluss von \(g\) und \(M\)

Erzeugte Abbildungen:

- `01_fir_comb_initial_delay.png`
- `02_fir_comb_delay_comparison.png`
- `03_iir_comb_initial_delay.png`
- `04_iir_comb_delay_comparison.png`
- `05_fir_comb_z_plane_2d.png`
- `06_fir_comb_z_plane_3d.png`
- `07_iir_comb_z_plane_2d.png`
- `08_iir_comb_z_plane_3d.png`
- `09_fir_comb_dense_z_plane_2d.png`
- `10_iir_comb_dense_z_plane_2d.png`

Die Bildserie zeigt zuerst \(M=6\) in Gruen und danach \(M=6\) in Grau plus
\(M=10\) in Gruen. Die Frequenzachse ist die normierte Kreisfrequenz
\(\Omega/\pi\). Positive Filterkoeffizienten sind durchgezogen, negative
Filterkoeffizienten gestrichelt. Die Filter sind so normiert, dass die maximale
Amplitude bei \(0\,\mathrm{dB}\) liegt.

Die Systemfunktionen werden nicht in den Spektrum-Plots gezeigt. Stattdessen
zeigen die z-Ebenen-Abbildungen die Pol-/Nullstellenlage und die zugehoerige
3D-Auswertung von \(|H(z)|\) im Layout der 8. Vorlesung.
Die 2D-Pol-/Nullstellendiagramme `05` und `07` zeigen die weniger dichte
Variante mit \(M=6\). Die zusaetzlichen Diagramme `09` und `10` zeigen die
dichtere Variante mit \(M=10\).
