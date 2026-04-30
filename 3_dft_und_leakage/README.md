# 3 DFT und iDFT

Vorlesungsordner fuer die dritte Vorlesung. Inhaltlich endet diese Vorlesung jetzt bei der einzelnen Block-DFT und iDFT. Der Leakage- und Fenstervergleich ist in die vierte Vorlesung verschoben und liegt dort als neuer Block 1.

## Aktueller Stand

In diesem Ordner liegen:

- `00_konzept_dft_und_leakage.md`
- `00_temp_konzept_block_04_diskrete_kreisfrequenz.md`
- `export_block_02_signal_zu_x_n.py`
- `export_block_03_aliasing.py`
- `export_block_03b_rechteckzug_zum_dirac_kamm.py`
- `export_block_03c_frequenzraster_und_aufloesung.py`
- `export_block_04a0_kontinuierlicher_phasor_helix.py`
- `export_block_04a_diskrete_kreisfrequenz_phasor_animation.py`
- `export_block_04a2_cos_sin_basisfunktionen.py`
- `export_block_04b_dft_bins_omega_raster.py`
- `export_block_05_dft_analyzerlogik.py`
- `export_block_06_idft_rekonstruktion.py`

Zugehoerige Storyboards liegen unter:

- `png_storyboards/02_zeitbereich_und_frequenzraster/`
- `png_storyboards/03_aliasing/`
- `png_storyboards/04_diskrete_kreisfrequenz/`
- `png_storyboards/05_dft_analyzerlogik/`
- `png_storyboards/06_idft_rekonstruktion/`

## Inhalt von Vorlesung 3

- Einstieg ueber Analyzer, Blockbildung und diskretes Signal
- Abtastung und diskrete Folge `x[n]`
- Aliasbildung, Nyquist und periodische Spektralkopien
- endlicher Beobachtungsblock, `T_obs`, `Delta f` und DFT-Bins
- diskrete Kreisfrequenz `Omega_k`, Binindex `k` und Bezug zu `f_k`
- DFT als Analyzerlogik
- iDFT als Rueckweg aus den Binwerten in denselben Zeitblock

## Umgesetzte Bloecke

- `Block 2A`: vom kontinuierlichen Signal zu `x[n]`
- `Block 3A`: Alias-Familien im Basisbereich
- `Block 3B`: periodische Spektralkopien von der Abtastung hergeleitet
- `Block 3C`: Beobachtungszeit, Frequenzraster und Aufloesung
- `Block 4A1`: kontinuierlicher komplexer Phasor und Helix als Vorbereitung auf `Omega`
- `Block 4A2`: diskrete Basisfunktion als Phasor-Animation
- `Block 4A3`: Cosinus- und Sinusanteile der diskreten DFT-Analysebasis
- `Block 4B`: DFT-Bin-Raster auf der diskreten Kreisfrequenzachse
- `Block 5A`: DFT-Probe-Serien fuer einzelne Bins
- `Block 6`: iDFT-Rekonstruktionsserie

## Anschluss

Die direkte Fortsetzung liegt in:

- `../4_stft_und_istft/`

Dort beginnt Vorlesung 4 mit `Block 1`: Leakage, Off-Bin-Analyse und Fenstervergleich. Danach folgen STFT und iSTFT.
