# Konzept Vorlesung 4: Leakage, STFT, Spektrogramm und iSTFT

## Ziel der Vorlesung

Die Studierenden sollen am Ende verstehen:

- warum ein nicht-binzentrierter Ton im endlichen DFT-Block Leakage erzeugt
- warum Fensterung keine Anzeigeoption, sondern eine reale Gewichtung des Zeitblocks ist
- wie Rechteck-, Hann- und Hamming-Fenster die Energieverteilung im Spektrum verändern
- dass die STFT keine neue Mathematik, sondern eine fortgesetzte Block-DFT ist
- wie aus Frame, Fensterlänge und Hop Size eine Zeit-Frequenz-Darstellung entsteht
- warum das Spektrogramm nur die Betragssicht auf komplexe STFT-Koeffizienten ist
- wie Fensterform, Fensterlänge und Hop Size das Bild verändern
- wie die iSTFT pro Frame in den Zeitbereich zurückführt
- warum Rekonstruktion nicht an fehlendem Leakage scheitert, sondern an vollständigen Koeffizienten, passender Fensterung und korrektem Overlap-Add hängt
- wie STFT-Parameter aus einer Fenster-Skizze abgelesen werden können

## Didaktische Rolle im Gesamtaufbau

Vorlesung 4 beginnt dort, wo Vorlesung 3 jetzt endet: Die DFT eines einzelnen Blocks ist verstanden, aber der off-bin Fall ist noch offen. Damit kann Leakage ruhig und ohne Zeitdruck als Eigenschaft endlicher Beobachtung behandelt werden.

Danach wird dieselbe Blocklogik auf viele verschobene Blöcke erweitert:

- ein einzelner Beobachtungsblock wird mit der DFT analysiert
- ein nicht-binzentrierter Inhalt verteilt Energie über mehrere Bins
- die Fensterform verändert diese Verteilung
- viele verschobene Beobachtungsbloecke ergeben die STFT
- die Betragssicht dieser Koeffizienten ergibt das Spektrogramm
- aus denselben komplexen Koeffizienten führt die iSTFT zurück in lokale Zeitbloecke
- Overlap-Add setzt diese Blöcke wieder zu einem globalen Signal zusammen

Diese Vorlesung schließt die Analyseperspektive ab. Erst danach beginnt in Vorlesung 5 die Systemsicht.

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
f_0 &\neq k \Delta f &&\to \text{Energieverteilung über mehrere Bins}
\end{aligned}
$$

STFT:

$$
X[m,k] = \sum_{\ell=0}^{N-1} x[mH + \ell] w[\ell] e^{-j 2 \pi k \ell / N}
$$

Spektrogramm:

$$
\lvert X[m,k]\rvert,    \lvert X[m,k]\rvert^2
$$

iSTFT pro Frame:

$$
\tilde{x}_m[\ell] = (1 / N) \sum_{k=0}^{N-1} X[m,k] e^{j 2 \pi k \ell / N}
$$

Da $X[m,k]$ die DFT des gefensterten Blocks $x[mH+\ell]w[\ell]$ ist, liefert die iDFT zuerst wieder genau diesen lokalen gefensterten Block:

$$
\tilde{x}_m[\ell] = x[mH+\ell] w[\ell]
$$

Synthesefenster:

$$
y_m[\ell] = \tilde{x}_m[\ell] w_s[\ell]
$$

Bei gleichem Analyse- und Synthesefenster $w_s[\ell]=w[\ell]$ wird jeder lokale Beitrag zweimal gewichtet:

$$
y_m[\ell] = x[mH+\ell] w^2[\ell]
$$

Overlap-Add:

Der lokale Index $\ell$ eines Frames wird beim Zurücksetzen in das globale Signal durch

$$
\ell = n - mH
$$

ersetzt. Die rohe Overlap-Add-Summe ist deshalb:

$$
s[n]
=
\sum_m y_m[n-mH]
$$

Mit dem Synthesefenster ausgeschrieben ist das:

$$
s[n]
=
\sum_m \tilde{x}_m[n-mH]\,w[n-mH]
$$

Diese Gleichung ist die allgemeinere Schreibweise für die rohe Overlap-Add-Summe. Erst wenn man einsetzt, dass die iDFT den analysierten, bereits gefensterten Block zurückliefert,

$$
\tilde{x}_m[n-mH]
=
x[n]\,w[n-mH],
$$

erhaelt man für einen einzelnen Frame-Beitrag:

$$
y_m[n-mH]
=
x[n] w^2[n-mH]
$$

Damit folgt für die rohe Summe:

$$
s[n] = x[n] \sum_m w^2[n-mH]
$$

Diese zweite Form ist also keine neue Definition von $s[n]$, sondern nur die vereinfachte Form nach dem Einsetzen von $\tilde{x}_m[n-mH]=x[n]w[n-mH]$.

Das globale Fenstergewicht ist:

$$
a[n] = \sum_m w^2[n-mH]
$$

Im normierten Fall kann die Rekonstruktion als Overlap-Add mit sampleweiser Fensterkorrektur gelesen werden:

$$
x_{\mathrm{rec}}[n] =
\frac{\sum_m \tilde{x}_m[n-mH] w[n-mH]}{a[n]}
$$

Also kurz:

$$
x_{\mathrm{rec}}[n] = \frac{s[n]}{a[n]}
$$

## Didaktischer roter Faden

1. Block 1A: Off-Bin-Analyzerlogik mit Rechteckfenster
2. Block 1B: gleicher Fall mit Hamming-Fenster
3. Block 1C: spektrale Erklärung von Leakage
4. Block 1D: Fenstervergleich für denselben Off-Bin-Ton
5. Block 2A: bewegte Block-DFT mit Rechteckfenster
6. Block 2B: gleicher nicht-binzentrierter Analysefall mit Rechteck- und Hann-Fenster
7. Block 2C: Zeit-Frequenz-Kompromiss über die Fensterlänge
8. Block 2D: Hop Size als Dichte der Zeitabtastung
9. Block 3A: iSTFT als Rückweg pro Frame
10. Block 3B: Zero Padding, Overlap-Add und Rekonstruktion des gesamten Signals
11. Block 4: Hausaufgaben zu STFT-Parametern, Leakage und iSTFT

## Block 1: Leakage und Fenstervergleich

### Kerngedanke

> Leakage ist kein Fehler der FFT, sondern die Konsequenz daraus, dass ein endlicher Block nur auf seinem DFT-Raster ausgewertet wird.

Didaktisch wichtig ist:

- zuerst beim diskreten Analyzerbild bleiben
- on-bin und off-bin mit gleicher Blocklaenge vergleichen
- Fensterung als Multiplikation im Zeitbereich zeigen
- erst danach die spektrale Huelle als zweite Erklärungsebene einführen

### Unterbloecke

- `1A`: Off-Bin-Analyzerlogik mit Rechteckfenster
- `1B`: Hamming-Fenster als paralleler Analysefall
- `1C`: spektrale Leakage-Erklärung
- `1D`: Fenstervergleich für denselben Off-Bin-Ton

## Block 2: STFT als fortgesetzte Blockanalyse

### Kerngedanke

> Die STFT ist DFT plus Fenster plus Verschiebung.

Didaktisch wichtig ist:

- jeder Frame ist wieder ein endlicher, gefensterter Block
- Leakage verschwindet in der STFT nicht, sondern erscheint lokal in jedem Frame
- das Spektrogramm ist nur die geordnete Darstellung vieler lokaler Spektren
- Fensterlänge bestimmt das lokale Frequenzraster, Hop Size die zeitliche Abtastung der Analyse

### Unterbloecke

- `2A`: Rechteckfenster als erster bewegter Signalausschnitt
- `2B`: gleiche Bildlogik für Rechteck- und Hann-Fenster bei nicht-binzentrierten Frequenzen
- `2C`: kurzes gegen langes Fenster für Zeit- und Frequenzaufloesung
- `2D`: große gegen kleine Hop Size bei gleicher Fensterlänge

## Block 3: iSTFT und Overlap-Add

### Leitfrage

> Wenn in jedem Frame Leakage sichtbar ist, warum kann die STFT dann trotzdem korrekt rekonstruiert werden?

Die Antwort sollte nicht mit dem Spektrogramm beginnen, sondern mit den vollständigen komplexen STFT-Koeffizienten.

### Kerngedanke

- die iSTFT arbeitet nicht mit dem Betragsspektrogramm allein
- sie arbeitet mit den vollständigen komplexen Werten $X[m,k]$
- Leakage verteilt Energie im Frame-Spektrum, zerstoert aber nicht automatisch die Information
- für die globale Rekonstruktion müssen Fenster, Hop Size und Normierung zusammenpassen

### Herleitung der iSTFT

Für die Herleitung werden zwei Indizes getrennt:

- $\ell$ ist der lokale Index innerhalb eines Frames, also $\ell=0,\ldots,N-1$
- $n$ ist der globale Sample-Index im Gesamtsignal

Frame $m$ beginnt bei:

$$
n_m = mH
$$

Der lokale Index $\ell$ eines Frames entspricht global:

$$
n = mH + \ell
$$

Der Ausgangspunkt ist die STFT eines lokalen Frames:

$$
X[m,k]
=
\sum_{\ell=0}^{N-1}
x[mH+\ell]\,w[\ell]\,
e^{-j2\pi k\ell/N}
$$

Hier ist $m$ der Frame-Index, $H$ die Hop Size, $N$ die DFT-Länge und $w[\ell]$ das Analysefenster. Der lokale Analyseblock ist:

$$
x_m[\ell] = x[mH+\ell]\,w[\ell]
$$

Die iDFT führt diesen Frame wieder in den lokalen Zeitbereich zurück:

$$
\tilde{x}_m[\ell]
=
\frac{1}{N}
\sum_{k=0}^{N-1}
X[m,k]\,
e^{j2\pi k\ell/N}
$$

Da $X[m,k]$ die DFT des gefensterten Blocks war, gilt:

$$
\tilde{x}_m[\ell] = x[mH+\ell]\,w[\ell]
$$

Didaktisch wichtig: Die iDFT liefert noch nicht den ungefensterten Originalblock, sondern den lokal gefensterten Block.

Wenn für die Synthese wieder dasselbe Fenster verwendet wird, entsteht:

$$
y_m[\ell] = \tilde{x}_m[\ell]\,w[\ell]
$$

Damit folgt:

$$
y_m[\ell] = x[mH+\ell]\,w^2[\ell]
$$

Das Quadrat entsteht also nicht durch die Fouriertransformation selbst, sondern durch die Kombination aus Analysefenster und Synthesefenster.

Anschließend wird jeder lokale Beitrag zurück an seine globale Position $mH$ geschoben. Für ein globales Sample $n$ ist der dazugehörige lokale Index im Frame $m$:

$$
\ell = n - mH
$$

Der Beitrag von Frame $m$ an der globalen Stelle $n$ ist also:

$$
y_m[n-mH]
=
\tilde{x}_m[n-mH]\,w[n-mH]
$$

Jetzt werden alle Frames addiert, die an der globalen Stelle $n$ einen gueltigen lokalen Index $\ell=n-mH$ besitzen:

$$
s[n]
=
\sum_m y_m[n-mH]
$$

Mit dem Synthesefenster ausgeschrieben:

$$
s[n]
=
\sum_m \tilde{x}_m[n-mH]\,w[n-mH]
$$

Das ist die direkte Overlap-Add-Schreibweise: iDFT-Block an die globale Position setzen, Synthesefenster anwenden und alles addieren.

Wenn man nun ausnutzt, dass

$$
\tilde{x}_m[n-mH]
=
x[n]\,w[n-mH],
$$

folgt für jeden Frame-Beitrag:

$$
y_m[n-mH]
=
x[n]\,w^2[n-mH]
$$

Damit steckt im rohen Overlap-Add-Signal noch das globale Gesamtgewicht aller überlappenden Fenster:

$$
s[n]
=
x[n]\sum_m w^2[n-mH]
$$

Diese Form mit $x[n]$ ist also die vereinfachte Form der vorherigen Summe mit $\tilde{x}_m$. Sie zeigt besonders klar, warum nach dem Overlap-Add noch durch das Fenstergewicht geteilt werden muss.

### Fenstergewicht

Das globale Fenstergewicht ist:

$$
a[n]
=
\sum_m w^2[n-mH]
$$

Dieses Gewicht beschreibt, wie stark das Sample $x[n]$ nach Analysefensterung, Synthesefensterung und Overlap-Add insgesamt skaliert wurde.

Anschaulich:

- liegt ein Sample nur in einem Fenster, bekommt es nur dessen lokales Gewicht
- liegt es in mehreren überlappenden Fenstern, addieren sich die Fenstergewichte
- am Signalrand ist das Gewicht ohne Zero Padding oft kleiner
- im inneren Bereich kann das Gewicht konstant sein, wenn Fensterform und Hop Size passend gewählt sind

Die normierte Rekonstruktion lautet deshalb:

$$
x_{\mathrm{rec}}[n]
=
\frac{s[n]}{a[n]}
$$

Voll ausgeschrieben:

$$
x_{\mathrm{rec}}[n]
=
\frac{
\sum_m \tilde{x}_m[n-mH]\,w[n-mH]
}{
a[n]
}
$$

Der zentrale Satz für die Folien:

> Die iSTFT setzt nicht einfach lokale iDFT-Blöcke zusammen. Sie setzt jeden lokalen Block $y_m[\ell]$ an seine globale Position $n=mH+\ell$, addiert die überlappenden Beitraege zu $s[n]$ und korrigiert danach durch das globale Fenstergewicht $a[n]$. Dieses Fenstergewicht hängt nur von Fensterform, Fensterlänge und Hop Size ab, nicht vom Signal.

### Unterbloecke

- `3A`: ein einzelner Frame wird per iDFT in einen lokalen Zeitblock zurückgeführt
- `3B`: Zero Padding an den Signalrändern erlaubt eine saubere Overlap-Add-Rekonstruktion des gesamten beobachteten Signals

## Block 4: Hausaufgaben

### Kerngedanke

> Die zentralen STFT-Parameter sollen nicht nur aus Formeln, sondern auch aus Skizzen und Signalbeobachtungen abgelesen werden können.

Die Hausaufgaben sichern die Begriffe aus der Vorlesung:

- Fensterlänge \(N\)
- Hop Size \(H\)
- Frame-Start \(n_m=mH\)
- Überlappung \(N-H\)
- Frequenzraster \(\Delta f=f_s/N\)
- Rekonstruktion über \(s[n]/a[n]\)

### Aufgabenreihe

Die Aufgaben sind als Selbstlernphase mit Studierendenfassung und Erwartungshorizont angelegt:

- `Aufgabe 1`: Frequenzraster eines Audio-Analyzers, \(\Delta f\), \(\Delta\Omega\), \(f_k\) und einseitiger Frequenzbereich
- `Aufgabe 2`: STFT-Fenster auf der \(n\)-Achse einzeichnen, \(n_m=mH\), Endindizes und Spaltendichte
- `Aufgabe 3`: STFT-Parameter aus einer Hann-Fenster-Skizze rueckwaerts bestimmen
- `Aufgabe 4`: lokaler Analyseblock eines Klicks, globaler Index \(n_c\), lokaler Fensterindex und breitbandiges STFT-Spektrum
- `Aufgabe 5`: STFT-Parameter für typische Audioanwendungen auswählen und begruenden

Zentrale Beziehungen für die Aufgaben sind:

$$
n_m = mH
$$

$$
\text{Überlappung in Samples} = N-H
$$

$$
\text{Überlappung in Prozent}
=
\frac{N-H}{N}\cdot 100\,\%
$$

$$
\Delta f = \frac{f_s}{N}
$$

$$
\Omega_k = \frac{2\pi k}{N}
$$

## Zeitplan für 120 Minuten

| Zeit | Abschnitt | Inhalt | mathematischer Fokus | didaktische Funktion |
|---|---|---|---|---|
| 0-8 min | Rückbezug | einzelner DFT-Block aus Vorlesung 3, off-bin Leitfrage | $\Delta f$, $f_k$, $X[k]$ | Anschluss sichern |
| 8-28 min | Block 1A/1B | off-bin Fall, Rechteck und Hamming | Multiplikation mit $w[n]$, Binmessung | Leakage als Blockeigenschaft zeigen |
| 28-42 min | Block 1C/1D | spektrale Leakage-Erklärung und Fenstervergleich | DFT-Samples eines gefensterten Spektrums | Fensterwirkung einordnen |
| 42-58 min | Block 2A | bewegte Block-DFT, Frame, Hop, lokale Spektren | $X[m,k]$ | STFT als fortgesetzte Block-DFT etablieren |
| 58-70 min | Block 2B | Rechteck/Hann im STFT-Kontext | gleiche STFT-Gleichung, anderes $w[n]$ | Leakage lokal in der STFT lesen |
| 70-78 min | Pause | kurze Unterbrechung | - | Entlastung |
| 78-92 min | Block 2C | kurzes gegen langes Fenster | Zeit-Frequenz-Kompromiss über $N$ | Aufloesung differenzieren |
| 92-102 min | Block 2D | Hop Size und Zeitabtastung | gleiche Bins, andere Frame-Dichte | Hop vom Frequenzraster trennen |
| 102-112 min | Block 3A | iSTFT als Rückweg pro Frame | iDFT eines einzelnen Frames | Analyse und Synthese verbinden |
| 112-120 min | Block 3B | Zero Padding, Fenstersumme, Rekonstruktion | $x_{\mathrm{rec}}[n] = s[n] / a[n]$ | Rekonstruktionsbedingung sichern |

## Typische Verständnishürden

- off-bin Leakage wird für einen Rechenfehler gehalten.
- Fensterung wird als Anzeigeoption missverstanden statt als Signaloperation.
- STFT wird für eine voellig neue Analyseart gehalten.
- das Spektrogramm wird mit dem Signal selbst verwechselt.
- Fensterlänge und Hop Size werden vermischt.
- dichtere Frames werden vorschnell mit feinerem Frequenzraster gleichgesetzt.
- iSTFT wird faelschlich als Rückweg aus dem Betragsspektrogramm verstanden.
- perfekte Rekonstruktion wird faelschlich mit "kein Leakage" begruendet.

## Demo-, Hör- und Python-Einsatz

- Analyzer-Vergleich: on-bin gegen off-bin bei gleicher Blocklaenge
- Python-Vergleich: Rechteck-, Hann- und Hamming-Fenster bei identischem Ton
- Spektrogramm-Demo: Sprache oder Drumloop mit kurzer versus langer Fensterlänge
- Python-Vergleich: Hop Size bei gleicher Fensterlänge
- iSTFT-Demo: ein einzelner Frame zurück in den Zeitbereich
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
- `04_hausaufgaben`
