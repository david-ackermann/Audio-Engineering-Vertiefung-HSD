# 5 Systeme, Faltung und Frequenzgang-Anschluss

Vorlesungsordner für die fünfte Vorlesung. Nach DFT, Leakage, STFT und iSTFT wechselt die Perspektive jetzt von der Analyse eines Signals zur Wirkung digitaler Systeme.

## Aktueller Stand

Vorhanden sind:

- `00_konzept_systeme_faltung_und_hz.md`
- `export_block_00_systembegriff.py`
- `export_block_01B_systemklassen.py`
- `export_block_02_diskrete_faltung.py`

Die aktuell erzeugte Storyboard-Struktur liegt unter:

- `png_storyboards/00/`
- `png_storyboards/01B_systemklassen/`
- `png_storyboards/02_diskrete_faltung/2A/`
- `png_storyboards/02_diskrete_faltung/2B/`
- `png_storyboards/02_diskrete_faltung/2C/`
- `png_storyboards/02_diskrete_faltung/2D/`
- `png_storyboards/02_diskrete_faltung/2D/m_0_bis_8/`

## Inhalt von Vorlesung 5

- Audioeffekte als Klanglandkarte: EQ, Delay, Reverb, Modulation, Dynamik, Distortion
- Orientierung an Zölzers `DAFX - Digital Audio Effects`: zuerst Wahrnehmung, dann Systemstruktur
- DAFX-Wahrnehmungsklassifikation nach Abschnitt 1.2.2: `L`, `D`, `P`, `S`, `T` und mehrdimensionale Effekte
- nach der DAFX-Landkarte: Einteilung in LTI-Systeme, zeitvariante lineare Systeme und nichtlineare Systeme
- danach zuerst LTI-Systeme einführen
- Block 1B enthält Effektbeispiele für nichtlineare und zeitvariante Systemklassen
- Systembegriff: Eingang `x[n]`, Ausgang `y[n]`
- Impuls `delta[n]` und Impulsantwort `h[n]`
- diskrete Faltung als Summe verschobener und gewichteter Impulsantworten
- Zusammenhang zwischen Impulsantwort und Frequenzgang als offener Anschluss
- der geplante Frequenzgang-Block wurde aus Zeitgründen nicht mehr gehalten und startet jetzt Vorlesung 6 als Block 1
- Delay, Speicher und FIR-Differenzengleichung folgen danach in Vorlesung 6;
  IIR/Biquad folgt in Vorlesung 7, `H(z)` erst in Vorlesung 8.

## Geplante Blöcke

- `Block 0`: Audioeffekte als Klanglandkarte und Motivation für Systemtheorie
- `Block 1`: Systemblock, diskreter Impuls, Impulsantwort-Beispiele und LTI-Prinzip
- `Block 2`: Faltung als Summe verschobener und gewichteter Impulsantworten
- `Block 3`: Impulsantwort und Frequenzgang (verschoben nach Vorlesung 6, Block 1)

## Umgesetzte Blöcke

- `Block 00`: Systembegriff mit Eingangsfolge, Ausgangsfolge, diskretem Impuls, Impulsantwort, Impulsspektrum, Phase und Gruppenlaufzeit
- `Block 1B`: Effektbeispiele mit geclippter Sinusfolge, LFO-Gainfolge und Sidechain-Kompressor-Gainfolge
- `Block 2`: diskrete Faltung in zwei kommutativen Lesarten: `2A` mit festem $\delta[m]$ und verschobenem $x[n-m]$, `2B` mit festem $x[m]$ und verschobenem $\delta[n-m]$; `2C` nutzt dieselbe Eingangsfolge und faltet sie mit einer nichtlinearphasigen Tiefpass-Impulsantwort $h[m]$; `2D` zeigt die LTI-Lesart als Summe verschobener und skalierter Kopien von $h[n]`, inklusive Einzelframes für $m=0,\dots,8$

## Verschoben nach Vorlesung 6

- `Block 3`: Impulsantwort und Frequenzgang wird als `Block 1` in `6_delay_speicher_differenzengleichung/` weitergeführt.
- Die neuen Exporte liegen dort unter `png_storyboards/01_impulsantwort_und_frequenzgang/`.

## Projektstruktur

- Konzeptdatei direkt im Ordner
- künftige Exportskripte direkt im Ordner
- generierte Bildserien unter `png_storyboards/`

## Anschluss

Vorlesung 6 baut darauf auf und startet zuerst mit dem nachgeholten Frequenzgang-Block. Danach folgen die konkreten DSP-Strukturen:

- Impulsantwort und Frequenzgang
- Delay als Speicher
- Feedforward- und Feedback-Delay
- Differenzengleichungen
- `H(z)` als kompakte Systemschreibweise erst in Vorlesung 8

## Demo-Material

Nachhallfreie Ausgangssamples werden zentral unter `audio_samples/nachhallfrei/` gesammelt.
