# PNG-Storyboards

Aktive Bildserie fuer die neu organisierte Vorlesung 7:

- `01_iir/`
- `02_frequenzgang_iir/`
- `03_rekursives_iir_mehrere_taps/`
- `04_verschobene_impulsantwort/`
- `05_feedforward_dirac_baustein/`
- `06_biquad_audiofilter/`

Diese Ordner enthalten die bisher ausgearbeiteten Bildserien der Vorlesung.

Unterserien:

- `01A_dirac_impuls`
- `01B_stabil_impulsantwort`
- `01C_grenzstabil_impulsantwort`
- `01D_instabil_impulsantwort`
- `01E_iir_p_plus_05`
- `01F_iir_p_minus_05`

Block 2:

- `02A_geometric_series`
- `02B_iir_magnitude_examples`

Block 3:

- `03A_recursive_iir_frequency_examples` mit Log/dB- und linearer Magnitude-Darstellung
- `03B_impulse_response_build`
- `03C_ir_superposition`

Block 4:

- `04A_shifted_ir_frequency_response`
- `04B_weighted_shifted_spectra`

Block 5:

- `05A_shifted_dirac_fir_term`

Block 6:

- `06A_typical_audio_filters`
- `06B_biquad_cascades`

Die Filtergalerie zeigt pro Filterklasse eine Aufbau-Serie mit drei
Parametervarianten fuer den Betragsfrequenzgang. Die aktuelle Kurve ist gruen,
bereits eingefuehrte Varianten derselben Klasse bleiben grau sichtbar.
Zusaetzlich gibt es pro Filterklasse je eine gemeinsame Phasen- und
Gruppenlaufzeit-Abbildung. Alle Achsenflaechen sind pixelgenau gleich
positioniert, damit die Bilder beim Durchschalten nicht springen.

`06B_biquad_cascades` zeigt Kaskadierung:

- Tiefpass-Kaskade,
- Hochpass-Kaskade,
- DAW-artige EQ-Kaskade mit Low-Shelf, vier Peaking-EQs und High-Shelf.

Pro Kaskade gibt es Betrag, Phase und Gruppenlaufzeit. Die Betragsplots nutzen
`-12...+12 dB`. Die Einzelstufen sind grau, die Gesamtkaskade ist gruen; bei
der DAW-Kaskade ist die Legende bewusst kompakt gehalten.

Weitere Bloecke werden erst angelegt, wenn die entsprechenden Storyboards wirklich erstellt werden.
