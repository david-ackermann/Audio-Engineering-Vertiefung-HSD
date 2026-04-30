# 5 Systeme, Faltung und H(z)

Vorlesungsordner fuer die fuenfte Vorlesung. Nach DFT, Leakage, STFT und iSTFT wechselt die Perspektive jetzt von der Analyse eines Signals zur Wirkung digitaler Systeme.

## Aktueller Stand

Vorhanden sind:

- `00_konzept_systeme_faltung_und_hz.md`

Die Storyboard-Struktur ist vorbereitet unter:

- `png_storyboards/01_systembegriff_und_impulsantwort/`
- `png_storyboards/02_diskrete_faltung/`
- `png_storyboards/03_impulsantwort_und_frequenzgang/`
- `png_storyboards/04_delay_speicher_differenzengleichung/`
- `png_storyboards/05_hz_als_systemsprache/`
- `png_storyboards/06_feedforward_feedback_ausblick/`

## Inhalt von Vorlesung 5

- Systembegriff: Eingang `x[n]`, Ausgang `y[n]`
- Impuls `delta[n]` und Impulsantwort `h[n]`
- diskrete Faltung als Summe verschobener und gewichteter Impulsantworten
- Zusammenhang zwischen Impulsantwort und Frequenzgang
- Delay als elementarer Speicherbaustein
- Differenzengleichung aus Feedforward- und Feedback-Strukturen
- `H(z)` als kompakte Systemsprache

## Geplante Bloecke

- `Block 1`: Systembegriff und Impulsantwort
- `Block 2`: diskrete Faltung
- `Block 3`: Impulsantwort und Frequenzgang
- `Block 4`: Delay, Speicher und Differenzengleichung
- `Block 5`: `H(z)` als Systemsprache
- `Block 6`: Feedforward und Feedback als Ausblick auf Pole/Nullstellen

## Projektstruktur

- Konzeptdatei direkt im Ordner
- kuenftige Exportskripte direkt im Ordner
- generierte Bildserien unter `png_storyboards/`

## Anschluss

Vorlesung 6 baut darauf auf und liest `H(z)` geometrisch:

- Auswertung auf dem Einheitskreis
- Pole und Nullstellen
- Stabilitaet
- Minimum Phase
