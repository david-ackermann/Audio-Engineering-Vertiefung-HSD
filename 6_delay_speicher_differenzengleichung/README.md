# 6 Systemwirkung im Frequenzbereich und FIR

Vorlesungsordner fuer die sechste Vorlesung. Die gehaltene Fassung startet fachlich bei Folie 34 mit der Systemwirkung im Frequenzbereich. Die Folien 1 bis 33 waren Wiederholung und Anschluss an Vorlesung 5: Systemklassen, LTI, Impulsantwort und Faltung.

IIR, Feedback und Biquad-/PEQ-Anwendungen liegen jetzt in Vorlesung 7. Die
z-Transformation mit Polen und Nullstellen beginnt in Vorlesung 8.

## Aktueller Stand

Vorhanden sind:

- `00_lehrkonzept_delay_speicher_differenzengleichung.md`
- `01_lehrplan_block_1_impulsantwort_und_frequenzgang.md`
- `export_block_01_impulsantwort_frequenzgang.py`
- `export_block_01B_spektrale_gewichtung.py`
- `export_block_02_fir.py`
- `export_block_03_terzaufloesung.py`
- `png_storyboards/`

## Inhalt von Vorlesung 6

- Wiederholung vor dem eigentlichen Einstieg: LTI, Impulsantwort und Faltung
- Systemwirkung im Frequenzbereich: Spektrum versus Frequenzgang
- DFT-Raster, Binfrequenzen, Nyquist und $Y_N[k]=H_N[k]X_N[k]$
- DSP-Grundoperationen: Gewichtung, Summation und Verzögerung
- FIR als endliche Feedforward-Struktur mit Koeffizienten $b_k$
- einfache FIR-Wirkungen wie Tiefpass, Hochpass und Kammfilter
- FIR-Notch als Koeffizienten- und Frequenzgangbeispiel
- FIR-Design-Trade-offs: lineare Phase, Taps, Rechenaufwand, Latenz und Stabilität
- Aufgaben zu Transientenglättung, Analyzer-Frequenzgang, Kopfhörerentzerrung und Feedforward-Delay

## Gehaltene Blockstruktur

- `Folien 1-33`: Wiederholung aus Vorlesung 5
- `Folien 34-62`: Systemwirkung im Frequenzbereich
- `Folien 63-65`: Grundoperationen digitaler Signalverarbeitung
- `Folien 66-110`: FIR-Filter als endliche Feedforward-Struktur
- `Folien 111-132`: FIR-Eigenschaften und Design-Trade-offs
- `Folien 133-140`: Aufgaben und Transfer
- `Folie 141`: Feedback

## Storyboards

- `png_storyboards/01_impulsantwort_und_frequenzgang/`
- `png_storyboards/02_fir/02A_tiefpass/`
- `png_storyboards/02_fir/02B_hochpass/`
- `png_storyboards/02_fir/02C_notch/`
- `png_storyboards/02_fir/02D_lowpass_design/`
- `png_storyboards/03_terzaufloesung/` als Zusatzmaterial

## Anschluss

Vorlesung 7 fuehrt die rekursive Seite ein:

- Feedback und einfache IIR-Filter
- Stabilitaet und Filterwirkung
- PEQ als Biquad-Anwendung und Rueckweg zu linearphasigem FIR

Vorlesung 8 fuehrt danach die z-Transformation, den Einheitskreis sowie Pole
und Nullstellen ein.
