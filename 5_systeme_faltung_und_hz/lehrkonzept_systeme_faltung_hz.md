# Lehrkonzept: Systeme, diskrete Faltung und $H(z)$ im Audio Engineering

**Veranstaltungskontext:** Audio Engineering / Digitale Signalverarbeitung, Bachelor Vertiefung  
**Zielumfang:** ca. 120 Minuten Vorlesung inklusive Aktivierungen und kurzer Pause  
**Didaktische Hauptfrage:** Nicht mehr: *Was steckt im Signal?* Sondern: *Was macht ein System mit einem Signal?*

---

## 1. Kurzdiagnose der Ausgangslage

Die bisherigen Folien und Aufgaben bauen bereits eine sehr tragfähige Analyseperspektive auf. Die Studierenden kennen den Weg vom kontinuierlichen Audiosignal $x_c(t)$ zur diskreten Folge $x[n]=x_c(nT_s)$, inklusive Abtastperiode $T_s$, Abtastfrequenz $f_s$ und Sampleindex $n$. Sie haben außerdem gesehen, dass Frequenzen nach der Abtastung nicht mehr beliebig eindeutig unterscheidbar sind, sondern im Zusammenhang mit Nyquist, Aliasbildung und Spektralwiederholung betrachtet werden müssen. Diese Basis ist wichtig, weil spätere digitale Filter nicht im abstrakten Vakuum arbeiten, sondern immer auf diskreten Folgen mit einer bestimmten Abtastrate.

Aus den FT/iFT-Folien ist bekannt, dass komplexe Exponentialfunktionen bzw. komplexe Sinusschwingungen als Analyse- und Synthesebausteine verwendet werden. Betrag und Phase wurden nicht nur formal eingeführt, sondern wiederholt mit Zeitverläufen, Phasoren und Betrag-/Phasenspektren verbunden. Das ist für diese Vorlesung zentral, weil der spätere Frequenzgang $H(e^{j\Omega})$ ebenfalls eine komplexe Größe ist: Er beschreibt nicht nur Pegeländerung, sondern auch Phasenänderung.

Aus den Fensterungs- und Faltungsfolien ist bekannt, dass Multiplikation im Zeitbereich und Faltung im Frequenzbereich zusammenhängen. Die vorhandenen Folien zeigen auch die Umkehrung: Faltung im Zeitbereich entspricht Multiplikation im Frequenzbereich. Besonders wichtig ist die bisherige Fensterlogik: Ein Beobachtungsfenster $w(t)$ oder $w[n]$ ist eine Analyseoperation. Es begrenzt den betrachteten Ausschnitt eines Signals. Diese Operation ist didaktisch sauber von der nun folgenden Systemwirkung zu trennen. Eine Impulsantwort $h[n]$ ist keine Fensterfunktion, sondern eine Eigenschaft eines Systems.

Aus den DFT-Folien ist bekannt, dass diskrete komplexe Exponentialfunktionen $e^{-j\Omega_k n}$ mit $\Omega_k=2\pi k/N$ als Analysebasis dienen. Die Folien verbinden außerdem Binindex $k$, Binfrequenz $f_k=kf_s/N$, Binabstand $\Delta f=f_s/N=1/T_{obs}$ und diskrete Kreisfrequenz $\Omega_k$. Diese präzise Trennung zwischen $f$ in Hz, $\omega$ in rad/s und $\Omega$ in rad/sample muss in der neuen Vorlesung beibehalten werden.

Aus den STFT-Folien kennen die Studierenden lokale, blockweise Analyse: Ein Signal wird in Frames betrachtet, mit einem Fenster multipliziert und für jeden Frame spektral analysiert. Didaktisch ist dies ein guter Ausgangspunkt für den Perspektivwechsel: Bei der STFT schauen wir lokal in ein Signal hinein. Bei Systemen fragen wir dagegen, wie ein Eingangssignal in ein Ausgangssignal verwandelt wird.

Die neue Vorlesung schließt daher genau an einer Schwelle an: Die Studierenden kennen Analyse, Spektrum, Fensterung und Faltung als mathematische Operationen. Jetzt wird Faltung nicht mehr primär als Analysefolge der Fensterung behandelt, sondern als Grundprinzip linearer zeitinvarianter Systeme.

**Korrektursatz für die Rahmung der Vorlesung:**  
> Bisher haben wir Signale beobachtet und analysiert. Jetzt betrachten wir Geräte, Räume, Filter und Effekte als Systeme, die Signale verändern.

---

## 2. Übergeordnete Lehridee

Die Vorlesung soll als zusammenhängende fachliche Bewegung angelegt werden. Ausgangspunkt ist die einfache Abbildung $x[n]\mapsto y[n]$: Ein digitales System nimmt eine Eingangsfolge und erzeugt daraus eine Ausgangsfolge. Dieser Systembegriff wirkt zunächst abstrakt, ist aber im Audio Engineering sehr konkret: Ein Lautsprecher, ein Raum, ein Mikrofon, ein Equalizer, ein Delay oder ein Reverb sind Systeme.

Der diskrete Impuls $\delta[n]$ wird als elementares Testsignal eingeführt. Er ist im digitalen Kontext besonders anschaulich: ein einzelner Sample-Anstoß, ein idealisierter Klick. Die Antwort eines Systems auf diesen Klick heißt Impulsantwort $h[n]$. Bei linearen zeitinvarianten Systemen beschreibt diese Impulsantwort das System vollständig.

Der zentrale didaktische Schritt besteht darin, jedes Eingangssignal als Summe verschobener und gewichteter Impulse zu lesen. Aus einem einzelnen Sample $x[m]$ wird ein Impuls $x[m]\delta[n-m]$. Ein LTI-System macht daraus eine skalierte und verschobene Impulsantwort $x[m]h[n-m]$. Die Summe aller dieser Einzelantworten ergibt die diskrete Faltung.

Im nächsten Schritt wird die bekannte Frequenzperspektive wieder aufgenommen. Ein LTI-System verändert komplexe Exponentialanteile nicht in ihrer Frequenz, sondern nur in Betrag und Phase. Diese komplexe Gewichtung ist der Frequenzgang $H(e^{j\Omega})$. Damit wird eine Brücke zwischen Impulsantwort, Faltung und späterer Filteranalyse geschlagen.

Anschließend wird Delay als elementarer digitaler Speicherbaustein eingeführt. $x[n-1]$ ist nicht nur eine Schreibweise, sondern der vorherige Samplewert. Aus Additionen, Multiplikationen und Delays entstehen Differenzengleichungen. Diese sind im Audio Engineering die Baupläne einfacher digitaler Effekte und Filter.

Der letzte Schritt übersetzt diese Baupläne in die z-Schreibweise. $z^{-1}$ wird zunächst bewusst nicht als abstrakte komplexe Variable eingeführt, sondern als algebraisches Symbol für ein Sample Delay. Aus der Differenzengleichung entsteht $H(z)=Y(z)/X(z)$. Damit endet die Vorlesung nicht mit Pol-Nullstellen-Geometrie, sondern mit einer klaren Lesesprache: Zähler bedeutet Feedforward, Nenner bedeutet Feedback, FIR bedeutet nur Zähler, IIR bedeutet Zähler und Nenner.

**Merksatz der gesamten Vorlesung:**  
> Die Impulsantwort beschreibt ein LTI-System im Zeitbereich; $H(z)$ beschreibt dieselbe Systemstruktur algebraisch; $H(e^{j\Omega})$ beschreibt später die Wirkung auf Frequenzen.

---

## 3. Lernziele

### 3.1 Fachliche Lernziele

Nach der Vorlesung sollen die Studierenden:

1. ein diskretes System formal als $y[n]=\mathcal{T}\{x[n]\}$ beschreiben können,
2. den diskreten Impuls $\delta[n]$ definieren und als digitales Testsignal interpretieren können,
3. die Impulsantwort $h[n]=\mathcal{T}\{\delta[n]\}$ als Systemeigenschaft erklären können,
4. Linearität und Zeitinvarianz so weit anwenden können, dass die Faltungsformel daraus plausibel wird,
5. die diskrete Faltung
   $
   y[n]=\sum_m x[m]h[n-m]
   $
   als Überlagerung skalierter, verschobener Impulsantworten lesen können,
6. den Unterschied zwischen Fensterung als Beobachtungsoperation und Faltung als Systemwirkung erklären können,
7. $x[n-1]$, $x[n-M]$, $y[n-1]$ und $y[n-M]$ als Delays bzw. gespeicherte vergangene Werte interpretieren können,
8. einfache Feedforward- und Feedback-Differenzengleichungen lesen und als Blockdiagramm skizzieren können,
9. aus einfachen Differenzengleichungen $H(z)$ herleiten können,
10. den Unterschied zwischen FIR- und IIR-Strukturen anhand von Zähler und Nenner erklären können.

### 3.2 Konzeptuelle Lernziele

Die Studierenden sollen verstehen:

- dass $h[n]$ nicht ein beliebiges Signal ist, sondern die Antwort eines Systems auf $\delta[n]$,
- dass Faltung nicht nur eine Rechenregel, sondern ein konstruktiver Überlagerungsprozess ist,
- dass ein System im Zeitbereich, im Frequenzbereich und in z-Schreibweise beschrieben werden kann,
- dass $H(z)$ nicht das Spektrum eines Signals ist, sondern eine Systembeschreibung,
- dass Feedback strukturell mehr ist als „ein Echo lauter machen“, weil vergangene Ausgänge wieder in das System eingehen.

### 3.3 Anwendungsbezogene Lernziele

Die Studierenden sollen in Audio-Engineering-Kontexten erklären können:

- warum eine Raumimpulsantwort Faltungshall ermöglicht,
- warum ein Lautsprecher über seine Impulsantwort und seinen Frequenzgang charakterisiert werden kann,
- wie ein Feedforward-Delay ein Echo bzw. Comb-Filter-artige Strukturen erzeugt,
- warum ein Feedback-Delay eine ausklingende Echo-Kette und Stabilitätsfragen erzeugt,
- wie einfache digitale Filter aus Delay, Multiplikation und Addition zusammengesetzt werden.

---

## 4. Notations- und Begriffssystem

| Symbol | Einheit / Bereich | Bedeutung | Didaktischer Hinweis |
|---|---:|---|---|
| $x_c(t)$ | kontinuierlich, Zeit $t$ in s | kontinuierliches Eingangssignal | Nur verwenden, wenn der Anschluss an Abtastung nötig ist. |
| $x[n]$ | Folge, $n\in\mathbb{Z}$ | diskrete Eingangsfolge | Hauptnotation dieser Vorlesung. |
| $y[n]$ | Folge, $n\in\mathbb{Z}$ | diskrete Ausgangsfolge | Immer als Systemausgang markieren. |
| $\mathcal{T}\{\cdot\}$ | Operator | Systemabbildung | Abstrakt, aber nützlich: Das System ist eine Vorschrift. |
| $\delta[n]$ | dimensionslos | diskreter Impuls | Ein Sample ist 1, alle anderen 0. |
| $h[n]$ | Folge | Impulsantwort des Systems | Systemeigenschaft, nicht Eingangssignal und nicht Fenster. |
| $n$ | Samples | laufender Zeitindex | „Bei welchem Ausgangssample schauen wir?“ |
| $m$, $\ell$ | Samples | Summationsindex bei Faltung | Dummy-Index; nicht mit $n$ verwechseln. |
| $k$ | dimensionslos | DFT-Binindex | Aus DFT bekannt; nicht Zeitindex. |
| $T_s$ | s | Abtastperiode | $T_s=1/f_s$. |
| $f_s$ | Hz | Abtastfrequenz | Wird für Umrechnung in reale Frequenzen benötigt. |
| $f$ | Hz | Frequenz in Zyklen pro Sekunde | Audio-nahe Frequenzangabe. |
| $\omega$ | rad/s | kontinuierliche Kreisfrequenz | Nur für kontinuierliche FT. |
| $\Omega$ | rad/sample | diskrete Kreisfrequenz | Zentrale Frequenzvariable für diskrete Systeme. |
| $\Omega_k$ | rad/sample | DFT-Binfrequenz | $\Omega_k=2\pi k/N$. |
| $z^{-1}$ | Delay-Operator | ein Sample Verzögerung | Zuerst als Speicherbaustein einführen. |
| $X(z),Y(z)$ | z-transformierte Folgen | z-Bereichsdarstellungen von Eingang/Ausgang | Nicht mit DFT-Spektrum gleichsetzen. |
| $H(z)$ | Systemfunktion | $H(z)=Y(z)/X(z)$ | Beschreibt das System, nicht ein Signal. |
| $H(e^{j\Omega})$ | komplexer Frequenzgang | Auswertung auf dem Einheitskreis | Übergang zur Filteranalyse. |
| $b_k$ | Koeffizienten | Feedforward-Gewichte | Zähler von $H(z)$. |
| $a_r$ | Koeffizienten | Feedback-Gewichte | Nenner von $H(z)$. |
| $M$ | Samples | maximale Eingangsverzögerung | FIR-Ordnung bzw. Feedforward-Länge. |
| $R$ | Samples | maximale Ausgangsverzögerung | Feedback-Ordnung. |

### Notationsdisziplin für die Vorlesung

Es sollte konsequent zwischen drei Frequenzsprachen unterschieden werden:

$$
\omega = 2\pi f \quad [\mathrm{rad/s}]
$$

für kontinuierliche Signale,

$$
\Omega = 2\pi \frac{f}{f_s} \quad [\mathrm{rad/sample}]
$$

für diskrete Signale, und

$$
\Omega_k = \frac{2\pi k}{N}, \qquad f_k = k\frac{f_s}{N}
$$

für DFT-Bins innerhalb eines Blocks.

**Dozentenhinweis:**  
In dieser Vorlesung möglichst selten $\omega$ verwenden. Für die neue diskrete Systemwelt ist $\Omega$ die saubere Variable. $f$ in Hz nur dann einsetzen, wenn es um Audiointerpretation oder konkrete Delayzeiten geht.

---

## 5. Detaillierter 120-Minuten-Ablauf

| Zeit | Inhalt | Lernziel | zentrale Formel | Visualisierung / Demo | didaktische Funktion |
|---:|---|---|---|---|---|
| 0–5 min | Einstieg: Analyse vs. Systemwirkung | Perspektivwechsel verstehen | $x[n]\to y[n]$ | Signalweg: Mikrofon → DSP → Lautsprecher → Raum | Vorwissen aktivieren |
| 5–10 min | Rückbezug auf FT/DFT/STFT/Fensterung | Beobachtung vs. Wirkung unterscheiden | $x_{obs}[n]=x[n]w[n]$ | Gegenüberstellung Fenster $w[n]$ vs. Impulsantwort $h[n]$ | Fehlkonzept früh vermeiden |
| 10–20 min | Systembegriff | System als Operator verstehen | $y[n]=\mathcal{T}\{x[n]\}$ | Blockdiagramm mit Audio-Beispielen | Abstraktion motivieren |
| 20–28 min | Linearität und Zeitinvarianz | LTI-Bedingungen für Faltung verstehen | Linearität, Zeitinvarianz | Gain/Clipping/Chorus-Beispiele | Geltungsbereich klären |
| 28–38 min | Impuls und Impulsantwort | $\delta[n]$ und $h[n]$ deuten | $h[n]=\mathcal{T}\{\delta[n]\}$ | Klick → Echo/Room/Delay | Systemantwort konkret machen |
| 38–55 min | Impulszerlegung und Faltung | Faltung aus LTI herleiten | $x[n]=\sum_m x[m]\delta[n-m]$, $y[n]=\sum_m x[m]h[n-m]$ | Zahlenfolge $[2,-1,0,3]$, gestapelte Kopien von $h[n]$ | Kernverständnis aufbauen |
| 55–62 min | Mini-Aktivierung 1 | Faltungsprozess anwenden | kurze diskrete Faltung | Studierende skizzieren Kopien von $h[n]$ | Verständnisprüfung |
| 62–70 min | Pause | — | — | — | kognitive Entlastung |
| 70–82 min | Impulsantwort und Frequenzgang | Zeit- und Frequenzsicht verbinden | $H(e^{j\Omega})=\sum_\ell h[\ell]e^{-j\Omega\ell}$ | Sinus durch Delay/Echo, Betrag/Phase | Brücke zur Filteranalyse |
| 82–92 min | Delay als Speicher | $x[n-1]$ als Baustein verstehen | $y[n]=x[n-M]$ | Delayline mit Samples | DSP-Struktur konkretisieren |
| 92–105 min | Feedforward und Feedback | Differenzengleichungen lesen | $y[n]=x[n]+gx[n-M]$, $y[n]=x[n]+gy[n-M]$ | Hörvergleich Echo vs. Feedback-Echo | Strukturunterschied zeigen |
| 105–115 min | Von Differenzengleichung zu $H(z)$ | z-Schreibweise herleiten | $x[n-k]\leftrightarrow z^{-k}X(z)$ | Gleichung links, $H(z)$ rechts | algebraische Systemsprache einführen |
| 115–120 min | Abschluss und Ausblick | Kernkompetenzen verdichten | allgemeine $H(z)$-Form | Zähler/Nenner/FIR/IIR-Ausblick | Anschluss an Pole/Nullstellen vorbereiten |

---

## 6. Ausführliche Blockkonzeption

### Block 0: Rückbezug und Perspektivwechsel

#### Kernaussage für Studierende

> Ein Spektrum sagt, was in einem Signal steckt. Eine Systembeschreibung sagt, was ein System mit diesem Signal macht.

#### Intuitive Erklärung

In den bisherigen Einheiten wurde ein Signal betrachtet: Wir haben gefragt, welche Frequenzen enthalten sind, wie Fensterung die Beobachtung verändert und wie ein Signal lokal über die STFT analysiert werden kann. Jetzt stellen wir ein Gerät, einen Raum oder einen Algorithmus in den Mittelpunkt. Ein Equalizer, ein Lautsprecher oder ein Hallgerät ist nicht selbst das Signal, sondern verändert ein Signal.

#### Mathematische Herleitung für mich als Dozent

Die bisherige Analyseperspektive lautete typischerweise:

$$
X[k] = \sum_{n=0}^{N-1} x[n]w[n]e^{-j\Omega_k n}.
$$

Hier wird ein Signal $x[n]$ beobachtet, gegebenenfalls durch ein Fenster $w[n]$ begrenzt, und dann auf komplexe Basisfunktionen projiziert. Das Ergebnis ist eine Analysegröße.

Die neue Systemperspektive lautet:

$$
 y[n] = \mathcal{T}\{x[n]\}.
$$

Hier steht nicht die Beobachtung eines Ausschnitts im Vordergrund, sondern eine Abbildung. Das System $\mathcal{T}$ erzeugt aus einem Eingang $x[n]$ einen Ausgang $y[n]$. Die mathematische Frage lautet nicht: „Welche Koeffizienten beschreiben $x[n]$?“, sondern: „Welche Vorschrift beschreibt die Transformation von $x[n]$ zu $y[n]$?“

Der didaktisch kritische Punkt ist die Trennung zwischen $w[n]$ und $h[n]$:

$$
 x_{obs}[n] = x[n]w[n]
$$

ist eine Beobachtungsoperation, während

$$
 y[n] = x[n]*h[n]
$$

eine Systemwirkung für ein LTI-System beschreibt.

#### Didaktische Reduktion für die Folie

Auf die Folie:

- links: „Analyse: Was steckt im Signal?“ mit $X[k]$, Spektrum, STFT,
- rechts: „System: Was macht etwas mit dem Signal?“ mit $x[n]\to y[n]$,
- Warnbox: $w[n]\neq h[n]$.

Mündlich:

- Fensterung ist unser Mess-/Analysewerkzeug,
- Impulsantwort ist eine Eigenschaft des Systems,
- beide können mathematisch Multiplikation/Faltung erzeugen, sind aber semantisch verschieden.

#### Audio-Engineering-Beispiel

Ein FFT-Analyzer im Studio zeigt, welche Frequenzen in einem Gitarrensignal enthalten sind. Ein Equalizer verändert diese Frequenzen. Der Analyzer ist Beobachtung, der Equalizer ist System.

#### Visualisierung oder Demo

Kurzes Tafelbild:

| Perspektive | Darstellung |
|---|---|
| Signalperspektive | $x[n]\rightarrow \text{Analyse}\rightarrow X[k]$ |
| Systemperspektive | $x[n]\rightarrow \text{System}\rightarrow y[n]$ |

Dazu zwei kleine Icons: Lupe für Analyse, Gerät/Blackbox für System.

#### Typische Stolperfalle

Studierende sagen: „Das Fenster macht doch auch etwas mit dem Signal, also ist es auch ein System.“ Das ist formal nicht völlig falsch, aber didaktisch gefährlich. In der Analyse verwenden wir das Fenster absichtlich als Beobachtungsbegrenzung. In der Systemtheorie interessiert uns eine reale oder algorithmische Signalverarbeitung.

#### Übergangssatz

> Wenn wir Systeme untersuchen wollen, brauchen wir zuerst eine allgemeine Sprache dafür, was ein System überhaupt ist.

---

### Block 1: Systembegriff

#### Kernaussage für Studierende

> Ein System ist eine Vorschrift, die aus einer Eingangsfolge $x[n]$ eine Ausgangsfolge $y[n]$ erzeugt.

#### Intuitive Erklärung

Ein System kann ein reales Gerät sein, ein akustischer Raum, ein Mikrofon, ein Lautsprecher oder ein Algorithmus in einer DAW. Entscheidend ist nicht zuerst, wie es innen aufgebaut ist. Entscheidend ist: Was kommt heraus, wenn etwas hineingeht?

Im Audio Engineering ist dieser abstrakte Blick praktisch, weil sehr unterschiedliche Dinge gleich beschrieben werden können: Ein Raum, ein EQ und ein Delay sind physikalisch oder algorithmisch verschieden, aber alle können als Abbildung von Eingang zu Ausgang betrachtet werden.

#### Mathematische Herleitung für mich als Dozent

Formal schreiben wir:

$$
 y[n] = \mathcal{T}\{x[n]\}.
$$

$\mathcal{T}$ ist ein Operator. Er nimmt nicht einen einzelnen Zahlenwert, sondern eine ganze Folge als Argument. Das ist wichtig: Der Ausgangswert $y[n]$ kann von vielen Eingangswerten abhängen, etwa von $x[n]$, $x[n-1]$, $x[n-2]$ usw.

Beispiel 1, reiner Gain:

$$
 y[n] = g x[n].
$$

Hier hängt $y[n]$ nur vom aktuellen Eingang ab.

Beispiel 2, Delay:

$$
 y[n] = x[n-M].
$$

Hier hängt $y[n]$ von einem früheren Eingangswert ab.

Beispiel 3, einfaches Echo:

$$
 y[n] = x[n] + g x[n-M].
$$

Hier werden aktueller Eingang und verzögerter Eingang addiert.

Beispiel 4, Feedback-Echo:

$$
 y[n] = x[n] + g y[n-M].
$$

Hier hängt der Ausgang von einem vergangenen Ausgang ab. Das ist strukturell anders, weil das System intern speichert und zurückführt.

#### Didaktische Reduktion für die Folie

Auf die Folie:

$$
 y[n] = \mathcal{T}\{x[n]\}
$$

mit Systemblock:

$$
x[n]\rightarrow \text{System }\mathcal{T}\rightarrow y[n]
$$

Darunter Beispiele:

- Lautsprecher,
- Raum,
- Mikrofon,
- EQ,
- Delay,
- Reverb.

Mündlich erklären:

- $\mathcal{T}$ ist eine Blackbox-Vorschrift,
- wir fragen zunächst nicht nach Bauteilen, sondern nach Ein-/Ausgangsverhalten,
- später wird diese Blackbox durch Impulsantwort und $H(z)$ beschreibbar.

#### Audio-Engineering-Beispiel

Ein Lautsprecher kann als System betrachtet werden: elektrische Eingangsspannung hinein, Schalldruckverlauf heraus. Ein Raum kann ebenfalls als System betrachtet werden: Schallereignis hinein, an einer Hörposition ankommender Schall heraus.

#### Visualisierung oder Demo

Drei Systemblöcke nebeneinander:

$$
\begin{aligned}
x[n] &\rightarrow \text{Gain}\rightarrow y[n] \\
x[n] &\rightarrow \text{Delay}\rightarrow y[n] \\
x[n] &\rightarrow \text{Room/Reverb}\rightarrow y[n]
\end{aligned}
$$

Hörbeispiel: kurzer trockener Klick oder Snarehit durch drei Systeme: Gain, Delay, Reverb.

#### Typische Stolperfalle

Studierende sehen $\mathcal{T}$ als „eine Formel“, obwohl es eine ganze Klasse von möglichen Verarbeitungen meint.

**Korrektursatz:**  
> $\mathcal{T}$ ist nicht eine bestimmte Rechnung, sondern ein Platzhalter für die gesamte Verarbeitung zwischen Eingang und Ausgang.

#### Übergangssatz

> Damit wir aus einem einzigen Testsignal auf das ganze System schließen dürfen, brauchen wir zwei Eigenschaften: Linearität und Zeitinvarianz.

---

### Block 2: Linearität und Zeitinvarianz

#### Kernaussage für Studierende

> Nur bei linearen zeitinvarianten Systemen reicht die Impulsantwort aus, um die Wirkung auf jedes Eingangssignal durch Faltung vorherzusagen.

#### Intuitive Erklärung

Linearität bedeutet: Wenn ich zwei Signale getrennt verarbeiten und anschließend addieren würde, bekomme ich dasselbe Ergebnis, als würde ich sie erst addieren und dann verarbeiten. Zeitinvarianz bedeutet: Wenn ich das Eingangssignal später starte, startet auch die Antwort später, aber sie verändert nicht ihre Form.

Viele Audiosysteme sind nur näherungsweise LTI. Ein Lautsprecher bei moderaten Pegeln kann näherungsweise linear sein. Bei Übersteuerung, Clipping oder Sättigung ist er es nicht mehr. Ein Raum ist ungefähr zeitinvariant, solange niemand Mikrofon, Lautsprecher oder Absorber bewegt. Ein Chorus oder Flanger mit LFO ist nicht zeitinvariant, weil sich seine Parameter über die Zeit ändern.

#### Mathematische Herleitung für mich als Dozent

Linearität besteht aus Additivität und Homogenität:

$$
\mathcal{T}\{a x_1[n] + b x_2[n]\}
= a\mathcal{T}\{x_1[n]\} + b\mathcal{T}\{x_2[n]\}.
$$

Wenn

$$
\mathcal{T}\{x_1[n]\}=y_1[n]
$$

und

$$
\mathcal{T}\{x_2[n]\}=y_2[n],
$$

muss gelten:

$$
\mathcal{T}\{a x_1[n] + b x_2[n]\}=a y_1[n]+b y_2[n].
$$

Zeitinvarianz bedeutet:

Wenn

$$
\mathcal{T}\{x[n]\}=y[n],
$$

muss für jede ganzzahlige Verzögerung $n_0$ gelten:

$$
\mathcal{T}\{x[n-n_0]\}=y[n-n_0].
$$

Diese Eigenschaft ist später entscheidend, weil aus der Antwort auf $\delta[n]$ die Antwort auf $\delta[n-m]$ wird:

$$
\mathcal{T}\{\delta[n]\}=h[n]
$$

und wegen Zeitinvarianz:

$$
\mathcal{T}\{\delta[n-m]\}=h[n-m].
$$

Wegen Linearität dürfen die gewichteten Einzelantworten addiert werden. Genau daraus entsteht die Faltung.

#### Didaktische Reduktion für die Folie

Auf die Folie:

**Linearität:**

$$
\mathcal{T}\{a x_1[n]+b x_2[n]\}=a y_1[n]+b y_2[n]
$$

**Zeitinvarianz:**

$$
 x[n]\to y[n]
\quad \Rightarrow \quad
 x[n-n_0]\to y[n-n_0]
$$

Darunter Beispiele:

- linear ungefähr: kleiner Pegel durch EQ,
- nichtlinear: Clipping, Sättigung, Distortion,
- zeitvariant: Chorus, bewegtes Mikrofon, automatisierter Filter.

Mündlich:

- LTI ist ein Modell, kein Naturgesetz,
- sehr viele Audioanalysen und Filterentwürfe starten mit diesem Modell.

#### Audio-Engineering-Beispiel

Ein Gitarren-Distortion-Pedal ist nicht linear: Zwei leise Sinustöne einzeln betrachtet erzeugen andere Spektren als beide zusammen, weil Intermodulation auftreten kann. Ein statischer EQ ist bei normalen Pegeln näherungsweise linear und zeitinvariant.

#### Visualisierung oder Demo

1. Zwei Sinustöne einzeln durch linearen Gain schicken, Summe vergleichen.
2. Zwei Sinustöne durch Clipping schicken, zusätzliche Spektrallinien zeigen.
3. Ein Delay mit konstantem $M$ vs. modulierter Delayzeit zeigen.

#### Typische Stolperfalle

Studierende denken, „linear“ bedeute „gerade Linie im Zeitverlauf“ oder „nicht verzerrt aussehend“.

**Korrektursatz:**  
> Linearität meint nicht, dass ein Signal gerade aussieht, sondern dass Skalierung und Addition vor und nach dem System gleichwertig sind.

#### Übergangssatz

> Wenn ein System LTI ist, können wir es mit dem einfachsten möglichen Signal testen: einem einzelnen Sample-Impuls.

---

### Block 3: Diskreter Impuls und Impulsantwort

#### Kernaussage für Studierende

> Die Impulsantwort ist die vollständige Antwort eines LTI-Systems auf einen Ein-Sample-Anstoß.

#### Intuitive Erklärung

Der diskrete Impuls ist der digitale Idealfall eines Klicks: genau ein Sample ist 1, alle anderen sind 0. Wenn wir diesen Klick in ein System schicken, sehen wir, was das System daraus macht. Ein ideales Durchleitungssystem gibt wieder einen einzelnen Klick aus. Ein Delay gibt den Klick später aus. Ein Echo-System erzeugt mehrere Klicks. Ein Raum erzeugt eine komplexe, ausklingende Antwort.

#### Mathematische Herleitung für mich als Dozent

Der diskrete Impuls ist definiert als:

$$
\delta[n]=
\begin{cases}
1, & n=0,\\
0, & n\neq 0.
\end{cases}
$$

Die Impulsantwort eines Systems $\mathcal{T}$ ist:

$$
 h[n] = \mathcal{T}\{\delta[n]\}.
$$

Beispiele:

1. Idealer Durchgang:

$$
 y[n]=x[n]
\Rightarrow h[n]=\delta[n].
$$

2. Gain:

$$
 y[n]=g x[n]
\Rightarrow h[n]=g\delta[n].
$$

3. Ein Sample Delay:

$$
 y[n]=x[n-1]
\Rightarrow h[n]=\delta[n-1].
$$

4. Feedforward-Echo:

$$
 y[n]=x[n]+g x[n-M]
\Rightarrow h[n]=\delta[n]+g\delta[n-M].
$$

5. Feedback-Echo:

$$
 y[n]=x[n]+g y[n-M].
$$

Für Eingang $x[n]=\delta[n]$ entsteht rekursiv:

$$
 h[n]=\delta[n]+g h[n-M].
$$

Daraus folgt bei $|g|<1$:

$$
 h[n]=\delta[n]+g\delta[n-M]+g^2\delta[n-2M]+g^3\delta[n-3M]+\dots
$$

Diese Reihe ist ein sehr anschaulicher erster Zugang zu IIR: Die Impulsantwort kann theoretisch unendlich lang sein.

#### Didaktische Reduktion für die Folie

Auf die Folie:

$$
\delta[n]=
\begin{cases}
1, & n=0\\
0, & n\neq 0
\end{cases}
$$

$$
 h[n]=\mathcal{T}\{\delta[n]\}
$$

Vier Mini-Plots:

- $\delta[n]$,
- $g\delta[n]$,
- $\delta[n-M]$,
- $\delta[n]+g\delta[n-M]$.

Mündlich:

- $x[n]$ ist Eingang,
- $y[n]$ ist Ausgang,
- $h[n]$ ist Systemeigenschaft.

#### Audio-Engineering-Beispiel

In der Lautsprechermesstechnik wird eine Impulsantwort gemessen. Daraus können zeitliches Ausschwingen, Reflexionen und Frequenzgang abgeleitet werden. In der Hallfaltung wird ein trockenes Signal mit einer Raumimpulsantwort verarbeitet.

#### Visualisierung oder Demo

Python- oder DAW-Demo:

- Erzeuge einen Ein-Sample-Impuls.
- Schicke ihn durch:
  - Gain,
  - Delay,
  - Feedforward-Echo,
  - Feedback-Echo,
  - kleine Raum-IR.
- Zeige jeweils den Zeitverlauf.

#### Typische Stolperfalle

Studierende sagen: „Die Impulsantwort ist der Klick.“

**Korrektursatz:**  
> Der Klick ist der Eingang $\delta[n]$; die Impulsantwort $h[n]$ ist das, was das System aus diesem Klick macht.

#### Übergangssatz

> Wenn wir jedes Signal als viele verschobene Klicks schreiben können, können wir aus der Impulsantwort die Antwort auf jedes Signal zusammensetzen.

---

### Block 4: Impulszerlegung und diskrete Faltung

#### Kernaussage für Studierende

> Jedes Eingangssample startet eine verschobene und skalierte Kopie der Impulsantwort; der Ausgang ist die Summe aller Kopien.

#### Intuitive Erklärung

Stellen Sie sich $h[n]$ als Klangantwort auf einen einzelnen Klick vor. Wenn ein Signal viele Samples enthält, dann ist jedes Sample ein kleiner Klick mit eigener Lautstärke und eigener Startzeit. Jedes dieser Samples startet eine Kopie der Impulsantwort. Alle Kopien überlagern sich. Diese Überlagerung heißt Faltung.

#### Mathematische Herleitung für mich als Dozent

Zuerst wird jede diskrete Folge als Summe gewichteter, verschobener Impulse geschrieben:

$$
 x[n] = \sum_m x[m]\delta[n-m].
$$

Warum stimmt das? Für ein festes $n$ ist $\delta[n-m]$ nur dann 1, wenn $m=n$. Für alle anderen $m$ ist es 0. Daher bleibt in der Summe nur ein Term übrig:

$$
\sum_m x[m]\delta[n-m] = x[n].
$$

Beispiel:

$$
 x[n]=[2,-1,0,3]
$$

mit Start bei $n=0$. Dann:

$$
 x[n]
=2\delta[n]
-1\delta[n-1]
+0\delta[n-2]
+3\delta[n-3].
$$

Der Nullterm kann weggelassen werden:

$$
 x[n]=2\delta[n]-\delta[n-1]+3\delta[n-3].
$$

Nun wird das System angewendet:

$$
 y[n]=\mathcal{T}\{x[n]\}
=\mathcal{T}\left\{\sum_m x[m]\delta[n-m]\right\}.
$$

Wegen Linearität:

$$
 y[n]=\sum_m x[m]\mathcal{T}\{\delta[n-m]\}.
$$

Wegen Zeitinvarianz:

$$
\mathcal{T}\{\delta[n-m]\}=h[n-m].
$$

Also:

$$
 y[n]=\sum_m x[m]h[n-m].
$$

Das ist die diskrete Faltung:

$$
 y[n]=(x*h)[n]=\sum_m x[m]h[n-m].
$$

Für das Zahlenbeispiel gilt:

$$
 y[n]=2h[n]-h[n-1]+3h[n-3].
$$

Diese Form ist didaktisch wertvoller als sofort die allgemeine Summe, weil sie direkt zeigt: Kopien von $h[n]$ werden skaliert, verschoben und addiert.

#### Didaktische Reduktion für die Folie

Folie 1:

$$
 x[n]=\sum_m x[m]\delta[n-m]
$$

mit Zahlenfolge:

$$
x[n]=[2,\,-1,\,0,\,3]
$$

Folie 2:

$$
 x[n]=2\delta[n]-\delta[n-1]+3\delta[n-3]
$$

Folie 3:

$$
\begin{aligned}
&2\cdot h[n] \\
&-1\cdot h[n-1] \\
&3\cdot h[n-3] \\
&\text{Summe}=y[n]
\end{aligned}
$$

Folie 4:

$$
 y[n]=\sum_m x[m]h[n-m]
$$

Mündlich:

- Erst konkrete Kopien zeigen,
- erst danach Summationsnotation,
- Indizes als „Startzeit der Kopie“ erklären.

#### Audio-Engineering-Beispiel

Ein trockenes Drumloop-Signal wird mit einer Raumimpulsantwort gefaltet. Jeder Sample-Anteil des Drumloops startet eine kleine, skalierte Kopie der Raumantwort. Daher entsteht der Eindruck, als sei das trockene Signal im gemessenen Raum abgespielt worden.

#### Visualisierung oder Demo

Tafelbild oder Python-Demo:

- $h[n]=[1,0.5,0.25]$,
- $x[n]=[2,-1,0,3]$,
- zeige vier Zeilen:
  - $2h[n]$,
  - $-h[n-1]$,
  - $0h[n-2]$,
  - $3h[n-3]$,
- addiere sampleweise zu $y[n]$.

#### Typische Stolperfalle

Studierende lesen $h[n-m]$ als willkürliche Indexmagie.

**Korrektursatz:**  
> Der Index $m$ sagt, bei welchem Eingangssample die Kopie der Impulsantwort gestartet wird; $h[n-m]$ ist genau diese um $m$ Samples verschobene Kopie.

#### Übergangssatz

> Diese Zeitbereichssicht erklärt, wie das Ausgangssignal zusammengesetzt wird. Jetzt verbinden wir das mit der bekannten Frequenzsicht.

---

### Block 5: Faltung als Audio-Engineering-Prozess

#### Kernaussage für Studierende

> Faltung ist die allgemeine LTI-Systemwirkung – Hall ist nur ein besonders hörbares Beispiel dafür.

#### Intuitive Erklärung

Faltung ist nicht automatisch Hall und nicht einfach Glättung. Wenn die Impulsantwort sehr kurz ist, kann die Faltung wie ein kleiner Filter wirken. Wenn sie Echos enthält, entstehen Echo- oder Kammfiltereffekte. Wenn sie eine lange Raumantwort enthält, entsteht Hall. Wenn sie eine Lautsprecherantwort enthält, beschreibt sie die Klangfärbung eines Lautsprechers.

#### Mathematische Herleitung für mich als Dozent

Für jedes LTI-System gilt:

$$
 y[n]=(x*h)[n].
$$

Die Form von $h[n]$ entscheidet über die hörbare Wirkung.

1. $h[n]=\delta[n]$:

$$
 y[n]=x[n].
$$

2. $h[n]=g\delta[n]$:

$$
 y[n]=gx[n].
$$

3. $h[n]=\delta[n-M]$:

$$
 y[n]=x[n-M].
$$

4. $h[n]=\delta[n]+g\delta[n-M]$:

$$
 y[n]=x[n]+g x[n-M].
$$

5. Lange Raumantwort:

$$
 y[n]=\sum_m x[m]h_{room}[n-m].
$$

Die gleiche Formel beschreibt sehr verschiedene Audioeffekte. Daher ist Faltung ein Strukturprinzip, keine bestimmte Klangästhetik.

#### Didaktische Reduktion für die Folie

Eine Tabelle:

| $h[n]$ | Systemwirkung | Audio-Begriff |
|---|---|---|
| $\delta[n]$ | unverändert | Bypass |
| $g\delta[n]$ | Pegeländerung | Gain |
| $\delta[n-M]$ | Verzögerung | Delay |
| $\delta[n]+g\delta[n-M]$ | Direkt + Kopie | Echo / Comb |
| lange Raum-IR | viele Reflexionen | Faltungshall |

#### Audio-Engineering-Beispiel

Faltungshall: Eine reale Raumimpulsantwort wird aufgenommen. Ein trockenes Sprach- oder Musiksample wird mit dieser Impulsantwort gefaltet. Das Ergebnis trägt die zeitlichen und spektralen Eigenschaften dieses Raumes.

#### Visualisierung oder Demo

Hörvergleich:

1. trockenes Signal,
2. mit kurzem Echo-$h[n]$,
3. mit Raum-$h[n]$,
4. mit Lautsprecherkorrektur-$h[n]$.

#### Typische Stolperfalle

Studierende sagen: „Faltung macht ein Signal weicher.“

**Korrektursatz:**  
> Faltung macht nicht automatisch weich; sie bildet die Wirkung der jeweiligen Impulsantwort ab – das kann Delay, Filterung, Hall, Auslöschung oder Resonanz sein.

#### Übergangssatz

> Wenn eine Impulsantwort ein System im Zeitbereich beschreibt, stellt sich die nächste Frage: Wie wirkt dasselbe System auf Frequenzanteile?

---

### Block 6: Impulsantwort und Frequenzgang

#### Kernaussage für Studierende

> Ein LTI-System verändert eine komplexe Sinusschwingung nicht in ihrer Frequenz, sondern nur in Amplitude und Phase.

#### Intuitive Erklärung

Wenn ein Sinus durch einen linearen zeitinvarianten Equalizer geht, kommt kein anderer Sinus mit neuer Frequenz heraus. Ein 1-kHz-Sinus bleibt 1 kHz. Er kann lauter, leiser oder phasenverschoben werden. Diese komplexe Gewichtung für jede Frequenz ist der Frequenzgang.

#### Mathematische Herleitung für mich als Dozent

Für ein LTI-System gilt:

$$
 y[n]=\sum_\ell h[\ell]x[n-\ell].
$$

Setze als Eingang eine komplexe Exponentialfolge:

$$
 x[n]=e^{j\Omega n}.
$$

Dann:

$$
 y[n]
=\sum_\ell h[\ell]e^{j\Omega(n-\ell)}.
$$

Der Faktor $e^{j\Omega n}$ hängt nicht von $\ell$ ab und kann aus der Summe gezogen werden:

$$
 y[n]
=e^{j\Omega n}\sum_\ell h[\ell]e^{-j\Omega\ell}.
$$

Definiere:

$$
 H(e^{j\Omega})=\sum_\ell h[\ell]e^{-j\Omega\ell}.
$$

Dann:

$$
 y[n]=H(e^{j\Omega})e^{j\Omega n}.
$$

Das zeigt die Eigenfunktions-Eigenschaft: Die Form $e^{j\Omega n}$ bleibt erhalten. Das System multipliziert sie nur mit einem komplexen Faktor.

$H(e^{j\Omega})$ ist im Allgemeinen komplex:

$$
 H(e^{j\Omega})=|H(e^{j\Omega})|e^{j\varphi(\Omega)}.
$$

Damit:

$$
 y[n]=|H(e^{j\Omega})|e^{j(\Omega n+\varphi(\Omega))}.
$$

Betrag entspricht Amplitudenänderung, Phase entspricht Phasenverschiebung.

#### Didaktische Reduktion für die Folie

Auf die Folie:

$$
 x[n]=e^{j\Omega n}
$$

$$
 y[n]=\sum_\ell h[\ell]e^{j\Omega(n-\ell)}
=e^{j\Omega n}\underbrace{\sum_\ell h[\ell]e^{-j\Omega\ell}}_{H(e^{j\Omega})}
$$

Merksatz:

> Frequenz bleibt, Betrag und Phase ändern sich.

Mündlich:

- Das ist dieselbe Logik wie bei der DFT-Basis,
- aber jetzt beschreiben wir nicht das Signal, sondern das Systemverhalten.

#### Audio-Engineering-Beispiel

Ein Lowpass-Filter lässt tiefe Sinustöne mit großem Betrag durch und schwächt hohe Sinustöne ab. Ein Allpass kann den Betrag gleich lassen, aber die Phase verändern.

#### Visualisierung oder Demo

Python-Demo:

- Erzeuge Sinus bei $\Omega=0.1\pi$, $0.5\pi$, $0.9\pi$,
- schicke durch gleitenden Mittelwert $h[n]=[1/3,1/3,1/3]$,
- zeige Eingangs- und Ausgangsamplitude,
- plotte $|H(e^{j\Omega})|$.

#### Typische Stolperfalle

Studierende denken, $H(e^{j\Omega})$ sei das Spektrum des Ausgangssignals.

**Korrektursatz:**  
> $H(e^{j\Omega})$ ist kein Signalspektrum, sondern die frequenzabhängige Gewichtung, die das System auf Eingangskomponenten anwendet.

#### Übergangssatz

> Um solche Systeme praktisch zu bauen, brauchen wir digitale Speicherbausteine. Der einfachste Speicher ist ein Sample Delay.

---

### Block 7: Delay als elementarer digitaler Speicher

#### Kernaussage für Studierende

> $x[n-1]$ ist der vorherige Samplewert – und $z^{-1}$ wird später genau diese Verzögerung algebraisch darstellen.

#### Intuitive Erklärung

Digitale Signalverarbeitung arbeitet sampleweise. Um den vorherigen Samplewert zu verwenden, muss er gespeichert werden. Ein Delay ist daher nicht nur „später abspielen“, sondern der elementare Speicherbaustein digitaler Systeme. Fast alle digitalen Filter bestehen aus solchen Delays, Multiplikationen und Additionen.

#### Mathematische Herleitung für mich als Dozent

Ein reines Delay um $M$ Samples:

$$
 y[n]=x[n-M].
$$

Die reale Verzögerungszeit ist:

$$
 T_D = M T_s = \frac{M}{f_s}.
$$

Ein Sample Delay:

$$
 y[n]=x[n-1].
$$

Feedforward-Echo:

$$
 y[n]=x[n]+g x[n-M].
$$

Das System verwendet nur Eingangswerte. Die Impulsantwort ist endlich:

$$
 h[n]=\delta[n]+g\delta[n-M].
$$

Feedback-Echo:

$$
 y[n]=x[n]+g y[n-M].
$$

Das System verwendet einen vergangenen Ausgangswert. Für Impulseingang entsteht:

$$
 h[n]=\delta[n]+g\delta[n-M]+g^2\delta[n-2M]+\dots
$$

Bei $|g|<1$ klingt die Folge ab. Bei $|g|\geq 1$ klingt sie nicht ab bzw. wächst.

#### Didaktische Reduktion für die Folie

Auf die Folie:

$$
\begin{aligned}
x[n] &\quad \text{aktueller Samplewert} \\
x[n-1] &\quad \text{vorheriger Samplewert} \\
x[n-M] &\quad \text{um } M \text{ Samples verzoegert}
\end{aligned}
$$

Dann:

$$
 y[n]=x[n-M]
$$

$$
 y[n]=x[n]+g x[n-M]
$$

$$
 y[n]=x[n]+g y[n-M]
$$

Mündlich:

- Feedforward: Eingangskopie,
- Feedback: Ausgang wird zurückgeführt,
- Feedback erzeugt potenziell unendlich lange Antwort.

#### Audio-Engineering-Beispiel

Ein Slapback-Delay im Mix kann als Feedforward-Struktur verstanden werden. Ein klassisches Echo mit Wiederholungen entsteht durch Feedback.

#### Visualisierung oder Demo

Hörbeispiel:

- $M=0.25\,\mathrm{s}$, $g=0.5$, Feedforward,
- $M=0.25\,\mathrm{s}$, $g=0.5$, Feedback,
- $g=0.9$, lange Echos,
- $g=1.05$, Warnung: instabil/wachsend.

#### Typische Stolperfalle

Studierende verstehen $x[n-1]$ als „Frequenzverschiebung“ oder als neue Achse.

**Korrektursatz:**  
> $x[n-1]$ ist keine Frequenzoperation, sondern schlicht der gespeicherte Eingangswert von einem Sample früher.

#### Übergangssatz

> Wenn wir Delays, Multiplikationen und Additionen kombinieren, erhalten wir Differenzengleichungen – die Baupläne digitaler Filter.

---

### Block 8: Differenzengleichung

#### Kernaussage für Studierende

> Eine Differenzengleichung ist ein Bauplan: Sie sagt, welche aktuellen und vergangenen Werte mit welchen Gewichten addiert werden.

#### Intuitive Erklärung

Eine digitale Audiostruktur kann man wie ein kleines Mischpult mit Speichern lesen. Manche Kanäle führen aktuelle oder verzögerte Eingangswerte. Andere führen verzögerte Ausgangswerte zurück. Die Koeffizienten sind Gain-Regler. Die Summe ergibt den neuen Ausgangswert.

#### Mathematische Herleitung für mich als Dozent

Allgemeines FIR-/Feedforward-System:

$$
 y[n]=\sum_{k=0}^{M} b_k x[n-k].
$$

Ausgeschrieben:

$$
 y[n]=b_0x[n]+b_1x[n-1]+b_2x[n-2]+\dots+b_Mx[n-M].
$$

Hier hängt der Ausgang nur von aktuellen und vergangenen Eingangswerten ab. Die Impulsantwort ist:

$$
 h[n]=\sum_{k=0}^{M} b_k\delta[n-k].
$$

Also gilt direkt:

$$
 h[0]=b_0,\quad h[1]=b_1,\quad \dots,\quad h[M]=b_M.
$$

Allgemeines IIR-/Feedback-System:

$$
 y[n]=\sum_{k=0}^{M} b_k x[n-k] - \sum_{r=1}^{R} a_r y[n-r].
$$

Ausgeschrieben:

$$
 y[n]=b_0x[n]+b_1x[n-1]+\dots+b_Mx[n-M]
-a_1y[n-1]-a_2y[n-2]-\dots-a_Ry[n-R].
$$

Der Ausgang hängt von vergangenen Ausgängen ab. Dadurch kann die Impulsantwort länger sein als die Anzahl der Koeffizienten. Bei Feedback kann eine endliche Gleichung eine unendlich lange Impulsantwort erzeugen.

#### Didaktische Reduktion für die Folie

Auf die Folie:

**Feedforward:**

$$
 y[n]=\sum_{k=0}^{M}b_kx[n-k]
$$

**Feedback:**

$$
 y[n]=\sum_{k=0}^{M}b_kx[n-k]-\sum_{r=1}^{R}a_ry[n-r]
$$

Beschriftung:

- $b_k$: Gewichte für Eingangsdelays,
- $a_r$: Gewichte für Ausgangsdelays,
- Feedforward: keine Rückführung,
- Feedback: vergangene Ausgänge gehen wieder ein.

#### Audio-Engineering-Beispiel

Ein einfacher FIR-Filter kann ein gleitender Mittelwert sein:

$$
 y[n]=\frac{1}{3}x[n]+\frac{1}{3}x[n-1]+\frac{1}{3}x[n-2].
$$

Ein einfacher IIR-Filter kann eine rekursive Glättung sein:

$$
 y[n]=(1-\alpha)x[n]+\alpha y[n-1].
$$

#### Visualisierung oder Demo

Tafelübung: Aus einem Blockdiagramm mit zwei Delays und drei $b$-Koeffizienten die Gleichung ablesen. Danach umgekehrt: Aus einer Gleichung ein Blockdiagramm zeichnen.

#### Typische Stolperfalle

Studierende behandeln $a_r$ und $b_k$ als austauschbare Koeffizienten.

**Korrektursatz:**  
> $b$-Koeffizienten gewichten verzögerte Eingänge; $a$-Koeffizienten gewichten rückgeführte Ausgänge – das ist strukturell nicht dasselbe.

#### Übergangssatz

> Mit $z^{-1}$ können wir dieselben Delay-Strukturen algebraisch viel kompakter schreiben.

---

### Block 9: Von der Differenzengleichung zur z-Schreibweise

#### Kernaussage für Studierende

> $z^{-1}$ ist zunächst die algebraische Schreibweise für ein Sample Delay.

#### Intuitive Erklärung

In Blockdiagrammen ist ein Delay oft als Kästchen mit $z^{-1}$ dargestellt. Dieses Symbol bedeutet: Der Wert wird um ein Sample verzögert. Die z-Transformation macht aus Verzögerungen algebraische Faktoren. Dadurch kann man aus einer Differenzengleichung eine kompakte Systemfunktion bilden.

#### Mathematische Herleitung für mich als Dozent

Die Verschiebungseigenschaft unter Nullanfangsbedingungen lautet:

$$
\mathcal{Z}\{x[n-k]\}=z^{-k}X(z).
$$

Für ein FIR-Beispiel:

$$
 y[n]=b_0x[n]+b_1x[n-1]+b_2x[n-2].
$$

z-Transformation:

$$
 Y(z)=b_0X(z)+b_1z^{-1}X(z)+b_2z^{-2}X(z).
$$

Faktorisieren:

$$
 Y(z)=\left(b_0+b_1z^{-1}+b_2z^{-2}\right)X(z).
$$

Systemfunktion:

$$
 H(z)=\frac{Y(z)}{X(z)}=b_0+b_1z^{-1}+b_2z^{-2}.
$$

Für ein Feedback-Beispiel:

$$
 y[n]=b_0x[n]-a_1y[n-1].
$$

z-Transformation:

$$
 Y(z)=b_0X(z)-a_1z^{-1}Y(z).
$$

Alle $Y(z)$-Terme auf eine Seite:

$$
 Y(z)+a_1z^{-1}Y(z)=b_0X(z).
$$

Ausklammern:

$$
 Y(z)(1+a_1z^{-1})=b_0X(z).
$$

Division durch $X(z)$ und durch den Klammerausdruck:

$$
 H(z)=\frac{Y(z)}{X(z)}=\frac{b_0}{1+a_1z^{-1}}.
$$

Allgemein:

$$
H(z)=
\frac{b_0+b_1z^{-1}+\dots+b_Mz^{-M}}
{1+a_1z^{-1}+\dots+a_Rz^{-R}}.
$$

#### Didaktische Reduktion für die Folie

Folie 1:

$$
 x[n-1] \leftrightarrow z^{-1}X(z)
$$

Merksatz:

> $z^{-1}$ bedeutet: ein Sample Delay.

Folie 2: FIR-Herleitung in drei Zeilen.

Folie 3: IIR-Herleitung in vier Zeilen.

Folie 4: allgemeine Form mit farblicher Markierung:

- Zähler = Feedforward,
- Nenner = Feedback.

#### Audio-Engineering-Beispiel

Ein dreitap-FIR-EQ oder Comb-Filter kann direkt aus seinen $b$-Koeffizienten als $H(z)$ geschrieben werden. Ein Feedback-Delay bekommt durch Rückführung einen Nenner.

#### Visualisierung oder Demo

Gleiche Struktur dreifach zeigen:

1. Blockdiagramm,
2. Differenzengleichung,
3. $H(z)$.

Beispiel:

$$
 y[n]=x[n]+0.5x[n-4]
$$

$$
 H(z)=1+0.5z^{-4}.
$$

Dann:

$$
 y[n]=x[n]+0.5y[n-4]
$$

$$
 H(z)=\frac{1}{1-0.5z^{-4}}.
$$

#### Typische Stolperfalle

Studierende denken, $z^{-1}$ sei eine Frequenzachse oder ein neuer Sampleindex.

**Korrektursatz:**  
> In dieser Lesart ist $z^{-1}$ zunächst kein neuer Zeitindex und keine Frequenzachse, sondern die algebraische Markierung eines Sample-Delays.

#### Übergangssatz

> Sobald wir $H(z)$ lesen können, können wir Feedforward, Feedback, FIR und IIR sehr kompakt unterscheiden.

---

### Block 10: Bedeutung von $H(z)$, FIR/IIR und Ausblick

#### Kernaussage für Studierende

> $H(z)$ beschreibt das System, nicht das Signal.

#### Intuitive Erklärung

$H(z)$ ist wie ein Schaltplan in Formelgestalt. Man kann daran sehen, welche verzögerten Eingangswerte verwendet werden und ob vergangene Ausgangswerte zurückgeführt werden. Es ist keine Audiodatei, kein Spektrogramm und kein einzelnes Spektrum.

#### Mathematische Herleitung für mich als Dozent

Für ein LTI-System gilt im z-Bereich:

$$
 Y(z)=H(z)X(z).
$$

Daraus:

$$
 H(z)=\frac{Y(z)}{X(z)}.
$$

Diese Division ist als Systemrelation sinnvoll, wenn $X(z)$ und $Y(z)$ über dasselbe LTI-System verbunden sind. $H(z)$ ist dann unabhängig vom konkreten Eingangssignal, solange das System LTI bleibt und die Transformationen existieren.

Allgemeine Form:

$$
H(z)=
\frac{b_0+b_1z^{-1}+\dots+b_Mz^{-M}}
{1+a_1z^{-1}+\dots+a_Rz^{-R}}.
$$

Nur Zähler:

$$
H(z)=b_0+b_1z^{-1}+\dots+b_Mz^{-M}
$$

entspricht FIR.

Zähler und Nenner:

$$
H(z)=\frac{B(z)}{A(z)}
$$

entspricht IIR, sofern Feedback vorhanden ist.

Ausblick:

- Nullstellen entstehen aus dem Zähler,
- Pole entstehen aus dem Nenner,
- Nullstellen können Frequenzanteile auslöschen,
- Pole können Resonanzen und Ausklingverhalten erzeugen,
- Stabilität hängt später mit Pollagen zusammen.

#### Didaktische Reduktion für die Folie

Auf die Folie:

$$
Y(z)=H(z)X(z)
$$

$$
H(z)=\frac{Y(z)}{X(z)}
$$

$$
H(z)=\frac{\text{Feedforward}}{\text{Feedback}}
=\frac{b_0+b_1z^{-1}+\dots+b_Mz^{-M}}
{1+a_1z^{-1}+\dots+a_Rz^{-R}}
$$

Mündlich:

- $H(z)$ ist Systemsprache,
- $H(e^{j\Omega})$ kommt später durch Einheitskreisauswertung,
- Pole/Nullstellen werden vorbereitet, nicht heute vertieft.

#### Audio-Engineering-Beispiel

Ein Feedback-Delay klingt länger aus als ein Feedforward-Delay, weil der Nenner von $H(z)$ Rückführung ausdrückt. In der späteren Filteranalyse wird sichtbar, wie diese Rückführung Resonanzen und Stabilitätsfragen erzeugt.

#### Visualisierung oder Demo

Schlussfolie:

$$
\begin{aligned}
\text{Zeitbereich:}      &\quad h[n] \\
\text{Faltung:}          &\quad y[n]=x[n]\ast h[n] \\
\text{Struktur:}         &\quad \text{Differenzengleichung} \\
\text{z-Sprache:}        &\quad H(z) \\
\text{Frequenzwirkung:}  &\quad H(e^{j\Omega})
\end{aligned}
$$

#### Typische Stolperfalle

Studierende setzen $H(z)$ mit einem Spektrogramm oder einer DFT gleich.

**Korrektursatz:**  
> Ein Spektrum beschreibt ein Signal; $H(z)$ beschreibt ein System, das Signale verändert.

#### Übergangssatz

> In der nächsten Vorlesung lesen wir $H(z)$ geometrisch: Was bedeuten Pole, Nullstellen und der Einheitskreis für den hörbaren Frequenzgang?

---

## 7. Typische Verständnisprobleme und direkte Korrektursätze

| Fehlvorstellung | Warum sie entsteht | Korrektursatz für die Vorlesung |
|---|---|---|
| $h[n]$ wird mit $x[n]$ verwechselt. | Beides sind Folgen im Zeitbereich. | „$x[n]$ ist das Eingangssignal; $h[n]$ ist die Systemantwort auf einen Impuls.“ |
| Die Impulsantwort wird als Messsignal verstanden. | Der Impuls ist der Testreiz; die Antwort wird gemessen. | „Der Impuls ist der Test; die Impulsantwort ist das gemessene Ergebnis des Systems.“ |
| Faltung wird als reine Rechenvorschrift verstanden. | Die Summenformel wirkt abstrakt. | „Faltung bedeutet: Jedes Eingangssample startet eine skalierte, verschobene Kopie der Impulsantwort.“ |
| Fensterung und Systemfaltung werden verwechselt. | Beide nutzen Multiplikation/Faltung-Zusammenhänge. | „Fensterung begrenzt unsere Beobachtung; eine Impulsantwort beschreibt eine reale oder algorithmische Systemwirkung.“ |
| $z^{-1}$ wirkt wie eine neue Frequenzachse. | Das Symbol $z$ ist ungewohnt und abstrakt. | „Für heute lesen wir $z^{-1}$ ganz praktisch als ein Sample Delay.“ |
| $H(z)$ wird mit einem Spektrogramm verwechselt. | Beide sehen wie Frequenz-/Transformationsdarstellungen aus. | „Ein Spektrogramm beschreibt ein Signal über Zeit und Frequenz; $H(z)$ beschreibt eine Systemstruktur.“ |
| Feedback wird nur als „mehr Echo“ verstanden. | Hörbeispiel klingt wie Wiederholungen. | „Feedback bedeutet strukturell: Ein vergangener Ausgang wird wieder Eingang des Systems.“ |
| $H(z)$ wird zu früh mit Pol-Nullstellen-Analyse überladen. | Viele DSP-Bücher springen schnell zur z-Ebene. | „Heute nutzen wir $H(z)$ zuerst als Delay-Sprache; Pole und Nullstellen sind die nächste Leseschicht.“ |
| $H(e^{j\Omega})$ wird als neues Signal missverstanden. | Es sieht wie eine Fouriertransformierte aus. | „$H(e^{j\Omega})$ ist die frequenzabhängige Wirkung des Systems, nicht der Inhalt eines bestimmten Signals.“ |
| FIR/IIR wird nur als endlich/unendlich auswendig gelernt. | Begriffe bleiben ohne Struktur. | „FIR heißt: keine Rückführung, endliche Impulsantwort. IIR heißt: Rückführung ist möglich, daher kann die Impulsantwort unendlich lang sein.“ |

---

## 8. Zentrale Herleitungen als Dozenten-Spickzettel

### 8.1 Impulszerlegung

Ziel:

$$
 x[n]=\sum_m x[m]\delta[n-m].
$$

Begründung:

Für festes $n$ ist $\delta[n-m]=1$ genau dann, wenn $m=n$. Daher verschwindet jeder Summand außer dem mit $m=n$:

$$
\sum_m x[m]\delta[n-m]=x[n]\cdot 1=x[n].
$$

Beispiel:

$$
 x[n]=[2,-1,0,3]
$$

$$
 x[n]=2\delta[n]-\delta[n-1]+0\delta[n-2]+3\delta[n-3].
$$

Didaktischer Satz:

> Jede Folge ist eine Summe aus einzelnen Sample-Anstößen.

---

### 8.2 Diskrete Faltung aus LTI-Eigenschaften

Start:

$$
 y[n]=\mathcal{T}\{x[n]\}
$$

Impulszerlegung:

$$
 x[n]=\sum_m x[m]\delta[n-m]
$$

Einsetzen:

$$
 y[n]=\mathcal{T}\left\{\sum_m x[m]\delta[n-m]\right\}
$$

Linearität:

$$
 y[n]=\sum_m x[m]\mathcal{T}\{\delta[n-m]\}
$$

Zeitinvarianz:

$$
\mathcal{T}\{\delta[n-m]\}=h[n-m]
$$

Ergebnis:

$$
 y[n]=\sum_m x[m]h[n-m]=(x*h)[n].
$$

Didaktischer Satz:

> Faltung ist die Summe aller Einzelantworten, die von den Eingangssamples ausgelöst werden.

---

### 8.3 Komplexe Exponentialfunktion als Eigenfunktion von LTI-Systemen

Eingang:

$$
 x[n]=e^{j\Omega n}
$$

Faltungsdarstellung:

$$
 y[n]=\sum_\ell h[\ell]x[n-\ell]
$$

Einsetzen:

$$
 y[n]=\sum_\ell h[\ell]e^{j\Omega(n-\ell)}
$$

Aufspalten:

$$
 e^{j\Omega(n-\ell)}=e^{j\Omega n}e^{-j\Omega\ell}
$$

Ausklammern:

$$
 y[n]=e^{j\Omega n}\sum_\ell h[\ell]e^{-j\Omega\ell}
$$

Definition:

$$
 H(e^{j\Omega})=\sum_\ell h[\ell]e^{-j\Omega\ell}
$$

Damit:

$$
 y[n]=H(e^{j\Omega})e^{j\Omega n}
$$

Didaktischer Satz:

> Der komplexe Sinus bleibt komplexer Sinus derselben Frequenz; das System multipliziert nur mit einem komplexen Faktor.

---

### 8.4 Frequenzgang aus Impulsantwort

Definition:

$$
 H(e^{j\Omega})=\sum_{n=-\infty}^{\infty} h[n]e^{-j\Omega n}
$$

Das ist die DTFT der Impulsantwort, sofern sie existiert.

Interpretation:

$$
 H(e^{j\Omega})=|H(e^{j\Omega})|e^{j\varphi(\Omega)}
$$

- $|H(e^{j\Omega})|$: Amplituden-/Pegelwirkung,
- $\varphi(\Omega)$: Phasenwirkung.

Ausblick:

$$
 H(e^{j\Omega}) = H(z)\big|_{z=e^{j\Omega}}
$$

Dieser Schritt sollte als Ausblick genannt, aber noch nicht geometrisch vertieft werden.

---

### 8.5 Delay-Eigenschaft der z-Transformation

Definition der z-Transformation:

$$
 X(z)=\sum_{n=-\infty}^{\infty}x[n]z^{-n}
$$

Für eine verzögerte Folge $x[n-k]$:

$$
\mathcal{Z}\{x[n-k]\}=\sum_n x[n-k]z^{-n}
$$

Substitution $r=n-k$, also $n=r+k$:

$$
\sum_r x[r]z^{-(r+k)}
=\sum_r x[r]z^{-r}z^{-k}
=z^{-k}X(z).
$$

Also:

$$
\mathcal{Z}\{x[n-k]\}=z^{-k}X(z).
$$

Didaktischer Satz:

> Verzögerung im Zeitbereich wird zum Faktor $z^{-k}$ im z-Bereich.

---

### 8.6 Differenzengleichung zu $H(z)$: FIR

Gegeben:

$$
 y[n]=b_0x[n]+b_1x[n-1]+b_2x[n-2]
$$

z-Transformation:

$$
 Y(z)=b_0X(z)+b_1z^{-1}X(z)+b_2z^{-2}X(z)
$$

Faktorisieren:

$$
 Y(z)=\left(b_0+b_1z^{-1}+b_2z^{-2}\right)X(z)
$$

Systemfunktion:

$$
 H(z)=\frac{Y(z)}{X(z)}=b_0+b_1z^{-1}+b_2z^{-2}
$$

---

### 8.7 Differenzengleichung zu $H(z)$: IIR

Gegeben:

$$
 y[n]=b_0x[n]-a_1y[n-1]
$$

z-Transformation:

$$
 Y(z)=b_0X(z)-a_1z^{-1}Y(z)
$$

Umstellen:

$$
 Y(z)+a_1z^{-1}Y(z)=b_0X(z)
$$

$$
 Y(z)(1+a_1z^{-1})=b_0X(z)
$$

Systemfunktion:

$$
 H(z)=\frac{Y(z)}{X(z)}=\frac{b_0}{1+a_1z^{-1}}
$$

---

### 8.8 Allgemeine FIR- und IIR-Form

FIR:

$$
 y[n]=\sum_{k=0}^{M}b_kx[n-k]
$$

$$
 H(z)=\sum_{k=0}^{M}b_kz^{-k}
$$

IIR:

$$
 y[n]=\sum_{k=0}^{M}b_kx[n-k]-\sum_{r=1}^{R}a_ry[n-r]
$$

$$
H(z)=
\frac{\sum_{k=0}^{M}b_kz^{-k}}
{1+\sum_{r=1}^{R}a_rz^{-r}}
$$

---

## 9. Formelbox für die Vorlesung

### System

$$
 y[n]=\mathcal{T}\{x[n]\}
$$

### Diskreter Impuls

$$
\delta[n]=
\begin{cases}
1, & n=0\\
0, & n\neq 0
\end{cases}
$$

### Impulsantwort

$$
 h[n]=\mathcal{T}\{\delta[n]\}
$$

### Linearität

$$
\mathcal{T}\{a x_1[n]+b x_2[n]\}=a\mathcal{T}\{x_1[n]\}+b\mathcal{T}\{x_2[n]\}
$$

### Zeitinvarianz

$$
 x[n]\to y[n]
\Rightarrow
x[n-n_0]\to y[n-n_0]
$$

### Impulszerlegung

$$
 x[n]=\sum_m x[m]\delta[n-m]
$$

### Diskrete Faltung

$$
 y[n]=(x*h)[n]=\sum_m x[m]h[n-m]
$$

### Frequenzgang aus Impulsantwort

$$
 H(e^{j\Omega})=\sum_n h[n]e^{-j\Omega n}
$$

### Delay

$$
 y[n]=x[n-M]
$$

$$
 T_D=\frac{M}{f_s}
$$

### Feedforward-Echo

$$
 y[n]=x[n]+gx[n-M]
$$

### Feedback-Echo

$$
 y[n]=x[n]+gy[n-M]
$$

### z-Delay-Eigenschaft

$$
\mathcal{Z}\{x[n-k]\}=z^{-k}X(z)
$$

### FIR

$$
 y[n]=\sum_{k=0}^{M}b_kx[n-k]
$$

$$
 H(z)=\sum_{k=0}^{M}b_kz^{-k}
$$

### IIR

$$
 y[n]=\sum_{k=0}^{M}b_kx[n-k]-\sum_{r=1}^{R}a_ry[n-r]
$$

$$
H(z)=
\frac{b_0+b_1z^{-1}+\dots+b_Mz^{-M}}
{1+a_1z^{-1}+\dots+a_Rz^{-R}}
$$

---

## 10. Storyboard für Folien oder Tafelbilder

| Folie | Hauptaussage | Visualisierungsidee | Was mündlich ergänzt wird |
|---:|---|---|---|
| 1 | Perspektivwechsel | „Was steckt im Signal?“ vs. „Was macht ein System?“ | Anschluss an FT/DFT/STFT |
| 2 | Analyse vs. System | $X[k]$ neben $y[n]=\mathcal{T}\{x[n]\}$ | Fenster ist Beobachtung, IR ist Systemantwort |
| 3 | Systemblock | $x[n]\to\mathcal{T}\to y[n]$ | Audio-Beispiele sammeln lassen |
| 4 | LTI-Bedingungen | Linearität und Zeitinvarianz als zwei Boxen | Clipping und Chorus als Gegenbeispiele |
| 5 | Diskreter Impuls | Stem-Plot $\delta[n]$ | Ein-Sample-Klick |
| 6 | Impulsantwort | Klick rein, Antwort raus | $h[n]$ ist Systemeigenschaft |
| 7 | Beispiele für $h[n]$ | Durchgang, Gain, Delay, Echo | Begriffe zuordnen |
| 8 | Impulszerlegung | $[2,-1,0,3]$ als Impulssumme | Samplewerte als Gewichte |
| 9 | Kopien von $h[n]$ | gestapelte verschobene IR-Kopien | Faltung als Aufbauprozess |
| 10 | Faltungsformel | $y[n]=\sum_m x[m]h[n-m]$ | Indizes langsam erklären |
| 11 | Faltung in Audio | trocken * Raum-IR = Hall | Faltung ist allgemeine LTI-Wirkung |
| 12 | Frequenzgang-Idee | Sinus rein, Sinus raus mit anderer Amplitude/Phase | Eigenfunktionsprinzip |
| 13 | Herleitung $H(e^{j\Omega})$ | drei Zeilen mit Ausklammern | Nur soweit wie nötig |
| 14 | Delay | $x[n]$, $x[n-1]$, $x[n-M]$ | Speicherbaustein |
| 15 | Feedforward-Delay | Blockdiagramm und Gleichung | endliche Antwort |
| 16 | Feedback-Delay | Rückführung im Blockdiagramm | ausklingende Echo-Kette |
| 17 | Differenzengleichung | $b$-Zweige und $a$-Zweige | Gleichung als Bauplan |
| 18 | $z^{-1}$ | Delay-Kästchen $z^{-1}$ | keine Frequenzachse, sondern Delay |
| 19 | FIR zu $H(z)$ | Gleichung → z-Form → $H(z)$ | Zähler lesen |
| 20 | IIR zu $H(z)$ | Feedback-Gleichung → Nenner | Rückführung lesen |
| 21 | Allgemeine Form | Zähler/Nenner farblich markieren | FIR/IIR vorbereiten |
| 22 | Abschluss | $h[n]$, Faltung, Differenzengleichung, $H(z)$, $H(e^{j\Omega})$ | Ausblick Pole/Nullstellen |

---

## 11. Python- und Hördemonstrationen

### Demo 1: Kurze Folge mit kurzer Impulsantwort falten

**Ziel:** Faltung als Summe verschobener Kopien sichtbar machen.

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.array([2, -1, 0, 3], dtype=float)
h = np.array([1, 0.5, 0.25], dtype=float)
y = np.convolve(x, h)

print("x =", x)
print("h =", h)
print("y =", y)

plt.figure()
plt.stem(np.arange(len(x)), x)
plt.title("Eingang x[n]")
plt.xlabel("n")
plt.ylabel("Amplitude")
plt.grid(True)

plt.figure()
plt.stem(np.arange(len(h)), h)
plt.title("Impulsantwort h[n]")
plt.xlabel("n")
plt.ylabel("Amplitude")
plt.grid(True)

plt.figure()
plt.stem(np.arange(len(y)), y)
plt.title("Ausgang y[n] = x[n] * h[n]")
plt.xlabel("n")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()
```

**Mündliche Leitfrage:**  
> Welche Kopie von $h[n]$ entsteht durch das Sample $x[3]=3$?

---

### Demo 2: Impuls durch verschiedene Systeme schicken

**Ziel:** Impulsantwort als Systemsignatur sichtbar machen.

```python
import numpy as np
import matplotlib.pyplot as plt

N = 80
imp = np.zeros(N)
imp[0] = 1

h_bypass = np.zeros(N); h_bypass[0] = 1
h_gain = np.zeros(N); h_gain[0] = 0.5
h_delay = np.zeros(N); h_delay[12] = 1
h_echo = np.zeros(N); h_echo[0] = 1; h_echo[20] = 0.6

systems = {
    "Bypass": h_bypass,
    "Gain": h_gain,
    "Delay": h_delay,
    "Feedforward-Echo": h_echo,
}

for name, h in systems.items():
    plt.figure()
    plt.stem(np.arange(N), h)
    plt.title(name + ": Impulsantwort h[n]")
    plt.xlabel("n")
    plt.ylabel("Amplitude")
    plt.grid(True)

plt.show()
```

**Mündliche Leitfrage:**  
> Welches System kann man an der Impulsantwort sofort erkennen?

---

### Demo 3: Feedforward- und Feedback-Delay vergleichen

**Ziel:** Endliche vs. rekursive Impulsantwort verstehen.

```python
import numpy as np
import matplotlib.pyplot as plt

N = 200
M = 24
g = 0.65
x = np.zeros(N)
x[0] = 1

# Feedforward
h_ff = np.zeros(N)
h_ff[0] = 1
h_ff[M] = g

# Feedback rekursiv
h_fb = np.zeros(N)
for n in range(N):
    h_fb[n] = x[n]
    if n - M >= 0:
        h_fb[n] += g * h_fb[n - M]

plt.figure()
plt.stem(np.arange(N), h_ff)
plt.title("Feedforward: h[n] = δ[n] + g δ[n-M]")
plt.xlabel("n")
plt.ylabel("Amplitude")
plt.grid(True)

plt.figure()
plt.stem(np.arange(N), h_fb)
plt.title("Feedback: h[n] = δ[n] + g h[n-M]")
plt.xlabel("n")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()
```

**Mündliche Leitfrage:**  
> Warum hört die Feedforward-Impulsantwort auf, während die Feedback-Impulsantwort weiterläuft?

---

### Demo 4: $H(z)$ aus Koeffizienten ablesen

**Ziel:** Koeffizienten als Systemstruktur interpretieren.

```python
b = [1, 0, 0, 0.5]  # 1 + 0.5 z^-3
# a[0] ist auf 1 normiert
# FIR: H(z) = 1 + 0.5 z^-3

a = [1, 0, 0, -0.5] # Nenner: 1 - 0.5 z^-3
# IIR: H(z) = 1 / (1 - 0.5 z^-3)

print("FIR H(z) = 1 + 0.5 z^-3")
print("IIR H(z) = 1 / (1 - 0.5 z^-3)")
```

**Mündliche Leitfrage:**  
> Wo sehen Sie Feedforward, wo Feedback?

---

### Demo 5: Frequenzgang einfacher Systeme plotten

**Ziel:** Zeitstruktur und Frequenzwirkung verbinden.

```python
import numpy as np
import matplotlib.pyplot as plt

Omega = np.linspace(0, np.pi, 1024)

# Moving average h[n] = [1/3, 1/3, 1/3]
H_ma = (1/3) * (1 + np.exp(-1j*Omega) + np.exp(-2j*Omega))

# Feedforward echo h[n] = δ[n] + g δ[n-M]
g = 0.7
M = 12
H_echo = 1 + g * np.exp(-1j*Omega*M)

plt.figure()
plt.plot(Omega/np.pi, np.abs(H_ma))
plt.title("Betrag: gleitender Mittelwert")
plt.xlabel("Ω / π")
plt.ylabel("|H(e^{jΩ})|")
plt.grid(True)

plt.figure()
plt.plot(Omega/np.pi, np.abs(H_echo))
plt.title("Betrag: Feedforward-Echo / Comb")
plt.xlabel("Ω / π")
plt.ylabel("|H(e^{jΩ})|")
plt.grid(True)
plt.show()
```

**Mündliche Leitfrage:**  
> Warum erzeugt ein Echo kammartige Frequenzgänge?

---

## 12. Mini-Übungen / Aktivierungen in der Vorlesung

### Mini-Übung 1: System oder Analyse?

Ordnen Sie zu: Beobachtungsoperation oder Systemwirkung?

1. $x_{obs}[n]=x[n]w[n]$
2. $y[n]=x[n]*h[n]$
3. FFT-Analyzer in einer DAW
4. Equalizer im Kanalzug
5. Raumimpulsantwort in einem Faltungshall

**Ziel:** Trennung von Fensterung und Systemfaltung sichern.

**Erwartete Interpretation:**  
1 und 3 sind Analyse/Beobachtung. 2, 4 und 5 sind Systemwirkung bzw. Systembeschreibung.

---

### Mini-Übung 2: Impulsantwort erraten

Gegeben sind drei Systeme:

$$
 y_1[n]=x[n]
$$

$$
 y_2[n]=x[n-4]
$$

$$
 y_3[n]=x[n]+0.5x[n-4]
$$

Skizzieren Sie jeweils $h[n]$.

**Ziel:** Impulsantwort aus Gleichung ablesen.

---

### Mini-Übung 3: Faltung als Kopiensumme

Gegeben:

$$
 x[n]=[1,2]
$$

$$
 h[n]=[1,0.5,0.25]
$$

Schreiben Sie $y[n]$ als Summe verschobener Kopien von $h[n]$, bevor Sie Zahlen addieren.

**Erwartung:**

$$
 y[n]=1h[n]+2h[n-1].
$$

---

### Mini-Übung 4: Feedforward oder Feedback?

Klassifizieren Sie:

1. $y[n]=0.5x[n]+0.5x[n-1]$
2. $y[n]=x[n]+0.8y[n-1]$
3. $y[n]=x[n]-x[n-1]$
4. $y[n]=0.2x[n]+0.7y[n-2]$

**Ziel:** $x$-Delays und $y$-Delays unterscheiden.

---

### Mini-Übung 5: $H(z)$ lesen

Gegeben:

$$
H(z)=1-0.5z^{-1}
$$

und

$$
H(z)=\frac{1}{1-0.5z^{-1}}.
$$

Welche Struktur ist Feedforward, welche Feedback? Welche hat wahrscheinlich eine endliche Impulsantwort?

---

## 13. Selbstlernaufgaben nach der Vorlesung

### Aufgabe 1: Impulsantworten interpretieren

Sie erhalten vier Impulsantworten als Stem-Plots:

1. ein einzelner Impuls bei $n=0$,
2. ein einzelner Impuls bei $n=10$,
3. zwei Impulse bei $n=0$ und $n=20$,
4. eine abklingende Folge von Impulsen bei $n=0,20,40,60,\dots$.

Bearbeiten Sie:

- Benennen Sie die wahrscheinliche Systemwirkung.
- Schreiben Sie eine passende Differenzengleichung, falls möglich.
- Entscheiden Sie, ob die Impulsantwort endlich oder potenziell unendlich ist.
- Beschreiben Sie, wie ein kurzer Snarehit nach diesem System klingen würde.

---

### Aufgabe 2: Von der Differenzengleichung zu $H(z)$

Gegeben sind:

$$
 y[n]=x[n]+0.7x[n-5]
$$

$$
 y[n]=x[n]+0.7y[n-5]
$$

$$
 y[n]=0.25x[n]+0.5x[n-1]+0.25x[n-2]
$$

Bearbeiten Sie jeweils:

- Markieren Sie Feedforward- und Feedback-Anteile.
- Bestimmen Sie $H(z)$.
- Entscheiden Sie FIR oder IIR.
- Beschreiben Sie eine mögliche Audio-Wirkung.

---

### Aufgabe 3: Faltung als Überlagerungsprozess

Gegeben:

$$
 x[n]=[1,-1,2]
$$

$$
 h[n]=[1,0.5]
$$

Bearbeiten Sie:

- Zerlegen Sie $x[n]$ in verschobene Impulse.
- Schreiben Sie $y[n]$ als Summe verschobener Impulsantworten.
- Berechnen Sie $y[n]$.
- Erklären Sie in drei Sätzen, warum dies mehr ist als eine Rechenregel.

---

### Aufgabe 4: Frequenzgang qualitativ erklären

Ein System hat die Impulsantwort:

$$
 h[n]=\delta[n]+\delta[n-8].
$$

Bearbeiten Sie:

- Was passiert im Zeitbereich mit einem Eingangssignal?
- Warum ist im Frequenzbereich mit Auslöschungen und Verstärkungen zu rechnen?
- Wie könnte dieses System bei Sprache oder Musik klingen?
- Welche Verbindung sehen Sie zu Kammfiltereffekten?

---

## 14. Prüfungsrelevante Kernkompetenzen

Studierende sollten nach dieser Vorlesung wirklich können:

1. den Unterschied zwischen Signal, System, Eingang, Ausgang und Impulsantwort sauber benennen,
2. $\delta[n]$ und $h[n]$ definieren und interpretieren,
3. eine kurze Folge als Summe gewichteter Impulse darstellen,
4. die diskrete Faltung aus Impulszerlegung, Linearität und Zeitinvarianz erklären,
5. einfache Faltungen per Hand ausführen,
6. aus einfachen Systemgleichungen die Impulsantwort skizzieren,
7. Feedforward- und Feedback-Strukturen unterscheiden,
8. Differenzengleichungen aus Blockdiagrammen ablesen,
9. einfache $H(z)$-Funktionen aus Differenzengleichungen herleiten,
10. FIR und IIR anhand von Zähler/Nenner und Rückführung unterscheiden,
11. erklären, warum $H(z)$ eine Systembeschreibung und kein Signalspektrum ist,
12. $f$, $\omega$ und $\Omega$ nicht vermischen.

Prüfungsaufgaben sollten nicht nur mechanisches Rechnen abfragen, sondern Interpretation verlangen, etwa:

- „Erklären Sie, warum diese Impulsantwort zu einem Feedback-System passen kann.“
- „Welche Aussage über das System können Sie aus dem Nenner von $H(z)$ ableiten?“
- „Warum ist diese Faltung kein Beobachtungsfenster?“
- „Beschreiben Sie die Audio-Wirkung dieser Differenzengleichung.“

---

## 15. Qualitätscheck

### Notation

- $x[n]$, $y[n]$, $h[n]$, $\delta[n]$ sind konsistent als diskrete Folgen verwendet.
- $n$ ist Zeitindex; $m$, $\ell$, $k$ werden nicht vermischt.
- $k$ bleibt primär DFT-/Summationsindex für Bins, nicht Zeitindex.
- $f$ in Hz, $\omega$ in rad/s und $\Omega$ in rad/sample sind getrennt.

### Didaktische Trennung

- Fensterung wird als Beobachtungsoperation erklärt.
- Faltung mit $h[n]$ wird als Systemwirkung erklärt.
- $h[n]$ wird nicht als Fensterfunktion dargestellt.
- $H(z)$ wird nicht als Spektrum eines Signals bezeichnet.

### Mathematischer Aufbau

- Impulszerlegung wird vor Faltung eingeführt.
- Linearität und Zeitinvarianz werden nur so tief behandelt, wie sie für die Faltungsherleitung gebraucht werden.
- Komplexe Exponentialfunktionen werden als Brücke zum Frequenzgang genutzt.
- $z^{-1}$ wird zuerst als Delay-Operator eingeführt.
- $H(z)$ wird aus Differenzengleichungen hergeleitet.

### Überlastungsvermeidung

- Pole und Nullstellen werden nur angekündigt.
- Stabilität wird am Feedback-Delay qualitativ vorbereitet, nicht vollständig formalisiert.
- Region of Convergence wird nicht eingeführt.
- Bilineartransformation, Filterdesign und Minimum Phase bleiben für spätere Einheiten.

### Audio-Bezug

- Jeder mathematische Block hat ein Audio-Beispiel.
- Die Beispiele reichen von Delay über Echo bis Lautsprecher-/Raumimpulsantwort.
- Hör- und Python-Demos sind so gewählt, dass sie die gleiche Struktur aus verschiedenen Perspektiven zeigen.

---

## 16. Abschluss: Drei Sätze, die hängen bleiben sollen

1. **Ein LTI-System ist durch seine Impulsantwort vollständig beschrieben.**
2. **Faltung bedeutet: Jedes Eingangssample startet eine skalierte und verschobene Kopie der Impulsantwort.**
3. **$H(z)$ ist die kompakte Delay-Sprache eines Systems; der Frequenzgang entsteht später durch Auswertung auf dem Einheitskreis.**

