# Lehrkonzept Vorlesung 7: Vom IIR im Zeitbereich zum Biquad

## Didaktische Entscheidung

Vorlesung 7 bleibt bewusst im Zeitbereich und im Frequenzgang

$$
H(e^{j\Omega}).
$$

Die z-Transformation, die z-Ebene sowie Pole und Nullstellen werden nicht mehr
in Vorlesung 7 eingefuehrt, sondern in Vorlesung 8.

Der neue Ablauf:

1. FIR und Impulsantwort aus Vorlesung 6 reaktivieren.
2. Reines IIR im Zeitbereich verstehen.
3. Frequenzgang aus der Impulsantwort herleiten.
4. Das einpolige IIR als bekannte Uebertragungsfunktion zeigen.
5. Mehrere Feedback-Taps `a_r` als rein rekursives IIR vorstellen.
6. Grenzen reiner Rueckfuehrung zeigen.
7. Feedforward und Feedback kombinieren.
8. Das Biquad als praktische Standardform vorstellen.
9. Damit typische Audiofilter motivieren.
10. z-Transformation, Pole und Nullstellen als Thema fuer Vorlesung 8 ankuendigen.

Leitgedanke:

> In Vorlesung 7 sehen die Studierenden, welche Kurven durch Impulsantwort,
> Feedforward und Feedback entstehen. In Vorlesung 8 bekommen diese Kurven ihre
> geometrische Erklaerung in der z-Ebene.

## Notation: `p`, `a_r` und `b_k`

Im Einstieg bleibt `p` sinnvoll:

$$
y[n]=b_0x[n]+p\,y[n-1]
$$

`p` ist anschaulich der direkte Rueckfuehrungsfaktor.

In der allgemeinen Standardform werden Feedforward- und Feedback-Indizes
getrennt:

- `b_k` gewichtet Eingangskopien und laeuft ueber `k=0...N-1`.
- `a_r` gewichtet Ausgangskopien und laeuft ueber `r=1...M`.

$$
y[n]
=
\sum_{k=0}^{N-1}b_kx[n-k]
-
\sum_{r=1}^{M}a_r y[n-r]
$$

Fuer den einpoligen Fall:

$$
y[n]=b_0x[n]-a_1y[n-1]
$$

Vergleich mit:

$$
y[n]=b_0x[n]+p\,y[n-1]
$$

ergibt:

$$
p=-a_1.
$$

Das sollte beim Uebergang explizit gesagt werden.

## Lernziele fuer Studierende

Nach der Sitzung sollen Studierende sagen koennen:

- Ein FIR nutzt gespeicherte Eingangswerte.
- Ein IIR nutzt zusaetzlich gespeicherte Ausgangswerte.
- Rueckfuehrung erzeugt eine theoretisch unendliche Impulsantwort.
- Der Frequenzgang eines LTI-Systems ist die frequenzabhaengige Wirkung der Impulsantwort.
- Ein einpoliges IIR hat den Frequenzgang

$$
H(e^{j\Omega})
=
\frac{b_0}{1-p e^{-j\Omega}}.
$$

- Mehrere Feedback-Taps `a_r` erzeugen komplexere rein rekursive Kurven.
- Reine Rueckfuehrung kann resonieren, aber keine gezielte Ausloeschung durch Eingangskopien erzeugen.
- Feedforward und Feedback zusammen fuehren zu

$$
H(e^{j\Omega})
=
\frac{
\sum_{k=0}^{N-1}b_k e^{-jk\Omega}
}{
1+\sum_{r=1}^{M}a_r e^{-jr\Omega}
}.
$$

- Biquads sind die praktische Grundform fuer viele Audiofilter.
- Tiefpass, Hochpass, Bandpass, Notch, Low-Shelf, High-Shelf und Peaking-EQ koennen mit Biquads realisiert werden.

## Gesamtstruktur fuer 120 Minuten

| Zeit | Block | Inhalt | Studierenden-Botschaft |
|---|---|---|---|
| 0-8 min | Einstieg | Rueckgriff FIR, Impulsantwort, Frequenzgang | Wir kennen Filter als Impulsantwort und Frequenzgang. |
| 8-30 min | 1 | Stabilitaet und reines IIR im Zeitbereich | Rueckfuehrung klingt ab, bleibt stehen oder waechst. |
| 30-45 min | 2 | Einpoliges IIR im Frequenzbereich | Aus der unendlichen Impulsantwort entsteht ein einfacher Frequenzgang. |
| 45-60 min | 3 | Mehrere Feedback-Taps `a_r` | Mehr Rueckfuehrung erzeugt mehr Kurvenform und Resonanz. |
| 60-70 min | 4 | Verschobene Impulsantwort im Frequenzgang | Verzoegerung erzeugt Phasenfaktoren. |
| 70-75 min | Pause | kurze Unterbrechung | Entlastung |
| 75-82 min | 5 | Feedforward-Dirac-Baustein | Eine Eingangskopie wird zum FIR-Phasenfaktor. |
| 82-92 min | 6 | Grenze reiner Rueckfuehrung | Fuer echte Ausloeschung braucht man Eingangskopien. |
| 92-105 min | 7 | Feedforward plus Feedback | Zaehler formt und loescht aus, Nenner speichert und resoniert. |
| 105-114 min | 8 | Biquad | Die allgemeine Gleichung wird zur praktischen Standardform. |
| 114-118 min | 9 | Audiotypische Filterkurven | LP, HP, Notch, BP, Shelves und Peaking-EQ werden als realisierbare Biquad-Kurven verstaendlich. |
| 118-120 min | Ausblick | Vorlesung 8 | z-Transformation, Pole und Nullstellen erklaeren das Design geometrisch. |

## Block 0: Rueckgriff auf Vorlesung 6

Startpunkt FIR:

$$
y[n]=\sum_{k=0}^{N-1}b_kx[n-k]
$$

Lesart:

- `x[n]` ist der aktuelle Eingang.
- `x[n-1]`, `x[n-2]`, ... sind gespeicherte Eingangswerte.
- Die `b_k` sind Gewichte fuer diese Eingangskopien.
- Die Impulsantwort ist endlich.

Frequenzgang aus der Impulsantwort:

$$
H(e^{j\Omega})
=
\sum_n h[n]e^{-j\Omega n}
$$

Didaktische Sprache:

> Der Frequenzgang sagt: Was macht das System mit einer Schwingung dieser
> Frequenz?

## Block 1: Reines IIR im Zeitbereich

Ziel:

> Rueckfuehrung als Erinnerung verstehen.

Einfacher Fall:

$$
y[n]=b_0x[n]+p\,y[n-1]
$$

Mit Dirac-Impuls:

$$
x[n]=\delta[n]
$$

folgt:

$$
h[0]=b_0
$$

$$
h[1]=b_0p
$$

$$
h[2]=b_0p^2
$$

Allgemein:

$$
h[n]=b_0p^n
\qquad n\ge 0
$$

Stabilitaetslogik:

- `|p|<1`: die Impulsantwort klingt ab.
- `|p|=1`: die Impulsantwort klingt nicht ab und ist nicht BIBO-stabil.
- `|p|>1`: die Impulsantwort waechst.

Aktive Storyboards:

- `png_storyboards/01_iir/01A_dirac_impuls`
- `png_storyboards/01_iir/01B_stabil_impulsantwort`
- `png_storyboards/01_iir/01C_grenzstabil_impulsantwort`
- `png_storyboards/01_iir/01D_instabil_impulsantwort`
- `png_storyboards/01_iir/01E_iir_p_plus_05`
- `png_storyboards/01_iir/01F_iir_p_minus_05`

## Block 2: Einpoliges IIR im Frequenzbereich

Jetzt wird der Frequenzgang aus der Impulsantwort motiviert.

Bekannt:

$$
h[n]=b_0p^n
\qquad n\ge 0
$$

Einsetzen:

$$
H(e^{j\Omega})
=
\sum_{n=0}^{\infty}b_0p^n e^{-j\Omega n}
$$

Umformen:

$$
H(e^{j\Omega})
=
b_0
\sum_{n=0}^{\infty}
\left(p e^{-j\Omega}\right)^n
$$

Geometrische Reihe:

$$
\sum_{n=0}^{\infty}q^n
=
\frac{1}{1-q}
$$

mit

$$
q=p e^{-j\Omega}.
$$

Also:

$$
H(e^{j\Omega})
=
\frac{b_0}{1-p e^{-j\Omega}}
$$

Betrag:

$$
\left|H(e^{j\Omega})\right|
=
\frac{|b_0|}
{\sqrt{1-2p\cos(\Omega)+p^2}}
$$

Interpretation:

- `p>0`: tieffrequente Anteile werden staerker gehalten.
- `p<0`: schnelle Vorzeichenwechsel werden staerker gehalten.
- `b_0` verschiebt die Kurve als Gain-Faktor.

Aktive Storyboards:

- `png_storyboards/02_frequenzgang_iir/02A_geometric_series`
- `png_storyboards/02_frequenzgang_iir/02B_iir_magnitude_examples`

## Block 3: Reines rekursives IIR mit mehreren Feedback-Taps

Jetzt wird das einpolige Beispiel erweitert:

$$
y[n]
=
b_0x[n]
-
\sum_{r=1}^{M}a_r y[n-r]
$$

Impulseingang:

$$
x[n]=\delta[n]
$$

Impulsantwort-Rekursion:

$$
h[n]
=
b_0\delta[n]
-
\sum_{r=1}^{M}a_r h[n-r]
$$

Frequenzgang ueber die Impulsantwort:

$$
H(e^{j\Omega})
=
\frac{b_0}
{1+\sum_{r=1}^{M}a_r e^{-jr\Omega}}
$$

Ausgeschrieben:

$$
H(e^{j\Omega})
=
\frac{b_0}
{1+a_1e^{-j\Omega}+a_2e^{-j2\Omega}+\ldots+a_Me^{-jM\Omega}}
$$

Didaktische Botschaft:

> Mehr Feedback-Taps machen den Nenner komplexer. Dadurch entstehen glattere,
> resonantere und komplexere Verlaeufe. Aber der Zaehler ist weiterhin nur
> `b_0`.

Aktives Storyboard:

- `png_storyboards/03_rekursives_iir_mehrere_taps/03A_recursive_iir_frequency_examples`
- `png_storyboards/03_rekursives_iir_mehrere_taps/03B_impulse_response_build`
- `png_storyboards/03_rekursives_iir_mehrere_taps/03C_ir_superposition`

Die Serie 3A zeigt:

- `M=2 Low-frequency emphasis`
- `M=2 High-frequency emphasis`
- `M=2 Mid resonance`
- `M=4 Two broad resonances`
- `M=6 Three resonances`
- `M=8 Complex recursive curve`

Die Log/dB-Plots in 3A verwenden denselben dB-Ausschnitt wie Block 2. Zu
jedem Beispiel gibt es zusaetzlich eine lineare Darstellung ueber die normierte
Kreisfrequenz `Omega/pi` mit linearer Magnitude. Beide Darstellungsarten werden
mit identischem Canvas und identischer Achsenposition exportiert, damit die
Bildserie beim Durchschalten pixelgenau stehen bleibt.

Die Serie 3B zeigt die Impulsantwort eines rekursiven IIR mit `M=4` als
Bildfolge. Fuer `n=0` wird der direkte Startwert `h[0]=b_0` gezeigt. Danach
werden `h[1]` bis `h[7]` aus farbigen gewichteten Kopien der bereits
berechneten Samples aufgebaut. Der entstehende Summenwert bekommt im Aufbau
direkt seine dauerhaft gehaltene Sample-Farbe; nur das Abschlussbild zeigt die
komplette Impulsantwort gruen. Das Beispiel ist so gewaehlt, dass positive und
negative `h[n]` auftreten; die Amplitudenachse bleibt in allen Bildern
symmetrisch um 0.

Die Serie 3C zeigt dieselbe Impulsantwort als Ueberlagerung von
`b_0 delta[n]` und den gewichteten, zeitlich verschobenen Kopien
`-a_r h[n-r]`. Die bereits eingefuehrten Kopien bleiben in der Bildfolge
stehen. Am Ende werden alle Kopien weiterhin sichtbar gezeigt und pro Sample
als gruene resultierende Impulsantwort aufsummiert. Dadurch wird der Uebergang
zu Block 4 vorbereitet: Eine zeitliche Verschiebung der Impulsantwort wird im
Frequenzbereich zu einem Phasenfaktor.

## Block 4: Verschobene Impulsantwort im Frequenzgang

Aktives Storyboard:

- `png_storyboards/04_verschobene_impulsantwort/04A_shifted_ir_frequency_response`
- `png_storyboards/04_verschobene_impulsantwort/04B_weighted_shifted_spectra`

Ziel dieses Blocks ist der Sprung

$$
\sum_n h[n-r]e^{-j\Omega n}
=
e^{-jr\Omega}H(e^{j\Omega})
$$

bildlich zu machen.

Wir betrachten dazu die verschobene Kopie der Impulsantwort

$$
g_r[n]=h[n-r].
$$

Ihr Frequenzgang ist

$$
G_r(e^{j\Omega})
=
\sum_n h[n-r]e^{-j\Omega n}.
$$

Mit der DFT- beziehungsweise Frequenzgang-Regel fuer eine zeitliche
Verschiebung folgt:

$$
G_r(e^{j\Omega})
=
e^{-jr\Omega}H(e^{j\Omega}).
$$

Daraus ergeben sich direkt zwei Aussagen:

$$
|G_r(e^{j\Omega})|
=
|H(e^{j\Omega})|
$$

und

$$
\angle G_r(e^{j\Omega})
=
\angle H(e^{j\Omega})-r\Omega.
$$

Die Bildserie zeigt `r=0` bis `r=4`. Pro `r` gibt es die aktuelle
verschobene Impulsantwort im Zeitbereich, den Betragsfrequenzgang und die
Phase. Der Betrag wird pro `r` als eigenes Bild gezeigt, obwohl die Kurve fuer
alle Verschiebungen identisch bleibt; der Titel zeigt den aktuellen Index. In
der Phasendarstellung laufen bereits gezeigte `r`-Werte grau mit. Dadurch wird
sichtbar:

- die Impulsantwort wandert im Zeitbereich nach rechts,
- alle verschobenen Kopien haben denselben Betrag,
- jede weitere Sample-Verzoegerung erzeugt eine zusaetzliche lineare
  Phasenneigung,
- feste Graustufen und eine Legende machen die gezeigten `r`-Werte zuordenbar,
- genau dieser Faktor erklaert spaeter die Terme
  \(e^{-jr\Omega}\) im Nenner.

Didaktischer Merksatz:

> Verschieben im Zeitbereich heisst: Betrag bleibt, Phase kippt.

Im zweiten Teil des Blocks wird diese Regel in die IIR-Herleitung eingesetzt.
Die verschobenen Spektren werden mit den Feedback-Koeffizienten gewichtet:

$$
a_r e^{-jr\Omega}H(e^{j\Omega}).
$$

Fuer das `M=4`-Beispiel entstehen vier Terme:

$$
a_1e^{-j\Omega}H(e^{j\Omega}),\quad
a_2e^{-j2\Omega}H(e^{j\Omega}),\quad
a_3e^{-j3\Omega}H(e^{j\Omega}),\quad
a_4e^{-j4\Omega}H(e^{j\Omega}).
$$

Die Bildserie 4B zeigt zuerst alle vier gewichteten Terme gemeinsam als Betrag
und danach gemeinsam als Phase. Feste Graustufen und Legenden ordnen die Kurven
den jeweiligen `r`-Werten zu. Negative Koeffizienten erzeugen zusaetzlich zur
Verzoegerungsphase eine Phasendrehung um \(\pi\). Zum Schluss wird die komplexe
Summe gezeigt. In den Summenbildern bleiben die vier gewichteten Einzelterme
grau sichtbar, damit die Summe direkt mit ihren Anteilen verglichen werden kann:

$$
S_a(e^{j\Omega})
=
\sum_{r=1}^{4}
a_r e^{-jr\Omega}H(e^{j\Omega}).
$$

Diese Summe ist der Rueckfuehrungsanteil, der in

$$
H(e^{j\Omega}) = b_0 - S_a(e^{j\Omega})
$$

auftritt. Didaktisch wichtig: Die Addition findet komplex statt. Man addiert
also nicht nur die Betraege, sondern Real- und Imaginaerteile der Spektren.

## Block 5: Feedforward-Dirac-Baustein

Aktives Storyboard:

- `png_storyboards/05_feedforward_dirac_baustein/05A_shifted_dirac_fir_term`

Ziel dieses Blocks ist der zweite Baustein der allgemeinen Herleitung:

$$
\sum_n \delta[n-k]e^{-j\Omega n}
=
e^{-jk\Omega}.
$$

Die Bildserie zeigt:

- die komplexe Testschwingung \(e^{-j\Omega n}\) als Samples auf dem Einheitskreis,
- die verschobene Dirac-Kopie \(\delta[n-k]\) fuer `k=0` bis `k=6`,
- dass \(\delta[n-k]\) nur bei \(n=k\) ungleich null ist,
- dass deshalb aus der Summe nur der Wert \(e^{-j\Omega n}\) bei \(n=k\) uebrig bleibt,
- dass dieser Wert genau \(e^{-jk\Omega}\) ist.

Didaktischer Merksatz:

> Eine verschobene Eingangskopie wird im Frequenzbereich zu einem
> FIR-Phasenfaktor.

## Block 6: Grenze reiner Rueckfuehrung

Die Grenze:

> Reine Rueckfuehrung kann Frequenzen bevorzugen oder abschwaechen, aber sie
> erzeugt keine gezielte Ausloeschung durch Eingangskopien.

Hochpass-Idee:

Ein echtes Entfernen von DC braucht:

$$
y[n]=x[n]-x[n-1]
$$

Denn fuer

$$
x[n]=C
$$

gilt:

$$
y[n]=C-C=0.
$$

Das ist Feedforward:

$$
b_0x[n]+b_1x[n-1]
$$

mit:

$$
b_0=1,\qquad b_1=-1.
$$

Didaktische Sprache:

> Ausloeschung entsteht durch Vergleich von Eingangskopien. Resonanz entsteht
> durch Rueckfuehrung.

## Block 7: Feedforward plus Feedback

Jetzt werden beide Strukturen kombiniert:

$$
y[n]
=
\sum_{k=0}^{N-1}b_kx[n-k]
-
\sum_{r=1}^{M}a_r y[n-r]
$$

Didaktischer Herleitungsweg:

Man kann an dieser Stelle sagen:

> Wir kennen bereits zwei Bausteine.

Der erste Baustein ist die verschobene Impulsantwort. Aus Block 4 ist bekannt:
Eine Verzoegerung um `r` Samples veraendert den Betrag nicht, sondern erzeugt
im Frequenzbereich nur einen Phasenfaktor:

$$
\sum_n h[n-r]e^{-j\Omega n}
=
e^{-jr\Omega}H(e^{j\Omega}).
$$

Dieser Term gehoert zum Feedback-Zweig, weil dort verschobene Ausgangs- bzw.
Impulsantwortwerte `h[n-r]` auftreten.

Der zweite Baustein ist die verschobene Dirac-Impuls-Kopie. Sie ist der
Feedforward-Baustein und entspricht genau dem FIR-Term aus Vorlesung 6:

$$
\sum_n \delta[n-k]e^{-j\Omega n}
=
e^{-jk\Omega}.
$$

Der Grund ist einfach: \(\delta[n-k]\) ist nur bei \(n=k\) ungleich null.
Deshalb bleibt in der Summe nur der Wert der komplexen Testschwingung bei
diesem Sample stehen:

$$
e^{-j\Omega n}\big|_{n=k}
=
e^{-jk\Omega}.
$$

Damit kann die allgemeine Herleitung sehr kurz, aber nachvollziehbar erfolgen.
Fuer einen Impulseingang gilt:

$$
x[n]=\delta[n],
\qquad
y[n]=h[n].
$$

Aus der Differenzengleichung wird die Impulsantwort-Rekursion:

$$
h[n]
=
\sum_{k=0}^{N-1}b_k\delta[n-k]
-
\sum_{r=1}^{M}a_r h[n-r].
$$

Jetzt wird auf beiden Seiten der Frequenzgang gebildet:

$$
H(e^{j\Omega})
=
\sum_n h[n]e^{-j\Omega n}.
$$

Die Impulsantwort-Rekursion wird eingesetzt:

$$
H(e^{j\Omega})
=
\sum_n
\left(
\sum_{k=0}^{N-1}b_k\delta[n-k]
-
\sum_{r=1}^{M}a_r h[n-r]
\right)
e^{-j\Omega n}.
$$

Nun wird die Summe in Feedforward- und Feedback-Anteil getrennt:

$$
H(e^{j\Omega})
=
\sum_n
\sum_{k=0}^{N-1}b_k\delta[n-k]e^{-j\Omega n}
-
\sum_n
\sum_{r=1}^{M}a_r h[n-r]e^{-j\Omega n}.
$$

Da `b_k` und `a_r` nicht vom Summationsindex `n` abhaengen, koennen sie vor die
jeweilige innere Summe gezogen werden:

$$
H(e^{j\Omega})
=
\sum_{k=0}^{N-1}b_k
\sum_n \delta[n-k]e^{-j\Omega n}
-
\sum_{r=1}^{M}a_r
\sum_n h[n-r]e^{-j\Omega n}.
$$

Jetzt werden die beiden bekannten Bausteine eingesetzt:

$$
\sum_n \delta[n-k]e^{-j\Omega n}
=
e^{-jk\Omega}
$$

und

$$
\sum_n h[n-r]e^{-j\Omega n}
=
e^{-jr\Omega}H(e^{j\Omega}).
$$

Damit folgt zunaechst:

$$
H(e^{j\Omega})
=
\sum_{k=0}^{N-1}b_k e^{-jk\Omega}
-
\sum_{r=1}^{M}a_r e^{-jr\Omega}H(e^{j\Omega}).
$$

Das ist der didaktisch wichtige Zwischenschritt:

- der erste Term ist der FIR- beziehungsweise Feedforward-Anteil,
- der zweite Term ist der bekannte Feedback-Anteil mit verschobener
  Impulsantwort,
- das \(H(e^{j\Omega})\) steht noch auf beiden Seiten, weil das System
  rekursiv ist.

Jetzt werden alle Terme mit \(H(e^{j\Omega})\) auf die linke Seite gebracht:

$$
H(e^{j\Omega})
+
\sum_{r=1}^{M}a_r e^{-jr\Omega}H(e^{j\Omega})
=
\sum_{k=0}^{N-1}b_k e^{-jk\Omega}.
$$

Dann wird \(H(e^{j\Omega})\) ausgeklammert:

$$
H(e^{j\Omega})
\left(
1+\sum_{r=1}^{M}a_r e^{-jr\Omega}
\right)
=
\sum_{k=0}^{N-1}b_k e^{-jk\Omega}.
$$

Und damit:

$$
H(e^{j\Omega})
=
\frac{
\sum_{k=0}^{N-1}b_k e^{-jk\Omega}
}{
1+\sum_{r=1}^{M}a_r e^{-jr\Omega}
}
$$

Ausgeschrieben:

$$
H(e^{j\Omega})
=
\frac{
b_0+b_1e^{-j\Omega}+b_2e^{-j2\Omega}+\ldots+b_{N-1}e^{-j(N-1)\Omega}
}{
1+a_1e^{-j\Omega}+a_2e^{-j2\Omega}+\ldots+a_Me^{-jM\Omega}
}
$$

Lesart:

- `b_k`: Eingangskopien, Formung und Ausloeschung.
- `a_r`: Ausgangskopien, Rueckfuehrung, Resonanz und Ausschwingen.

Merksatz:

> Praktische IIR-Audiofilter kombinieren meistens Feedforward und Feedback.

## Block 8: Biquad als praktische Standardform

Ein Biquad ist ein Filter zweiter Ordnung:

$$
y[n]
=
b_0x[n]
+
b_1x[n-1]
+
b_2x[n-2]
-
a_1y[n-1]
-
a_2y[n-2]
$$

Der Frequenzgang:

$$
H(e^{j\Omega})
=
\frac{
b_0+b_1e^{-j\Omega}+b_2e^{-j2\Omega}
}{
1+a_1e^{-j\Omega}+a_2e^{-j2\Omega}
}
$$

Warum Biquads fuer Audio zentral sind:

- effizient,
- kompakt,
- gut kaskadierbar,
- ausreichend fuer viele Standardkurven,
- geeignet fuer Tiefpass, Hochpass, Notch, Bandpass, Shelves und Peaking-EQ.

Kaskadierung:

Mehrere Biquads koennen hintereinander geschaltet werden. Im Frequenzbereich
werden die Uebertragungsfunktionen multipliziert:

$$
H_\mathrm{ges}(e^{j\Omega})
=
H_1(e^{j\Omega})H_2(e^{j\Omega})\ldots H_L(e^{j\Omega}).
$$

Fuer die Magnitude in dB bedeutet das:

$$
20\log_{10}|H_\mathrm{ges}(e^{j\Omega})|
=
\sum_{i=1}^{L}20\log_{10}|H_i(e^{j\Omega})|.
$$

Didaktische Lesart:

- ein Biquad ist ein einzelner zweiter Ordnung Baustein,
- mehrere Biquads bilden zusammen einen komplexeren Equalizer,
- dadurch kann man zum Beispiel Hochpass, Tiefpass, Shelves und mehrere
  Peaking-EQs gemeinsam einsetzen.

## Block 9: Audiotypische Filterkurven mit Biquads

Dieser Block kommt bewusst nach dem Biquad. Erst kennen die Studierenden die
praktische Standardform, danach sehen sie, welche typischen Audiofilter damit
realisierbar sind.

Unterblock 9A:

`png_storyboards/06_biquad_audiofilter/06A_typical_audio_filters`

Darstellungsregel fuer alle Bilder:

- logarithmische Frequenzachse von `20 Hz` bis `20 kHz`,
- Magnitude in dB mit festem Achsenausschnitt `-12...+12 dB`,
- pro Filterklasse drei Betragsbilder als Aufbau-Serie,
- pro Filterklasse eine gemeinsame Phasenabbildung,
- pro Filterklasse eine gemeinsame Gruppenlaufzeit-Abbildung,
- aktuelle Kurve gruen,
- vorherige Parametervarianten derselben Filterklasse grau,
- Koeffizienten des aktuellen Biquads rechts oben,
- beim High-Shelf im Betragsfrequenzgang links unten, damit die Kurve frei bleibt,
- Legenden in den Gruppenlaufzeit-Abbildungen rechts oben,
- alle Achsenflaechen pixelgenau gleich positionieren, damit die Bilder beim
  Durchschalten nicht springen,
- alle Beispiele bei `f_s=48 kHz`.

Hinweis fuer die Gruppenlaufzeit:

Bei idealen Notches ist die Phase an der exakten Ausloeschfrequenz nicht
definiert, weil der Betrag dort gegen null geht. Im Plot wird dieser singulaere
Punkt maskiert, damit die Umgebung der Gruppenlaufzeit sichtbar bleibt.

Die Reihenfolge ist:

1. Tiefpass,
2. Hochpass,
3. Notch,
4. Bandpass,
5. Low-Shelf,
6. High-Shelf,
7. Peaking-EQ.

### Tiefpass

Laesst tiefe Frequenzen durch und daempft hohe Frequenzen. In der Bildserie
wird die Grenzfrequenz verschoben. Die Studierenden sehen: gleiche Filterklasse,
aber andere Koeffizienten und andere Eckfrequenz.

Typische Anwendungen:

- Rauschen oder Zischanteile reduzieren,
- Klang dunkler machen,
- Woofer-Signal begrenzen.

### Hochpass

Daempft tiefe Frequenzen und laesst hohe Frequenzen durch. In der Bildserie
wird die Grenzfrequenz verschoben.

Typische Anwendungen:

- Trittschall entfernen,
- DC-Anteil entfernen,
- Mikrofon-Rumpeln reduzieren.

### Notch

Unterdrueckt einen engen Frequenzbereich. In der Bildserie werden Mittenfrequenz
und Guete variiert.

Typische Anwendungen:

- Brummen entfernen,
- Pfeifen oder Feedback-Frequenz unterdruecken,
- Stoerfrequenz aus Messdaten entfernen.

### Bandpass

Laesst einen Frequenzbereich durch und daempft darunter und darueber. In der
Bildserie werden Mittenfrequenz und Guete variiert.

Typische Anwendungen:

- Telefonklang,
- Resonanzbereich isolieren,
- Messsignal auf einen Bereich begrenzen.

### Low-Shelf

Hebt oder senkt tiefe Frequenzen relativ zum Rest. In der Bildserie werden
Eckfrequenz und Gain variiert.

Typische Anwendungen:

- Bass-Anhebung,
- Bass-Absenkung,
- tonale Korrektur.

### High-Shelf

Hebt oder senkt hohe Frequenzen relativ zum Rest. In der Bildserie werden
Eckfrequenz und Gain variiert.

Typische Anwendungen:

- Brillanz erhoehen,
- scharfe Hoehen reduzieren,
- Mastering-Korrektur.

### Peaking-EQ

Hebt oder senkt einen Bereich um eine Mittenfrequenz. Der Peaking-EQ ist fuer
Audio besonders wichtig, weil mehrere PEQs kaskadiert werden koennen und damit
sehr gezielte Korrekturen moeglich sind.

Typische Parameter:

- Mittenfrequenz,
- Gain,
- Guete beziehungsweise Bandbreite.

### Unterblock 9B: Kaskadierung von Biquads

Unterblock 9B zeigt, was Kaskadierung praktisch bedeutet:

`png_storyboards/06_biquad_audiofilter/06B_biquad_cascades`

Mehrere Biquads werden hintereinander geschaltet. Die Gesamtuebertragungsfunktion
ist das Produkt der einzelnen Stufen:

$$
H_\mathrm{ges}(e^{j\Omega})
=
\prod_{i=1}^{L}H_i(e^{j\Omega}).
$$

Fuer den Betrag in dB wird daraus eine Summe:

$$
20\log_{10}|H_\mathrm{ges}(e^{j\Omega})|
=
\sum_{i=1}^{L}20\log_{10}|H_i(e^{j\Omega})|.
$$

Auch die Phase addiert sich:

$$
\varphi_\mathrm{ges}(\Omega)
=
\sum_{i=1}^{L}\varphi_i(\Omega).
$$

Damit addiert sich auch die Gruppenlaufzeit:

$$
\tau_{g,\mathrm{ges}}(\Omega)
=
\sum_{i=1}^{L}\tau_{g,i}(\Omega),
$$

solange die Phase in diesem Bereich sinnvoll definiert ist.

Die Bildserie enthaelt drei Beispiele:

1. Tiefpass-Kaskade: zwei Biquads ergeben eine steilere Tiefpassflanke.
2. Hochpass-Kaskade: zwei Biquads ergeben eine steilere Hochpassflanke.
3. DAW-artiger parametrischer EQ: Low-Shelf, vier Peaking-EQs und High-Shelf
   werden zu einer Gesamtkurve kombiniert.

Didaktische Botschaft:

- eine einzelne Biquad-Stufe ist ein Baustein,
- mehrere Stufen ergeben ein hoeherwertiges Filter,
- bei Tiefpass und Hochpass wird die Flanke steiler,
- bei EQs addieren sich mehrere lokale Korrekturen zu einer Gesamtentzerrung.

Darstellungsregel:

- Einzelstufen grau,
- Gesamtkaskade gruen,
- pro Kaskade je ein Plot fuer Betrag, Phase und Gruppenlaufzeit,
- Betrag jeweils mit festem Achsenausschnitt `-12...+12 dB`,
- DAW-Kaskade mit kompakter Legende, damit die Filterkurve nicht verdeckt wird,
- Achsenflaechen pixelgenau gleich positioniert.

Didaktischer Abschluss:

> Das Biquad ist die Praxisform der allgemeinen Gleichung. Die Filtergalerie
> zeigt nur, was damit praktisch moeglich ist. In Vorlesung 8 erklaeren wir mit
> der z-Transformation, warum diese Koeffizienten geometrisch als Pole und
> Nullstellen interpretiert werden koennen.

## Vorlesung 8: geplanter Anschluss

Vorlesung 8 startet mit der offenen Frage:

> Wie entwerfe ich diese Koeffizienten gezielt?

Dazu werden dann eingefuehrt:

- z-Transformation,
- `z^{-1}` als Delay-Schreibweise,
- Systemfunktion `H(z)`,
- Pole und Nullstellen,
- Biquad-Design in der z-Ebene,
- praktische Audioeffekte mit Biquads.

## Empfohlene Folienfolge

1. FIR-Erinnerung: Eingangskopien.
2. Frequenzgang als Wirkung der Impulsantwort.
3. Was aendert Feedback?
4. Stabilitaet im Zeitbereich.
5. Stabile Impulsantwort.
6. Grenzstabile Impulsantwort.
7. Instabile Impulsantwort.
8. Einpolige Rekursion `y[n]=b_0x[n]+p y[n-1]`.
9. Impulsantwort `h[n]=b_0p^n`.
10. Geometrische Reihe.
11. Frequenzgang des einpoligen IIR.
12. Vier einpolige Frequenzgaenge.
13. `b_0` als Gain-Faktor.
14. Uebergang `p=-a_1`.
15. Mehrere Feedback-Taps.
16. Reines rekursives IIR mit `a_r`.
17. Impulsantwort eines `M=4`-IIR sampleweise aufbauen.
18. Sechs rein rekursive Frequenzgangbeispiele.
19. Grenze reiner Rueckfuehrung.
20. Hochpass-Idee durch `x[n]-x[n-1]`.
21. Feedforward plus Feedback.
22. Allgemeiner Frequenzgang `H(e^{j\Omega})`.
23. Biquad-Differenzengleichung.
24. Biquad-Frequenzgang.
25. Kaskadierung mehrerer Biquads.
26. Filtertypen-Uebersicht als Biquad-Anwendung.
27. Tiefpass und Hochpass.
28. Notch und Bandpass.
29. Low-Shelf und High-Shelf.
30. Peaking-EQ als zentraler Audio-EQ.
31. Ausblick auf z-Transformation und Vorlesung 8.

## Merksaetze

1. FIR mischt gespeicherte Eingangswerte.
2. IIR fuehrt gespeicherte Ausgangswerte zurueck.
3. Rueckfuehrung erzeugt Erinnerung und Ausschwingen.
4. Der Frequenzgang entsteht aus der Impulsantwort.
5. Ein einpoliges IIR fuehrt auf eine geometrische Reihe.
6. Mehr Feedback-Taps erzeugen komplexere Nennerkurven.
7. Feedforward erzeugt gezielte Ausloeschung durch Eingangskopien.
8. Praktische IIR-Filter kombinieren Feedforward und Feedback.
9. Das Biquad ist die zentrale praktische Standardform.
10. z-Transformation, Pole und Nullstellen folgen in Vorlesung 8.
