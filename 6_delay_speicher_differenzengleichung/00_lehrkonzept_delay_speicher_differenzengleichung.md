# Lehrkonzept Vorlesung 6: Systemwirkung im Frequenzbereich und FIR-Filter

## Stand nach gehaltener Vorlesung

Die Vorlesung wurde am 22.05.2026 erfolgreich gehalten. Die Folien 1 bis 33 dienten als Wiederholung und Anschluss an Vorlesung 5. Der eigentliche neue Teil von Vorlesung 6 beginnt in der gehaltenen Fassung bei Folie 34 mit der Systemwirkung im Frequenzbereich.

Quelle für diese Fassung ist `AEV_6_FIR_MASTER.pptx` aus `6_FIR_Filter/`.

## Ziel der Vorlesung

Die Studierenden sollen am Ende verstehen:

- dass ein Spektrum ein Signal beschreibt, ein Frequenzgang aber ein System,
- wie die Systemwirkung im Zeitbereich als Faltung und im Frequenzbereich als Multiplikation gelesen wird,
- warum ein DFT-Binraster nur eine diskrete Auswertung des Frequenzgangs ist,
- wie Grundoperationen der digitalen Signalverarbeitung aussehen: Gewichtung, Summation und Verzögerung,
- was FIR bedeutet: endliche Impulsantwort ohne Rückführung,
- wie FIR-Koeffizienten als Impulsantwort gelesen werden,
- wie einfache FIR-Filter Klanganteile glätten, differenzieren oder spektral formen,
- warum FIR-Filter immer stabil sind, aber bei steilen Anforderungen viele Taps, Rechenaufwand und Latenz benötigen.

IIR, Feedback, z-Transformation, Pole und Nullstellen bleiben der Anschluss für Vorlesung 7.

## Wiederholung vor dem eigentlichen Einstieg

Folien 1 bis 33 waren Wiederholung und Aktivierung:

- Audioeffekte und Systemklassen,
- LTI-Systeme als zentrale Klasse für Filter, EQ, Echo und Reverb,
- Linearität, Zeitinvarianz und Kommutativität der Faltung,
- Impulsantwort als Systemantwort auf den diskreten Impuls,
- Faltung als Überlagerung verschobener und skalierter Impulsantworten,
- sampleweise Berechnung der Faltung mit einer Tiefpass-Impulsantwort.

Diese Folien gehören inhaltlich noch zum Rückgriff auf Vorlesung 5. Für die Dokumentation von Vorlesung 6 sind sie ein vorgeschalteter Wiederholungsblock, nicht der eigentliche neue Stoff.

## Mathematischer Kern

Diskrete Faltung als Zeitbereichsbeschreibung:

$$
y[n] = (x*h)[n] = \sum_m x[m]h[n-m]
$$

Frequenzgang aus der Impulsantwort:

$$
H(e^{j\Omega})=\sum_m h[m]e^{-j\Omega m}
$$

DFT-Rasterdarstellung:

$$
H_N[k]=H(e^{j2\pi k/N})
$$

Binfrequenz und Frequenzauflösung:

$$
\Delta f = \frac{f_s}{N},
\qquad
f_k = k\Delta f = k\frac{f_s}{N}
$$

Systemwirkung auf gemeinsamem DFT-Raster:

$$
Y_N[k]=H_N[k]X_N[k]
$$

Grundoperation Verzögerung:

$$
y[n]=x[n-M]
$$

FIR-System:

$$
y[n]=\sum_{k=0}^{M} b_k x[n-k]
$$

Koeffizienten als Impulsantwort:

$$
h[n]=b_n,\qquad n=0,\dots,M
$$

FIR-Frequenzgang:

$$
H(e^{j\Omega})=\sum_{k=0}^{M}b_k e^{-j\Omega k}
$$

Gruppenlaufzeit:

$$
\tau_g(\Omega)=-\frac{d\varphi(\Omega)}{d\Omega}
$$

Für symmetrische linearphasige FIR-Filter mit \(L\) Taps:

$$
\tau_g = \frac{L-1}{2}
$$

## Block 1: Systemwirkung im Frequenzbereich

Folien: 34 bis 62

Kerngedanke:

> Im Zeitbereich beschreibt Faltung die Systemwirkung. Im Frequenzbereich wird dieselbe Wirkung zur Multiplikation: Das System gewichtet die Frequenzanteile des Eingangssignals.

Didaktisch wichtig:

- Der Frequenzgang gehört zum System, nicht zum konkreten Eingangssignal.
- Ein Signalspektrum und ein Frequenzgang können auf derselben Frequenz- oder Binachse gezeichnet werden, beantworten aber unterschiedliche Fragen.
- \(H_N[k]\) ist die Auswertung von \(H(e^{j\Omega})\) auf einem DFT-Raster.
- Bei reellen Signalen reicht die einseitige Betrachtung bis Nyquist.
- Die Binfrequenzen ergeben sich aus \(f_k=kf_s/N\).
- Das gemeinsame Raster ist entscheidend, wenn \(Y_N[k]=H_N[k]X_N[k]\) berechnet oder visualisiert wird.

Storyboard-Bezug:

- `01_impulsantwort_und_frequenzgang/1A_zero_padding_tiefpass`
- `01_impulsantwort_und_frequenzgang/1B_spektrale_gewichtung`

## Block 2: Grundoperationen digitaler Signalverarbeitung

Folien: 63 bis 65

Kerngedanke:

> Aus wenigen Rechenoperationen entstehen digitale Filter: Gewichtung, Summation und Verzögerung.

Didaktisch wichtig:

- Gewichtung eines Signals entspricht einer Multiplikation mit einem Faktor.
- Summation kombiniert mehrere Signalzweige.
- Verzögerung um \(M\) Abtastwerte greift auf vergangene Eingangswerte zu.
- Diese drei Operationen bilden die Sprache für Feedforward-Strukturen und FIR-Filter.

## Block 3: FIR-Filter als endliche Feedforward-Struktur

Folien: 66 bis ca. 110

Kerngedanke:

> Ein FIR-Filter nutzt aktuelle und vergangene Eingangswerte, gewichtet sie und addiert sie. Weil keine Rückführung verwendet wird, ist die Impulsantwort endlich.

Didaktisch wichtig:

- FIR steht für `Finite Impulse Response`.
- Ein FIR-Filter hat keine Rückführung vergangener Ausgangswerte.
- Die Koeffizienten \(b_k\) sind direkt die Impulsantwort.
- Schon wenige Taps können Tiefpass-, Hochpass- oder Kammfilterwirkung erzeugen.
- Betrag und Phase gehören zusammen; Filterwirkung ist nicht nur eine Amplitudenfrage.

Storyboard-Bezug:

- `02_fir/02A_tiefpass`
- `02_fir/02B_hochpass`
- `02_fir/02C_notch`

## Block 4: FIR-Design und Trade-offs

Folien: ca. 111 bis 132

Kerngedanke:

> FIR-Filter sind stabil und können linearphasig entworfen werden. Dafür kosten steile oder sehr genaue Filter viele Taps, Rechenaufwand und Latenz.

Didaktisch wichtig:

- Endliche Impulsantwort bedeutet: Nach endlich vielen Samples ist die Systemantwort vorbei.
- Symmetrische FIR-Koeffizienten ermöglichen lineare Phase.
- Lineare Phase bedeutet konstante Gruppenlaufzeit, aber nicht null Latenz.
- Mehr Taps bedeuten mehr Freiheitsgrade und schärfere Frequenzformung.
- Mehr Taps bedeuten auch mehr Multiplikationen pro Sample und größere Verzögerung.
- FIR-Filter sind ohne Feedback strukturell stabil.

Storyboard-Bezug:

- `02_fir/02D_lowpass_design`

## Block 5: Aufgaben und Sicherung

Folien: 133 bis 140, Feedbackfolie 141

Die Aufgaben sichern den Stoff praxisnah:

1. Transientenglättung mit kurzem FIR-Filter:
   sampleweise Faltung, Ausgangslänge, Wertetabellen, Stem-Plots und Interpretation.

2. Frequenzgang statt Signalspektrum:
   zwei einfache FIR-Filter auf einem DFT-Raster, Betrag, Betrag in dB und Zuordnung zu Glättung oder Differenzbildung.

3. FIR-Kopfhörerentzerrung:
   linearphasige FIR-Filter, Gruppenlaufzeit, Rechenaufwand, Live-Monitoring versus Offline-Rendering.

4. Feedforward-Delay als FIR-Kammfilter:
   verzögerte Eingangskopie, Delayzeit, Kammfilterstruktur und praktische DAW-Interpretation.

## Tatsächlicher Ablauf der gehaltenen Fassung

| Folien | Abschnitt | Funktion |
|---|---|---|
| 1-33 | Wiederholung aus Vorlesung 5 | LTI, Impulsantwort, Faltung reaktivieren |
| 34-62 | Systemwirkung im Frequenzbereich | Übergang von Faltung zu \(Y_N[k]=H_N[k]X_N[k]\) |
| 63-65 | DSP-Grundoperationen | Gewichtung, Summation, Verzögerung |
| 66-110 | FIR-Filter | Begriff, Feedforward-Struktur, einfache FIR-Wirkungen |
| 111-132 | FIR-Eigenschaften und Design-Trade-offs | lineare Phase, Taps, Rechenaufwand, Latenz, Stabilität |
| 133-140 | Aufgaben | Anwendung und Transfer |
| 141 | Feedback | Abschluss |

## Merksätze

1. Faltung beschreibt die Systemwirkung im Zeitbereich.
2. Im Frequenzbereich wird dieselbe Systemwirkung zur Multiplikation.
3. Ein Spektrum beschreibt ein Signal; ein Frequenzgang beschreibt ein System.
4. \(H_N[k]\) ist ein DFT-Raster des Frequenzgangs.
5. FIR heißt: endliche Impulsantwort, Feedforward, keine Rückführung.
6. Die FIR-Koeffizienten sind die Impulsantwort.
7. Linearphasige FIR-Filter sind möglich, aber sie verursachen Gruppenlaufzeit.
8. Mehr Taps bringen mehr Gestaltungsmöglichkeit, aber auch mehr Rechenaufwand und Latenz.
9. Feedback, IIR, z-Transformation, Pole und Nullstellen beginnen in Vorlesung 7.
