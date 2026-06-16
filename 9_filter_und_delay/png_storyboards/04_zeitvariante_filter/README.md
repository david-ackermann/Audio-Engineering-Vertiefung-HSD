# Block 4: Zeitvariante Filter

Ziel: Wah-Wah als bewegten Bandpass und Phaser als zeitvariante
Allpass-/Notch-Struktur zeigen.

Geplante Bildideen:

- Wah-Wah-Sweep: bewegter, auf 0 dB normalisierter TPT-SVF-Bandpasspeak
  - Startstandbild plus GIF fuer \(Q=5\)
  - zusaetzliches Startstandbild plus GIF fuer \(Q=15\)
  - weitere Serie mit \(Q=15\) und 50 Prozent Dry-Zumischung; \(MIX=0\) ist der reine Bandpass
  - dazu: statischer 2D Pol-/Nullstellenplot und statische 3D z-Ebene an der Referenz
- Phaser aus Allpass-Kaskade:
  - vier Standbilder zum Aufbau der Phaser-Notch:
    - Allpass A: Allpass zweiter Ordnung aus Block 2
    - Allpass B: Allpass zweiter Ordnung mit höherer Frequenz
    - Allpass-Kaskade \(A(z)B(z)\)
    - Dry plus Allpass-Kaskade
  - bewegte Notches durch vier zeitvariable Allpass-Stufen wie im Plugin
  - Startstandbild plus GIF
  - erste Serie ohne Feedback: \(f_b=0\)
  - dazu: statischer 2D Pol-/Nullstellenplot und statische 3D z-Ebene für den Summenfilter \(d+eA(z)B(z)\)
- Phaser-Feedback-Serie:
  - nur \(f_b\) wird bewegt
  - graue Referenz ist \(f_b=0\)
  - \(f_\mathrm{AP}\), \(a\) und \(e\) bleiben konstant
  - Startstandbild plus GIF
- Phaser-Dry/Wet-Serie:
  - Mix als Tiefenregler der Ausloeschungen
  - Startstandbild plus GIF
- Spektrogramme eines bandbegrenzten Rechtecksignals:
  - Wah-Wah als bewegter Bandpass
  - Phaser als zeitvariante Allpass-/Notch-Struktur

Render-Skripte:

- `export_block_04_wah_wah.py`: rendert nur die Wah-Wah-Abbildungen.
- `export_block_04_phaser.py`: rendert nur die Phaser-Abbildungen.
- `export_block_04_zeitvariante_filter.py`: rendert den gesamten Block.

Erzeugte Spektrogramme:

- `17_square_wah_wah_spectrogram.png`
- `18_square_phaser_spectrogram.png`
