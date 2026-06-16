# Audio Engineering Vertiefung HSD

Zentrale Python-Arbeitsumgebung für die Vorlesungen der Audio-Engineering-Vertiefung.

## Aktuelle Struktur

```text
00_lehrkonzept_vorlesungen_3_bis_9.md
00_lehrkonzept_audio_effekte_vorlesungen_5_bis_9.md
00_vorlesungs_plot_stilguide.md
README.md
1_fourier_transformation/
2_fensterung_und_faltung/
3_dft_und_leakage/
4_stft_und_istft/
5_systeme_faltung_und_hz/
6_delay_speicher_differenzengleichung/
7_iir_frequenzgang_biquad/
8_z_transformation_pole_nullstellen/
9_filter_und_delay/
10_modulation_und_morphing/
binder/
interactive_apps/
```

## Inhalt der Hauptordner

- `00_lehrkonzept_vorlesungen_3_bis_9.md`  
  Uebergreifendes Lehrkonzept fuer die jetzt neu sortierten Vorlesungen 3 bis 11.
- `00_lehrkonzept_audio_effekte_vorlesungen_5_bis_9.md`  
  Audio-FX-Leitfaden fuer Vorlesung 5 bis 11; Vorlesung 9 folgt Zoelzer 2011, Kapitel 2.
- `00_vorlesungs_plot_stilguide.md`  
  Gemeinsame Referenz für Layout, Farben, Schriftgroessen und Plotlogik.
- `1_fourier_transformation/`  
  Exportskripte, Storyboards und Kernlogik für Vorlesung 1.
- `2_fensterung_und_faltung/`  
  Konzept, Exportskripte, Daten und Storyboards für Vorlesung 2.
- `3_dft_und_leakage/`  
  Vorlesung 3: digitale Analyse bis DFT, FFT und iDFT. Der Ordnername bleibt vorerst historisch bestehen.
- `4_stft_und_istft/`  
  Vorlesung 4: Block 1 Leakage und Fenstervergleich, Block 2 STFT/Spektrogramm, Block 3 iSTFT/Overlap-Add.
- `5_systeme_faltung_und_hz/`  
  Vorlesung 5: Systeme, Impulsantwort und diskrete Faltung; Frequenzgang als verschobener Anschluss.
- `6_delay_speicher_differenzengleichung/`  
  Vorlesung 6: nachgeholter Frequenzgang-Block, Delay als Speicher, Feedforward-FIR und Differenzengleichung.
- `7_iir_frequenzgang_biquad/`  
  Vorlesung 7: IIR im Zeitbereich, Grenzen reiner Rueckfuehrung, Frequenzgang $H(e^{j\Omega})$, Feedforward+Feedback, Filtertypen und Biquad. z-Transformation und Pole/Nullstellen folgen in Vorlesung 8.
- `8_z_transformation_pole_nullstellen/`  
  Vorlesung 8: z-Transformation als Erweiterung von $H(e^{j\Omega})$ zu $H(z)$, Einheitskreis, Systemfunktion, Pole, Nullstellen, Stabilitaet, Biquad-z-Ebene, Systemklassen und Aufgaben zur Filteranalyse.
- `9_filter_und_delay/`  
  Vorlesung 9: Filter und Delay-basierte Audioeffekte nach Zoelzer 2011, Kapitel 2.
- `10_modulation_und_morphing/`  
  Vorlesung 10: Modulation und Morphing nach Zölzer 2011, Kapitel 3.
- `interactive_apps/`  
  Binder- und notebookfaehige interaktive Anwendungen.
- `binder/`  
  Gemeinsame Binder-Abhaengigkeiten.

## Aktueller Vorlesungsstand

- Vorlesung 1: Fourier-Transformation, inverse Fourier-Transformation und interaktive App
- Vorlesung 2: Fensterung und Faltung, inklusive Fenstervergleich, Fensterlänge und IR-Beispiele
- Vorlesung 3: DFT-/iDFT-Serie mit Exportskripten und Storyboards
- Vorlesung 4: Leakage-, STFT- und iSTFT-Serie mit neu sortierten Blocknummern
- Vorlesung 5: Systeme und Faltung bis Block 2 gehalten; Block 3 Frequenzgang nach Vorlesung 6 verschoben
- Vorlesung 6: Frequenzgang als Block 1 angelegt, danach Delay, Speicher und Differenzengleichung
- Vorlesung 7: neu organisiert; Start mit vorhandenem IIR-Block im Zeitbereich, danach Grenzen reiner Rueckfuehrung, FIR+IIR-Kombination, Filtertypen und Biquad
- Vorlesung 8: Master-Stand uebernommen; z-Transformation, Systemfunktion, Pol-/Nullstellenlage, Systemklassen und Aufgaben zur Filteranalyse sind dokumentiert
- Vorlesung 9: Lehrkonzept und Blockstruktur fuer Filter- und Delay-basierte Audioeffekte angelegt
- Vorlesung 10: Ordnerstruktur, Lehrkonzept und Storyboard-Plan für Modulation und Morphing angelegt
- Vorlesung 11: Audio-FX-Roadmap nach Zölzer 2011, Kapitel 4 im Lehrkonzept vorbereitet

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
