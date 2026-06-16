# Lehrkonzept Vorlesungen 3 bis 11

## Übergeordnete Leitidee

Die Vorlesungen 3 bis 11 bilden eine zusammenhängende Bewegung vom beobachteten Audiosignal zum gestalteten Audiosystem:

1. digitale Ein-Block-Analyse aufbauen
2. Leakage und Fensterung als Konsequenz endlicher Beobachtung verstehen
3. Zeit-Frequenz-Analyse und Rekonstruktion sauber abschließen
4. digitale Systeme beschreiben
5. Filter lesen und vergleichen
6. Audiostrukturen aus Grundbausteinen verstehen
7. Audioeffekte als Fortsetzung dieser Strukturen lesen: Filter/Delay, Modulation/Demodulation und Nichtlinearitaet

Die aktuelle Umstellung schafft eine klarere Trennung:

- Vorlesung 3 endet bei DFT, FFT und iDFT eines einzelnen Blocks.
- Vorlesung 4 beginnt mit Leakage und Fenstervergleich als Block 1.
- Danach folgen in Vorlesung 4 STFT/Spektrogramm als Block 2 und iSTFT/Overlap-Add als Block 3.
- Die Systemsicht beginnt dadurch erst in Vorlesung 5.

Ab Vorlesung 5 werden digitale Audioeffekte zum durchgehenden Anwendungsfaden. Leitquelle ist Zölzers `DAFX - Digital Audio Effects`: Effekte werden zuerst über Wahrnehmung eingeführt und danach über Blockdiagramm, Gleichung und Plot erklärt. Das Detailkonzept dazu liegt in `00_lehrkonzept_audio_effekte_vorlesungen_5_bis_9.md`; es wurde inhaltlich bis Vorlesung 11 erweitert. Trockene Ausgangssignale liegen unter `audio_samples/nachhallfrei/`.

## Gesamtaufbau

### Vorlesung 3: Digitale Analyse, DFT und iDFT

Kernidee:

- aus $x(t)$ wird $x[n]$
- aus dem endlichen Block folgen $T_{\mathrm{obs}}$, $\Delta f$ und DFT-Bins
- aus der DFT folgt das diskrete Analyzerbild
- aus der iDFT folgt der Rückweg in denselben Zeitblock

Mathematischer Kern:

- $x[n] = x_c(n T_s)$
- $T_{\mathrm{obs}} = N / f_s$
- $\Delta f = f_s / N = 1 / T_{\mathrm{obs}}$
- $\Omega_k = 2 \pi k / N$
- $X[k] = \sum x[n] w[n] e^{-j 2 \pi k n / N}$
- $x[n] = (1 / N) \sum X[k] e^{j 2 \pi k n / N}$

Didaktischer Fokus:

- diskrete Folge statt kontinuierlicher Kurve
- DFT-Bins als Prüffrequenzen
- DFT als Messlogik
- iDFT als Rückweg zum Block
- off-bin Analyse nur als Ausblick auf Vorlesung 4

### Vorlesung 4: Leakage, STFT, Spektrogramm und iSTFT

Kernidee:

- off-bin Frequenzen erzeugen Leakage im endlichen DFT-Block
- Fensterung verändert diese Energieverteilung
- viele verschobene Block-DFTs ergeben die STFT
- das Spektrogramm ist die Betragssicht auf diese Koeffizienten
- iSTFT und Overlap-Add führen aus denselben komplexen Koeffizienten wieder zum Signal zurück

Mathematischer Kern:

- $x_B[n] = x[n] w[n]$
- $X[k] = \sum x_B[n] e^{-j 2 \pi k n / N}$
- $X[m,k] = \sum x[n + m H] w[n] e^{-j 2 \pi k n / N}$
- $\lvert X[m,k]\rvert$
- $\tilde{x}_m[n] = (1 / N) \sum X[m,k] e^{j 2 \pi k n / N}$
- $\hat{x}[n] = \sum_m y_m[n - m H]$

Didaktischer Fokus:

- Leakage als Eigenschaft endlicher Beobachtung
- Fensterform und Fensterlänge unterscheiden
- STFT als fortgesetzte Block-DFT
- Fensterlänge gegen Hop Size sauber trennen
- Spektrogramm nicht mit dem Signal verwechseln
- Rekonstruktion an Koeffizienten und Overlap-Add binden, nicht an "Leakage-frei"

### Vorlesung 5: Systeme, Faltung und Frequenzgang-Anschluss

Kernidee:

- aus der Impulsantwort $h[n]$ wird die diskrete Faltung
- aus der Faltung wird die Systemwirkung im Zeitbereich
- der Frequenzgang bleibt als offene zweite Systemsicht stehen und wird in Vorlesung 6 als Block 1 nachgeholt
- Audioeffekte wie EQ, Filter, Echo und Faltungshall dienen als hörbare Einstiegsbeispiele
- die Vorlesung darf mit einer ausführlichen Audioeffekt-Landkarte beginnen, bevor die Systemtheorie startet

Mathematischer Kern:

- $y[n] = (x \ast h)[n]$
- $y[n] = \sum_m x[m]h[n-m]$

Didaktischer Fokus:

- 5 Minuten Orga und 10 Minuten Wiederholung einplanen
- danach 30 bis 40 Minuten Effektüberblick nach DAFX 1.2.2: erst Wahrnehmungsattribute `L`, `D`, `P`, `S`, `T`, dann Systemklassen LTI, zeitvariante lineare Systeme und nichtlineare Systeme; anschließend Einstieg in LTI-Systeme
- Impulsantwort als anschauliches Audioobjekt
- Faltung als Systemwirkung
- Frequenzgang als bewusst verschobener Anschluss in Vorlesung 6
- zuerst Dry/Wet hören, dann Impulsantwort und Kopiensumme lesen; der Frequenzgang folgt direkt zu Beginn von Vorlesung 6

### Vorlesung 6: Frequenzgang, Delay, Speicher und FIR

Kernidee:

- Delay ist der elementare Speicherbaustein digitaler Systeme
- der aus Vorlesung 5 verschobene Frequenzgang-Block verbindet zuerst $h[n]$ mit $H(e^{j\Omega})$ und $H_N[k]$
- FIR-Feedforward-Strukturen werden als erste baubare Filter hörbar
- Differenzengleichungen sind Baupläne aus Delays, Gains und Summen
- IIR und Feedback werden bewusst in Vorlesung 7 verschoben; $H(z)$ folgt erst in Vorlesung 8

Mathematischer Kern:

- $y[n]=x[n-M]$
- $H(e^{j\Omega})=\sum_m h[m]e^{-j\Omega m}$
- $H_N[k]=H(e^{j2\pi k/N})$
- $Y_N[k]=H_N[k]X_N[k]$
- $y[n]=\sum_{k=0}^{M} b_kx[n-k]$
- $h[n]=b_n$
- $H(e^{j\Omega})=\sum_{k=0}^{M} b_ke^{-j\Omega k}$

Didaktischer Fokus:

- $x[n-M]$ als gespeicherten Eingangswert lesen
- Frequenzgang als Systemgröße und nicht als Signalspektrum lesen
- FIR-Koeffizienten als Impulsantwort lesen
- Feedforward-Strukturen vor rekursiven Strukturen sichern
- Tap-Anzahl, Fensterung, Gruppenlaufzeit und Rechenaufwand zusammen denken
- Feedback/IIR als offene Anschlussfrage für Vorlesung 7 vorbereiten

### Vorlesung 7: Vom IIR im Zeitbereich zum Biquad

Kernidee:

- Feedback und einfache IIR-Systeme ergaenzen die FIR-Sprache aus Vorlesung 6
- die Vorlesung startet direkt im Zeitbereich mit dem vorhandenen IIR-Block
- reine IIR-Systeme werden erst ueber Rekursion, Impulsantwort und Filterkurve verstanden
- `p` bleibt im einpoligen Einstieg der direkte Rueckfuehrungsfaktor; die allgemeine Standardform nutzt danach `a_r`
- die Grenzen reiner Rueckfuehrung werden sichtbar: Hochpass, Notch und gezielte Ausloeschungen brauchen Feedforward
- die allgemeine rekursive Filterform kombiniert `b_k`-Feedforward und `a_r`-Feedback
- Tiefpass, Hochpass, Bandpass, Notch, Low-Shelf, High-Shelf und Peaking-EQ werden als relevante Kurven vorgestellt
- der Frequenzgang wird weiterhin als $H(e^{j\Omega})$ aus der Impulsantwort beziehungsweise Rekursion gelesen
- das Biquad wird als praktische Standardform fuer Audiofilter eingefuehrt
- z-Transformation, z-Ebene, Pole und Nullstellen werden nur als Ausblick auf Vorlesung 8 angekuendigt

Mathematischer Kern:

- $y[n]=b_0x[n]+p\,y[n-1]$
- $h[n]=b_0p^n$ fuer $n\ge 0$
- $H(e^{j\Omega})=b_0\sum_{n=0}^{\infty}(p e^{-j\Omega})^n=\frac{b_0}{1-p e^{-j\Omega}}$
- $H(e^{j\Omega})=\frac{b_0}{1+\sum_{r=1}^{M}a_re^{-jr\Omega}}$
- $y[n]=\sum_{k=0}^{N-1}b_kx[n-k]-\sum_{r=1}^{M}a_ry[n-r]$
- $H(e^{j\Omega})=\frac{\sum_{k=0}^{N-1}b_ke^{-jk\Omega}}{1+\sum_{r=1}^{M}a_re^{-jr\Omega}}$
- Biquad: $H(e^{j\Omega})=\frac{b_0+b_1e^{-j\Omega}+b_2e^{-j2\Omega}}{1+a_1e^{-j\Omega}+a_2e^{-j2\Omega}}$

Didaktischer Fokus:

- vorhandenes `01_iir`-Storyboard als Einstieg nutzen
- Stabilitaet zuerst im Zeitbereich ueber abklingende und wachsende Impulsantworten zeigen
- Feedback als Ursache von IIR und unendlicher Impulsantwort lesen
- reine Rueckfuehrung: tiefpassartig, resonant, glatt, aber nicht vollstaendig frei
- Hochpass und Notch als Motivation fuer Feedforward-`b_k`
- allgemeine rekursive Gleichung als FIR+IIR-Kombination lesen
- Filtertypen kurz akustisch und grafisch einordnen
- Biquad als kompakte Realisierungsform fuer die Filtertypen einfuehren
- keine Pol-/Nullstellen-Sprache in Vorlesung 7; diese Begriffe gehoeren in Vorlesung 8

### Vorlesung 8: z-Transformation, Pole/Nullstellen und Systemklassen

Kernidee:

- die z-Transformation steht am Anfang und erweitert den bekannten Frequenzgang zu \(H(z)\)
- Pole und Nullstellen erklaeren geometrisch, warum die Biquads aus Vorlesung 7 so wirken
- die Systemfunktion wird fuer FIR, IIR und Biquad gelesen und auf dem Einheitskreis sowie in der z-Ebene ausgewertet
- der Abschluss ordnet LTI-Filter in die groessere Systemklassenlogik der Audioeffekte ein

Mathematischer Kern:

- $H(z)=\frac{\sum_{k=0}^{N-1}b_kz^{-k}}{1+\sum_{r=1}^{M}a_rz^{-r}}$
- $H(e^{j\Omega})=H(z)|_{z=e^{j\Omega}}$
- Nullstellen: $B(z)=0$
- Pole: $A(z)=0$
- z-Transformation als Erweiterung der DTFT:
  $H(z)=\sum_n h[n]z^{-n}$ mit $z=re^{j\Omega}$
- auf dem Einheitskreis entsteht der Frequenzgang, abseits davon die z-Ebenen-Struktur

Didaktischer Fokus:

- z-Transformation als Fortsetzung von \(e^{-j\Omega}\) einfuehren
- Einheitskreis, Frequenzgang, Pole, Nullstellen und Stabilitaet verbinden
- FIR, IIR und Biquad ueber dieselbe Systemfunktion lesen
- Nullstellen als Ausloeschungen und Pole als Resonanz-/Stabilitaetsstruktur verstehen
- Audioeffekte nach Systemklassen einordnen: LTI, NTI, LTV und NTV
- Aufgaben zur Filteranalyse aus Koeffizienten, Blockdiagramm, \(H(z)\), Frequenzgang und Pol-/Nullstellenlage vorbereiten

### Vorlesung 9: Filter und Delay-basierte Audioeffekte

Kernidee:

- Vorlesung 9 startet den konkreten Audio-FX-Block nach Zoelzer 2011, Kapitel 2
- gaengige Filter, parametrische Equalizer und Delay-Strukturen werden als Studio- und Plugin-Werkzeuge gelesen
- Filter- und Delay-FX bleiben nahe an \(H(z)\), Frequenzgang, Phase, Delayline, Mix und Feedback

Mathematischer Kern:

- Filterparameter: \(f_c\), \(Q\), Bandbreite, Gain \(G\), Phase und Gruppenlaufzeit
- Peak-EQ als Biquad mit Koeffizienten aus \(f_c\), \(Q\) und \(G\)
- Allpass: \(|H(e^{j\Omega})|=1\), aber \(\angle H(e^{j\Omega})\) veraendert sich
- FIR-Comb: \(H(z)=1+gz^{-M}\)
- IIR-Comb: \(H(z)=c/(1-gz^{-M})\)
- variable Delayzeit \(M[n]\) fuer Vibrato, Flanger und Chorus

Didaktischer Fokus:

- Plugin-Parameter technisch lesen: \(f_c\), \(Q\), \(G\), Rate, Depth, Mix, Feedback, Delay Time
- Allpass und Phaser ueber Phase verstehen
- Comb-Filter als Bruecke zwischen Delay und Frequenzgang lesen
- Vibrato, Flanger, Chorus, Slapback und Echo ueber Delayzeit, Modulation, Mix und Feedback unterscheiden
- keine allgemeine FIR-/Convolution-Behandlung; keine Multiband- oder Natural-sounding-Comb-Vertiefung

### Vorlesung 10: Modulatoren und Demodulatoren

Kernidee:

- Vorlesung 10 folgt Zoelzer 2011, Kapitel 3
- Amplituden-, Ring-, Frequenz- und Phasenmodulation werden als eigene Effektklasse eingefuehrt
- Demodulatoren und Detektoren liefern Steuersignale fuer adaptive Effekte

### Vorlesung 11: Nichtlineare Effekte

Kernidee:

- Vorlesung 11 folgt Zoelzer 2011, Kapitel 4
- Dynamikprozessoren, Saturation, Distortion, Exciter und Enhancer verlassen die reine LTI-Sprache
- zentrale Beschreibung sind Kennlinien, Envelope-Follower, harmonische Verzerrung und Aliasing-Risiko

## Übergänge zwischen den Vorlesungen

### Von Vorlesung 3 zu Vorlesung 4

Vorlesung 3 klärt den einzelnen Analyseblock. Vorlesung 4 beginnt mit der Frage, was passiert, wenn die analysierte Frequenz nicht genau auf ein DFT-Bin passt.

Studierende müssen aus Vorlesung 3 mitnehmen:

- $x[n]$ als diskrete Folge
- $\Delta f = f_s / N = 1 / T_{\mathrm{obs}}$
- Blockdenken und DFT-Bins
- DFT als Projektion auf diskrete Prüfschwingungen
- iDFT als Rückweg aus vollständigen Binwerten

Das bereitet in Vorlesung 4 vor:

- Leakage und Fensterform
- lokale Spektren eines nichtstationären Signals
- Frame, Hop und Overlap
- Rekonstruktion aus komplexen STFT-Koeffizienten

### Von Vorlesung 4 zu Vorlesung 5

Vorlesung 4 schließt die Analysekette ab. Erst danach ist die Systemsicht didaktisch sauber:

- das Signal ist als diskrete Folge geklärt
- Analyse und Rekonstruktion sind abgeschlossen
- der Fokus kann von der Beobachtung zur Wirkung eines Systems wechseln

### Von Vorlesung 5 zu Vorlesung 6

Vorlesung 5 liefert die LTI-Grundsprache:

- Systembegriff
- Impulsantwort
- diskrete Faltung

Darauf baut Vorlesung 6 konstruktiv auf:

- Frequenzgang als nachgeholte zweite LTI-Sicht
- Delay als Speicher
- Feedforward und FIR
- FIR-Differenzengleichung
- FIR-Entwurf aus Zielkurve, sinc, Fensterung und Tap-Anzahl

### Von Vorlesung 6 zu Vorlesung 7

Nach Delay, FIR und nichtrekursiven Differenzengleichungen fuehrt die naechste Sitzung Feedback und IIR ein. Sie startet direkt im Zeitbereich mit dem vorhandenen IIR-Block und zeigt danach die Grenze reiner Rueckfuehrung: Tiefpassartige und resonante Formen gehen gut, echte Hochpaesse, Notches und gezielte Ausloeschungen brauchen Feedforward. Daraus entsteht die allgemeine rekursive Filterform mit `b_k` und `a_r`. Der Frequenzgang wird weiter als $H(e^{j\Omega})$ gelesen; die z-Transformation bleibt fuer Vorlesung 8 reserviert.

### Von Vorlesung 7 zu Vorlesung 8

Nach reinem IIR, allgemeiner rekursiver Filterform, Filtertypen und Biquad reicht Vorlesung 8 die z-Transformation, Pole und Nullstellen als Designsprache nach. Der Schwerpunkt liegt auf Systemfunktion, Einheitskreis, z-Ebene, Stabilitaet und Aufgaben zur Filteranalyse.

### Von Vorlesung 8 zu Vorlesung 9

Vorlesung 8 startet mit z-Transformation, Polen und Nullstellen und schliesst mit der Systemklassifikation von Audioeffekten. Vorlesung 9 greift diese Klassifikation auf und beginnt den Audio-FX-Block mit Filtern und Delay-basierten Effekten nach Zoelzer 2011, Kapitel 2.

## Was in welcher Vorlesung wirklich mathematisch verstanden werden muss

- **Vorlesung 3:** $x[n] = x_c(n T_s)$, $\Delta f = f_s / N = 1 / T_{\mathrm{obs}}$, DFT, iDFT
- **Vorlesung 4:** Leakage, Fensterung, STFT, Spektrogramm, iSTFT, Overlap-Add
- **Vorlesung 5:** Systembegriff, Impulsantwort, diskrete Faltung
- **Vorlesung 6:** Frequenzgang, Delay, Feedforward-FIR, Koeffizienten, FIR-Design, Gruppenlaufzeit
- **Vorlesung 7:** Feedback/IIR im Zeitbereich, Grenzen reiner Rueckfuehrung, allgemeine rekursive Filterform, Filtertypen, Biquad
- **Vorlesung 8:** z-Transformation, Systemfunktion \(H(z)\), Einheitskreis, Pole/Nullstellen, Stabilitaet, Biquad-z-Ebene, Systemklassen und Filteranalyse-Aufgaben
- **Vorlesung 9:** Filtertypen, Peak-EQ-Koeffizienten, Allpass, FIR-/IIR-Comb, zeitvariante Filter und Delay-basierte Effekte
- **Vorlesung 10:** Modulatoren, Demodulatoren, AM/RM/FM/PM und Detektoren
- **Vorlesung 11:** Dynamik, Nichtlinearitaet, Saturation, Distortion und Exciter/Enhancer

Eher Hintergrund und nur knapp zu halten sind:

- tiefe FFT-Algorithmik
- vollständige allgemeine STFT-Rekonstruktionstheorie
- umfassende ROC-Theorie
- allgemeine Filterentwurfsverfahren

## Demo-, Hör- und Python-Einsatz

### Vorlesung 3

- Alias-Demo mit Sweep oberhalb von $f_s / 2$
- DFT-Bins als diskrete Prüffrequenzen
- iDFT-Rekonstruktion eines endlichen Blocks

### Vorlesung 4

- on-bin gegen off-bin im selben Analyzer
- Rechteck-, Hann- und Hamming-Fenster im direkten Vergleich
- Spektrogramm mit kurzer versus langer Fensterlänge
- Hop-Size-Vergleich bei gleichem $N$
- iSTFT- und Overlap-Add-Demo

### Vorlesung 5

- trockenes Signal gegen EQ/Filter, Echo und kurze Raum-IR
- Impulsantworten von Direktpfad, Echo und Raum hören/plotten
- Faltung als Summe verschobener Impulsantworten am kurzen Zahlenbeispiel

### Vorlesung 6

- nachgeholter Frequenzgang-Block: $H(e^{j\Omega})$, $H_N[k]$ und spektrale Gewichtung $Y_N[k]=H_N[k]X_N[k]$
- Delayline mit Klick, Sprache und perkussivem Signal hören
- Zwei-Tap-FIR als Tiefpass und Hochpass zeigen
- k-Tap-FIR, Koeffizienten und FIR-Notch lesen
- FIR-Design mit idealem Tiefpass, sinc, Fensterung, Tap-Anzahl und Gruppenlaufzeit zeigen

### Vorlesung 7

- mit dem vorhandenen IIR-Storyboard `01_iir` starten
- stabile und instabile Impulsantworten als Einstieg in Block 1 zeigen
- `p=+0.5` und `p=-0.5` als Feedback-Wirkung hoeren und plotten
- reine IIRs mit mehreren Feedback-Taps als Tiefpass-/Resonanzidee zeigen
- erklaeren, warum ein echter Hochpass und ein Notch Feedforward-Ausloeschung brauchen
- allgemeine Gleichung mit `b_k` und `a_k` als FIR+IIR-Kombination einfuehren
- Filtertypen Tiefpass, Hochpass, Bandpass, Notch, Low-Shelf, High-Shelf und Peaking-EQ gegenueberstellen
- Biquad als praktische Standardform einfuehren
- z-Transformation, Systemfunktion, Pole und Nullstellen nur als Ausblick auf Vorlesung 8 nennen

### Vorlesung 8

- \(H(e^{j\Omega})\) zu \(H(z)\) erweitern
- Einheitskreis, Pole, Nullstellen und Stabilitaet als zentrales Storyboard
- Systemfunktion fuer FIR, IIR und Biquad herleiten und geometrisch lesen
- z-Transformation als Erweiterung der DTFT mit freiem Radius einfuehren
- Pole und Nullstellen als Ursache von Resonanz, Ausloeschung und Stabilitaet lesen
- Audioeffekte abschliessend nach LTI, NTI, LTV und NTV sortieren
- Aufgaben zur Filteranalyse aus Koeffizienten, \(H(z)\), Frequenzgang und Pol-/Nullstellenlage nutzen

### Vorlesung 9

- Filtertypen, Parameter und Phase wiederholen
- Peak-EQ als Biquad mit Koeffizienten aus \(f_c\), \(Q\) und \(G\)
- Allpass als Phasenfilter einfuehren
- FIR- und IIR-Comb-Filter vergleichen
- Wah-Wah und Phaser als zeitvariante Filtereffekte einordnen
- Vibrato, Flanger, Chorus, Slapback und Echo ueber Delayline, Mix, Modulation und Feedback unterscheiden

## Projektstruktur nach der Umstellung

- `3_dft_und_leakage/` enthält Vorlesung 3 bis DFT/iDFT; der Ordnername bleibt aus Kontinuitätsgründen vorerst bestehen.
- `4_stft_und_istft/` enthält jetzt Block 1 Leakage, Block 2 STFT und Block 3 iSTFT.
- `5_systeme_faltung_und_hz/` bereitet Vorlesung 5 mit Systembegriff, Impulsantwort und Faltung vor; der ursprünglich geplante Frequenzgang-Block ist in Vorlesung 6 verschoben.
- `6_delay_speicher_differenzengleichung/` setzt mit dem nachgeholten Frequenzgang-Block ein und führt danach Delay, Speicher, FIR-Koeffizienten und FIR-Differenzengleichungen fort.
- `7_iir_frequenzgang_biquad/` startet mit dem vorhandenen IIR-Block im Zeitbereich und fuehrt von reiner Rueckfuehrung ueber Feedforward-Grenzen, Filtertypen und $H(e^{j\Omega})$ zum Biquad. z-Transformation, Systemfunktion und Pol-/Nullstellen-Sprache werden in Vorlesung 8 verschoben.
- `8_z_transformation_pole_nullstellen/` fuehrt die z-Transformation ein und baut darauf Einheitskreis, Systemfunktion, Pole, Nullstellen, Stabilitaet, Biquad-z-Ebene, Systemklassen und Aufgaben zur Filteranalyse auf.
- `9_filter_und_delay/` startet den Audio-FX-Block mit Filtertypen, Peak-EQ, Allpass, Comb-Filtern, zeitvarianten Filtern und Delay-basierten Effekten nach Zölzer 2011, Kapitel 2.
- Die frühere Systemsicht beginnt damit inhaltlich und strukturell mit Vorlesung 5.
