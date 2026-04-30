# 1 Fourier Transformation

Materialien der ersten Vorlesung zur Fourier-Transformation.

## Aufbau

Die Vorlesung ist jetzt wie Vorlesung 2 blockweise organisiert:

- Block `01`: Phasor-Intro
- Block `02`: Fourier-Transformation
- Block `03`: Reale Audiosignale und Phasenvariation
- Block `04`: Inverse Fourier-Transformation ohne Fensterung
- Block `05`: Inverse Fourier-Transformation mit Fensterung
- Block `06`: Aufgaben und Rekonstruktionsbeispiele

Gemeinsame Hilfsdateien:

- `fourier_phasor_core.py`: gemeinsame Signal- und Spektrumlogik
- `storyboard_paths.py`: zentrale Ausgabepfade

## Skripte Nach Block

- Block `01`
  - `export_block_01A_phasor_intro_animation.py`
  - `export_block_01B_phasor_components_animation.py`
  - `export_block_01C_sine_signal_phasor_animation.py`
  - `export_block_01D_real_signal_phasor_animation.py`
  - `export_block_01E_cosine_signal_only_animation.py`

- Block `02`
  - `export_block_02A_fourier_png_storyboard.py`
  - `export_block_02B_sine_two_sided_spectrum.py`
  - `export_block_02C_cosine_two_sided_spectrum.py`
  - `export_block_02D_mixed_signal_two_sided_spectrum.py`
  - `export_block_02E_mixed_signal_one_sided_windowed_spectrum.py`

- Block `03`
  - `export_block_03A_phase_shift_intro.py`
  - `export_block_03B_phase_shift_series.py`
  - `export_block_03C_phase_shift_series_cos_no_components.py`
  - `export_block_03D_phase_shift_series_mixed_extracted.py`

- Block `04`
  - `export_block_04A_inverse_ft_png_storyboard.py`
  - `export_block_04B_inverse_ft_one_sided_png_storyboard.py`

- Block `05`
  - `export_block_05A_inverse_ft_windowed_png_storyboard.py`

- Block `06`
  - `export_block_06A_homework_reconstruction_spectra.py`
  - `export_block_06B_zeitfunktion_zu_spektrum_waehlen.py`

## Output-Struktur

Die exportierten Serien liegen eindeutig blockweise unter:

- `png_storyboards/01_phasor_intro/`
- `png_storyboards/02_fourier_transformation/`
- `png_storyboards/03_reale_audiosignale/`
- `png_storyboards/04_inverse_fouriertransformation/`
- `png_storyboards/05_inverse_ft_mit_fensterung/`
- `png_storyboards/06_aufgaben/`

Innerhalb dieser Blockordner tragen die Unterordner jetzt ebenfalls die Blockkennung, zum Beispiel:

- `01A_phasor_intro_und_grundbilder`
- `02A_fourier_probe_serien/02A_probe_2_hz`
- `03D_phase_shift_series_mixed_extracted`
- `04A_inverse_ft_storyboard_serien/04A_inverse_ft_storyboard_t0p18`
- `05A_inverse_ft_windowed_storyboard_t0p18`
- `06A_homework_reconstruction_spectra`
- `06B_zeitfunktion_zu_spektrum_waehlen`

## Stilreferenz

Vorlesung 1 liefert weiterhin die gestalterische und didaktische Referenz für die späteren Blöcke:

- stabile Grundlayouts
- wenige neue Elemente pro Bildschritt
- klare Farbrollen für Signal, Vergleich, Hilfselemente und aktive Markierung

Die aktuell gueltigen Plotstandards sind zusätzlich im Root-Dokument
`00_vorlesungs_plot_stilguide.md` zusammengefasst.

## Interaktive App

Die Binder- und Notebook-fähige Variante liegt separat unter:

- `interactive_apps/1_fourier_transformation/`
