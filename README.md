# Audio Engineering Vertiefung HSD

Zentrale Python-Arbeitsumgebung fuer die Vorlesungen der Audio-Engineering-Vertiefung.

## Aktuelle Struktur

```text
00_lehrkonzept_vorlesungen_3_bis_9.md
00_vorlesungs_plot_stilguide.md
README.md
1_fourier_transformation/
2_fensterung_und_faltung/
3_dft_und_leakage/
4_stft_und_istft/
5_systeme_faltung_und_hz/
binder/
interactive_apps/
```

## Inhalt der Hauptordner

- `00_lehrkonzept_vorlesungen_3_bis_9.md`  
  Uebergreifendes Lehrkonzept fuer die jetzt neu sortierten Vorlesungen 3 bis 9.
- `00_vorlesungs_plot_stilguide.md`  
  Gemeinsame Referenz fuer Layout, Farben, Schriftgroessen und Plotlogik.
- `1_fourier_transformation/`  
  Exportskripte, Storyboards und Kernlogik fuer Vorlesung 1.
- `2_fensterung_und_faltung/`  
  Konzept, Exportskripte, Daten und Storyboards fuer Vorlesung 2.
- `3_dft_und_leakage/`  
  Vorlesung 3: digitale Analyse bis DFT, FFT und iDFT. Der Ordnername bleibt vorerst historisch bestehen.
- `4_stft_und_istft/`  
  Vorlesung 4: Block 1 Leakage und Fenstervergleich, Block 2 STFT/Spektrogramm, Block 3 iSTFT/Overlap-Add.
- `5_systeme_faltung_und_hz/`  
  Vorlesung 5: Systeme, Impulsantwort, diskrete Faltung, Differenzengleichung und `H(z)`.
- `interactive_apps/`  
  Binder- und notebookfaehige interaktive Anwendungen.
- `binder/`  
  Gemeinsame Binder-Abhaengigkeiten.

## Aktueller Vorlesungsstand

- Vorlesung 1: Fourier-Transformation, inverse Fourier-Transformation und interaktive App
- Vorlesung 2: Fensterung und Faltung, inklusive Fenstervergleich, Fensterlaenge und IR-Beispiele
- Vorlesung 3: DFT-/iDFT-Serie mit Exportskripten und Storyboards
- Vorlesung 4: Leakage-, STFT- und iSTFT-Serie mit neu sortierten Blocknummern
- Vorlesung 5: Konzept und Storyboard-Struktur fuer Systeme, Faltung und `H(z)` vorbereitet

## Ordnungsprinzip

- Themenbezogene Konzepte bleiben im jeweiligen Vorlesungsordner.
- Gemeinsame Stil- und Gestaltungsregeln liegen bewusst auf Root-Ebene.
- Exportskripte liegen direkt im Themenordner.
- Generierte Bildserien liegen immer unter `png_storyboards/`.
- Daten, WAV-Dateien oder Hilfsdateien bleiben themenbezogen im jeweiligen Vorlesungsordner.

## Interaktive App

Aktuell vorhanden:

- `interactive_apps/1_fourier_transformation/`

Binder-Links und lokale Hinweise stehen in der dortigen `README.md`.
