# Block 2: Filtertypen, Parameter und Allpass

Ziel: TP, HP, BP, BR/Notch und Allpass mit ihren zentralen
Parametern wiederholen.

Geplante Bildideen:

- Betrag in dB und Phase pro Filtertyp
- logarithmische Frequenzachse von 20 Hz bis 20 kHz bei \(f_s=48\,\mathrm{kHz}\)
- Betragsachse von \(-15\,\mathrm{dB}\) bis \(5\,\mathrm{dB}\)
- Einordnung von \(f_c\), \(Q\), Bandbreite und Gain
- Phasenlage an der Cutoff- beziehungsweise Mittenfrequenz
- Frequenzen: Low-pass \(5\,\mathrm{kHz}\), High-pass \(200\,\mathrm{Hz}\),
  Band-pass/Notch/All-pass \(500\,\mathrm{Hz}\)
- Zusatzserie mit etwas höherer Güte \(Q=1.25\); die Referenzgüte
  \(Q=1/\sqrt{2}\) bleibt grau sichtbar. Der Achsenausschnitt bleibt
  gegenüber den Referenzabbildungen konstant.

Erzeugte Abbildungen:

- `01_low_pass_filter_response.png`: Low-pass mit magnitude response und gestrichelter phase response.
- `02_high_pass_filter_response.png`: High-pass mit magnitude response und gestrichelter phase response.
- `03_band_pass_filter_response.png`: Band-pass mit magnitude response und gestrichelter phase response.
- `04_band_stop_filter_response.png`: Band-stop mit magnitude response und gestrichelter phase response.
- `05_all_pass_filter_response.png`: All-pass zweiter Ordnung mit konstantem Betrag und gestrichelter phase response.
- `05a_all_pass_first_order_filter_response.png`: All-pass erster Ordnung mit konstantem Betrag und gestrichelter phase response.
- `06_low_pass_high_q_response.png`: Low-pass mit \(Q=1.25\) in Grün und Referenzgüte in Grau.
- `07_high_pass_high_q_response.png`: High-pass mit \(Q=1.25\) in Grün und Referenzgüte in Grau.
- `08_band_pass_high_q_response.png`: Band-pass mit \(Q=1.25\) in Grün und Referenzgüte in Grau.
- `09_band_stop_high_q_response.png`: Band-stop mit \(Q=1.25\) in Grün und Referenzgüte in Grau.
- `10_all_pass_high_q_response.png`: All-pass zweiter Ordnung mit \(Q=1.25\) in Grün und Referenzgüte in Grau.

Die rechte Phasenachse zeigt \(-\pi\), \(-\pi/2\), \(0\), \(\pi/2\) und \(\pi\).
