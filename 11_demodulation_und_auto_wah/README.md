# Vorlesung 11: Demodulation, Auto-Wah und Nichtlinearitäten

Diese Vorlesung nimmt die aus Vorlesung 10 verschobenen Demodulatoren auf und
führt anschließend in nichtlineare Systeme ein. Die Vorlesung ist jetzt gekürzt:
musikalische Verzerrung, Sättigung und Dynamic Range Control beginnen in
Vorlesung 12.

Referenz ist Zölzer, DAFX:

- Kapitel 3.3: Demodulators
- Kapitel 4.1 und 4.1.1: Nonlinear Processing, statische Kennlinien
- Kapitel 4.2 als Ausblick auf Oversampling bei nichtlinearen Effekten

## Zentrale Dateien

- `00_lehrkonzept_vorlesung_11.md`
- `01_storyboard_und_exportplan.md`
- `png_storyboards/`
- `audio_exports/`

## Blockstruktur

- `01_demodulators_envelope_followers`
  - `01a_detector_types`
  - `01b_averager_smoothing`
  - `01c_envelope_follower_control`
  - `01d_attack_release_build`
- `02_applications_auto_wah_morphing`
  - `02a_sidechain_auto_wah`
- `03_nonlinear_processing_intro`
  - `03A_delay_clipper_helix`
  - `03B_harmonic_decomposition`
  - `03C_real_cos_harmonic_decomposition`
- `04_imd`
  - `04A_single_sine`
  - `04B_two_sine_mixture`
- `05_aliasing`
  - `05A_48khz`
  - `05B_96khz`
  - `05C_192khz`
  - `05D_384khz`

## Inhaltlicher Fokus

- Demodulatoren als Gewinnung von Steuersignalen aus Audiosignalen
- Detektoren, Mittelung, Zeitkonstanten, Attack und Release
- Sidechain Auto-Wah als Anwendung: Envelope steuert Bandpass-Mittenfrequenz
- lineares System versus nichtlineares System
- statische Kennlinie als Taylor-Reihe
- harmonische Verzerrungen bei einem Sinus
- Intermodulationsverzerrungen bei zwei Sinussignalen
- digitales Aliasing nichtlinear erzeugter Obertöne und Oversampling

## Reaper-Plugins

- `audio_exports/reaper_jsfx/simple_sidechain_auto_wah.jsfx`
- `audio_exports/reaper_jsfx/simple_oversampling_sine_clipper.jsfx`

## Exportskripte

- `export_block_01_demodulators_envelope_followers.py`
- `export_block_02_applications_auto_wah_morphing.py`
- `export_block_03_1_delay_clipper_helix.py`
- `export_block_03_1_harmonic_decomposition.py`
- `export_block_03_1c_real_cos_harmonic_decomposition.py`
- `export_block_03_2_imd.py`
- `export_block_03_3_aliasing.py`
