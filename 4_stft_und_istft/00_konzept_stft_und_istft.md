# Konzept Vorlesung 4: Leakage, STFT, Spektrogramm und iSTFT

## Ziel der Vorlesung

Die Studierenden sollen am Ende verstehen:

- warum ein nicht-binzentrierter Ton im endlichen DFT-Block Leakage erzeugt
- warum Fensterung keine Anzeigeoption, sondern eine reale Gewichtung des Zeitblocks ist
- wie Rechteck-, Hann- und Hamming-Fenster die Energieverteilung im Spektrum veraendern
- dass die STFT keine neue Mathematik, sondern eine fortgesetzte Block-DFT ist
- wie aus Frame, Fensterlaenge und Hop Size eine Zeit-Frequenz-Darstellung entsteht
- warum das Spektrogramm nur die Betragssicht auf komplexe STFT-Koeffizienten ist
- wie Fensterform, Fensterlaenge und Hop Size das Bild veraendern
- wie die iSTFT pro Frame in den Zeitbereich zurueckfuehrt
- warum Rekonstruktion nicht an fehlendem Leakage scheitert, sondern an vollstaendigen Koeffizienten, passender Fensterung und korrektem Overlap-Add haengt

## Didaktische Rolle im Gesamtaufbau

Vorlesung 4 beginnt dort, wo Vorlesung 3 jetzt endet: Die DFT eines einzelnen Blocks ist verstanden, aber der off-bin Fall ist noch offen. Damit kann Leakage ruhig und ohne Zeitdruck als Eigenschaft endlicher Beobachtung behandelt werden.

Danach wird dieselbe Blocklogik auf viele verschobene Bloecke erweitert:

- ein einzelner Beobachtungsblock wird mit der DFT analysiert
- ein nicht-binzentrierter Inhalt verteilt Energie ueber mehrere Bins
- die Fensterform veraendert diese Verteilung
- viele verschobene Beobachtungsbloecke ergeben die STFT
- die Betragssicht dieser Koeffizienten ergibt das Spektrogramm
- aus denselben komplexen Koeffizienten fuehrt die iSTFT zurueck in lokale Zeitbloecke
- Overlap-Add setzt diese Bloecke wieder zu einem globalen Signal zusammen

Diese Vorlesung schliesst die Analyseperspektive ab. Erst danach beginnt in Vorlesung 5 die Systemsicht.

## Mathematischer Kern

Ein einzelner gefensterter DFT-Block:

$$
x_B[n] = x[n] w[n],    0 \le n \le N - 1
$$

$$
X[k] = \sum_{n=0}^{N-1} x_B[n] e^{-j 2 \pi k n / N}
$$

Binzentrierung und off-bin Fall:

$$
f_k = k f_s / N,    \Delta f = f_s / N
$$

$$
\begin{aligned}
f_0 &= k_0 \Delta f &&\to \text{konzentrierter Bin-Fall} \\
f_0 &\neq k \Delta f &&\to \text{Energieverteilung ueber mehrere Bins}
\end{aligned}
$$

STFT:

$$
X[m,k] = \sum_{n=0}^{N-1} x[n + m H] w[n] e^{-j 2 \pi k n / N}
$$

Spektrogramm:

$$
\lvert X[m,k]\rvert,    \lvert X[m,k]\rvert^2
$$

iSTFT pro Frame:

$$
\tilde{x}_m[n] = (1 / N) \sum_{k=0}^{N-1} X[m,k] e^{j 2 \pi k n / N}
$$

Overlap-Add:

$$
y_m[n] = \tilde{x}_m[n] w_s[n]
$$

$$
\hat{x}[n] = \sum_m y_m[n - m H]
$$

Im normierten Fall kann die Rekonstruktion als Overlap-Add mit lokaler Fensterkorrektur gelesen werden:

$$
x_{\mathrm{rec}}[n] =
\frac{\sum_m \tilde{x}_m[n-mH] w[n-mH]}{\sum_m w^2[n-mH]}
$$

## Didaktischer roter Faden

1. Block 1A: Off-Bin-Analyzerlogik mit Rechteckfenster
2. Block 1B: gleicher Fall mit Hamming-Fenster
3. Block 1C: spektrale Erklaerung von Leakage
4. Block 1D: Fenstervergleich fuer denselben Off-Bin-Ton
5. Block 2A: bewegte Block-DFT mit Rechteckfenster
6. Block 2B: gleicher nicht-binzentrierter Analysefall mit Rechteck- und Hann-Fenster
7. Block 2C: Zeit-Frequenz-Kompromiss ueber die Fensterlaenge
8. Block 2D: Hop Size als Dichte der Zeitabtastung
9. Block 3A: iSTFT als Rueckweg pro Frame
10. Block 3B: Zero Padding, Overlap-Add und Rekonstruktion des gesamten Signals

## Block 1: Leakage und Fenstervergleich

### Kerngedanke

> Leakage ist kein Fehler der FFT, sondern die Konsequenz daraus, dass ein endlicher Block nur auf seinem DFT-Raster ausgewertet wird.

Didaktisch wichtig ist:

- zuerst beim diskreten Analyzerbild bleiben
- on-bin und off-bin mit gleicher Blocklaenge vergleichen
- Fensterung als Multiplikation im Zeitbereich zeigen
- erst danach die spektrale Huelle als zweite Erklaerungsebene einfuehren

### Unterbloecke

- `1A`: Off-Bin-Analyzerlogik mit Rechteckfenster
- `1B`: Hamming-Fenster als paralleler Analysefall
- `1C`: spektrale Leakage-Erklaerung
- `1D`: Fenstervergleich fuer denselben Off-Bin-Ton

## Block 2: STFT als fortgesetzte Blockanalyse

### Kerngedanke

> Die STFT ist DFT plus Fenster plus Verschiebung.

Didaktisch wichtig ist:

- jeder Frame ist wieder ein endlicher, gefensterter Block
- Leakage verschwindet in der STFT nicht, sondern erscheint lokal in jedem Frame
- das Spektrogramm ist nur die geordnete Darstellung vieler lokaler Spektren
- Fensterlaenge bestimmt das lokale Frequenzraster, Hop Size die zeitliche Abtastung der Analyse

### Unterbloecke

- `2A`: Rechteckfenster als erster bewegter Signalausschnitt
- `2B`: gleiche Bildlogik fuer Rechteck- und Hann-Fenster bei nicht-binzentrierten Frequenzen
- `2C`: kurzes gegen langes Fenster fuer Zeit- und Frequenzaufloesung
- `2D`: grosse gegen kleine Hop Size bei gleicher Fensterlaenge

## Block 3: iSTFT und Overlap-Add

### Leitfrage

> Wenn in jedem Frame Leakage sichtbar ist, warum kann die STFT dann trotzdem korrekt rekonstruiert werden?

Die Antwort sollte nicht mit dem Spektrogramm beginnen, sondern mit den vollstaendigen komplexen STFT-Koeffizienten.

### Kerngedanke

- die iSTFT arbeitet nicht mit dem Betragsspektrogramm allein
- sie arbeitet mit den vollstaendigen komplexen Werten $X[m,k]$
- Leakage verteilt Energie im Frame-Spektrum, zerstoert aber nicht automatisch die Information
- fuer die globale Rekonstruktion muessen Fenster, Hop Size und Normierung zusammenpassen

### Unterbloecke

- `3A`: ein einzelner Frame wird per iDFT in einen lokalen Zeitblock zurueckgefuehrt
- `3B`: Zero Padding an den Signalraendern erlaubt eine saubere Overlap-Add-Rekonstruktion des gesamten beobachteten Signals

## Zeitplan fuer 120 Minuten

| Zeit | Abschnitt | Inhalt | mathematischer Fokus | didaktische Funktion |
|---|---|---|---|---|
| 0-8 min | Rueckbezug | einzelner DFT-Block aus Vorlesung 3, off-bin Leitfrage | $\Delta f$, $f_k$, $X[k]$ | Anschluss sichern |
| 8-28 min | Block 1A/1B | off-bin Fall, Rechteck und Hamming | Multiplikation mit $w[n]$, Binmessung | Leakage als Blockeigenschaft zeigen |
| 28-42 min | Block 1C/1D | spektrale Leakage-Erklaerung und Fenstervergleich | DFT-Samples eines gefensterten Spektrums | Fensterwirkung einordnen |
| 42-58 min | Block 2A | bewegte Block-DFT, Frame, Hop, lokale Spektren | $X[m,k]$ | STFT als fortgesetzte Block-DFT etablieren |
| 58-70 min | Block 2B | Rechteck/Hann im STFT-Kontext | gleiche STFT-Gleichung, anderes $w[n]$ | Leakage lokal in der STFT lesen |
| 70-78 min | Pause | kurze Unterbrechung | - | Entlastung |
| 78-92 min | Block 2C | kurzes gegen langes Fenster | Zeit-Frequenz-Kompromiss ueber $N$ | Aufloesung differenzieren |
| 92-102 min | Block 2D | Hop Size und Zeitabtastung | gleiche Bins, andere Frame-Dichte | Hop vom Frequenzraster trennen |
| 102-112 min | Block 3A | iSTFT als Rueckweg pro Frame | iDFT eines einzelnen Frames | Analyse und Synthese verbinden |
| 112-120 min | Block 3B | Zero Padding, Fenstersumme, Rekonstruktion | $\hat{x}[n] = \sum_m y_m[n - m H]$ | Rekonstruktionsbedingung sichern |

## Typische Verstaendnishuerden

- off-bin Leakage wird fuer einen Rechenfehler gehalten.
- Fensterung wird als Anzeigeoption missverstanden statt als Signaloperation.
- STFT wird fuer eine voellig neue Analyseart gehalten.
- das Spektrogramm wird mit dem Signal selbst verwechselt.
- Fensterlaenge und Hop Size werden vermischt.
- dichtere Frames werden vorschnell mit feinerem Frequenzraster gleichgesetzt.
- iSTFT wird faelschlich als Rueckweg aus dem Betragsspektrogramm verstanden.
- perfekte Rekonstruktion wird faelschlich mit "kein Leakage" begruendet.

## Demo-, Hoer- und Python-Einsatz

- Analyzer-Vergleich: on-bin gegen off-bin bei gleicher Blocklaenge
- Python-Vergleich: Rechteck-, Hann- und Hamming-Fenster bei identischem Ton
- Spektrogramm-Demo: Sprache oder Drumloop mit kurzer versus langer Fensterlaenge
- Python-Vergleich: Hop Size bei gleicher Fensterlaenge
- iSTFT-Demo: ein einzelner Frame zurueck in den Zeitbereich
- Overlap-Add-Demo: Zero Padding und lokale Normierung der Fenstersumme

## Geplante Export- und Storyboard-Struktur

- `01_leakage_und_fenstervergleich`
- `01_leakage_und_fenstervergleich/01A_rechteckfenster`
- `01_leakage_und_fenstervergleich/01B_hamming_fenster`
- `01_leakage_und_fenstervergleich/01C_spektrale_erklaerung`
- `01_leakage_und_fenstervergleich/01D_fenstervergleich`
- `02_stft_und_spektrogramm`
- `02_stft_und_spektrogramm/02A_stft_als_bewegte_block_dft`
- `02_stft_und_spektrogramm/02B_stft_mit_hann_fenster`
  - `01_rechteckfenster_nicht_binzentriert`
  - `02_hannfenster_nicht_binzentriert`
- `02_stft_und_spektrogramm/02C_zeit_frequenz_kompromiss`
- `02_stft_und_spektrogramm/02D_hop_size_zeitabtastung`
- `03_istft_und_overlap_add`
- `03_istft_und_overlap_add/03A_istft_rueckweg_pro_frame`
- `03_istft_und_overlap_add/03B_zero_padding_rekonstruktion`
