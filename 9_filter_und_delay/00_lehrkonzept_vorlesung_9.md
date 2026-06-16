# Lehrkonzept Vorlesung 9: Filter und Delay-basierte Audioeffekte

Referenz: Zölzer, U. (Hrsg.): DAFX - Digital Audio Effects, 2nd edition,
2011, Kapitel 2 "Filters and delays", S. 47-80.

## Einordnung in die neue Audio-FX-Trilogie

Vorlesung 9 startet den nächsten großen Block der Veranstaltung:
Audioeffekte nicht mehr nur als abstrakte Systeme, sondern als konkrete
Studio- und Plugin-Werkzeuge.

Die drei Vorlesungen werden didaktisch so getrennt:

| Vorlesung | Referenz in Zölzer 2011 | Schwerpunkt |
|---:|---|---|
| 9 | Kapitel 2: Filters and delays | Filter, Equalizer, Allpass, Comb, zeitvariante Filter und Delay-FX |
| 10 | Kapitel 3: Modulators and demodulators | Ringmodulation, AM, FM/PM, Detektoren, Demodulation und typische Anwendungen |
| 11 | Kapitel 4: Nonlinear processing | Dynamik, Compressor/Gate, Saturation, Distortion, Exciter/Enhancer |

Vorlesung 9 bleibt bewusst in der LTI- und schwach zeitvarianten Welt:
Filter und Delays sind noch gut mit Systemfunktion, Frequenzgang,
Pol-/Nullstellenlage, Phase und Blockdiagrammen erklärbar. Sobald die
Zeitvariation durch LFOs, Pedale oder Hüllkurven hinzukommt, wird sie
zunächst als kontrollierte Parameterbewegung gelesen. Die eigentliche
Modulations- und Demodulationssprache wird erst in Vorlesung 10 systematisch.

## Rückblick nach Durchführung

Die gehaltene Folienspur besteht aus 29 Folien. Sie führt von Roadmap,
Filtertypen, Allpass, Shelving-/Peak-EQ und DAW-EQ über eine kurze
Evaluation zu Wah-Wah, Phaser, Kammfiltern, Slapback/Echo und den
zeitvarianten Delay-Effekten Vibrato, Flanger, Chorus und Doubler. Den
Abschluss bilden vier Aufgaben.

Die ursprünglich geplanten eigenen Blöcke 7 und 8 wurden nicht benötigt:
`Fractional Delay Lines` und die `Standardstruktur variabler Delay-FX` bleiben
als Hintergrund- und Reservematerial erhalten, sind aber nicht Teil der
tatsächlich gehaltenen Vorlesung 9. Die Storyboard-Ordner 07 und 08 wurden
deshalb entfernt. Didaktisch war die Entscheidung sinnvoll, weil die
Vorlesung damit stärker bei hörbaren Effektklassen, Phasen-/Interferenzlogik
und Parameterdeutung blieb.

## Scope-Entscheidung

Enthalten:

- gängige Filtertypen: Tiefpass, Hochpass, Bandpass, Bandsperre/Notch,
  Shelving, Peak/Peaking-EQ und Allpass
- Parameter: Grenzfrequenz, Mittenfrequenz, Bandbreite, Q, Gain, Mix,
  Feedback, Delayzeit, Modulationstiefe und Modulationsrate
- Shelving- und Peaking-EQ mit Koeffizientenberechnung aus \(f_c\), \(Q\) und \(G\)
- Allpass als Filter mit konstantem Betrag und veränderter Phase
- Wah-Wah und Phaser als zeitvariante Filtereffekte
- Comb-Filter als Feedforward/FIR-Comb und Feedback/IIR-Comb
- Vibrato, Flanger, Chorus, Slapback und Echo als Delay-basierte Effekte
- Aufgabenphase zu Phasenverschiebung/Kammfilter, Feedforward/Feedback,
  Allpass/Phaser und Delay-FX-Abgrenzung

Nicht enthalten:

- kein allgemeines FIR-Filterdesign
- keine Faltung und keine Faltungshall- oder Convolution-FX
- keine Multiband-Delayeffekte
- kein "natural sounding comb filter" mit frequenzabhängigem Feedback
- keine eigenständigen Folienblöcke zu Fractional Delay Lines oder zur
  Standardstruktur aus Zölzer 2011, Abb. 2.34; beides bleibt Reserve- und
  Implementationskontext für spätere Vertiefung
- keine tiefen Fractional-Delay-Filterdesigns
- keine vollständige Modulations-/Demodulationstheorie; das ist Vorlesung 10
- keine Nichtlinearität, kein Compressor, keine Saturation; das ist
  Vorlesung 11

Wichtige didaktische Präzisierung:

> "FIR" kommt in dieser Vorlesung nur als Feedforward-Comb vor. Es geht nicht
> um allgemeine FIR-Filtergestaltung oder Faltung. Die Studierenden sollen
> erkennen: Eine einzelne verzögerte Kopie reicht bereits aus, um Kammfilter-
> Kerben zu erzeugen.

## Inhaltliche Anknüpfung an Vorlesung 7 und 8

Die Studierenden kennen:

- Frequenzgang \(H(e^{j\Omega})\)
- Biquad-Differenzengleichung
- Systemfunktion \(H(z)\)
- \(z^{-1}\) als Sample-Delay
- Pole und Nullstellen
- Einheitskreis als Ort des Frequenzgangs
- Q, Resonanz, Gain und Cutoff aus Filterplots

In Vorlesung 9 wird diese Sprache auf konkrete Audioeffekte angewendet.
Rückblickend sind das inhaltliche Voraussetzungen, aber keine benötigten
Materialordner im Ablauf der gehaltenen Folienspur.

## Lernziele

Nach der Vorlesung sollen Studierende:

1. gängige Filtertypen anhand ihres Frequenzgangs benennen können,
2. die wichtigsten Parameter von Audiofiltern erklären können,
3. Shelving-EQs und einen Peaking-EQ aus \(f_c\), \(Q\) und \(G\) als Biquads verstehen,
4. Allpass-Filter als Phasenfilter lesen können,
5. Wah-Wah und Phaser als zeitvariant gesteuerte Filtereffekte einordnen,
6. FIR- und IIR-Comb-Filter im Zeit- und Frequenzbereich unterscheiden,
7. Vibrato, Flanger, Chorus, Slapback und Echo über Delayzeit, Mix,
   Feedback und Modulation unterscheiden,
8. typische Effektaufgaben über Phasenlage, Interferenz, Feedback und
   Parameterbereiche begründet lösen können.

## Zeitplanung und Blockstruktur

| Zeit | Block | Thema | Ziel |
|---:|---|---|---|
| 0-6 min | 1 | Audio-FX-Roadmap 9-11 | Filter/Delay, Modulation/Demodulation und Nichtlinearität trennen |
| 6-24 min | 2 | Filtertypen, Parameter und Allpass | TP, HP, BP, BR/Notch, Allpass, Phase und Q wiederholen |
| 24-40 min | 3 | Shelving- und Peak-EQ als parametrische Biquads | Koeffizienten aus \(f_c\), \(Q\), \(G\) herleiten und interpretieren |
| 40-46 min | Einschub | Evaluation | Lehrveranstaltungsevaluation durchführen |
| 46-60 min | 4 | Zeitvariante Filter | Wah-Wah und Phaser als Filtereffekte einordnen |
| 60-72 min | 5 | Comb-Filter, Slapback und Echo | Delaykopien, Kerben, Peaks, Feedback und hörbare Wiederholung vergleichen |
| 72-84 min | 6 | Zeitvariante Delay-FX | Vibrato, Flanger, Chorus und Doubler über Delayzeit, Mix, Feedback und Modulation unterscheiden |
| 84-100 min | Aufgaben | Transfer | Phasenlage, Kammfilter, Allpass/Phaser und Delay-FX in Anwendungen begründen |

## Block 1: Audio-FX-Roadmap 9-11

### Story

Vorlesung 8 endete mit Systemklassen. Jetzt werden konkrete Effekte in drei
Sitzungen aufgeteilt:

- Vorlesung 9: Filter und Delays als lineare oder schwach zeitvariante
  Effekte
- Vorlesung 10: Modulatoren und Demodulatoren
- Vorlesung 11: nichtlineare Effekte

Die Studierenden sollen verstehen, dass "Audioeffekt" kein einzelnes
mathematisches Modell ist. Ein EQ, ein Phaser, ein Ringmodulator und ein
Distortion-Pedal gehören zu unterschiedlichen Systemklassen.

### Tafelbild

```latex
\[
\text{VL9: } H(z), H(e^{j\Omega}), \text{Delayline}
\]

\[
\text{VL10: } y[n]=x[n]\cdot m[n],\quad \text{Modulation/Demodulation}
\]

\[
\text{VL11: } y[n]=f(x[n]),\quad \text{nichtlineare Kennlinie}
\]
```

### Lehrenden-Notiz

Modulationseffekte, bei denen direkt die Amplitude oder ein Trägersignal
bearbeitet wird, bleiben in Vorlesung 10. Der LFO wird in Vorlesung 9 nur dort
verwendet, wo er einen Filter- oder Delayparameter bewegt.

### Schriftliche Folien-Zusammenfassung

Dieser Block ordnet die nächsten drei Vorlesungen ein. Audioeffekte sind keine
einheitliche mathematische Struktur. Ein Equalizer, ein Phaser, ein
Ringmodulator und ein Distortion-Effekt verändern zwar alle ein Audiosignal,
aber sie tun das mit unterschiedlichen Systemprinzipien. Deshalb wird der
Audio-FX-Teil in drei Schritte aufgeteilt.

In Vorlesung 9 stehen Filter und Delay-basierte Effekte im Mittelpunkt. Diese
Effekte lassen sich gut mit den bisherigen Werkzeugen beschreiben:
Frequenzgang \(H(e^{j\Omega})\), Systemfunktion \(H(z)\), Pole und
Nullstellen, Delayline, Mix und Feedback. Einige Effekte sind zeitvariant,
bleiben aber noch nah an linearen Filter- und Delaystrukturen.

Vorlesung 10 behandelt Modulatoren und Demodulatoren. Dort werden Signale mit
Steuersignalen oder Trägern multipliziert oder aus modulierten Signalen wieder
ausgewertet. Vorlesung 11 verlässt dann die lineare Sicht und behandelt
nichtlineare Effekte wie Saturation, Distortion und Dynamikprozessoren. Die
wichtige Orientierung lautet: Erst hören, dann die Wirkung benennen, danach
Blockdiagramm, Gleichung und Parameter lesen.

## Block 2: Filtertypen, Parameter und Allpass wiederholen

### Inhalt

Aus Zölzer 2011, Kap. 2.2.1:

- Tiefpass: lässt tiefe Frequenzen durch, dämpft hohe Frequenzen.
- Hochpass: lässt hohe Frequenzen durch, dämpft tiefe Frequenzen.
- Bandpass: lässt einen Frequenzbereich um eine Mittenfrequenz durch.
- Bandsperre/Notch: dämpft einen Frequenzbereich um eine Mittenfrequenz.
- Allpass: lässt alle Frequenzen im Betrag durch, ändert aber die Phase.

### Parameter

| Filtertyp | Hauptparameter | Audio-Bedeutung |
|---|---|---|
| Tiefpass | \(f_c\), \(Q\), ggf. Resonanz | dumpfer, weicher, weniger Brillanz |
| Hochpass | \(f_c\), \(Q\) | weniger Rumpeln, weniger Bass, mehr Klarheit |
| Bandpass | \(f_c\), Bandbreite oder \(Q\) | Telefonklang, Nasalität, Formantbereich |
| Notch/Bandreject | \(f_c\), Bandbreite oder \(Q\) | Störton oder Resonanz herausnehmen |
| Low-/High-Shelf | \(f_c\), Gain \(G\), Steilheit | Bass-/Treble-Regler |
| Peak-EQ | \(f_c\), \(Q\), Gain \(G\) | gezielte Anhebung oder Absenkung |
| Allpass | \(f_c\), \(Q\), Ordnung | Phase und Gruppenlaufzeit ohne Betragseingriff |

### Cutoff, Q und Phase

Der Begriff \(f_c\) ist nicht bei jedem Filter gleich zu lesen:

- Bei TP/HP ist \(f_c\) die Grenzfrequenz. Bei klassischen Butterworth-
  Einstellungen liegt dort typischerweise der -3-dB-Punkt.
- Bei BP/BR/Peak ist \(f_c\) die Mittenfrequenz.
- Bei Shelving-Filtern ist \(f_c\) die Übergangsfrequenz zwischen den
  Pegelbereichen.
- Beim Allpass kann \(f_c\) die Frequenz bezeichnen, um die herum die
  Phasendrehung besonders stark verläuft. Für die Abbildungen wird ein
  Allpass zweiter Ordnung genutzt, damit auch \(Q\) als Güteparameter sichtbar
  wird.

Die Abbildungen in diesem Block werden in der üblichen Audioansicht gezeigt:
Betrag in dB, logarithmische Frequenzachse von \(20\,\mathrm{Hz}\) bis
\(20\,\mathrm{kHz}\), \(f_s=48\,\mathrm{kHz}\). Der dB-Ausschnitt liegt bei
\(-15\,\mathrm{dB}\) bis \(5\,\mathrm{dB}\). Damit sind sowohl Passband,
Grenzbereich als auch Sperrbereich gut sichtbar. Für die Beispiele werden
folgende Frequenzen verwendet:

- Tiefpass/High-cut: \(f_c=5\,\mathrm{kHz}\)
- Hochpass/Low-cut: \(f_c=200\,\mathrm{Hz}\)
- Bandpass, Bandsperre und Allpass: \(f_c=500\,\mathrm{Hz}\)

Lehrenden-Notiz zur Phase:

- Ein Filter verändert nicht nur Betrag, sondern meistens auch Phase.
- Bei einem kausalen Tiefpass drehen hohe Frequenzen stärker nach.
- Bei einem Hochpass entsteht ebenfalls Phasendrehung, aber mit anderer
  Referenzlage.
- Bei einem Allpass ist genau diese Phasendrehung die eigentliche Wirkung.
- Bei Notches kann die Phase um die Nullstelle herum sehr schnell springen.

Didaktischer Merksatz:

> Betrag sagt, welche Frequenzen lauter oder leiser werden. Phase sagt, wie
> die Zeitlage der Frequenzanteile verschoben wird. Viele Effekte entstehen
> erst aus der Kombination beider Perspektiven.

### Allpass als fünfter Filtertyp

Der Allpass wird an dieser Stelle bewusst zusammen mit den anderen
Filterfunktionen eingeführt. Technisch ist er keine eigene Effektklasse,
sondern eine Filterstruktur mit einer besonderen Eigenschaft:

```latex
\[
|A(e^{j\Omega})|=1
\]
```

für alle Frequenzen. Der Betrag bleibt also unverändert. Die Phase ändert
sich aber:

```latex
\[
\angle A(e^{j\Omega}) \neq 0.
\]
```

Für die Abbildungen werden jetzt zwei Allpass-Varianten gezeigt: zuerst ein
Allpass erster Ordnung und danach ein Allpass zweiter Ordnung. Der Allpass
erster Ordnung ist die elementare Stufe, wie sie später im Phaser-Plugin
kaskadiert wird:

```latex
\[
A_1(z)
=
\frac{a-z^{-1}}{1-a z^{-1}}.
\]
```

mit:

```latex
\[
g=\tan\left(\pi\frac{f_\mathrm{AP}}{f_s}\right),
\qquad
a=\frac{1-g}{1+g}.
\]
```

Der Betrag bleibt idealerweise überall gleich \(1\), die Phase dreht sich aber
frequenzabhängig. Danach wird der Allpass als Biquad, also als Filter zweiter
Ordnung, gezeigt:

```latex
\[
A_2(z)
=
\frac{
(1-\alpha)-2\cos(\omega_0)z^{-1}+(1+\alpha)z^{-2}
}{
(1+\alpha)-2\cos(\omega_0)z^{-1}+(1-\alpha)z^{-2}
}.
\]
```

mit:

```latex
\[
\omega_0 = 2\pi\frac{f_c}{f_s},
\qquad
\alpha=\frac{\sin(\omega_0)}{2Q}.
\]
```

Didaktisch ist hier wichtig: Der Allpass ist im Betragsgang unauffällig,
aber im Phasengang sichtbar. Wenn das allpassgefilterte Signal später mit dem
Direktsignal gemischt wird, entstehen frequenzabhängige Verstärkungen und
Auslöschungen. Damit ist der Allpass die technische Brücke zum Phaser, bleibt
aber zunächst ein Filtertyp innerhalb der Filterstruktur. Bei diesem Allpass
zweiter Ordnung verändert \(Q\) nicht den Betrag, sondern die Steilheit und
Bündelung der Phasendrehung um \(f_c\).

Lehrenden-Notiz:

> Die Studierenden erwarten oft: "Wenn der Betrag gleich bleibt, hört man
> nichts." Das ist nur für ein isoliertes Signal unter idealisierten
> Bedingungen grob richtig. Sobald ein Allpass-Signal mit einem trockenen
> Signal gemischt wird, entscheidet die frequenzabhängige Phase über
> Auslöschung und Verstärkung.

### Schriftliche Folien-Zusammenfassung

Dieser Block wiederholt die wichtigsten Filtertypen. Ein Tiefpass lässt tiefe
Frequenzen durch und dämpft hohe Frequenzen. Ein Hochpass macht das Gegenteil:
tiefe Frequenzen werden gedämpft, hohe Frequenzen bleiben erhalten. Ein
Bandpass lässt nur einen Frequenzbereich um eine Mittenfrequenz durch, während
eine Bandsperre oder ein Notch genau diesen Bereich absenkt. Shelving-Filter
heben oder senken ganze tiefe oder hohe Frequenzbereiche an. Ein Peak-EQ hebt
oder senkt gezielt einen Bereich um eine Mittenfrequenz. Ein Allpass ist ein
Sonderfall: Der Betrag bleibt gleich, aber die Phase wird verändert.

Die wichtigsten Parameter sind \(f_c\), \(Q\), Bandbreite und Gain \(G\). Die
Bedeutung von \(f_c\) hängt vom Filtertyp ab. Beim Tiefpass und Hochpass ist
\(f_c\) die Grenzfrequenz. Beim Bandpass, Notch und Peak-EQ ist \(f_c\) die
Mittenfrequenz. Bei Shelving-Filtern beschreibt \(f_c\) den Übergangsbereich
zwischen zwei Pegelbereichen. Der Parameter \(Q\) beschreibt, wie breit oder
schmal ein Filterbereich ist. Ein hoher \(Q\)-Wert bedeutet meist: schmaler,
resonanter oder gezielter.

In den Referenzabbildungen wird \(Q=1/\sqrt{2}\) verwendet. Die Kurven werden
als Betrag in dB auf logarithmischer Frequenzachse gezeigt. Eine zusätzliche
Bildserie zeigt dieselben Filter mit etwas höherer Güte \(Q=1.25\); die
Referenzkurve bleibt darin grau sichtbar.

Wichtig ist, Filter nicht nur über den Betrag zu verstehen. Der Betrag sagt,
welche Frequenzen lauter oder leiser werden. Die Phase sagt, wie die einzelnen
Frequenzanteile zeitlich gegeneinander verschoben werden. Der Allpass macht
diese Trennung besonders deutlich: Der Betrag bleibt idealerweise überall
gleich, aber die Phase ändert sich. Viele Audioeffekte entstehen erst, wenn
Betrag, Phase, Mischung und Zeitverhalten gemeinsam betrachtet werden.

## Block 3: Shelving- und Peak-EQ als parametrische Biquads

### Ziel

Low-Shelf, High-Shelf und Peak-EQ sind zentrale Studiofilter dieser Vorlesung.
Sie verbinden die Biquad-Sprache aus Vorlesung 7/8 mit einem vertrauten
Plugin-Interface:

- Grenz- beziehungsweise Mittenfrequenz \(f_c\)
- Güte \(Q\)
- Gain \(G\) in dB

### Systemfunktion

Die Biquad-Systemfunktion bleibt:

```latex
\[
H(z)
=
\frac{b_0+b_1z^{-1}+b_2z^{-2}}
{1+a_1z^{-1}+a_2z^{-2}}.
\]
```

Die Differenzengleichung in der verwendeten Vorzeichenkonvention:

```latex
\[
y[n]
=
b_0x[n]+b_1x[n-1]+b_2x[n-2]
-a_1y[n-1]-a_2y[n-2].
\]
```

### Parameterumrechnung nach Zölzer 2011, Kap. 2.3.2

Für die Koeffizientenberechnung werden verwendet:

```latex
\[
K=\tan\left(\pi\frac{f_c}{f_s}\right),
\qquad
V_0=10^{G/20}.
\]
```

Dabei ist:

- \(f_c\): Übergangsfrequenz beim Shelf, Mittenfrequenz beim Peak-EQ
- \(f_s\): Abtastrate
- \(G\): Boost/Cut in dB
- \(V_0\): linearer Gainfaktor
- \(Q\): Güte; hohe Werte bedeuten steilere Shelves beziehungsweise schmalere Peak-Eingriffe

### Bildserie im Block

Die Abbildungen werden ab hier in der typischen Audio-EQ-Sicht gezeigt:
Betrag in dB und logarithmische Frequenzachse von \(20\,\mathrm{Hz}\) bis
\(20\,\mathrm{kHz}\). Die vertikale schwarze gestrichelte Linie markiert
jeweils \(f_c\), ohne dass ein zusätzliches Textlabel im Plot steht.

Die Bildserie besteht aus neun Schritten:

- Peak-EQ bei \(f_c=500\,\mathrm{Hz}\) mit Referenzgüte \(Q=1/\sqrt{2}\) und
  vier Gain-Werten \(G=\pm6\,\mathrm{dB}\) und
  \(G=\pm12\,\mathrm{dB}\). Dadurch wird zuerst sichtbar, dass dieselbe
  Struktur einen Frequenzbereich unterschiedlich stark anheben oder absenken
  kann.
- Peak-EQ bei gleicher Mittenfrequenz mit erhöhter Güte \(Q=1.25\). Die
  Referenzgüte bleibt grau sichtbar, die höhere Güte wird grün ergänzt. Damit
  wird deutlich, dass \(Q\) die Breite des Eingriffs bestimmt.
- Low-Shelf bei \(f_c=200\,\mathrm{Hz}\) mit mehreren Gain-Werten und
  Referenzgüte \(Q=1/\sqrt{2}\). Damit wird zuerst sichtbar, dass ein Shelf
  nicht nur einen schmalen Bereich verändert, sondern einen ganzen unteren
  Frequenzbereich auf ein neues Pegelniveau bringt.
- Low-Shelf bei gleicher Grenzfrequenz mit erhöhter Güte \(Q=1.25\). Die
  Referenzgüte bleibt grau im Plot stehen, die erhöhte Güte wird grün
  ergänzt. Dadurch wird der steilere beziehungsweise stärker betonte Übergang
  direkt vergleichbar.
- High-Shelf bei \(f_c=5\,\mathrm{kHz}\) mit mehreren Gain-Werten und
  Referenzgüte \(Q=1/\sqrt{2}\). Es zeigt die entsprechende Bearbeitung des
  oberen Frequenzbereichs.
- High-Shelf bei gleicher Grenzfrequenz mit erhöhter Güte \(Q=1.25\). Auch hier
  bleibt die Referenz grau sichtbar, während die höhere Güte grün aufgebaut
  wird.
- DAW-EQ-Kaskade aus Hochpass, drei Peak-EQs und High-Shelf. Die einzelnen
  Filter werden grau gezeigt, die resultierende Kaskade grün.
- Summenphase derselben Kaskade. Damit wird sichtbar, dass ein DAW-EQ nicht
  nur den Betrag verändert, sondern auch die Phase.
- Gruppenlaufzeit derselben Kaskade als eigene Abbildung. Hier wird das
  Laufzeitverhalten separat lesbar, inklusive negativer Werte im Plotbereich.

### Boost-Fall \(G\geq0\)

Hilfsnenner:

```latex
\[
D_B = 1+\frac{1}{Q}K+K^2.
\]
```

Koeffizienten:

```latex
\[
b_0=\frac{1+\frac{V_0}{Q}K+K^2}{D_B},
\qquad
b_1=\frac{2(K^2-1)}{D_B},
\qquad
b_2=\frac{1-\frac{V_0}{Q}K+K^2}{D_B},
\]

\[
a_1=\frac{2(K^2-1)}{D_B},
\qquad
a_2=\frac{1-\frac{1}{Q}K+K^2}{D_B}.
\]
```

### Cut-Fall \(G<0\)

Hilfsnenner:

```latex
\[
D_C = 1+\frac{1}{V_0Q}K+K^2.
\]
```

Koeffizienten:

```latex
\[
b_0=\frac{1+\frac{1}{Q}K+K^2}{D_C},
\qquad
b_1=\frac{2(K^2-1)}{D_C},
\qquad
b_2=\frac{1-\frac{1}{Q}K+K^2}{D_C},
\]

\[
a_1=\frac{2(K^2-1)}{D_C},
\qquad
a_2=\frac{1-\frac{1}{V_0Q}K+K^2}{D_C}.
\]
```

### Lehrenden-Notiz

Das ist didaktisch stark, weil die Studierenden sehen:

1. Das Plugin zeigt nur \(f_c\), \(Q\), \(G\).
2. Intern werden daraus die Biquad-Koeffizienten.
3. Diese Koeffizienten bestimmen Pole und Nullstellen.
4. Pole und Nullstellen erzeugen den sichtbaren Frequenzgang.

Wichtig ist, nicht in algebraischer Detailtiefe stecken zu bleiben. Die
Koeffizientenformeln sollen zeigen: Ein musikalischer Parameter wird in eine
DSP-Struktur übersetzt.

### Typische Erklärung im Unterricht

> Low-Shelf, High-Shelf und Peak-EQ sind keine Sonderfälle außerhalb unserer
> Theorie. Sie sind Biquads. Das Plugin rechnet aus \(f_c\), \(Q\) und \(G\)
> die Koeffizienten \(b_0,b_1,b_2,a_1,a_2\) aus. Danach ist es wieder genau
> unsere bekannte Systemfunktion \(H(z)\).

### Schriftliche Folien-Zusammenfassung

Low-Shelf, High-Shelf und Peak-EQ sind typische Beispiele dafür, wie
musikalische Plugin-Parameter in eine DSP-Struktur übersetzt werden. Im Plugin
werden meist Grenz- beziehungsweise Mittenfrequenz \(f_c\), Güte \(Q\) und
Gain \(G\) eingestellt. Intern werden daraus die Biquad-Koeffizienten
\(b_0,b_1,b_2,a_1,a_2\) berechnet. Danach sind diese EQs keine neue Theorie,
sondern genau die bekannte Biquad-Systemfunktion:

```latex
\[
H(z)=
\frac{b_0+b_1z^{-1}+b_2z^{-2}}
{1+a_1z^{-1}+a_2z^{-2}}.
\]
```

Der Parameter \(f_c\) legt fest, wo die Anhebung oder Absenkung im Spektrum
liegt. Beim Low-Shelf betrifft sie den unteren Frequenzbereich, beim High-Shelf
den oberen Frequenzbereich und beim Peak-EQ einen Bereich um die
Mittenfrequenz. Der Parameter \(Q\) legt fest, wie steil der Übergang ist
beziehungsweise wie breit der Peak-Eingriff ausfällt. Ein kleiner \(Q\)-Wert
erzeugt eine breite Klangveränderung, ein größerer \(Q\)-Wert einen
steileren oder gezielteren Eingriff. Der Gain \(G\) bestimmt, ob der Bereich
angehoben oder abgesenkt wird und wie stark diese Änderung ist. Über
\(V_0=10^{G/20}\) wird der dB-Wert in einen linearen Verstärkungsfaktor
übersetzt.

Didaktisch ist dieser EQ-Block wichtig, weil er die Brücke zwischen
Bedienoberfläche und Systemtheorie zeigt. Die Studierenden sehen im Plugin
\(f_c\), \(Q\) und \(G\). Das System arbeitet aber mit Koeffizienten. Diese
Koeffizienten bestimmen Pole und Nullstellen und damit den sichtbaren
Frequenzgang.

Ein vollständiger DAW-EQ entsteht dann durch Kaskadierung mehrerer solcher
Biquads: zum Beispiel ein Hochpass, mehrere Peak-EQs und ein High-Shelf. Die
Einzelfilter haben jeweils ihren eigenen Frequenzgang. Multipliziert man diese
Systemfunktionen, erhält man den Summenfrequenzgang des EQs. Deshalb wird im
Plot die Summe grün und die einzelnen Filter grau gezeigt.

## Block 4: Zeitvariante Filter - Wah-Wah und Phaser

### Wah-Wah

Nach Zölzer 2011, Kap. 2.4.1:

Ein Wah-Wah ist im Kern ein Bandpassfilter mit veränderlicher Mittenfrequenz
und relativ kleiner Bandbreite:

```latex
\[
f_c[n]=f_\mathrm{min}+
\frac{1+m[n]}{2}\left(f_\mathrm{max}-f_\mathrm{min}\right).
\]
```

Parameter im Demonstrations-Plugin:

- Center Frequency \(f_\mathrm{center}\)
- Depth in Oktaven
- Q oder Bandbreite
- Rate des LFO
- Mix/Dry-Wet
- Steuerquelle: Pedal, LFO, Envelope-Follower

Für die neue Bildserie wird das Wah-Wah als zeitvarianter Bandpass zweiter
Ordnung dargestellt. Die grüne Kurve ist der momentane Frequenzgang, die graue
Kurve bleibt als feste Referenz stehen.

Die Mittenfrequenz wird wie im JSFX logarithmisch um die Center Frequency
bewegt:

```latex
\[
f_c[n]
=
f_\mathrm{center}\,2^{D\,m[n]}.
\]
```

Verwendete Parameter:

| Parameter | Wert |
|---|---:|
| Abtastrate | \(f_s=48\,\mathrm{kHz}\) |
| Center Frequency | \(f_\mathrm{center}=500\,\mathrm{Hz}\) |
| Depth | \(D=1{,}2\,\mathrm{oct}\) |
| LFO Rate | \(1{,}2\,\mathrm{Hz}\) |
| Mix Serie 1 und 2 | \(0{,}0\) |
| Mix Serie 3 | \(0{,}5\) |
| Güte Serie 1 | \(Q=5\) |
| Güte Serie 2 | \(Q=15\) |

Die Animation läuft hin und zurück und startet bei der Referenzfrequenz. Da
die Frequenzachse logarithmisch dargestellt wird, wird auch die Bewegung im
Log-Frequenzraum berechnet. Dadurch wirkt der Sweep in der Abbildung
gleichmäßig:

```latex
\[
\log f_c[n]
=
\log f_\mathrm{ref}
+
m[n]\left(\log f_\mathrm{ziel}-\log f_\mathrm{center}\right).
\]
```

Der TPT-State-Variable-Bandpass aus dem JSFX hat am Bandpassausgang zunächst
einen Peak, der mit \(Q\) skaliert. Für die Abbildungen und das
Demonstrations-JSFX wird deshalb der Bandpassausgang durch \(Q\) geteilt:

```latex
\[
y_\mathrm{BP,norm}[n]
=
\frac{y_\mathrm{BP}[n]}{Q}.
\]
```

Damit verändert \(Q\) sichtbar die Bandbreite und Resonanzform, aber nicht die
maximale dargestellte Amplitude. Beide Wah-Wah-Serien erreichen deshalb
maximal \(0\,\mathrm{dB}\).

In der dritten Wah-Wah-Serie wird dieselbe hohe Güte \(Q=15\) verwendet, aber
zum reinen Bandpass wird 50 Prozent Dry-Signal zugemischt. In dieser
Darstellung bedeutet \(M=0\): reiner Wah-/Bandpass. \(M=0{,}5\) bedeutet:
50 Prozent Dry-Anteil:

```latex
\[
H_\mathrm{Wah,Mix}(e^{j\Omega})
=
(1-M)H_\mathrm{BP,norm}(e^{j\Omega})+M,
\qquad
M=0{,}5.
\]
```

Damit ist sichtbar, dass der Effekt nicht nur durch die bewegte
Mittenfrequenz und \(Q\), sondern auch durch den Dry/Wet-Mix geprägt wird.

Didaktischer Punkt: Beim Wah-Wah bewegt sich der Betrag direkt. Der Peak des
Bandpassfilters wandert durch das Spektrum. Genau deshalb klingt das
Wah-Wah wie ein bewegter Formant. Die Animation startet bei der grauen
Referenzfrequenz \(f_\mathrm{center}=500\,\mathrm{Hz}\), läuft zu höheren und
tieferen Mittenfrequenzen und kehrt wieder zur Referenz zurück.

Klang:

- formantartig
- sprach-/vokalartig
- besonders wirksam auf Gitarre, Synth, Bass

Das begleitende Wah-Wah-JSFX liegt im Projektordner unter
`audio_exports/reaper_jsfx/simple_wah_wah_bandpass.jsfx`. Für die Abbildungen
kann nur der Wah-Wah-Teil mit `export_block_04_wah_wah.py` neu gerendert
werden. Der Phaser-Teil liegt entsprechend in `export_block_04_phaser.py`.
Das gemeinsame Skript `export_block_04_zeitvariante_filter.py` rendert den
gesamten Block.

Zusätzlich gibt es für Block 4 zwei Spektrogramme mit demselben
bandbegrenzten Rechtecksignal wie Eingangsmaterial:
`17_square_wah_wah_spectrogram.png` und
`18_square_phaser_spectrogram.png`. Das Wah-Wah-Spektrogramm zeigt, welche
Harmonischen durch den wandernden Bandpass gerade betont werden. Das
Phaser-Spektrogramm zeigt dagegen keine bewegte Tonhöhe, sondern zeitabhängige
Pegeländerungen durch Allpass-Phase, Dry/Wet-Summation und Feedback.

### Phaser

Nach Zölzer 2011, Kap. 2.4.2:

Ein Phaser entsteht nicht primär aus einer Delayline, sondern aus
frequenzabhängiger Phase. Typisch ist:

- Kaskade aus Allpassfiltern
- langsame Bewegung der Allpass-Parameter
- Mischung mit Direktsignal
- dadurch wandernde Auslöschungen und Verstärkungen

Blockidee:

```latex
\[
y[n]=x[n]+g\,x_\mathrm{AP}[n]
\]
```

wobei \(x_\mathrm{AP}[n]\) aus einer Kaskade zeitvarianter Allpassfilter
kommt.

Für die Abbildungen im Block wird die Erklärung in zwei Teile getrennt.
Zuerst wird statisch gezeigt, wie aus zwei Allpässen zweiter Ordnung durch
Dry/Wet-Summation eine Phaser-artige Notch-Struktur entsteht. Danach wird die
zeitvariante 4-Stage-Struktur gezeigt, die zum Reaper-JSFX passt.

Die elementare Allpass-Stufe erster Ordnung wurde in Block 2 eingeführt:

```latex
\[
A_1(z)
=
\frac{a-z^{-1}}{1-a z^{-1}}.
\]
```

Der Koeffizient \(a\) ist der interne Allpass-Koeffizient. Er bestimmt, wo
und wie stark die Allpass-Stufe die Phase dreht. Damit verschiebt \(a\)
indirekt die Notches des Phasers. Wichtig ist die Notation: Das \(d\) im
Schaltbild ist der Dry-Gain. Für die Umrechnung von \(f_\mathrm{AP}\) nach
\(a\) wird dieselbe Form wie im Plugin verwendet:

```latex
\[
g
=
\tan\left(\pi\frac{f_\mathrm{AP}}{f_s}\right),
\qquad
a=
\frac{1-g}{1+g}.
\]
```

Hier ist \(f_\mathrm{AP}\) nicht direkt eine Grenzfrequenz wie beim
Tiefpass, sondern der Steuerwert, mit dem die Phasendrehung des Allpasses
verschoben wird. Der LFO moduliert also \(f_\mathrm{AP}\) beziehungsweise
\(a\), nicht den Dry-Gain \(d\).

Für den statischen Aufbau werden zwei Allpässe zweiter Ordnung verwendet:
\(A(z)\) bei \(500\,\mathrm{Hz}\) und \(B(z)\) bei \(1600\,\mathrm{Hz}\). Die
Abbildung von \(A(z)\) entspricht dem Allpass zweiter Ordnung aus Block 2.
\(B(z)\) zeigt dieselbe Struktur mit höherer Frequenz. Beide Allpässe haben
idealerweise Betrag \(1\), aber unterschiedliche Phasendrehungen:

```latex
\[
\left|A(e^{j\Omega})\right|=1,
\qquad
\left|B(e^{j\Omega})\right|=1.
\]
```

Werden beide Allpässe hintereinander geschaltet, multiplizieren sich die
Systemfunktionen:

```latex
\[
A_\mathrm{cas}(z)=A(z)B(z).
\]
```

Auch diese Kaskade ist noch ein Allpass:

```latex
\[
\left|A_\mathrm{cas}(e^{j\Omega})\right|=1.
\]
```

Erst die Dry/Wet-Summation erzeugt den sichtbaren Notch im Betragsgang:

```latex
\[
H_\mathrm{static}(z)
=
d+e\,A(z)B(z).
\]
```

Für die statischen Abbildungen gilt:

| Parameter | Wert |
|---|---:|
| Abtastrate | \(f_s=48\,\mathrm{kHz}\) |
| Allpass A | Allpass 2. Ordnung, \(f_\mathrm{AP,A}=500\,\mathrm{Hz}\), \(Q=1/\sqrt{2}\) |
| Allpass B | Allpass 2. Ordnung, \(f_\mathrm{AP,B}=1600\,\mathrm{Hz}\), \(Q=1/\sqrt{2}\) |
| Dry Gain | \(d=0{,}5\) |
| Wet Gain | \(e=0{,}5\) |
| Feedback | \(f_b=0\) |

Wenn man stattdessen bereits gebildete Dry/Allpass-Notches hintereinander
schalten würde, wäre das eine andere Struktur:

```latex
\[
H_{\mathrm{Notch\,cascade}}(z)
=
\left(\frac{1+A(z)}{2}\right)
\left(\frac{1+B(z)}{2}\right)
\neq
\frac{1+A(z)B(z)}{2}.
\]
```

Für den Phaser ist also nicht „zwei Notchfilter hintereinander“ der technische
Kern, sondern „Allpass-Kaskade und danach Dry/Wet-Summation“.

Wichtig für die Erklärung: Die Allpass-Kaskade allein verändert den Betrag
nicht. Sie verändert aber die Phase. Die Notches entstehen erst, wenn das
allpassgefilterte Signal mit dem Direktsignal gemischt wird. Auslöschungen
treten dort auf, wo die Allpass-Kaskade gegenüber dem Direktsignal ungefähr
gegenphasig ist:

```latex
\[
\angle A_N(e^{j\Omega})
\approx
(2k+1)\pi .
\]
```

Die Abstände der Notches sind beim Phaser deshalb nicht konstant wie beim
Comb-Filter. Beim Comb-Filter setzt die Delayzeit \(M\) den regelmäßigen
Abstand. Beim Phaser bestimmt die gekrümmte Phasenkurve der Allpässe, wo die
Auslöschungen liegen. Wird \(a\) zeitlich bewegt, wandern diese Stellen.

Die Anzahl der Allpässe bestimmt, wie stark sich die Phase insgesamt drehen
kann. Ein Allpass erster Ordnung dreht die Phase von \(0\) bis ungefähr
\(-\pi\). Vier kaskadierte Allpässe drehen entsprechend bis ungefähr
\(-4\pi\). Dadurch entstehen bei der Dry/Wet-Mischung prinzipiell zwei
Gegenphasenstellen und damit zwei Notches. Genau deshalb wird der animierte
Phaser ab der zweiten Serie als 4-Stage-Phaser gezeigt.

Für die Animation wird \(a[n]\) aus einem langsam bewegten
\(f_\mathrm{AP}[n]\) gebildet. Auch hier läuft die Bewegung im
Log-Frequenzraum, damit die Notches auf der logarithmischen Frequenzachse
gleichmäßig wandern:

```latex
\[
\log f_\mathrm{AP}[n]
=
\log f_\mathrm{AP,ref}
+
m[n]\left(\log f_\mathrm{ziel}-\log f_\mathrm{AP,ref}\right)
\]

\[
g[n]
=
\tan\left(\pi\frac{f_\mathrm{AP}[n]}{f_s}\right),
\qquad
a[n]
=
\frac{1-g[n]}{1+g[n]}.
\]
```

Mit \(f_\mathrm{min}=250\,\mathrm{Hz}\) und
\(f_\mathrm{max}=1600\,\mathrm{Hz}\) bewegt sich der Frequenzgang im GIF hin
und zurück. Die graue Kurve bleibt als feste Referenz bei
\(f_\mathrm{AP,ref}=500\,\mathrm{Hz}\) stehen, die grüne Kurve zeigt den
momentanen Frequenzgang. Auch diese Animation startet bei der Referenz, sodass
die grüne Kurve zu Beginn auf der grauen Referenz liegt. Diese erste
Phaser-Serie wird bewusst ohne Feedback gezeigt:

```latex
\[
H_{\mathrm{Phaser},\,f_b=0}(z)
=
d
+
e\,A_1^4(z).
\]
```

Damit ist zuerst der 4-Stage-Phaser ohne Feedback sichtbar. Danach wird
\(f_b\) zugeschaltet.

Als zweite Phaser-Serie wird \(f_b\) variiert. Dabei bleiben
\(f_\mathrm{AP}=500\,\mathrm{Hz}\) und der eingestellte Wet-Gain
\(e=0{,}5\)
konstant. \(f_b\) bestimmt die Rückkopplung um die Allpass-Kaskade:

```latex
\[
H_\mathrm{Phaser}(z,f_b)
=
d
+
e\,
\frac{A_1^4(z)}{1-f_bA_1^4(z)}.
\]
```

Für die Abbildungen und das JSFX wird der rückgekoppelte Allpass-Ausgang
zusätzlich mit \(1-f_b\) pegelkompensiert. Damit bleibt die maximale Amplitude
der dargestellten Kurve bei 0 dB, während die Formänderung durch \(f_b\)
weiterhin sichtbar bleibt:

```latex
\[
H_{\mathrm{Plot}}(z,f_b)
=
d
+
e(1-f_b)\,
\frac{A_1^4(z)}{1-f_bA_1^4(z)}.
\]
```

Man kann das auch als effektiven Wet-Gain lesen:

```latex
\[
e_\mathrm{eff}
=
e(1-f_b).
\]
```

Der Bedienparameter \(e\) bleibt also konstant. Für die pegelnormalisierte
Darstellung ändert sich aber der tatsächlich ausgegebene Wet-Anteil
\(e_\mathrm{eff}\), sobald \(f_b\) verändert wird.

Die graue Referenz ist in dieser Serie der Fall \(f_b=0\). Die grüne Kurve
zeigt den jeweils aktiven Feedbackwert. Je größer \(f_b\) wird, desto stärker
ändert sich die Form des Frequenzgangs: Resonanzen und Auslöschungen werden
ausgeprägter. Bei zu großem Feedback kann der Effekt schnell sehr spitz und
instabil wirkend werden. In der Bildserie wird \(f_b\) deshalb nur in einem
stabilen Bereich zwischen \(0\) und ungefähr \(0{,}9\) bewegt.

Zusätzlich gibt es eine dritte Phaser-Serie, in der nicht \(a[n]\), sondern
der Wet-Anteil \(e\) verändert wird:

```latex
\[
H_\mathrm{Phaser}(z,e)
=
d
+
e\,A_1^4(z)
\qquad
\text{für } f_b=0.
\]
```

Für diese Bildserie bleibt \(f_\mathrm{AP}=500\,\mathrm{Hz}\) fest. Der
Wet-Anteil startet bei der Referenz \(e=0{,}5\), läuft bis \(e=0\) und
kehrt wieder zur Referenz zurück. Bei \(e=0\) ist nur der trockene Anteil
sichtbar, der Frequenzgang ist deshalb flach. Mit größerem \(e\) werden die
Auslöschungen und Verstärkungen sichtbar. Diese Serie erklärt also nicht die
typische LFO-Modulation, sondern die Rolle der Dry/Wet-Mischung.

Der Dry-Gain \(d\) bleibt dabei konstant. Er wird in dieser Darstellung nicht
vom LFO moduliert. Das entspricht der üblichen Phaser-Struktur: Der LFO bewegt
die Allpass-Parameter, während \(d\), \(e\) und \(f_b\) Bedienparameter sind.

Typische LFO-modulierte Phaser-Parameter sind:

- der Allpass-Koeffizient \(a[n]\) beziehungsweise der zugehörige
  Sweep-Bereich,
- Rate und Depth des Sweeps,
- bei manchen Geräten zusätzlich Stereo-Phase oder Feedback-Tiefe.

Der Dry/Wet-Mix ist in der Regel ein statischer Bedienparameter oder wird per
Automation geändert. Er wird normalerweise nicht als eigentlicher
Phaser-LFO-Parameter moduliert.

Parameter:

- Rate
- Depth
- Feedback
- Anzahl der Stages, hier für die Animation \(N=4\)
- Mix

Das begleitende Reaper-JSFX liegt im Projektordner unter
`audio_exports/reaper_jsfx/simple_4_stage_mono_allpass_phaser.jsfx`. Es nutzt
fest vier Allpass-Stufen. Die Studierenden hören dadurch dieselbe Struktur wie
in der animierten Bildserie: \(f_\mathrm{AP}\) bewegt den
Allpass-Koeffizienten \(a\), \(d\) ist der Dry-Anteil, \(e\) der
Allpass-/Wet-Anteil und \(f_b\) die Rückkopplung um die Allpass-Kaskade.

Lehrenden-Notiz:

Der Phaser klingt dem Flanger verwandt, aber die Ursache ist anders:

- Flanger: kurze modulierte Delayline -> Kammfilter bewegt sich.
- Phaser: Allpass-/Notch-Struktur -> Phasenauslöschungen bewegen sich.

Das ist ein guter Punkt für eine kurze Hörfrage: "Klingt ähnlich, aber
welche Struktur steckt dahinter?"

Didaktische Einordnung:

Der Phaser bleibt bewusst im Filterblock. Der Allpass wurde in Block 2 schon
als Filter eingeführt, der den Betrag nicht verändert, aber die Phase dreht.
Im Phaser wird genau diese Phasenwirkung zeitlich bewegt und mit dem
Direktsignal gemischt. Dadurch entstehen wandernde Auslöschungen. Damit ist
der Phaser kein Delay-Effekt im engeren Sinn, sondern ein zeitvarianter
Filtereffekt.

### Schriftliche Folien-Zusammenfassung

Zeitvariante Filtereffekte verändern Filterparameter während das Signal läuft.
Dadurch ist das System nicht mehr zeitinvariant. Ein gleicher Eingang klingt
unterschiedlich, je nachdem, zu welchem Zeitpunkt er durch das System läuft.
Der wichtigste neue Begriff ist der LFO: ein langsamer Oszillator, der nicht
als Audiosignal gehört wird, sondern einen Effektparameter steuert.

Beim Wah-Wah bewegt der LFO, ein Pedal oder ein Envelope-Follower die
Mittenfrequenz eines Bandpassfilters. Dadurch wandert ein betonter
Frequenzbereich durch das Spektrum. Das klingt sprach- oder vokalartig. Beim
Phaser werden dagegen Allpass-Parameter bewegt und das allpassgefilterte Signal
mit dem trockenen Signal gemischt. Dadurch entstehen wandernde
Auslöschungen. Phaser und Flanger können ähnlich klingen, beruhen aber auf
unterschiedlichen Strukturen: Phaser auf bewegter Phase, Flanger auf einer
kurzen modulierten Delayline.

Beim Phaser ist die Anzahl der Allpässe ein wichtiger Klangparameter. Ein
einzelner Allpass verändert den Betrag nicht, dreht aber die Phase. Werden
mehrere Allpässe kaskadiert, addieren sich diese Phasendrehungen. Dadurch gibt
es im Dry/Wet-Signal mehr Frequenzen, bei denen beide Signalanteile
gegeneinander auslöschen. Mehr Allpass-Stages bedeuten daher typischerweise
mehr Notches und einen dichteren, stärkeren Phaser-Klang. In der statischen
Herleitung wird zuerst die Kaskade aus zwei Allpässen zweiter Ordnung
\(A(z)B(z)\) gezeigt. In der Animation bleibt die Anzahl der Stages dann fest
bei \(N=4\), passend zum begleitenden Reaper-JSFX. Zeitvariant ist der
Allpass-Koeffizient \(a[n]\). Wenn \(a[n]\) durch den LFO verändert wird,
ändert sich die Phasenkurve der Allpass-Kaskade. Dadurch verschieben sich die
Auslöschungen und der momentane Frequenzgang wandert.

Die zusätzliche Feedback-Serie zeigt, dass \(f_b\) nicht nur die Stärke des
Effekts, sondern die Form des Frequenzgangs verändert. Ohne Feedback sieht man
zuerst die reine Dry/Wet-Interferenz aus Dry-Signal und Allpass-Signal. Mit
zunehmendem Feedback werden Resonanzen und Auslöschungen deutlicher.

Die zusätzliche Dry/Wet-Serie zeigt einen anderen Zusammenhang: Ohne Wet-Anteil
bleibt nur das trockene Signal übrig, der Frequenzgang ist flach. Je stärker
der Wet-Anteil zugemischt wird, desto deutlicher werden die Auslöschungen und
Verstärkungen. Dry/Wet bestimmt also die Stärke des hörbaren Phaser-Effekts,
ist aber normalerweise kein LFO-modulierter Parameter. Der LFO bewegt beim
klassischen Phaser vor allem die Allpass-Parameter.

### Didaktische Abgrenzung

Nicht jeder zeitlich bewegte Effekt ist ein zeitvarianter Filtereffekt. Für
diese Vorlesung ist die Trennung:

| Gruppe | Beispiele | Technischer Kern |
|---|---|---|
| zeitvariante Filtereffekte | Wah-Wah, Phaser | Filter-, Allpass- oder Notch-Parameter bewegen sich |
| zeitvariante Delay-Effekte | Vibrato, Flanger, Chorus | Delayzeit \(M[n]\) bewegt sich |
| statische Delay-Effekte | Slapback, Echo | feste Delayzeit, ggf. Feedback |
| Modulationseffekte | Amplitudenmodulation, Ringmodulation | Signal wird mit Steuer- oder Trägersignal multipliziert |

## Block 5: Comb-Filter als FIR- und IIR-Implementierung

### Einordnung

Der Comb-Filter ist der Übergang von den Filtereffekten zu den
Delay-basierten Effekten. Technisch entsteht er aus einer Delayline. Seine
unmittelbare Wirkung wird hier aber zuerst als Filterwirkung gelesen: Durch
die Mischung eines Signals mit einer verzögerten Kopie entstehen periodische
Peaks und Kerben im Frequenzgang.

Didaktischer Satz:

> Dieselbe Grundidee, eine verzögerte Kopie zuzumischen, kann je nach
> Delayzeit als Klangfärbung, Slapback oder Echo wahrgenommen werden. Bei sehr
> kurzen Delayzeiten hören wir vor allem die Kammfilterwirkung.

### Feedforward-Comb / FIR-Comb

Nach Zölzer 2011, Kap. 2.5.1:

```latex
\[
y[n]=x[n]+g\,x[n-M].
\]
```

Systemfunktion:

```latex
\[
H(z)=1+gz^{-M}.
\]
```

Parameter:

- \(M\): Delay in Samples
- \(\tau=M/f_s\): Delayzeit in Sekunden
- \(g\): Pegel der verzögerten Kopie

Frequenzabstand der Kammstruktur:

```latex
\[
\Delta f = \frac{f_s}{M}=\frac{1}{\tau}.
\]
```

Didaktischer Kern:

> Eine direkte Kopie plus eine verzögerte Kopie erzeugt Interferenz. Aus einem
> simplen Zeitversatz wird ein periodischer Frequenzgang.

Für die Bildserie wird der FIR-Comb zusätzlich auf maximale Amplitude
\(0\,\mathrm{dB}\) normiert. Verwendet wird:

```latex
\[
H_\mathrm{FIR}(z)
=
\frac{1+g z^{-M}}{1+|g|}.
\]
```

Dadurch bleibt der höchste Wert des Betragsfrequenzgangs bei
\(0\,\mathrm{dB}\), unabhängig davon, ob \(g\) positiv oder negativ ist.

### Feedback-Comb / IIR-Comb

Nach Zölzer 2011, Kap. 2.5.2:

```latex
\[
y[n]=c\,x[n]+g\,y[n-M].
\]
```

Systemfunktion:

```latex
\[
H(z)=\frac{c}{1-gz^{-M}}.
\]
```

Stabilität:

```latex
\[
|g|<1.
\]
```

Zeitbereich:

- Das Eingangssignal wird immer wieder durch die Delayline geführt.
- Nach jeder Runde ist die Amplitude um \(g\) skaliert.
- Die Impulsantwort klingt geometrisch ab.

Frequenzbereich:

- Es entstehen schmale Resonanzpeaks.
- Je größer \(|g|\), desto stärker und schmaler die Resonanzen.
- Bei \(|g|\to1\) wird das System sehr resonant und nähert sich der
  Stabilitätsgrenze.

Für die Bildserie wird der IIR-Comb ebenfalls auf maximale Amplitude
\(0\,\mathrm{dB}\) normiert. Dafür wird der Vorfaktor

```latex
\[
c=1-|g|
\]
```

gesetzt:

```latex
\[
H_\mathrm{IIR}(z)
=
\frac{1-|g|}{1-gz^{-M}}.
\]
```

Für \(g>0\) liegt ein Resonanzmaximum bei \(\Omega=0\). Dort gilt
\(|1-g|=1-|g|\), deshalb wird der Betrag genau \(1\), also
\(0\,\mathrm{dB}\). Für \(g<0\) verschiebt sich das Maximum um
\(\pi/M\), aber die Normierung bleibt gleich.

### Bildserie im Block

Die Spektrum-Plots zeigen den Kammfilter über der normierten Kreisfrequenz
\(\Omega/\pi\). Die Systemfunktion wird dort nicht als Formel eingeblendet,
damit die Interferenzstruktur im Vordergrund bleibt. Positive
Filterkoeffizienten werden durchgezogen dargestellt, negative
Filterkoeffizienten gestrichelt. Die Kurven sind so normiert, dass die
Maximalamplitude bei \(0\,\mathrm{dB}\) liegt.

Die Systemfunktion wird anschließend separat über die z-Ebene gezeigt:

- als 2D Pol-/Nullstellendiagramm,
- als 3D-Auswertung von \(|H(z)|\).

Damit bleibt die Erzählung sauber getrennt: zuerst Frequenzgang als hörbare
Kammstruktur, danach Pol-/Nullstellen und \(H(z)\) als Systembeschreibung.

### Verwendete Parameter in der Bildserie

Für die Spektrum-Bildserie werden zwei Delaylängen gezeigt:

| Zustand | Delay \(M\) | Abstand in \(\Omega/\pi\) |
|---|---:|---:|
| initial | \(6\) Samples | \(\Delta(\Omega/\pi)=2/6\approx0{,}333\) |
| neu | \(10\) Samples | \(\Delta(\Omega/\pi)=2/10=0{,}2\) |

Die Filterkoeffizienten sind:

```latex
\[
g=+0{,}7
\qquad\text{und}\qquad
g=-0{,}7.
\]
```

Positive Koeffizienten werden durchgezogen gezeichnet, negative
Koeffizienten gestrichelt. Die graue Kurve zeigt jeweils den initialen
Delaywert \(M=6\), die grüne Kurve den neuen Delaywert \(M=10\).

Der Abstand der periodischen Kammstruktur ergibt sich aus der Phasenbedingung
des Verzögerungsglieds. Der Term \(z^{-M}\) entspricht auf dem Einheitskreis

```latex
\[
z^{-M}=e^{-j\Omega M}.
\]
```

Wenn die Phase \(\Omega M\) um \(2\pi\) weiterläuft, wiederholt sich die
Struktur. Daher ist der Abstand in rad/Sample:

```latex
\[
\Delta\Omega=\frac{2\pi}{M}.
\]
```

Auf der in den Plots verwendeten normierten Achse \(\Omega/\pi\) wird daraus:

```latex
\[
\Delta\left(\frac{\Omega}{\pi}\right)
=
\frac{\Delta\Omega}{\pi}
=
\frac{2}{M}.
\]
```

Wenn stattdessen eine Frequenzachse in Hertz verwendet wird, gilt:

```latex
\[
\Delta f=\frac{f_s}{M}.
\]
```

Für \(f_s=48\,\mathrm{kHz}\) wären das:

```latex
\[
M=6:\quad \Delta f=8\,\mathrm{kHz},
\qquad
M=10:\quad \Delta f=4{,}8\,\mathrm{kHz}.
\]
```

In den Folien wird trotzdem \(\Omega/\pi\) genutzt, weil der Zusammenhang zu
Vorlesung 8 direkter ist und die Anzahl der sichtbaren Peaks überschaubar
bleibt.

Für die z-Ebenen-Abbildungen wird der neue Delaywert verwendet:

```latex
\[
M=10,\qquad g=+0{,}7.
\]
```

Beim FIR-Comb liegen die Nullstellen aus

```latex
\[
1+gz^{-M}=0
\quad\Longleftrightarrow\quad
z^M=-g.
\]
```

Bei \(M=10\) entstehen also zehn Nullstellen. Durch die Schreibweise mit
\(z^{-M}\) entstehen zusätzlich Pole im Ursprung, die aber die
Frequenzgangkerben nicht verursachen, sondern aus der negativen Potenz in der
Systemfunktion stammen.

Beim IIR-Comb entstehen die Pole aus

```latex
\[
1-gz^{-M}=0
\quad\Longleftrightarrow\quad
z^M=g.
\]
```

Bei \(M=10\) entstehen zehn Pole. Weil \(|g|=0{,}7<1\), liegen diese Pole
innerhalb des Einheitskreises. Die Nullstellen liegen bei dieser normierten
Darstellung im Ursprung.

### Vergleich

| Struktur | Gleichung | Impulsantwort | Klangbild |
|---|---|---|---|
| FIR-Comb | \(x[n]+g x[n-M]\) | zwei Impulse | Interferenz, Kammkerben |
| IIR-Comb | \(c x[n]+g y[n-M]\) | unendlich, abklingend | Resonanz, Echo-Serie, Nachschwingen |

### Lehrenden-Notiz

Hier passt der Rückbezug auf Vorlesung 8:

- FIR-Comb: Nullstellen bestimmen die Kerben.
- IIR-Comb: Pole bestimmen die Resonanzen.
- Beide sind Delay-Strukturen, aber mit unterschiedlicher Richtung:
  Feedforward erzeugt endliche Kopien, Feedback erzeugt Rückkopplung.

Diese Stelle bereitet Block 6 vor: Wenn das Delay länger wird, löst sich die
Filterwirkung zunehmend in wahrnehmbare Einzelreflexionen oder Echos auf.

### Schriftliche Folien-Zusammenfassung

Ein Comb-Filter entsteht, wenn ein Signal mit einer verzögerten Version von
sich selbst kombiniert wird. Dadurch interferieren die beiden Signalanteile.
Einige Frequenzen addieren sich konstruktiv, andere löschen sich teilweise
oder vollständig aus. Im Frequenzgang entsteht dadurch eine regelmäßige
Folge von Peaks und Kerben. Diese Form erinnert an einen Kamm, daher der Name
Comb-Filter.

Beim FIR-Comb wird das Eingangssignal mit einer verzögerten Eingangskopie
gemischt:

```latex
\[
y[n]=x[n]+g\,x[n-M],
\qquad
H_\mathrm{FIR}(z)=\frac{1+gz^{-M}}{1+|g|}.
\]
```

Die Impulsantwort ist endlich: Es gibt den direkten Impuls und nach \(M\)
Samples eine zweite Kopie. Die Normierung durch \(1+|g|\) sorgt in der
Bildserie dafür, dass die maximale Amplitude bei \(0\,\mathrm{dB}\) bleibt.
Die Kerben im Frequenzgang lassen sich über Nullstellen erklären. Beim
IIR-Comb wird dagegen ein verzögertes Ausgangssignal zurückgeführt:

```latex
\[
y[n]=c\,x[n]+g\,y[n-M],
\qquad
H_\mathrm{IIR}(z)=\frac{1-|g|}{1-gz^{-M}}.
\]
```

Die Impulsantwort ist dann eine abklingende Echo-Serie. Im z-Bild entstehen
Pole, die Resonanzen erzeugen. Je größer \(|g|\) wird, desto länger klingt
das System nach und desto näher kommt es an die Stabilitätsgrenze.

Der Abstand der Kammstruktur wird durch die Delaylänge \(M\) bestimmt. Auf der
normierten Kreisfrequenzachse gilt:

```latex
\[
\Delta\left(\frac{\Omega}{\pi}\right)=\frac{2}{M}.
\]
```

In der Bildserie werden \(M=6\) und \(M=10\) verwendet. Dadurch ergeben sich
die Abstände \(0{,}333\) und \(0{,}2\) auf der \(\Omega/\pi\)-Achse. Ein
größeres \(M\) bedeutet also: Die Peaks und Kerben liegen dichter
beieinander. Positive \(g\)-Werte und negative \(g\)-Werte haben denselben
Abstand, verschieben aber die Lage von Peaks und Kerben gegeneinander.

Wichtig für die Einordnung: Der Comb-Filter wird aus einer Delayline gebaut,
aber zuerst über seine Filterwirkung verstanden. Bei sehr kurzen Delayzeiten
dominiert die Klangfärbung durch Interferenz. Bei längeren Delayzeiten wird
aus derselben Grundstruktur ein Delay-Effekt wie Slapback oder Echo.

## Block 6: Delay-basierte Audioeffekte

### Variable Delayline

Delay-basierte FX entstehen aus:

```latex
\[
y[n]=x[n-M[n]]
\]
```

oder aus Mischungen mit dem trockenen Signal:

```latex
\[
y[n]=x[n]+g\,x[n-M[n]].
\]
```

Wenn \(M[n]\) nicht ganzzahlig ist, braucht man Interpolation. Dieser Punkt
bleibt in der gehaltenen Folienspur ein kurzer Implementationshinweis und
wird nicht als eigener Block ausgeführt. Für diesen Block reicht:

> Variable Delayzeit bedeutet meistens fractional delay. Interpolation sorgt
> dafür, dass Werte zwischen zwei Samples geschätzt werden.

### Vibrato

Nach Zölzer 2011, Kap. 2.6.1:

Vibrato entsteht durch periodisch veränderte Delayzeit, aber ohne starkes
Dry-Signal:

```latex
\[
M[n]=M_0+\Delta M\sin\left(2\pi f_\mathrm{LFO}\frac{n}{f_s}\right).
\]
```

```latex
\[
y[n]=x[n-M[n]].
\]
```

Klang:

- periodische Tonhöhenabweichung
- kein eigentliches Echo
- kein Kammfilter, wenn der trockene Anteil fehlt

Für Vibrato ist ein statischer Frequenzgang keine gute Hauptdarstellung. Das
System ist zeitvariant: Die Delayzeit bewegt sich, und dadurch ändert sich die
momentane Tonhöhe. Sichtbar wird das besser im Spektrogramm. In den
Abbildungen wird ein Sägezahn mit \(f_0=500\,\mathrm{Hz}\) verwendet. Der
unmodulierte Sägezahn zeigt zuerst eine feste Grundfrequenz und ihre
Obertöne. Danach wird derselbe Sägezahn mit einem langsamen LFO moduliert. Im
Spektrogramm wandern dann Grundton und Obertöne gemeinsam. Die STFT nutzt hier
eine eher hohe Frequenzauflösung mit \(N=4096\) und \(H=256\), damit die
Tonhöhenbewegung sichtbar wird. Für die Bildserie werden die oberen Werte aus
Zölzer, Tabelle 2.9, verwendet: Vibrato nutzt \(5\,\mathrm{Hz}\) Sinus,
Flanger \(1\,\mathrm{Hz}\) Sinus. Der Chorus ist bewusst die Ausnahme: Nach
Zölzer wird die Delayzeit beim Chorus nicht idealisiert als Sinus-LFO, sondern
als kleine zufällige Delayzeitvariation beschrieben. In der Bildserie wird das
als Lowpass-Noise-Modulation umgesetzt.

Für die Abbildungen in Block 6 wird die Standardstruktur aus Zölzer,
Abb. 2.34, als internes Modell verwendet. Sie wurde in der gehaltenen
Folienspur nicht als eigener Abschlussblock ausgespielt. Die drei
Pegelparameter sind dabei:

- \(BL\): direkter beziehungsweise Bypass-Anteil
- \(FF\): Feedforward-Anteil der variabel verzögerten Delayline
- \(FB\): Feedback-Anteil der Delayline

In vereinfachter Schreibweise kann man die Struktur so lesen:

```latex
\[
x_h[n]=x[n]+FB\,x_h[n-K]
\]

\[
y[n]=BL\,x[n]+FF\,x_h[n-D[n]].
\]
```

Die konkreten Werte entsprechen den in Block 6 gerenderten
Spektrogrammen und Momentan-Frequenzgängen:

| Effekt | \(BL\) | \(FF\) | \(FB\) | Delay | Depth | Modulation |
|---|---:|---:|---:|---:|---:|---|
| Vibrato | 0 | 1 | 0 | \(0\,\mathrm{ms}\) | \(0\dots3\,\mathrm{ms}\) | Sinus, hier \(5\,\mathrm{Hz}\) |
| Flanger | 0,7 | 0,7 | 0,7 | \(0\,\mathrm{ms}\) | \(0\dots2\,\mathrm{ms}\) | Sinus, hier \(1\,\mathrm{Hz}\) |
| Chorus | 0,7 | 0,7 | -0,7 | \(20\,\mathrm{ms}\) | \(6\,\mathrm{ms}\) | Lowpass-Noise |
| Doubler | 0,7 | 0,7 | 0 | \(100\,\mathrm{ms}\) | \(100\,\mathrm{ms}\) | Lowpass-Noise |

Vor den Effekt-Spektrogrammen werden zwei Referenzabbildungen gezeigt:
das Eingangssignal im Zeitbereich und sein Spektrum. Beide sind Schwarz, damit
klar bleibt: Das ist noch kein Effekt, sondern das Eingangsmaterial.
FIR- und IIR-Comb-Spektrogramme werden in Block 6 nicht erneut gezeigt, weil
die Kammfilterwirkung bereits in Block 5 behandelt wurde.

Als Einstieg in den Chorus wird vor der allgemeinen Multi-Effect-Struktur ein
einfaches Ersatzschaltbild gezeigt: ein Dry-Anteil plus zwei unabhängig
modulierte Delaylines. Das ist didaktisch näher an der Klangidee "mehrere
leicht gegeneinander verstimmte Kopien" und noch ohne Feedback:

```latex
\[
y[n]
=
l\,x[n]
+g_1\,x[n-M_1[n]]
+g_2\,x[n-M_2[n]].
\]
```

Für die Abbildung `02_simple_two_voice_chorus_spectrogram.png` werden
\(l=0{,}50\), \(g_1=g_2=0{,}35\),
\(M_1[n]=12\,\mathrm{ms}\pm2\,\mathrm{ms}\) und
\(M_2[n]=20\,\mathrm{ms}\pm3\,\mathrm{ms}\) verwendet. Beide Delayzeiten
werden mit zwei unabhängigen Lowpass-Noise-Signalen bewegt. Dadurch entsteht
keine periodische Sinusbewegung, sondern eine leicht verwaschene, zufällige
Tonhöhen- und Phasenbewegung. So sieht man zunächst die Grundidee des Chorus,
bevor mit Abb. 2.34 die allgemeinere DAFX-Struktur mit \(BL\), \(FF\), \(FB\)
und variablem Feedforward-Tap folgt.

Direkt danach werden die beiden Modulationsarten als Zeitsignal gezeigt:
`03a_modulation_sine.png` enthält die Sinusmodulation als durchgezogene
violette Kurve. `03b_modulation_sine_lowpass_noise.png` ergänzt die
Lowpass-Noise-Modulation als gestrichelte violette Kurve. Damit ist sichtbar,
warum Vibrato und Flanger periodisch wirken, während der Chorus eher eine
unregelmäßige, weich verrauschte Delaybewegung nutzt.

Beim Chorus wird also eine längere Delayzeit verwendet
\((D[n]\approx20\dots26\,\mathrm{ms})\), die durch tiefpassgefiltertes
Rauschen bewegt wird. Wichtig: Dieses Rauschen wird nicht als Audiosignal
addiert, sondern dient nur als langsame Steuerspannung beziehungsweise
Modulationsquelle für die Delayzeit. Dadurch erscheinen im Spektrogramm feste
Harmonische des trockenen Signals und weich, nicht periodisch bewegte Anteile
der Delaykopie.
In der Simulation wird dieselbe Lowpass-Noise-Logik wie im JSFX verwendet:
alle \(1/20\,\mathrm{s}\) wird ein neuer Zufallszielwert gewählt und anschließend
mit einem \(1\,\mathrm{Hz}\)-Einpolfilter geglättet.
Beim Flanger ist die Delayzeit deutlich kürzer
\((D[n]=0\dots2\,\mathrm{ms})\) und wird sinusförmig bewegt. Dadurch steht
weniger eine getrennte Tonhöhenlinie im Vordergrund, sondern stärker die
zeitlich wandernde Kammfilterwirkung.

Deshalb kann der Flanger zusätzlich wieder als Frequenzgang-Animation gezeigt
werden. Streng genommen ist auch der Flanger zeitvariant und besitzt keinen
einzigen festen LTI-Frequenzgang. Für die Lehre ist aber die eingefrorene
Momentaufnahme sehr nützlich. Dasselbe Prinzip wird für Chorus und Doubler
genutzt: Auch dort wird pro Frame die aktuelle Delayzeit eingefroren und als
Momentan-Frequenzgang dargestellt. Beim Vibrato wird das bewusst nicht gemacht,
weil dort die Tonhöhenbewegung die zentrale visuelle Aussage ist.

```latex
\[
H_\mathrm{DelayFX}(e^{j\Omega},n)
=
BL+
\frac{FF\,e^{-j\Omega D[n]}}
{1-FB\,e^{-j\Omega K}}.
\]
```

Dabei ist \(D[n]\) der variable Feedforward-Tap und
\(K=D_\mathrm{base}+0{,}5\,DEPTH\) der feste Feedback-Tap aus dem JSFX. Beim
Chorus ist \(FB=-0{,}7\). Das Minuszeichen bedeutet: Die Rückführung wird
invertiert und verändert damit die Lage der Resonanzen und Kerben gegenüber
positivem Feedback. Beim Doubler ist \(FB=0\), damit vereinfacht sich die
Darstellung zu:

```latex
\[
H(e^{j\Omega},n)
=
BL+FF\,e^{-j\Omega D[n]}.
\]
```

Wenn \(D[n]\) bewegt wird, wandern die Kammfilterkerben. Beim Flanger sind die
Kerben durch die kurze Delayzeit breit genug, um als klassische
Frequenzgang-Animation lesbar zu sein. Beim Chorus sind die Kerben dichter und
weicher zu interpretieren: Die Animation zeigt nur eine einzelne Voice, nicht
den vollen subjektiven Chorus-Eindruck. Beim Doubler sind die Kerben sehr
dicht; didaktisch zeigt die Animation vor allem, dass aus längeren
Delayzeiten eher eine zweite Stimme als ein klarer Filtereindruck entsteht.

Genau das unterscheidet diese Effekte vom Vibrato: Beim Vibrato steht die
Tonhöhenbewegung im Spektrogramm im Vordergrund, bei Flanger, Chorus und
Doubler die Interferenz zwischen Dry-Anteil und verzögerter Kopie. Als
Merksatz: Der Flanger ist ein zeitvariantes Kammfilter, der Phaser ein
zeitvariantes Kerbfilter durch bewegte Allpass-Phase und Dry/Wet-Interferenz.

Parameter:

- Rate
- Depth
- Grunddelay
- Interpolationsqualität

Die drei Momentan-Frequenzgänge werden mit getrennten Skripten gerendert:

- `export_block_06_flanger_frequency_response.py`
- `export_block_06_chorus_frequency_response.py`
- `export_block_06_doubler_frequency_response.py`

Alle drei Skripte verwenden dasselbe pixelgenaue Frequenzgang-Layout wie die
Phaser-Animation in Block 4.

### Flanger

Nach Zölzer 2011, Kap. 2.6.2 und Tabelle 2.9:

- kurze Delayzeit, in der Standardstruktur hier \(0\dots2\,\mathrm{ms}\)
- sinusförmige Modulation
- Dry + Wet mit \(BL=0{,}7\), \(FF=0{,}7\)
- Feedback mit \(FB=0{,}7\)

```latex
\[
y[n]=0{,}7x[n]+0{,}7x_h[n-D[n]].
\]
```

Klang:

- wandernde Kammfilterkerben
- metallisch
- Jet-/Sweep-Charakter

### Chorus

Typischer Bereich nach Zölzer 2011, Tabelle 2.9:

- etwa 1-30 ms Grunddelay
- in den Abbildungen \(D[n]\approx20\dots26\,\mathrm{ms}\)
- Lowpass-Noise statt Sinus-LFO, aber nur als Modulationsquelle für \(D[n]\)
- mehrere Stimmen oder Delay-Taps möglich
- \(BL=0{,}7\), \(FF=0{,}7\), \(FB=-0{,}7\)

Klang:

- breiter
- dichter
- leichte Verstimmung
- weniger metallisch als Flanger

### Doubler / Doubling

Nach Zölzer 2011, Tabelle 2.9:

- \(BL=0{,}7\), \(FF=0{,}7\), \(FB=0\)
- \(DELAY=100\,\mathrm{ms}\)
- \(DEPTH=100\,\mathrm{ms}\)
- \(MOD=\) Lowpass-Noise

Doubling liegt zwischen Chorus und hörbarer Wiederholung. Die Delayzeit ist
größer als beim Chorus; gleichzeitig wird der verzögerte Anteil weich und
nicht periodisch bewegt. Dadurch wirkt das Signal wie eine zweite,
nicht exakt synchrone Stimme.

### Slapback und Echo

Typische Bereiche nach Zölzer 2011, Kap. 2.6:

- Slapback: etwa 25-50 ms, keine Modulation
- Echo: größer als 50 ms, keine Modulation

Slapback:

- einzelne schnelle Reflexion
- Rockabilly-/Vocal-/Gitarrencharakter
- oft ohne Feedback oder mit wenig Feedback

Echo:

- wahrnehmbar getrennte Wiederholung
- Feedback erzeugt mehrere Wiederholungen
- Delayzeit wird rhythmisch/musikalisch relevant

### Vergleichstabelle

| Effekt | Delayzeit | Modulation | Dry-Anteil | Hauptwirkung |
|---|---:|---|---|---|
| Vibrato | kurz | ja | nein/gering | Tonhöhenbewegung |
| Flanger | 0-15 ms | sinusförmig | ja | wandernde Kammfilter |
| Chorus | 1-30 ms | Lowpass-Noise | ja | Breite, Verdopplung |
| Doubling | 10-100 ms | Lowpass-Noise | ja | zweite Stimme |
| Slapback | 25-50 ms | nein | ja | kurze einzelne Reflexion |
| Echo | >50 ms | nein | ja | erkennbare Wiederholung |

### Schriftliche Folien-Zusammenfassung

Delay-basierte Audioeffekte entstehen aus verzögerten Kopien des Signals. Die
entscheidenden Parameter sind Delayzeit, Modulation, Dry/Wet-Mix und Feedback.
Schon kleine Änderungen dieser Parameter führen zu sehr unterschiedlichen
Effekten.

Vibrato entsteht durch eine zeitlich veränderte Delayzeit. Wenn die Delayzeit
wächst oder schrumpft, wird das Signal lokal gedehnt oder gestaucht. Dadurch
entsteht eine Tonhöhenbewegung. Beim Vibrato steht normalerweise nicht die
Mischung aus trockenem und verzögertem Signal im Vordergrund, sondern die
bewegte Delayline selbst.

Beim Flanger wird eine sehr kurze, modulierte Delayline mit dem trockenen
Signal gemischt. Dadurch entstehen Kammfilter, deren Kerben sich bewegen. Das
klingt metallisch und schwebend. Chorus nutzt längere Delayzeiten und weichere
oder leicht zufällige Modulation. Dadurch entsteht eher Breite,
Verdopplung und Ensemble-Eindruck. Slapback und Echo nutzen feste Delayzeiten:
Slapback ist eine kurze, einzelne Reflexion, Echo ist eine deutlich hörbare
Wiederholung. Feedback erzeugt mehrere Wiederholungen und verlängert den
Nachklang.

## Optionaler Nachtrag: Fractional Delay Lines

### Bezug auf Zölzer 2011, Kap. 2.5.4

Dieser Abschnitt war ursprünglich als eigener Block 7 geplant, wurde in der
gehaltenen Vorlesung 9 aber nicht benötigt. Er bleibt als Reservematerial für
eine spätere Vertiefung oder für ein ergänzendes Skript erhalten.

Bis hier wurden Delayzeiten oft so geschrieben, als könne man einfach auf
\(x[n-M]\) zugreifen. Das funktioniert direkt nur, wenn \(M\) eine ganze Zahl
ist. Bei zeitvarianten Delay-Effekten ist die Delayzeit aber meistens nicht
genau ganzzahlig. Ein LFO liefert zum Beispiel nicht nur \(M=120\) oder
\(M=121\), sondern Werte dazwischen.

Zölzer beschreibt deshalb eine Verzögerung aus einem ganzzahligen Anteil und
einem fractional Anteil:

```latex
\[
D = M+\mathrm{frac},
\qquad 0 \leq \mathrm{frac} \leq 1.
\]
```

Die gewünschte Verzögerung ist dann formal:

```latex
\[
y[n]=x\!\left(n-\left[M+\mathrm{frac}\right]\right).
\]
```

Didaktisch wichtig:

> Der Ausdruck bedeutet nicht, dass ein diskretes Signal plötzlich echte
> Zwischen-Samples besitzt. Er bedeutet: Wir schätzen den Signalwert zwischen
> zwei gespeicherten Samples der Delayline.

### Lineare Interpolation als einfachstes Modell

Die Delayline enthält echte Samples bei ganzzahligen Positionen. Für eine
Verzögerung zwischen \(M\) und \(M+1\) Samples wird der Ausgabewert zwischen
den beiden benachbarten Delayline-Samples gebildet:

```latex
\[
y[n]
=(1-\mathrm{frac})\,x[n-M]
+\mathrm{frac}\,x[n-(M+1)].
\]
```

Interpretation:

- \(\mathrm{frac}=0\): exakt \(M\) Samples Delay
- \(\mathrm{frac}=1\): exakt \(M+1\) Samples Delay
- \(\mathrm{frac}=0{,}5\): Mittelwert zwischen beiden Samples

Damit wird aus einem stufigen Delayparameter ein kontinuierlich bewegbarer
Delayparameter. Das ist die technische Voraussetzung für Vibrato, Flanger und
Chorus, weil deren Delayzeit während des Signals langsam bewegt wird.

### Interpolationsverfahren nach Zölzer

Zölzer nennt für Audioanwendungen mehrere Möglichkeiten:

| Verfahren | Idee | Didaktische Rolle |
|---|---|---|
| Lineare Interpolation | Wert zwischen zwei Samples gewichten | einfachste und anschaulichste Variante |
| Allpass-Interpolation | Verzögerung mit möglichst konstantem Betrag approximieren | wichtig, wenn Amplitudenfehler klein bleiben sollen |
| Sinc-Interpolation | ideale Bandbegrenzung annähern | theoretisch hochwertig, rechenaufwendiger |
| Spline-Interpolation | glattere Kurve aus mehreren Nachbarsamples | höherwertige praktische Interpolation |
| Fractionally addressed delay lines | Delayline anders adressieren | Implementationsvariante |

Für diese Vorlesung reicht die lineare Interpolation als Grundmodell. Die
anderen Verfahren werden nur genannt, damit klar ist: Fractional Delay ist ein
eigenes Designproblem, wenn hohe Audioqualität oder starke Modulation gefordert
ist.

### Lehrenden-Notiz

Dieser Block sollte nicht als neuer Filterdesign-Block wirken. Er beantwortet
eine konkrete Frage aus Block 6:

> Wie kann eine Delayline eine Verzögerung von zum Beispiel \(120{,}37\)
> Samples erzeugen?

Die Antwort lautet: Speicherzugriff auf die benachbarten Samples plus
Interpolation. Damit kann anschließend die Standardstruktur aus Zölzer,
Abb. 2.34, sauber gelesen werden, weil dort explizit ein ganzzahliger
Delayanteil und ein fractional Anteil vorkommen.

### Schriftliche Folien-Zusammenfassung

Eine normale digitale Delayline speichert Samples an ganzzahligen Positionen.
Ein Zugriff wie \(x[n-M]\) ist deshalb direkt möglich, wenn \(M\) eine ganze
Zahl ist. Viele Delay-Effekte benötigen aber zeitveränderliche Delayzeiten.
Beim Vibrato, Flanger oder Chorus bewegt ein LFO die Delayzeit kontinuierlich.
Dadurch entstehen Werte wie \(M=120{,}37\) Samples. Ein solcher Zugriff liegt
zwischen zwei gespeicherten Samples.

Eine Fractional Delay Line zerlegt die Verzögerung deshalb in einen
ganzzahligen Anteil \(M\) und einen Anteil \(\mathrm{frac}\) zwischen 0 und 1:

```latex
\[
D=M+\mathrm{frac}.
\]
```

Der fehlende Zwischenwert wird durch Interpolation geschätzt. Bei linearer
Interpolation werden die beiden benachbarten Samples gewichtet:

```latex
\[
y[n]
=(1-\mathrm{frac})\,x[n-M]
+\mathrm{frac}\,x[n-(M+1)].
\]
```

Für \(\mathrm{frac}=0\) erhält man exakt das Sample bei \(M\). Für
\(\mathrm{frac}=1\) erhält man exakt das Sample bei \(M+1\). Dazwischen wird
ein gewichteter Zwischenwert gebildet. Damit kann eine Delayzeit glatt bewegt
werden, ohne dass sie nur in ganzen Samples springt. Zölzer nennt neben der
linearen Interpolation auch Allpass-, Sinc- und Spline-Interpolation. Diese
Verfahren unterscheiden sich in Rechenaufwand und Klangqualität.

## Optionaler Nachtrag: Standardstruktur für variable Delay-FX

### Bezug auf Zölzer 2011, Abb. 2.34

Dieser Abschnitt war ursprünglich als eigener Block 8 geplant, wurde in der
gehaltenen Vorlesung 9 aber nicht benötigt. Die Standardstruktur bleibt im
Delay-FX-Block als internes Modell und kann später als vertiefender Abschluss
nachgereicht werden.

Abb. 2.34 zeigt eine Standardstruktur für Effekte mit variabler Delayline.
Die zentrale Idee:

- ein Eingangssignal \(x[n]\)
- ein interner Delayline-Zustand \(x_h[n]\)
- eine variable Feedforward-Delayline \(z^{-[M(n)+\mathrm{frac}(n)]}\)
- ein Feedback-Tap
- Koeffizienten für Blend, Feedforward und Feedback
- ein Modulationssignal \(\mathrm{MOD}(n)\), das die Delaylänge bewegt

### Didaktische Lesart der Parameter

| Parameter | Rolle |
|---|---|
| BL | trockener beziehungsweise direkter Anteil |
| FF | Anteil des variabel verzögerten Signals |
| FB | Rückkopplung aus der Delayline |
| \(M[n]\) | zeitveränderliche Delayzeit |
| \(\mathrm{frac}[n]\) | fractional-delay-Anteil |
| MOD[n] | LFO oder Steuersignal |

### Warum ist diese Abbildung der Abschluss?

Die Abbildung verbindet fast alle Effekte des Blocks:

- Vibrato: vor allem variable Delayline, kaum Dry-Anteil.
- Flanger: Dry + kurze modulierte Delayline, oft Feedback.
- Chorus: Dry + mehrere oder weich modulierte Delayanteile.
- Slapback: Dry + feste kurze Delayline.
- Echo: Dry + längere Delayline, ggf. Feedback.

Merksatz:

> Viele Delay-FX unterscheiden sich nicht durch eine völlig neue Struktur,
> sondern durch Delayzeit, Modulation, Mix und Feedback.

### Lehrenden-Notiz

Die Abbildung sollte nicht als komplizierte Schaltung gelesen werden, sondern
als Parameterlandkarte. Die Studierenden sollen sehen:

1. Wo kommt das trockene Signal her?
2. Wo entsteht die verzögerte Kopie?
3. Wo wird die Delayzeit verändert?
4. Wo entsteht Feedback?
5. Welche Parameter machen daraus Vibrato, Flanger, Chorus, Slapback oder Echo?

### Schriftliche Folien-Zusammenfassung

Die Standardstruktur für variable Delay-Effekte zeigt, dass viele bekannte
Effekte nicht aus völlig verschiedenen Schaltungen bestehen. Sie nutzen eine
gemeinsame Grundidee: ein Eingangssignal, eine Delayline, einen direkten Anteil,
einen verzögerten Anteil, optional Feedback und ein Modulationssignal für die
Delayzeit.

Der direkte Anteil wird oft als Dry- oder Blend-Anteil beschrieben. Der
Feedforward-Pfad mischt eine verzögerte Kopie zum Signal. Der Feedback-Pfad
führt einen Teil des verzögerten Signals wieder in die Delayline zurück. Das
Modulationssignal \(\mathrm{MOD}[n]\) bewegt die Delayzeit \(M[n]\). Wenn die
Delayzeit nicht ganzzahlig ist, wird ein fractional-delay-Anteil benötigt.

Mit derselben Struktur lassen sich unterschiedliche Effekte einstellen.
Vibrato nutzt vor allem die bewegte Delayline. Flanger nutzt kurze Delayzeiten,
Dry/Wet-Mischung und oft Feedback. Chorus nutzt etwas längere, weich bewegte
Delayanteile. Slapback und Echo nutzen feste Delayzeiten; beim Echo ist die
Wiederholung deutlich getrennt wahrnehmbar. Die zentrale Erkenntnis ist:
Delayzeit, Modulation, Mix und Feedback entscheiden, welcher Effekt aus der
Struktur entsteht.

## Zusammenfassende Kernbotschaften

1. Filter formen Spektren. Delaystrukturen erzeugen Interferenz und
   Wiederholungen.
2. Ein EQ-Plugin ist ein Interface für Biquad-Koeffizienten.
3. Ein Allpass kann hörbar relevant sein, obwohl sein Betrag konstant bleibt.
4. Wah-Wah und Phaser entstehen durch bewegte Filter- oder Allpassparameter.
5. Ein FIR-Comb entsteht durch direkte plus verzögerte Kopie.
6. Ein IIR-Comb entsteht durch Feedback in der Delayline.
7. Zeitvariation entsteht, wenn Parameter wie Gain, Cutoff oder Delayzeit
   langsam bewegt werden.
8. Variable Delayzeiten benötigen in der Implementierung Interpolation; in
   Vorlesung 9 bleibt das ein Hinweis im Delay-FX-Block.
9. Delay-FX lassen sich über Delayzeit, Modulation, Mix und Feedback
   systematisch unterscheiden.

## Mögliche Hörbeispiele

Falls Audio-Beispiele vorbereitet werden:

- trockene Gitarre oder Synth für Filter, Wah-Wah, Phaser, Flanger, Chorus
- trockene Stimme für Hochpass, Peak-EQ, Slapback und Echo
- kurzer perkussiver Sound für Comb-Filter und Feedback-Delay

Wichtig: Erst trockenes Signal, dann Effekt mit moderaten Parametern, dann
übertriebene Parameter. So werden die Mechanismen hörbar.

## Mögliche kurze Aufgaben

1. Phasenverschiebung und Kammfilter im In-Ear-Monitoring: Wann entstehen
   Verstärkung und Auslöschung durch zwei Signalpfade?
2. Feedforward-Delay oder Feedback-Delay: Welche Struktur passt zu einem
   kurzen räumlichen Snare-Effekt, und welche Risiken bringt Feedback?
3. Warum ist der Allpass allein noch kein Phaser?
4. Vibrato, Flanger, Chorus oder Doubler: Welcher Effekt passt zu welchen
   Delayzeiten, Modulationsformen, Dry-Anteilen und Feedbackwerten?

## Literaturanker

- Zölzer 2011, Kap. 2.2: Basic filters
- Zölzer 2011, Kap. 2.3: Equalizers
- Zölzer 2011, Kap. 2.4: Time-varying filters
- Zölzer 2011, Kap. 2.5: Basic delay structures
- Zölzer 2011, Kap. 2.6: Delay-based audio effects
- Zölzer 2011, Kap. 2.5.4 und Abb. 2.34: Reserve- und Implementationskontext,
  nicht als eigener Folienblock durchgeführt

## Abgrenzung zu den folgenden Vorlesungen

Vorlesung 10:

- Ringmodulator
- Amplitudenmodulator
- Single-Side-Band-Modulator
- Frequenz- und Phasenmodulator
- Demodulatoren, Detektoren und Anwendungen

Vorlesung 11:

- Dynamikprozessoren
- Limiter, Compressor, Expander, Gate, De-Esser
- Saturation, Distortion, Overdrive, Fuzz
- Exciter und Enhancer

Diese Abgrenzung verhindert, dass Vorlesung 9 zu breit wird. Die 9. Vorlesung
bleibt bei Filtern und Delaylines.
