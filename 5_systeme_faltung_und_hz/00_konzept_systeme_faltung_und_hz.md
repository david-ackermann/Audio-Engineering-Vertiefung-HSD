# Konzept Vorlesung 5: Systeme, Faltung und Frequenzgang-Anschluss

## Ziel der Vorlesung

Die Studierenden sollen am Ende verstehen:

- was ein diskretes System aus einer Eingangsfolge $x[n]$ macht
- warum die Impulsantwort $h[n]$ ein System vollständig beschreibt, wenn das System linear und zeitinvariant ist
- wie die diskrete Faltung als Summe verschobener und gewichteter Impulsantworten gelesen wird
- dass Impulsantwort und Frequenzgang als zweite Systemsicht in Vorlesung 6 direkt nachgeholt werden
- dass Delay, Speicher und Differenzengleichung danach der nächste konstruktive Schritt in Vorlesung 6 sind

## Didaktische Rolle im Gesamtaufbau

Vorlesung 4 schließt die Analyseperspektive ab: Ein Signal kann als Folge betrachtet, analysiert und wieder rekonstruiert werden. Vorlesung 5 wechselt die Frage:

> Nicht mehr: Was steckt im Signal? Sondern: Was macht ein System mit dem Signal?

Die fachliche Kette lautet:

- ein System bildet $x[n]$ auf $y[n]$ ab
- ein Impuls testet, wie das System auf einen einzelnen Sample-Anstoß reagiert
- bei linearen zeitinvarianten Systemen reichen verschobene und gewichtete Impulsantworten aus
- daraus entsteht die Faltung $y[n] = (x \ast h)[n]$
- der Frequenzgang beschreibt dieselbe Systemwirkung als komplexe Gewichtung von Frequenzanteilen und wird aus Zeitgründen in Vorlesung 6 als erster Fachblock nachgeholt
- Delay, Speicher und FIR-Differenzengleichung werden danach in Vorlesung 6
  als Fortsetzung eingefuehrt. IIR/Biquad folgt in Vorlesung 7; \(H(z)\)
  beginnt erst in Vorlesung 8.

## Anschluss an Vorlesung 4

Aus Vorlesung 4 nehmen die Studierenden mit:

- $x[n]$ als diskrete Folge
- lokale Analyse und Rekonstruktion aus vollständigen Koeffizienten
- Fensterung und Blockdenken als Beobachtungsoperation

Vorlesung 5 verlässt die Beobachtung und behandelt Wirkung:

- $h[n]$ ist nicht Beobachtungsfenster, sondern Systemantwort
- Faltung ist nicht Fensterung, sondern Systemwirkung
- der Frequenzgang beschreibt ein System, nicht ein Spektrogramm

## Mathematischer Kern

Impuls und Impulsantwort:

$$
\delta[n] = \begin{cases}
1, & n = 0 \\
0, & n \neq 0
\end{cases}
$$

$$
h[n] = \mathcal{T}\{\delta[n]\}
$$

Lineares zeitinvariantes System:

$$
\mathcal{T}\{a x_1[n] + b x_2[n]\} = a\mathcal{T}\{x_1[n]\} + b\mathcal{T}\{x_2[n]\}
$$

$$
\mathcal{T}\{x[n - n_0]\} = y[n - n_0]
$$

Diskrete Faltung:

$$
y[n] = (x \ast h)[n] = \sum_m x[m] h[n - m]
$$

Frequenzgang eines LTI-Systems:

$$
H(e^{j\Omega}) = \sum_m h[m]e^{-j\Omega m}
$$

## Didaktischer roter Faden

0. Block 0: Audioeffekte als Klanglandkarte und Motivation für Systemtheorie
00. Block 00: Allgemeiner Systembegriff, Eingang, Ausgang, Impuls und Impulsantwort
0A. Block 0A: DAFX-Effekte nach Systemklassen sortieren
1. Block 1: Systembegriff, Ein- und Ausgangsfolge, Impuls als Testsignal
2. Block 2: Impulsantwort und diskrete Faltung als Überlagerung
3. Block 3: Impulsantwort, Spektrum und Systemwirkung (nicht mehr gehalten; verschoben nach Vorlesung 6, Block 1)

## Block 0: Audioeffekte als Klanglandkarte

### Kerngedanke

> Bevor die Systemtheorie beginnt, bekommen die Studierenden eine hörbare Landkarte: Welche Audioeffekte gibt es, was verändern sie am Klang und welche Systemklassen stecken dahinter?

Dieser Block darf in Ruhe 30 bis 40 Minuten einnehmen. Es ist kein Problem, wenn Vorlesung 5 dadurch weniger weit in Faltung oder Frequenzgang kommt. Die Orientierung ist hier wichtiger als Stoffdurchsatz, weil alle weiteren Vorlesungen davon profitieren.

Didaktisch wichtig:

- zuerst hören, dann ordnen, dann erst systemtheoretisch benennen
- trockene und bearbeitete Signale direkt vergleichen
- Effektgruppen nach Wahrnehmung sortieren, nicht sofort nach Formeln
- Systemklassen nur als grobe Vorschau einführen: LTI, zeitvariant, pegelabhängig, nichtlinear, blockbasiert
- die Brücke setzen: Wir starten danach mit der einfachsten und wichtigsten Klasse, den linearen zeitinvarianten Systemen

Effektlandkarte nach DAFX, Abschnitt 1.2.2:

| DAFX-Attribut | Wahrnehmungsfrage | Beispiele | Erste Systemidee |
|---|---|---|---|
| `L` Loudness | Wird das Signal lauter, leiser, dichter oder dynamisch kontrollierter? | compressor, limiter, expander, noise gate, gain/amplification, tremolo | Gain, Pegelmessung, Kennlinie, LFO |
| `D` Duration and rhythm | Ändern sich Dauer, Tempo oder rhythmische Lage? | time-scaling, time inversion, rhythm/swing change | Blockverarbeitung, OLA, STFT |
| `P` Pitch and harmony | Ändern sich Tonhöhe, Intonation oder Harmonie? | pitch-shifting, auto-tune, harmonizer | Resampling, Phase-Vocoder, Analyse/Resynthese |
| `S` Spatial qualities | Ändern sich Ortung, Entfernung, Bewegung oder Raum? | echo, reverberation, panning, Doppler, rotary/Leslie | Delay, Impulsantwort, Faltung, HRTF |
| `T` Timbre and quality | Ändern sich Klangfarbe, Helligkeit, Textur oder Qualität? | filter, equalizer, wah-wah, chorus, flanger, phaser, distortion, vocoding | Frequenzgang, Phase, Kennlinie, Spektralstruktur |
| mehrere Hauptattribute | Ändern sich mehrere Wahrnehmungsdimensionen gleichzeitig? | resampling, ring modulation, robotization, spectral tremolo, vibrato | kombinierte oder blockbasierte Verarbeitung |

Mögliche Hördramaturgie:

1. trockenes Signal
2. EQ/Filter
3. Delay oder Echo
4. Reverb oder Faltungshall
5. Chorus/Flanger/Phaser
6. Compressor
7. Distortion/Saturation

Systemklassen als Brücke zur Theorie:

| Systemklasse | Beispiele aus der DAFX-Landkarte | Erste technische Sprache |
|---|---|---|
| lineare zeitinvariante Systeme | filter, equalizer, echo mit festen Parametern, reverberation über feste Impulsantwort, comb filter | Systemblock, Impulsantwort, Faltung, Frequenzgang |
| zeitvariante lineare Systeme | tremolo, chorus, flanger, phaser, vibrato, rotary/Leslie | zeitabhängiger Gain, bewegtes Delay, LFO |
| nichtlineare Systeme | distortion, fuzz, overdrive, compressor, limiter, expander, noise gate | Kennlinie, Pegelabhängigkeit, Obertöne |

Blockbasierte Effekte wie time-scaling, pitch-shifting und Phase-Vocoder-Effekte werden als spätere Erweiterung angekündigt, aber nicht vor den LTI-Grundlagen ausgebaut.

Zielsatz für den Übergang:

> Viele Audioeffekte sehen zuerst sehr verschieden aus. Systemtheorie liefert die Sprache, um ihre gemeinsamen Bausteine zu erkennen. Wir beginnen mit Systemen, die über Impulsantwort, Faltung und Frequenzgang beschrieben werden können.

## Block 00: Allgemeiner Systembegriff

### Kerngedanke

> Ein System ist eine Abbildung von $x[n]$ nach $y[n]$. Die Impulsantwort zeigt, was das System aus einem einzelnen Sample-Anstoß macht.

Dieser Block steht zwischen der Audioeffekt-Landkarte und der Einteilung in Systemklassen. Die Studierenden sollen zuerst die gemeinsame Grundsprache sehen, bevor zwischen LTI, LTV, NTI und NTV unterschieden wird.

Didaktisch wichtig:

- Eingang und Ausgang zuerst als diskrete Folgen zeigen
- den diskreten Impuls als einfachstes Testsignal einführen
- die Impulsantwort als Antwort auf genau diesen einzelnen Sample-Anstoß lesen
- noch nicht behaupten, dass die Impulsantwort jedes System vollständig beschreibt
- den Merksatz vorbereiten: Eine Impulsantwort kann man bei vielen Systemen messen, aber nur bei LTI-Systemen beschreibt eine einzige Impulsantwort das System vollständig

Geplante Storyboards:

- einfache Eingangsfolge $x[n]$
- dazugehörige Ausgangsfolge $y[n]$
- diskreter Impuls $\delta[n]$
- Impulsantwort $h[n]$
- ideales Betragsspektrum des diskreten Impulses als DFT-Bin-Folge
- Phase des diskreten Impulses als DFT-Bin-Folge
- Gruppenlaufzeit des diskreten Impulses als DFT-Bin-Folge
- Tiefpass-Impulsantwort in Abb. 8 didaktisch pegelangehoben wie im Faltungsblock; die Rechen-IR bleibt normalisiert. Einseitige Tiefpass-Darstellung bis Nyquist: bei $N=16$ nur $k=0,\dots,8$; die zweite DFT-Hälfte wäre für reelle $h[n]$ die gespiegelte Fortsetzung

## Block 1B: Systemklassen als technische Blockdiagramme

### Kerngedanke

> Nach der DAFX-Wahrnehmungslandkarte brauchen die Studierenden eine zweite, technische Sortierung: LTI, LTV und NLS. Diese Sortierung erklärt, warum wir zuerst mit LTI-Systemen beginnen.

Didaktisch wichtig:

- `LTI`: linear und zeitinvariant, daher über Impulsantwort, Faltung und Frequenzgang beschreibbar
- `LTV`: linear, aber zeitabhängig; Parameter wie Gain oder Delay bewegen sich in der Zeit
- `NLS`: nichtlinear; Kennlinien und Pegelabhängigkeiten können neue Frequenzanteile erzeugen
- zuerst die drei Systemklassen als technische Signalflussbilder zeigen, danach konkrete Effekte wieder einsortieren

Geplante Storyboards:

- NLS-Beispiel: Sinusfolge, geclippte Folge und idealisierte Obertöne
- LTV-Beispiel: einfache LFO-Gainfolge $g[n]$ für Tremolo
- nichtlinear-zeitvariantes Beispiel: Sidechain-Kompressor mit $s[n]$, $e_s[n]$ und $g_s[n]$

## Block 1: Systembegriff und Impulsantwort

### Kerngedanke

> Ein System ist eine Abbildung von $x[n]$ nach $y[n]$. Die Impulsantwort zeigt, was das System aus einem einzelnen Sample-Anstoß macht.

Didaktisch wichtig:

- zuerst mit Folgen und nicht mit Formeln beginnen
- $\delta[n]$ als digitales Klicksignal verstehen
- $h[n]$ als messbare Antwort des Systems lesen
- LTI nur so weit einführen, wie es für Faltung gebraucht wird

Geplante Storyboards:

- Eingang $x[n]$, Systemblock, Ausgang $y[n]$
- diskreter Impuls $\delta[n]$
- kurze Impulsantworten: Direktpfad, Echo, gedämpfte Antwort
- LTI-Prinzip: ein Sample startet eine verschobene und gewichtete Kopie von $h[n]$

## Block 2: Diskrete Faltung

### Kerngedanke

> Der Dirac zeigt zuerst die Mechanik der diskreten Faltung: Flip, Verschiebung, Produkt und Summe. Die Benennung als Impulsantwort $h[n]$ folgt erst danach.

Didaktisch wichtig:

- Faltung als Aufbauprozess zeigen, nicht nur als fertige Summe
- erst wenige Samples, dann die allgemeine Formel
- Zeitverschiebung und Gewichtung sichtbar machen
- Vorzeichenkonvention in $x[n-m]$ beziehungsweise $\delta[n-m]$ nicht überbetonen, sondern über verschobene Folgen motivieren

Geplante Storyboards:

- Einstieg nur mit dem Dirac $\delta[n]$, noch ohne Benennung als Impulsantwort $h[n]$
- einfache Eingangsfolge $x[n]$ mit positiven und negativen Samples
- Hilfsindex $m$: oben zuerst festes $\delta[m]$ und $x[m]$
- Flip-Schritt: $x[m]$ wird zu $x[-m]$
- Verschiebeschritt: $x[-m]$ wird zu $x[n-m]$
- unten baut sich $x[n] = \sum_m \delta[m]x[n-m]$ sampleweise als Bildreihe und GIF auf
- fertiges Signal $x[n]\ast\delta[n]=x[n]$
- zweite Unterserie zur Kommutativität: $x[m]$ bleibt fest, der Dirac wird geflippt und als $\delta[n-m]$ verschoben
- beide Unterserien rekonstruieren die gleiche Folge $x[n]$
- danach in `2C`: Übergang vom Dirac zur konkreten nichtlinearphasigen Tiefpass-Impulsantwort $h[n]$ bei gleicher Eingangsfolge $x[n]$
- danach in `2D`: LTI-Lesart über Impulsantwort-Kopien; jedes Sample $x[m]$ startet eine verschobene und skalierte Kopie $x[m]h[n-m]$, deren Summe $y[n]$ ergibt

## Verschobener Block 3: Impulsantwort und Frequenzgang

### Kerngedanke

> Dieselbe Systemwirkung kann im Zeitbereich als Faltung und im Frequenzbereich als Gewichtung gelesen werden.

Dieser Block war für Vorlesung 5 geplant, wurde aber aus Zeitgründen nicht vorgestellt. Er wird in Vorlesung 6 als Block 1 vollständig nachgeholt.

Didaktisch wichtig:

- an Vorlesung 1 bis 4 anschließen: Zeitfolge und Spektrum sind zwei Sichten
- $h[n]$ hat ein Spektrum, das die Wirkung auf Sinusanteile beschreibt
- $H(e^{j\Omega})$ ist die allgemeine, von der Beobachtungslänge unabhängige Systembeschreibung
- $H_N[k]=H(e^{j2\pi k/N})$ ist nur die Abtastung dieser Systemantwort auf dem DFT-Raster der Länge $N$
- die Impulsantwort $h[n]$ wird nicht an das Eingangssignal angepasst; dieselbe Systemantwort wird nur auf einem passenden Frequenzraster ausgewertet
- im Frequenzbereich wirkt das LTI-System als binweise Gewichtung: $Y_N[k]=H_N[k]X_N[k]$
- bei DFT-Rechnung entsteht zunächst zirkuläre Faltung; für lineare Faltung muss ausreichend aufgefüllt werden: $N\geq N_x+N_h-1$

Geplante Storyboards:

- `3A`: derselbe Tiefpass $h[n]$ wird mit verschiedenen DFT-Längen dargestellt; die Systemantwort bleibt gleich, nur das Frequenzraster wird feiner
- `3A`: Spektren zuerst nur als DFT-Stützstellen zeigen, danach die gemeinsame Hüllkurve $H(e^{j\Omega})$ ergänzen
- `3B`: periodisches Rechtecksignal $x[n]$ von $-1$ bis $+1$, dessen Spektrum $X_N[k]$ durch $H_N[k]$ gewichtet wird
- `3B`: im Ausgangsspektrum $Y_N[k]$ zuerst $X_N[k]$ grau zeigen, dann $Y_N[k]$ blau darüber; im Zeitbereich zuerst $x[n]$ grau, dann $y[n]$ blau darüber
- `3B`: längere Beobachtung mit größerem $N$ zeigen; altes $H[k]$ passt nicht mehr binweise, daher muss $H_N[k]$ für das neue Raster neu ausgewertet werden
- Systemantworten $h[n]$, $H[k]$ und $H(e^{j\Omega})$ werden konsistent grün dargestellt; Eingang schwarz/grau, Ausgang blau

## Anschlussblock für Vorlesung 6

### Kerngedanke

> Wenn Impulsantwort und Faltung klar sind, wird zuerst die Frequenzsicht ergänzt. Danach kann das System als konkrete DSP-Struktur gebaut werden: aus Delay, Multiplikation und Addition.

Dieser Inhalt wird bewusst nicht mehr in Vorlesung 5 vertieft. Vorlesung 6
startet mit dem verschobenen Frequenzgang-Block und fuehrt danach zu Delay,
Speicher und Feedforward/FIR-Differenzengleichungen. Feedback/IIR und Biquad
folgen in Vorlesung 7; \(H(z)\) folgt erst in Vorlesung 8.

Anschlussfragen:

- Wie speichert ein digitales System vergangene Samples?
- Warum ist $x[n-1]$ nicht nur eine Verschiebung, sondern ein Speicherbaustein?
- Wie entstehen aus Delays, Gains und Summen einfache Audioeffekte wie Echo, Comb-Filter und Feedback-Echo?
- Wie liest man aus einem Blockdiagramm eine Differenzengleichung?

## Zeitplan für 120 Minuten

| Zeit | Abschnitt | Inhalt | mathematischer Fokus | didaktische Funktion |
|---|---|---|---|---|
| 0-5 min | Orga | Ablauf, Material, kurze Einordnung | - | Ankommen |
| 5-15 min | Wiederholung | Von DFT/STFT/iSTFT zur Frage nach Systemwirkung | $x[n] \to y[n]$ | Vorwissen aktivieren |
| 15-35 min | Block 0 | DAFX-Wahrnehmungslandkarte: `L`, `D`, `P`, `S`, `T`, mehrere Attribute | Wahrnehmungsattribute | Motivation und gemeinsame Sprache |
| 35-45 min | Block 00 | Allgemeiner Systembegriff, Impuls und Impulsantwort | $x[n] \to y[n]$, $\delta[n]$, $h[n]$ | gemeinsame technische Grundsprache |
| 45-60 min | Block 0A | DAFX-Effekte nach Systemklasse sortieren | LTI, LTV, NTI, NTV | Brücke zur Systemtheorie |
| 60-68 min | Pause | kurze Unterbrechung | - | Entlastung |
| 68-85 min | Block 1 | Systembegriff, Impuls, Impulsantwort | $h[n] = \mathcal{T}\{\delta[n]\}$ | Systemantwort anschaulich machen |
| 85-105 min | Block 2 | Faltung als Summe verschobener Impulsantworten | $y[n] = \sum_m x[m] h[n-m]$ | Faltung mechanisch verstehen |
| 105-116 min | Sicherung | Faltung als Systemwirkung, offene Frequenzsicht | $y[n] = \sum_m x[m] h[n-m]$ | tatsächlich erreichten Stand sichern |
| 116-120 min | Abschluss | Was nehmen wir mit? Effektlandkarte, LTI, Impulsantwort, Faltung | wenige Merksätze | Block 3 für Vorlesung 6 ankündigen |

Alternative bei mehr Diskussion im Effektblock:

- Block 0 bis 55 Minuten laufen lassen.
- Danach nur Block 1 sauber abschließen.
- Faltung als Hauptthema in die nächste Sitzung ziehen.

## Typische Verständnishürden

- Faltung wird als abstrakte Rechenvorschrift statt als Systemwirkung verstanden.
- Impulsantwort und Fensterfunktion werden verwechselt.
- $h[n]$ wird als Eingangssignal statt als Systemeigenschaft gelesen.
- Frequenzgang wird als Spektrum eines Signals statt als Systemeigenschaft gelesen.
- Phase und Gruppenlaufzeit werden von der Betragswirkung getrennt betrachtet.
- Delay, Differenzengleichung und \(H(z)\) werden zu frueh vermischt; \(H(z)\)
  gehoert erst in Vorlesung 8.

## Demo-, Hör- und Python-Einsatz

- Systembegriff: Eingangsfolge, Ausgangsfolge, diskreter Impuls, Impulsantwort, ideales Impulsspektrum, Phase und Gruppenlaufzeit
- Systemklassenbeispiele: geclippte Sinusfolge, LFO-Gainfolge und Sidechain-Kompressor-Gainfolge
- diskrete Faltung mit dem Dirac $\delta[m]$: `2A` verschiebt $x[n-m]$, `2B` verschiebt $\delta[n-m]$; beide GIFs zeigen dieselbe Ausgangsfolge $y[n]$
- diskrete Faltung mit einer nichtlinearphasigen Tiefpass-Impulsantwort: `2C` nutzt dieselbe Eingangsfolge und zeigt, wie $y[n]=\sum_m h[m]x[n-m]$ sampleweise entsteht
- Aufbau der Faltung als Überlagerung: `2D` zeigt die einzelnen Kopien $x[m]h[n-m]$ und ihre Summe $y[n]$
- Klick oder Clap durch kurze Raum-IR
- trockener Impuls gegen Echo und Raumantwort
- direkte Faltung einer kurzen Folge mit einer kurzen Impulsantwort
- Audiobeispiel: trockenes Signal durch kurze IR falten
- Frequenzgang aus einer einfachen Impulsantwort lesen (verschoben nach Vorlesung 6, Block 1)

## Geplante Export- und Storyboard-Struktur

- `00`
- `01B_systemklassen`
- `02_diskrete_faltung`
- `03_impulsantwort_und_frequenzgang`

## Anschluss an Vorlesung 6

Vorlesung 5 endet beim Aufbau der Faltung als LTI-Systemwirkung. Vorlesung 6 startet deshalb mit dem nachgeholten Frequenzgang-Block und geht danach in den nächsten konstruktiven Schritt:

- Impulsantwort und Frequenzgang als zweite Systemsicht
- Delay als elementarer Speicherbaustein
- Feedforward- und Feedback-Strukturen als Audioeffekte
- Differenzengleichungen als Baupläne digitaler Systeme
- \(H(z)\) als kompakte Delay-Sprache erst in Vorlesung 8
