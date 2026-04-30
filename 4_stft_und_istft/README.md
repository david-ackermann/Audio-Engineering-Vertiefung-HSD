# 4 Leakage, STFT und iSTFT

Vorlesungsordner fuer die vierte Vorlesung. Die Vorlesung beginnt jetzt mit Leakage und Fenstervergleich als Block 1. Danach folgen STFT/Spektrogramm als Block 2 und iSTFT/Overlap-Add als Block 3.

## Aktueller Stand

Vorhanden sind:

- `00_konzept_stft_und_istft.md`
- `export_block_01a_offbin_analyzerlogik.py`
- `export_block_01b_hamming_analyzerlogik.py`
- `export_block_01c_spektrale_erklaerung.py`
- `export_block_01d_fenstervergleich.py`
- `export_block_02a_stft_als_bewegte_block_dft.py`
- `export_block_02b_stft_mit_hann_fenster.py`
- `export_block_02c_fensterlaenge_zeit_frequenz_kompromiss.py`
- `export_block_02d_hop_size_zeitabtastung.py`
- `export_block_03a_istft_rueckweg_pro_frame.py`
- `export_block_03b_zero_padding_rekonstruktion.py`

Storyboards liegen unter:

- `png_storyboards/01_leakage_und_fenstervergleich/01A_rechteckfenster/`
- `png_storyboards/01_leakage_und_fenstervergleich/01B_hamming_fenster/`
- `png_storyboards/01_leakage_und_fenstervergleich/01C_spektrale_erklaerung/`
- `png_storyboards/01_leakage_und_fenstervergleich/01D_fenstervergleich/`
- `png_storyboards/02_stft_und_spektrogramm/02A_stft_als_bewegte_block_dft/`
- `png_storyboards/02_stft_und_spektrogramm/02B_stft_mit_hann_fenster/`
  - `01_rechteckfenster_nicht_binzentriert/`
  - `02_hannfenster_nicht_binzentriert/`
- `png_storyboards/02_stft_und_spektrogramm/02C_zeit_frequenz_kompromiss/`
- `png_storyboards/02_stft_und_spektrogramm/02D_hop_size_zeitabtastung/`
- `png_storyboards/03_istft_und_overlap_add/03A_istft_rueckweg_pro_frame/`
- `png_storyboards/03_istft_und_overlap_add/03B_zero_padding_rekonstruktion/`

## Inhalt von Vorlesung 4

- Leakage als Folge endlicher Beobachtung und nicht-binzentrierter Frequenzen
- Fensterform als reale Gewichtung des Zeitblocks
- STFT als fortgesetzte Block-DFT
- Spektrogramm als Darstellung von `|X[m,k]|`
- Einfluss von Fensterlaenge und Hop Size
- iSTFT als Rueckweg pro Frame
- Overlap-Add und Bedingungen fuer saubere Rekonstruktion

## Umgesetzte Bloecke

- `Block 1A`: Off-Bin-Analyzerlogik mit Rechteckfenster
- `Block 1B`: paralleler Hamming-Fall
- `Block 1C`: spektrale Leakage-Erklaerung
- `Block 1D`: Fenstervergleich fuer denselben Off-Bin-Ton
- `Block 2A`: bewegte Block-DFT mit Rechteckfenster
- `Block 2B`: Vergleich Rechteckfenster gegen Hann-Fenster bei nicht-binzentrierten Frequenzen
- `Block 2C`: Zeit-Frequenz-Kompromiss ueber die Fensterlaenge
- `Block 2D`: Einfluss der Hop Size auf die Zeitabtastung
- `Block 3A`: iSTFT als Rueckweg pro Frame
- `Block 3B`: Zero Padding und Rekonstruktion des gesamten Signals

## Anschluss

Die anschliessende Systemsicht beginnt im uebergreifenden Lehrplan mit Vorlesung 5.
