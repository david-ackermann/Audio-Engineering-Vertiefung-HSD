# Storyboard- und Exportplan Vorlesung 11

Die Vorlesung 11 ist gekürzt und endet bei Aliasing/Oversampling. Die folgenden
Blöcke sind die aktuelle Zielstruktur für Folien und Exportskripte.

## Block 1: Demodulatoren und Envelope Follower

Ordner:

`png_storyboards/01_demodulators_envelope_followers/`

Unterordner:

- `01a_detector_types`
- `01b_averager_smoothing`
- `01c_envelope_follower_control`
- `01d_attack_release_build`

Inhalt:

- Sinus- und Audio-Beispiele für Detektoren
- Detektorsignal und gemittelter Envelope
- Attack/Release-Vergleich
- analytische Attack/Release-Aufbauserie

Exportskript:

- `export_block_01_demodulators_envelope_followers.py`

## Block 2: Auto-Wah als Anwendung

Ordner:

`png_storyboards/02_applications_auto_wah_morphing/02a_sidechain_auto_wah/`

Inhalt:

- Sidechain-Signal `s[n]`
- Envelope aus dem Sidechain-Signal
- synchroner Wah-Frequenzgang
- Animationen für Envelope, Bandpass und Sidechain

Exportskript:

- `export_block_02_applications_auto_wah_morphing.py`

Plugin:

- `audio_exports/reaper_jsfx/simple_sidechain_auto_wah.jsfx`

## Block 3: Einstieg in nichtlineare Systeme

Ordner:

`png_storyboards/03_nonlinear_processing_intro/`

Unterordner:

- `03A_delay_clipper_helix`
- `03B_harmonic_decomposition`
- `03C_real_cos_harmonic_decomposition`

Inhalt:

- lineare Verzögerung als Rückgriff auf Vorlesung 8
- Verzögerung plus Hard Clipper
- Helix- und Phasor-Darstellung
- Zerlegung in Harmonische
- realer Cosinus als Summe konjugiert-komplexer Zeiger

Exportskripte:

- `export_block_03_1_delay_clipper_helix.py`
- `export_block_03_1_harmonic_decomposition.py`
- `export_block_03_1c_real_cos_harmonic_decomposition.py`

## Block 4: Intermodulationsverzerrungen

Ordner:

`png_storyboards/04_imd/`

Unterordner:

- `04A_single_sine`
- `04B_two_sine_mixture`

Inhalt:

- Einzelsinus bei \(4\,\mathrm{kHz}\)
- Power Terms \(x^2,x^3,x^4,x^5\)
- Taylor-Beiträge im Zeitbereich und Spektrum
- Zweiton-Signal symmetrisch um \(4\,\mathrm{kHz}\)
- IMD-Produkte aus Quadrat- und Kubikterm

Exportskript:

- `export_block_03_2_imd.py`

Hinweis: Der Skriptname bleibt vorerst erhalten, schreibt aber in den neuen
Blockordner `04_imd`.

## Block 5: Aliasing und Oversampling

Ordner:

`png_storyboards/05_aliasing/`

Unterordner:

- `05A_48khz`
- `05B_96khz`
- `05C_192khz`
- `05D_384khz`

Inhalt:

- 5-kHz-Sinus vor der Nichtlinearität
- Hard Clipping mit \(T=0{,}5\)
- Spektrum bis \(96\,\mathrm{kHz}\)
- Nyquist-Grenze und schrittweise Foldback-Darstellung
- idealer Tiefpass vor dem Downsampling
- Zeitbereich mit und ohne Lowpass

Exportskript:

- `export_block_03_3_aliasing.py`

Hinweis: Der Skriptname bleibt vorerst erhalten, schreibt aber in den neuen
Blockordner `05_aliasing`.

Plugin:

- `audio_exports/reaper_jsfx/simple_oversampling_sine_clipper.jsfx`

## Verschobene Inhalte

Die bisherigen Blöcke zu musikalischer Verzerrung, Sättigung und Dynamic Range
Control wurden nach Vorlesung 12 verschoben:

- `12_distortion_und_dynamic_range_control/png_storyboards/01_distortion_saturation`
- `12_distortion_und_dynamic_range_control/png_storyboards/02_dynamic_range_control`
- `12_distortion_und_dynamic_range_control/png_storyboards/03_transfer_from_lecture_11`
