# Lehrkonzept Vorlesungen 3 bis 9

## Uebergeordnete Leitidee

Die Vorlesungen 3 bis 9 bilden eine zusammenhaengende Bewegung vom beobachteten Audiosignal zum gestalteten Audiosystem:

1. digitale Ein-Block-Analyse aufbauen
2. Leakage und Fensterung als Konsequenz endlicher Beobachtung verstehen
3. Zeit-Frequenz-Analyse und Rekonstruktion sauber abschliessen
4. digitale Systeme beschreiben
5. Filter lesen und vergleichen
6. Audiostrukturen aus Grundbausteinen verstehen
7. zeitvariante Effekte als Fortsetzung dieser Strukturen lesen

Die aktuelle Umstellung schafft eine klarere Trennung:

- Vorlesung 3 endet bei DFT, FFT und iDFT eines einzelnen Blocks.
- Vorlesung 4 beginnt mit Leakage und Fenstervergleich als Block 1.
- Danach folgen in Vorlesung 4 STFT/Spektrogramm als Block 2 und iSTFT/Overlap-Add als Block 3.
- Die Systemsicht beginnt dadurch erst in Vorlesung 5.

## Gesamtaufbau

### Vorlesung 3: Digitale Analyse, DFT und iDFT

Kernidee:

- aus $x(t)$ wird $x[n]$
- aus dem endlichen Block folgen $T_{\mathrm{obs}}$, $\Delta f$ und DFT-Bins
- aus der DFT folgt das diskrete Analyzerbild
- aus der iDFT folgt der Rueckweg in denselben Zeitblock

Mathematischer Kern:

- $x[n] = x_c(n T_s)$
- $T_{\mathrm{obs}} = N / f_s$
- $\Delta f = f_s / N = 1 / T_{\mathrm{obs}}$
- $\Omega_k = 2 \pi k / N$
- $X[k] = \sum x[n] w[n] e^{-j 2 \pi k n / N}$
- $x[n] = (1 / N) \sum X[k] e^{j 2 \pi k n / N}$

Didaktischer Fokus:

- diskrete Folge statt kontinuierlicher Kurve
- DFT-Bins als Prueffrequenzen
- DFT als Messlogik
- iDFT als Rueckweg zum Block
- off-bin Analyse nur als Ausblick auf Vorlesung 4

### Vorlesung 4: Leakage, STFT, Spektrogramm und iSTFT

Kernidee:

- off-bin Frequenzen erzeugen Leakage im endlichen DFT-Block
- Fensterung veraendert diese Energieverteilung
- viele verschobene Block-DFTs ergeben die STFT
- das Spektrogramm ist die Betragssicht auf diese Koeffizienten
- iSTFT und Overlap-Add fuehren aus denselben komplexen Koeffizienten wieder zum Signal zurueck

Mathematischer Kern:

- $x_B[n] = x[n] w[n]$
- $X[k] = \sum x_B[n] e^{-j 2 \pi k n / N}$
- $X[m,k] = \sum x[n + m H] w[n] e^{-j 2 \pi k n / N}$
- $\lvert X[m,k]\rvert$
- $\tilde{x}_m[n] = (1 / N) \sum X[m,k] e^{j 2 \pi k n / N}$
- $\hat{x}[n] = \sum_m y_m[n - m H]$

Didaktischer Fokus:

- Leakage als Eigenschaft endlicher Beobachtung
- Fensterform und Fensterlaenge unterscheiden
- STFT als fortgesetzte Block-DFT
- Fensterlaenge gegen Hop Size sauber trennen
- Spektrogramm nicht mit dem Signal verwechseln
- Rekonstruktion an Koeffizienten und Overlap-Add binden, nicht an "Leakage-frei"

### Vorlesung 5: Systeme, Faltung und H(z)

Kernidee:

- aus der Impulsantwort $h[n]$ wird die diskrete Faltung
- aus Delay und Speicher wird die Differenzengleichung
- daraus entsteht $H(z)$ als Lesesprache digitaler Systeme

Mathematischer Kern:

- $y[n] = (x \ast h)[n]$
- $x[n - 1] \leftrightarrow z^{-1}$
- $y[n] = \sum b_k x[n-k] - \sum a_r y[n-r]$
- $H(z) = Y(z) / X(z)$

Didaktischer Fokus:

- Impulsantwort als anschauliches Audioobjekt
- Faltung als Systemwirkung
- Delay als elementarer Speicherbaustein
- $H(z)$ als kompakte Sprache fuer diese Struktur

### Vorlesung 6: Pole, Nullstellen, IIR und Minimum Phase

Kernidee:

- der Frequenzgang ist die Systemfunktion auf dem Einheitskreis
- Pole und Nullstellen werden als Ursache von Resonanzen und Ausloeschungen gelesen

Mathematischer Kern:

- $H(e^{j \Omega}) = H(z) \vert_{z = e^{j \Omega}}$
- einfache IIR-Formen
- Stabilitaet ueber Pol-Lage

Didaktischer Fokus:

- Einheitskreis als Auswerteort
- Pole, Nullstellen und Stabilitaet hoer- und plotbezogen lesen
- Minimum Phase von linearer Phase unterscheiden

### Vorlesung 7: FIR, lineare Phase und Faltung

Kernidee:

- FIR ist die bewusste Alternative, wenn Phase, Delay oder lange Faltung wichtig werden

Mathematischer Kern:

- $y[n] = \sum h[m] x[n-m]$
- Symmetrie $h[n] = h[M-n]$
- konstante Gruppenlaufzeit bei linearer Phase

Didaktischer Fokus:

- lineare gegen minimale Phase
- Pre-Ringing, Latenz und Systementscheidung
- lange FIRs und FFT-basierte Realisierung

### Vorlesung 8: Delay, Comb und Allpass als Audio-Bausteine

Kernidee:

- viele Audioeffekte lassen sich auf wenige lesbare Grundstrukturen reduzieren

Mathematischer Kern:

- $H(z) = z^{-M}$
- $H(z) = 1 + g z^{-M}$
- $H(z) = 1 / (1 - g z^{-M})$
- einfacher Allpass erster Ordnung

Didaktischer Fokus:

- Delay, Echo, Comb und Allpass sauber klassifizieren
- spektrale und zeitliche Wirkung aus der Struktur vorhersagen
- Reverb-Bausteine vorbereiten

### Vorlesung 9: Zeitvariante Effekte

Kernidee:

- bekannte Systembausteine bleiben dieselben, aber ihre Parameter werden zeitabhaengig

Mathematischer Kern:

- $m[n] = \sin(\Omega_L n)$
- Tremolo: $y[n] = (1 + alpha m[n]) x[n]$
- Vibrato: $y[n] = x[n - D(n)]$
- Flanger: $y[n] = x[n] + g x[n - D(n)]$

Didaktischer Fokus:

- zeitvariable Verstaerkung, Delay und Allpassstruktur
- Flanger und Phaser als Fortsetzung von Comb- und Allpasswissen
- Plugin-Parameter strukturell lesen

## Uebergaenge zwischen den Vorlesungen

### Von Vorlesung 3 zu Vorlesung 4

Vorlesung 3 klaert den einzelnen Analyseblock. Vorlesung 4 beginnt mit der Frage, was passiert, wenn die analysierte Frequenz nicht genau auf ein DFT-Bin passt.

Studierende muessen aus Vorlesung 3 mitnehmen:

- $x[n]$ als diskrete Folge
- $\Delta f = f_s / N = 1 / T_{\mathrm{obs}}$
- Blockdenken und DFT-Bins
- DFT als Projektion auf diskrete Pruefschwingungen
- iDFT als Rueckweg aus vollstaendigen Binwerten

Das bereitet in Vorlesung 4 vor:

- Leakage und Fensterform
- lokale Spektren eines nichtstationaeren Signals
- Frame, Hop und Overlap
- Rekonstruktion aus komplexen STFT-Koeffizienten

### Von Vorlesung 4 zu Vorlesung 5

Vorlesung 4 schliesst die Analysekette ab. Erst danach ist die Systemsicht didaktisch sauber:

- das Signal ist als diskrete Folge geklaert
- Analyse und Rekonstruktion sind abgeschlossen
- der Fokus kann von der Beobachtung zur Wirkung eines Systems wechseln

### Von Vorlesung 5 zu Vorlesung 6

Vorlesung 5 liefert die eigentliche Systemsprache:

- Delay $z^{-1}$
- Differenzengleichung
- $H(z)$

Darauf baut Vorlesung 6 auf:

- $H(e^{j \Omega})$
- Pole und Nullstellen
- Stabilitaet und Minimum Phase

### Von Vorlesung 6 zu Vorlesung 7

Nach IIR und Pole-Nullstellen-Verstaendnis wird FIR nicht als zweites Kapitel gleicher Art gelesen, sondern als bewusste Alternative mit anderen Phasen- und Implementationsfolgen.

### Von Vorlesung 7 zu Vorlesung 8

Nach FIR, Faltung und Phase lassen sich Delay-, Comb- und Allpassstrukturen als elementare Audio-Bausteine lesen.

### Von Vorlesung 8 zu Vorlesung 9

Vorlesung 8 behandelt statische Strukturen. Vorlesung 9 aendert daran genau eine Sache: Die Parameter werden zeitabhaengig.

## Was in welcher Vorlesung wirklich mathematisch verstanden werden muss

- **Vorlesung 3:** $x[n] = x_c(n T_s)$, $\Delta f = f_s / N = 1 / T_{\mathrm{obs}}$, DFT, iDFT
- **Vorlesung 4:** Leakage, Fensterung, STFT, Spektrogramm, iSTFT, Overlap-Add
- **Vorlesung 5:** diskrete Faltung, Differenzengleichung, $H(z)$
- **Vorlesung 6:** $H(e^{j \Omega})$, Pole, Nullstellen, Stabilitaet, Minimum Phase
- **Vorlesung 7:** FIR-Summe, Symmetrie, lineare Phase
- **Vorlesung 8:** Delay-, Comb- und Allpassfunktionen
- **Vorlesung 9:** einfache Modulationsgleichungen fuer Tremolo, Vibrato, Flanger, Phaser

Eher Hintergrund und nur knapp zu halten sind:

- tiefe FFT-Algorithmik
- vollstaendige allgemeine STFT-Rekonstruktionstheorie
- umfassende ROC-Theorie
- allgemeine Filterentwurfsverfahren

## Demo-, Hoer- und Python-Einsatz

### Vorlesung 3

- Alias-Demo mit Sweep oberhalb von $f_s / 2$
- DFT-Bins als diskrete Prueffrequenzen
- iDFT-Rekonstruktion eines endlichen Blocks

### Vorlesung 4

- on-bin gegen off-bin im selben Analyzer
- Rechteck-, Hann- und Hamming-Fenster im direkten Vergleich
- Spektrogramm mit kurzer versus langer Fensterlaenge
- Hop-Size-Vergleich bei gleichem $N$
- iSTFT- und Overlap-Add-Demo

### Vorlesung 5

- Klick oder Clap durch kurze Raum-IR
- direkte Faltung versus FFT-Faltung
- Strukturdemo fuer Feedforward- und Feedback-Delay

### Vorlesung 6

- Pole/Zero interaktiv verschieben
- stabil versus instabil hoerbar machen
- IIR-EQ an einfachem Audiomaterial

### Vorlesung 7

- Minimum-Phase- versus Linear-Phase-EQ
- Impuls- und Step-Responses vergleichen
- lange FIRs und Convolution Reverb

### Vorlesung 8

- Impulsantworten und Frequenzgaenge von Delay, Comb und Allpass
- kuenstlicher Hall aus wenigen Grundbausteinen
- Kerbabstand aus der Delaylaenge ableiten

### Vorlesung 9

- Tremolo, Vibrato, Flanger, Phaser auf demselben Ausgangsmaterial
- bewegte Kerben im Spektrum oder Spektrogramm
- Zuordnungsuebung Audio zu Blockdiagramm

## Projektstruktur nach der Umstellung

- `3_dft_und_leakage/` enthaelt Vorlesung 3 bis DFT/iDFT; der Ordnername bleibt aus Kontinuitaetsgruenden vorerst bestehen.
- `4_stft_und_istft/` enthaelt jetzt Block 1 Leakage, Block 2 STFT und Block 3 iSTFT.
- `5_systeme_faltung_und_hz/` bereitet Vorlesung 5 mit Systembegriff, Impulsantwort, Faltung, Differenzengleichung und $H(z)$ vor.
- Die fruehere Systemsicht beginnt damit inhaltlich und strukturell mit Vorlesung 5.
