# Vorlesung 10: Modulation und Morphing

Vorlesung 10 ist der zweite Teil des Audio-FX-Blocks:

- VL9: Filter und Delay-basierte Audioeffekte
- VL10: Modulation und Morphing
- VL11: Demodulation, Auto-Wah und weitere Inhalte

Referenzen für Vorlesung 10:

- Zölzer 2011, Kapitel 3 "Modulators and demodulators"
- Wardle 1998, "A Hilbert-transformer frequency shifter for audio"

## Zentrale Dateien

- `00_lehrkonzept_vorlesung_10.md`
- `01_storyboard_und_exportplan.md`
- `png_storyboards/`
- `audio_exports/`

## Blockstruktur

- `01_audio_fx_roadmap`
- `02_am_modulation`
- `03_single_sideband_modulator`
- `04_pm_fm_delayline_modulation`
- `05_applications_stereo_phaser_rotary`

Die ursprünglich geplanten Blöcke `06_demodulators_envelope_followers`
und `07_applications_auto_wah_morphing` wurden nach
`../11_demodulation_und_auto_wah/` verschoben.

## Inhaltlicher Fokus

- Ringmodulation und Amplitudenmodulation als Multiplikation im Zeitbereich
- Seitenbänder im Spektralbereich
- Zeigerprodukt-Erklärung für Summen- und Differenzfrequenzen
- Tremolo, Rauigkeit und hörbare Seitenbänder über die Modulationsfrequenz
- Single-Side-Band-Modulation mit Hilbertfilter, Quadraturprodukten und
  USB/LSB-Auswahl
- Frequenz- und Phasenmodulation
- variable Delayline als Phasenmodulator
- Stereo Phaser als SSB-/Hilbert-Anwendung nach Wardle/Zölzer
- Rotary Speaker als Kombination aus Delayline-, Amplituden- und
  Stereo-Modulation

## Bewusste Ausgrenzung

- keine vollständige Nachrichtentechnik
- keine analoge Schaltungstechnik
- kein erneuter Vibrato-Block, da Vibrato in VL9 über fractional delay
  behandelt wurde
- kein vollständiger Pitch-Shifter oder Phase-Vocoder
- kein Modulation-Vocoder
- keine Dynamikprozessoren im Detail, da diese in Vorlesung 11 folgen
