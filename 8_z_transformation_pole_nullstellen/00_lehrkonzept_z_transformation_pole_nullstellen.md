# Lehrkonzept Vorlesung 8: z-Ebene, z-Transformation, Pole und Nullstellen

## Didaktische Leitidee

Die Vorlesung beginnt nicht mit Polen, Nullstellen oder einer abstrakten
Transformation. Sie beginnt mit einem Baustein, den die Studierenden aus
digitalen Audiosystemen bereits kennen:

$$
y[n]=x[n-1].
$$

Das ist ein Delay um ein Sample. Aus diesem Zeitbereichsbaustein wird zuerst
der frequenzabhaengige Phasenversatz hergeleitet. Dann wird die bekannte
Frequenzbereichsschreibweise verwendet:

$$
Y(e^{j\Omega})=e^{-j\Omega}X(e^{j\Omega}).
$$

Erst danach wird \(z\) zunaechst nur auf dem Einheitskreis betrachtet:
\(z=e^{j\Omega}\). Das ist ein Zeiger mit Radius 1. Der Kehrwert dieses
Zeigers ist genau der bekannte Delay-Phasenfaktor \(e^{-j\Omega}\). Daraus
wird die Schreibweise \(z^{-1}\) als kompakte Delay-Notation motiviert. Der
Radius \(r\) wird erst nach dem ersten FIR-Beispiel als neue Erweiterung
eingefuehrt.

Die zentrale Progression ist:

1. Ein Delay verschiebt ein Signal im Zeitbereich.
2. Bei einem Sinus entspricht diese Verschiebung einem Phasenversatz.
3. Bei komplexen Exponentialsignalen wird das Delay zu einem komplexen Faktor.
4. Im Frequenzbereich wird daraus
   \(Y(e^{j\Omega})=e^{-j\Omega}X(e^{j\Omega})\).
5. Auf dem Einheitskreis gilt \(z=e^{j\Omega}\), also \(z^{-1}=e^{-j\Omega}\).
6. Als kompakte Schreibweise fuer ein Ein-Sample-Delay entsteht daraus \(z^{-1}\).
7. Mit \(z^{-1}\), \(z^{-2}\) werden erste FIR- und IIR-Systemfunktionen
   aufgebaut.
8. Aus \(H(z)\) entsteht auf dem Einheitskreis der Frequenzgang.
9. Aus \(H(z)\) entsteht in der z-Ebene die Flaechen- beziehungsweise
   Zeltdarstellung.
10. Die z-Transformation wird als Erweiterung der DTFT eingeordnet.
11. Nullstellen erklaeren Ausloeschungen, Pole erklaeren Resonanzen und
   Zeitverhalten.
12. Stabilitaet wird ueber die Lage der Pole in der z-Ebene sichtbar.

Damit bleibt die z-Transformation fuer die Studierenden an ein konkretes
Audiobild gekoppelt: Delay, Phase, Filterstruktur und Frequenzgang.

## Lernziele

Nach dieser Einheit sollen die Studierenden erklaeren koennen,

- warum ein Delay im Zeitbereich zu einem Phasenversatz im Frequenzbereich
  fuehrt,
- warum komplexe Exponentialsignale fuer LTI-Systeme besonders wichtig sind,
- warum der Operator \(z^{-1}\) natuerlich als Schreibweise fuer eine
  Sample-Verzoegerung entsteht,
- was die z-Ebene mit Zeitverhalten, Frequenz und Stabilitaet zu tun hat,
- warum der Frequenzgang durch Auswertung von \(H(z)\) auf dem Einheitskreis
  entsteht,
- wie Pole und Nullstellen den Frequenzgang beeinflussen,
- warum diese Konzepte im Audio Engineering bei Delay, EQ, Allpass,
  IIR-Filtern, Resonanzen, Kammfiltern, Phasengang und Gruppenlaufzeit
  praktisch relevant sind.

## Notation

Die Notation aus Vorlesung 7 bleibt erhalten:

- \(b_k\): Feedforward-Koeffizienten, Laufindex \(k=0,\dots,N-1\)
- \(a_r\): Feedback-Koeffizienten, Laufindex \(r=1,\dots,M\)
- \(N\): Anzahl der Feedforward-Taps
- \(M\): Anzahl der Feedback-Taps
- \(\Omega\): normierte Kreisfrequenz in rad/Sample
- \(f_s\): Abtastrate

Zeitbereich:

$$
y[n]
=
\sum_{k=0}^{N-1}b_k x[n-k]
-
\sum_{r=1}^{M}a_r y[n-r].
$$

Frequenzbereich aus Vorlesung 7:

$$
H(e^{j\Omega})
=
\frac{
\sum_{k=0}^{N-1}b_k e^{-jk\Omega}
}{
1+\sum_{r=1}^{M}a_r e^{-jr\Omega}
}.
$$

z-Bereich in Vorlesung 8:

$$
H(z)
=
\frac{
\sum_{k=0}^{N-1}b_k z^{-k}
}{
1+\sum_{r=1}^{M}a_r z^{-r}
}.
$$

## Zeitplanung und Blockstruktur

| Zeit | Block | Thema | Ziel |
|---:|---|---|---|
| 0-18 min | 1 | Delay im Zeitbereich und Phasenversatz | Aus \(y[n]=x[n-D]\) den linearen Phasengang herleiten |
| 18-35 min | 2 | Komplexe Exponentialsignale und Frequenzbereich | \(Y(e^{j\Omega})=e^{-j\Omega}X(e^{j\Omega})\) als Delay-Wirkung zeigen |
| 35-43 min | 3 | z-Ebene und Zeiger \(z\) | Einheitskreis, \(z=e^{j\Omega}\) und Kehrwert \(z^{-1}\) geometrisch zeigen |
| 43-55 min | 4 | Systemfunktion aus FIR und IIR | \(H(z)\) herleiten und Frequenzgang/Zelt auswerten |
| 55-66 min | 5 | z-Transformation als Erweiterung der DTFT | \(z=re^{j\Omega}\) und \(h[n]\xrightarrow{\mathcal{Z}}H(z)\) einordnen |
| 66-86 min | 6 | Biquads in der z-Ebene | Audiofilter als Kombination aus Polen und Nullstellen lesen |
| 86-92 min | 7 | Peaking-EQ-Sweep | Bewegte Pole/Nullstellen mit Spektrum und z-Ebenenflaeche synchron lesen |
| 92-96 min | 8 | Audioeffekte nach Systemklassen | LTI, LTV, NTI und NTV als Abschlussrahmen einordnen |
| 96-100 min | 9 | Aufgaben zur Filteranalyse | Koeffizienten, \(H(z)\), Frequenzgang und Pol-/Nullstellenlage verbinden |

## Block 1: Delay im Zeitbereich und Phasenversatz

Ausgangspunkt:

$$
y[n]=x[n-1].
$$

Das bedeutet:

> Der Ausgangswert zum Zeitpunkt \(n\) ist der Eingangswert von einem Sample
> frueher.

Ein Impuls bei \(n=0\) erscheint am Ausgang bei \(n=1\). Ein Sinus erscheint
ebenfalls spaeter. Bei einem Sinus kann diese Verschiebung als Phasenversatz
beschrieben werden.

Fuer ein Delay um \(D\) Samples gilt:

$$
y[n]=x[n-D].
$$

Fuer einen realen Sinus:

$$
x[n]=\cos(\Omega n)
$$

folgt:

$$
y[n]
=
\cos(\Omega(n-D))
=
\cos(\Omega n-D\Omega).
$$

Damit ist der Phasenversatz:

$$
\varphi(\Omega)=-D\Omega.
$$

Die Gruppenlaufzeit ist:

$$
\tau_g(\Omega)
=
-
\frac{d\varphi(\Omega)}{d\Omega}
=
D.
$$

Didaktischer Kern:

> Ein Delay verschiebt alle Frequenzen um dieselbe Zeit, aber nicht um
> denselben Phasenwinkel. Hohe Frequenzen durchlaufen pro Sample einen
> groesseren Winkel.

Aktives Storyboard:

- `png_storyboards/01_delay_phase_zeitbereich/01A_sinus_durch_delay`
- `png_storyboards/01_delay_phase_zeitbereich/01B_phasenfaktor_multiplikation`
- `png_storyboards/01_delay_phase_zeitbereich/01C_phasor_kreisfrequenz`

Ergaenzend zeigt Block 1C die drei Grundpositionen des Phasors auf dem
Einheitskreis: DC mit \(\Omega=0\), halbe Nyquist-Frequenz mit
\(\Omega=\pi/2\) und Nyquist mit \(\Omega=\pi\). Der Pfeilbogen ausserhalb
des Einheitskreises markiert direkt den Phasenwinkel \(\Omega\).

## Block 2: Komplexe Exponentialsignale und Frequenzbereich

Jetzt wird die reelle Sinus-Idee auf komplexe Exponentialsignale erweitert:

$$
x[n]=e^{j\Omega n}.
$$

Dabei ist \(\Omega\) die normierte Kreisfrequenz in rad/Sample. Sie gibt an,
um welchen Winkel sich der komplexe Zeiger pro Sample weiterdreht.

Ein Delay um ein Sample liefert:

$$
y[n]=x[n-1].
$$

Einsetzen:

$$
y[n]
=
e^{j\Omega(n-1)}
=
e^{j\Omega n}e^{-j\Omega}
=
e^{-j\Omega}x[n].
$$

Der Faktor \(e^{-j\Omega}\) hat Betrag 1 und Winkel \(-\Omega\):

$$
|e^{-j\Omega}|=1,
\qquad
\arg(e^{-j\Omega})=-\Omega.
$$

Fuer ein Delay um \(D\) Samples:

$$
y[n]
=
e^{j\Omega(n-D)}
=
e^{-jD\Omega}e^{j\Omega n}.
$$

Also:

$$
\boxed{
\text{Ein Delay um }D\text{ Samples erzeugt den Phasenfaktor }e^{-jD\Omega}.
}
$$

### Von der Einzelfrequenz zur Frequenzbereichsschreibweise

Bis hier wurde eine einzelne komplexe Testschwingung betrachtet. Das passt
aber direkt zur Frequenzbereichsschreibweise, weil ein beliebiges Signal als
Summe beziehungsweise Ueberlagerung solcher Frequenzanteile gedacht werden
kann. Fuer jeden Frequenzanteil gilt beim Delay derselbe Zusammenhang:

$$
x[n-D]
\quad\Longleftrightarrow\quad
e^{-jD\Omega}X(e^{j\Omega}).
$$

Fuer ein Ein-Sample-Delay:

$$
y[n]=x[n-1]
$$

gilt daher im Frequenzbereich:

$$
\boxed{
Y(e^{j\Omega})=e^{-j\Omega}X(e^{j\Omega}).
}
$$

Fuer \(D\) Samples:

$$
\boxed{
Y(e^{j\Omega})=e^{-jD\Omega}X(e^{j\Omega}).
}
$$

Das ist der zentrale Zwischenschritt vor der z-Schreibweise:

> Eine Verzoegerung ist im Frequenzbereich kein neuer Betragseffekt. Sie
> multipliziert jeden Frequenzanteil mit einem Phasenfaktor.

Warum sind komplexe Exponentialsignale fuer LTI-Systeme so geeignet?

Fuer ein LTI-System mit Impulsantwort \(h[m]\) gilt:

$$
y[n]
=
\sum_m h[m]x[n-m].
$$

Fuer

$$
x[n]=e^{j\Omega n}
$$

folgt:

$$
y[n]
=
\sum_m h[m]e^{j\Omega(n-m)}
=
e^{j\Omega n}\sum_m h[m]e^{-j\Omega m}.
$$

Der Ausdruck

$$
\sum_m h[m]e^{-j\Omega m}
$$

ist der Frequenzgang:

$$
H(e^{j\Omega}).
$$

Damit:

$$
\boxed{
y[n]=H(e^{j\Omega})e^{j\Omega n}.
}
$$

Didaktischer Kern:

> Ein LTI-System veraendert die Frequenz eines komplexen Exponentialsignals
> nicht. Es multipliziert es nur mit einem komplexen Faktor. Dieser Faktor
> enthaelt Betrag und Phase.

Aktive Storyboards:

- `png_storyboards/02_komplexe_exponentialsignale_lti/02A_normierte_kreisfrequenz`
- `png_storyboards/02_komplexe_exponentialsignale_lti/02B_phasenfaktor_multiplikation`

## Block 3: z-Ebene und Zeiger \(z\)

An dieser Stelle wird noch nicht die ganze z-Transformation eingefuehrt. Nach
Block 2B ist aber der Phasenfaktor des Ein-Sample-Delays bereits bekannt:

$$
e^{-j\Omega}.
$$

Jetzt wird zuerst die z-Ebene als Bild eingefuehrt. Im ersten Schritt sieht
man nur die komplexe Ebene mit Real- und Imaginaerachse und den
Einheitskreis. Im zweiten Schritt wird ein Zeiger auf dem Einheitskreis
eingetragen:

$$
z=e^{j\Omega}.
$$

Fuer die Bildserie wird ein konkreter Winkel gezeigt, aber nur symbolisch als
\(\Omega\) beschriftet. Anschaulich ist \(z\) hier ein Zeiger mit Radius 1.
Der freie Radius wird an dieser Stelle noch nicht eingefuehrt; fuer den
Moment interessiert nur der Einheitskreis.

Im dritten Schritt wird der zuvor gezeigte Zeiger grau stehen gelassen. Der
aktive neue Zeiger ist der Kehrwert:

Damit gilt:

$$
e^{-j\Omega}
=
\left(e^{j\Omega}\right)^{-1}
=
z^{-1}.
$$

Da dieser Kehrwert durch das Delay-System als Phasenfaktor wirksam wird, wird
der aktive Kehrwert-Zeiger gruen dargestellt.

Aktive Bildserie:

- `png_storyboards/03_z_ebene_zeiger_z/01_z_plane_unit_circle.png`
- `png_storyboards/03_z_ebene_zeiger_z/02_z_vector_r1_omega.png`
- `png_storyboards/03_z_ebene_zeiger_z/03_inverse_vector_z_minus_1.png`

Aktives Skript:

- `export_block_03_z_ebene_zeiger_z.py`

Didaktischer Kern:

> \(z\) wird zuerst als Zeiger auf dem Einheitskreis eingefuehrt. Der Kehrwert
> dieses Zeigers ist genau der Phasenfaktor eines Ein-Sample-Delays:
> \(z^{-1}=e^{-j\Omega}\). Der freie Radius \(r\) kommt erst spaeter.

## Block 4: Systemfunktion aus FIR und IIR

Jetzt ist die Schreibweise mit dem Delay-Operator vorhanden:

$$
z^{-1}\quad\text{steht fuer eine Sample-Verzoegerung.}
$$

### Block 4A1: Drei-Tap-FIR als Notch

Damit wird direkt eine Systemfunktion gebaut. Als erstes Beispiel wird bewusst
ein Drei-Tap-FIR verwendet, damit der Term \(z^{-2}\) sofort auftaucht. Fuer
ein gut sichtbares Notch-Beispiel wird

$$
H_\mathrm{FIR}(z)=\frac{1}{2}\left(1+z^{-2}\right)
$$

verwendet. Die Koeffizienten sind:

$$
b_0=\frac{1}{2},\qquad b_1=0,\qquad b_2=\frac{1}{2}.
$$

Die Impulsantwort ist deshalb unmittelbar:

$$
h_\mathrm{FIR}[n]=\frac{1}{2}\delta[n]+\frac{1}{2}\delta[n-2].
$$

Die Nullstellen liegen bei:

$$
z_{0,1/2}=e^{\pm j\pi/2}=\pm j.
$$

Setzt man spaeter \(z=e^{j\Omega}\), entsteht also ein Notch bei
\(\Omega_0=\pi/2\). Bei \(f_s=48\,\mathrm{kHz}\) entspricht das
\(f_0=f_s/4=12\,\mathrm{kHz}\). Dieses Beispiel ist fuer den Einstieg
guenstig, weil \(z^{-2}\) sichtbar ist und DC sowie Nyquist durch die
Normierung bei \(0\,\mathrm{dB}\) bleiben.

### Block 4A2: Drei-Tap-FIR mit verschobenen Nullstellen

Als zweites FIR-Beispiel werden nur die Filterkoeffizienten veraendert. Damit
wird sichtbar: Die Nullstellen sind nicht fest durch die Struktur
vorgegeben, sondern durch die Koeffizienten des Zaehlerpolynoms. Verwendet
wird:

$$
H_{\mathrm{FIR},2}(z)=1-0.6z^{-1}+0.36z^{-2}.
$$

Die Koeffizienten sind:

$$
b_0=1,\qquad b_1=-0.6,\qquad b_2=0.36.
$$

Die Impulsantwort ist:

$$
h_{\mathrm{FIR},2}[n]
=
\delta[n]-0.6\delta[n-1]+0.36\delta[n-2].
$$

Die Nullstellen werden wieder aus \(H(z)=0\) berechnet:

$$
1-0.6z^{-1}+0.36z^{-2}=0.
$$

Multiplikation mit \(z^2\) liefert:

$$
z^2-0.6z+0.36=0.
$$

Die Loesungen sind:

$$
z_{0,1/2}
=
0.3\pm j0.5196
=
0.6e^{\pm j\pi/3}.
$$

Die Nullstellen liegen damit innerhalb des Einheitskreises. Deshalb entsteht
keine vollstaendige Ausloeschung wie beim Notch, sondern eine breitere
Frequenzgangformung. Der didaktische Punkt ist:

> Andere FIR-Koeffizienten bedeuten ein anderes Zaehlerpolynom und damit
> andere Nullstellen.

### Block 4C: IIR-Filter als Nenner-Systemfunktion

Nach den FIR-Beispielen wird dieselbe Bildlogik fuer ein IIR-Filter genutzt.
Der didaktische Wechsel ist jetzt:

- Beim FIR entstehen die Nullstellen aus dem Zaehler.
- Beim IIR entstehen die Polstellen aus dem Nenner.

Als Beispiel wird ein rein rekursiver IIR mit zwei verzoegerten
Ausgangssignalen verwendet. Die Differenzengleichung lautet:

$$
y[n]=x[n]+0.9y[n-1]-0.81y[n-2].
$$

Die Rueckkopplungsterme werden auf die linke Seite gebracht:

$$
y[n]-0.9y[n-1]+0.81y[n-2]=x[n].
$$

In der Standardform

$$
y[n]=b_0x[n]-a_1y[n-1]-a_2y[n-2]
$$

sind die Koeffizienten:

$$
b_0=1,\qquad a_1=-0.9,\qquad a_2=0.81.
$$

Mit dem Delay-Operator wird daraus:

$$
Y(z)-0.9z^{-1}Y(z)+0.81z^{-2}Y(z)=X(z).
$$

Also:

$$
Y(z)\left(1-0.9z^{-1}+0.81z^{-2}\right)=X(z).
$$

Daraus folgt die Systemfunktion:

$$
H_\mathrm{IIR}(z)
=
\frac{Y(z)}{X(z)}
=
\frac{1}{1-0.9z^{-1}+0.81z^{-2}}.
$$

Die Polstellen sind die Nullstellen des Nenners:

$$
1-0.9z^{-1}+0.81z^{-2}=0.
$$

Multiplikation mit \(z^2\) liefert:

$$
z^2-0.9z+0.81=0.
$$

Die Loesungen sind:

$$
p_{1,2}
=
0.45\pm j0.7794
=
0.9e^{\pm j\pi/3}.
$$

Die Pole liegen also innerhalb des Einheitskreises, aber nahe daran. Deshalb
entsteht eine Resonanz und eine abklingende Impulsantwort. Genau diese
Zusammenhaenge werden in der Bildserie `04C_iir_two_delay_resonator` genauso
gezeigt wie bei den FIR-Beispielen: Impulsantwort, Frequenzgang, Auswertung
auf dem Einheitskreis, Auswertung fuer mehrere Radien, z-Ebenen-Flaeche und
abschliessend die 2D-z-Ebene mit den Polstellen.

### Block 4D: Biquad-Hochpass als Pol-Nullstellen-System

Nach FIR und rein rekursivem IIR folgt ein Biquad. Didaktisch ist das der
naechste natuerliche Schritt:

- Der Zaehler liefert Nullstellen.
- Der Nenner liefert Pole.
- Beide zusammen formen den Frequenzgang.

Als Beispiel wird ein stabiler Highpass-Biquad mit \(f_s=48\,\mathrm{kHz}\),
\(f_0=4\,\mathrm{kHz}\) und \(Q=1/\sqrt{2}\) verwendet. Die
Differenzengleichung lautet:

$$
\begin{aligned}
y[n]
=\;&0.68931x[n]-1.37861x[n-1]+0.68931x[n-2]\\
&+1.27963y[n-1]-0.47759y[n-2].
\end{aligned}
$$

In der Standardform

$$
y[n]=b_0x[n]+b_1x[n-1]+b_2x[n-2]-a_1y[n-1]-a_2y[n-2]
$$

sind die Koeffizienten:

$$
b_0=0.68931,\qquad b_1=-1.37861,\qquad b_2=0.68931,
$$

$$
a_1=-1.27963,\qquad a_2=0.47759.
$$

Daraus folgt die Systemfunktion:

$$
H_{\mathrm{BQ}}(z)
=
\frac{
0.68931-1.37861z^{-1}+0.68931z^{-2}
}{
1-1.27963z^{-1}+0.47759z^{-2}
}.
$$

Die Nullstellen sind die Loesungen des Zaehlerpolynoms:

$$
0.68931-1.37861z^{-1}+0.68931z^{-2}=0.
$$

Multiplikation mit \(z^2\) liefert:

$$
0.68931z^2-1.37861z+0.68931=0.
$$

Damit liegt eine doppelte Nullstelle bei:

$$
z_{0,1}=z_{0,2}=1.
$$

Die Polstellen sind die Loesungen des Nennerpolynoms:

$$
1-1.27963z^{-1}+0.47759z^{-2}=0.
$$

Multiplikation mit \(z^2\) liefert:

$$
z^2-1.27963z+0.47759=0.
$$

Die Loesungen sind:

$$
p_{1,2}
\approx
0.6398\pm j0.2612
=
0.6911e^{\pm j0.1234\pi}.
$$

Die doppelte Nullstelle bei \(z=1\) unterdrueckt die Gleichanteil- bzw.
DC-Komponente. Das Polpaar liegt innerhalb des Einheitskreises und formt den
Uebergang des Hochpasses. Die Bildserie `04D_biquad_highpass` zeigt deshalb
beides zusammen: Nullstellen und Pole in derselben z-Ebene.

Damit sind die ersten klaren Unterschiede sichtbar:

- FIR: verzoegerte Eingangskopien bilden den Zaehler.
- IIR: verzoegerte Ausgangskopien werden auf die linke Seite gebracht und
  bilden den Nenner.
- Biquad: Zaehler und Nenner wirken gemeinsam; Nullstellen druecken den
  Frequenzgang herunter, Pole ziehen ihn hoch.

### Was macht man jetzt mit \(H(z)\)?

Zuerst wird der Frequenzgang gewonnen. Dazu wird auf dem Einheitskreis
ausgewertet:

$$
z=e^{j\Omega}.
$$

Damit gilt:

$$
H(e^{j\Omega})=H(z)\big|_{z=e^{j\Omega}}.
$$

Didaktisch heisst das:

> Der Frequenzgang ist die Systemfunktion, ausgewertet auf dem Einheitskreis.

Dieser Schritt wird zuerst als 2D-Frequenzgang bis Nyquist gezeigt:

$$
0\leq \Omega \leq \pi
\qquad\leftrightarrow\qquad
0\leq \Omega/\pi\leq 1.
$$

Zuerst wird der Betrag linear gezeigt. Dadurch ist der Notch direkt als
Ausloeschung \(|H(e^{j\Omega})|=0\) lesbar. Danach wird dieselbe Kurve in dB
gezeigt. Im dB-GIF ist der vollstaendige Frequenzgang hellgrau vorbereitet.
Dieselben Frequenzpunkte werden dann sampleweise in Gruen aufgebaut. Das
Startbild des GIFs wird zusaetzlich als Standbild gezeigt.

Danach wird die Achse erweitert:

$$
0\leq \Omega/\pi \leq 2.
$$

Der Bereich \(0\leq\Omega/\pi\leq1\) bleibt pixelgenau derselbe Nyquist-Plot.
Der Bereich \(1\leq\Omega/\pi\leq2\) wird rechts angefuegt und blau gezeigt.
So wird sichtbar: Wir laufen nun nicht nur bis \(\pi\), sondern einmal um den
ganzen Einheitskreis.

Anschliessend wird exakt dieselbe Folge von Frequenzpunkten in der z-Ebene
gezeigt: Der Zeiger \(e^{j\Omega}\) laeuft zuerst von \(1\) bis \(-1\) auf
dem oberen Halbkreis, und die Hoehe der gruenen Kurve ist
\(|H(e^{j\Omega})|\) in dB. Unten bleibt der vollstaendige Einheitskreis als
grauer Referenzkreis sichtbar; der bereits abgefahrene Kreisabschnitt wird im
GIF orange aufgebaut. Zusaetzlich zeigt ein orangefarbener Zeiger unten die
aktuelle Projektion des Analysepunkts. Danach folgt ein Standbild fuer den
ganzen Einheitskreis:
oberer Halbkreis gruen, unterer Halbkreis blau. An dieser Stelle gibt es noch
keine Flaeche. Die Aussage ist nur:

> Wenn ich \(z=e^{j\Omega}\) einsetze, laufe ich auf dem Einheitskreis und
> bekomme den Frequenzgang.

Danach wird die ganze z-Ebene genutzt. Fuer

$$
z=re^{j\Omega}
$$

kann dieselbe Systemfunktion auch ausserhalb des Einheitskreises ausgewertet
werden. Der Betrag

$$
|H(z)|
$$

ergibt die Flaechen- beziehungsweise Zeltdarstellung in der z-Ebene.

Bevor die Flaeche gezeigt wird, wird noch ein Zwischenschritt eingefuehrt:
Zuerst ist fuer \(r=1\) der Einheitskreis unten orange hervorgehoben. Danach
wird dieselbe Auswertung als Serie fuer kleiner werdende Radien
\(r=0.8,0.6,0.4,0.2,0\) gezeichnet. In jedem Standbild ist unten in der
z-Ebene der aktuell zugehoerige Radius-Kreis orange hervorgehoben; bereits
gezeigte Radien bleiben als transparente Spuren sichtbar. Danach fasst ein
weiteres Standbild die Radiuskurven zusammen. Dadurch entsteht bereits ein
raeumlicher Eindruck davon, dass die Systemfunktion nicht nur auf dem
Einheitskreis definiert ist.

Diese Flaeche wird erst nach den Frequenzgangkurven gezeigt. Auf der Flaeche
bleibt die gruene/blaue Kurve auf dem Einheitskreis sichtbar, diesmal ueber
alle Frequenzen des Umlaufs. So ist klar: Die 2D-Kurve war nur der
Einheitskreisschnitt derselben Systemfunktion.

Als Abschluss dieses Blocks wird die z-Ebene noch einmal in 2D gezeigt: Beim
ersten FIR werden die Nullstellen \(z=\pm j\) und der formale Delay-Pol im
Ursprung markiert, beim zweiten FIR die Nullstellen
\(z=0.6e^{\pm j\pi/3}\) und ebenfalls der formale Delay-Pol im Ursprung,
beim IIR die Polstellen
\(p_{1,2}=0.9e^{\pm j\pi/3}\), beim Biquad sowohl die doppelte Nullstelle
bei \(z=1\) als auch das Polpaar
\(p_{1,2}\approx0.6398\pm j0.2612\). Damit wird die Verbindung zwischen
Systemfunktion, berechneten Wurzeln und geometrischer Lage in der z-Ebene
sichtbar.

Wichtig fuer die Formulierung in der Vorlesung:

> Die z-Ebenen-Flaeche ist nicht direkt das Zeitsignal. Sie zeigt die Struktur
> des Systems. Nullstellen erzeugen Senken, Pole erzeugen Spitzen. Aus Lage
> und Radius der Pole wird sichtbar, warum ein System schwingt, abklingt oder
> instabil wird.

Beim FIR in der \(z^{-1}\)-Schreibweise tauchen formal Delay-Pole im Ursprung
auf, wenn man die Funktion in der ganzen z-Ebene auswertet. Deshalb ist der
Punkt \(r=0\) im FIR-Bild ein Grenzfall. Auf dem Einheitskreis haben die
Delay-Faktoren Betrag 1. Fuer die Notch-Wirkung sind also vor allem die
Nullstellen auf dem Einheitskreis entscheidend.

Aktive Bildserie:

- `png_storyboards/04_systemfunktion_fir_iir/04A1_fir_three_tap_notch`
- `png_storyboards/04_systemfunktion_fir_iir/04A2_fir_three_tap_inside_zeros`
- `png_storyboards/04_systemfunktion_fir_iir/04C_iir_two_delay_resonator`
- `png_storyboards/04_systemfunktion_fir_iir/04D_biquad_highpass`

Aktives Skript:

- `export_block_04_systemfunktion_fir_iir.py`

Didaktischer Kern:

> Aus der Systemfunktion bekommt man zwei Sichten: Auf dem Einheitskreis den
> Frequenzgang, in der ganzen z-Ebene die Pol-Nullstellen-Struktur des
> Systems.

## Block 5: z-Transformation als Erweiterung der DTFT

Nach Block 4 ist klar: Wenn eine Systemfunktion \(H(z)\) vorliegt, kann sie auf
dem Einheitskreis als Frequenzgang und in der z-Ebene als Systemflaeche
betrachtet werden. Jetzt wird erklaert, woher diese Funktion allgemein kommt:
aus der z-Transformation.

Die DTFT betrachtet stationaere rotierende Anteile auf dem Einheitskreis:

$$
z=e^{j\Omega}
\qquad (r=1).
$$

Die z-Transformation erweitert diese Sicht auf einen freien Radius:

$$
z=re^{j\Omega}.
$$

Damit wird aus einem reinen Frequenzzeiger ein Wachstums- oder
Abklingfaktor:

$$
z^n
=
\left(re^{j\Omega}\right)^n
=
r^n e^{j\Omega n}.
$$

Die Bildserie zeigt diese anschauliche Zeitfunktion \(z^n\):

- \(r=1\): konstante Amplitude,
- \(r<1\): abklingender Anteil,
- \(r>1\): wachsender Anteil,
- \(r=|p|\): natuerlicher Modusradius des Biquad-Hochpasses aus Block 4D.

Die eigentliche z-Transformationssumme lautet:

$$
X(z)=\sum_{n=-\infty}^{\infty}x[n]z^{-n}.
$$

Fuer kausale Impulsantworten wird daraus die Systemfunktion:

$$
H(z)=\sum_{n=0}^{\infty}h[n]z^{-n}.
$$

Damit entsteht die Bruecke:

$$
h[n]\quad\xrightarrow{\mathcal{Z}}\quad H(z).
$$

Und aus \(H(z)\) folgen wieder die beiden Sichten:

$$
H(e^{j\Omega})=H(z)\big|_{z=e^{j\Omega}}
$$

als Frequenzgang und

$$
|H(z)|
$$

als Auswertung in der z-Ebene. Die vollstaendige Flaeche ist bereits aus
Block 4 bekannt; in Block 5 wird die Systemantwort gezielt als Kurve fuer
einzelne Radien gezeigt.

Im Einheitskreisfall `05A` wird der Frequenzgang des Biquad-Hochpasses aus
Block 4D fuer dieselben diskreten Analysekerne noch einmal in 2D gezeigt: die
vollstaendige Kurve bleibt grau, der Abschnitt bis zur aktuellen
Zeigerposition wird gruen. Danach wird dieselbe Systemantwort in der
3D-z-Ebene ohne Flaeche gezeigt. Erst wird auf dem Einheitskreis ausgewertet,
danach fuer \(r=0.86\), fuer \(r=1.08\) und schliesslich fuer den Polradius

In der z-Ebene wird die doppelte Nullstelle des Biquad-Hochpasses bei \(z=1\)
markiert. In der \(r>1\)-Serie werden die Polstellen von Anfang an
mitgezeigt. In der Polradius-Serie erscheinen sie erst, sobald der aktive
Zeiger den Polwinkel erreicht oder ueberschritten hat. Diese Markierungslogik
gilt in der 2D-z-Ebene und entsprechend auch unten in der 3D-z-Ebene.

$$
|p|\approx0.6911.
$$

Am Polwinkel

$$
\Omega_p\approx0.1234\pi
$$

trifft der Analysepunkt den Pol des Biquads. Dadurch wird sichtbar: Pole sind
die Stellen, an denen die Systemantwort in der z-Ebene sehr gross wird.

Aktive Bildserie:

- `png_storyboards/05_z_transformation_analysekern/05A_r_1_unit_circle`
- `png_storyboards/05_z_transformation_analysekern/05B_r_less_1_decay`
- `png_storyboards/05_z_transformation_analysekern/05C_r_greater_1_growth`
- `png_storyboards/05_z_transformation_analysekern/05D_r_pole_radius`
- `png_storyboards/05_z_transformation_analysekern/05E_biquad_poles_zeros_2d`

Aktives Skript:

- `export_block_05_z_transformation_analysis_kernel.py`

Didaktischer Kern:

> Die DTFT ist die Sicht auf den Einheitskreis. Die z-Transformation erweitert
> diese Sicht auf die ganze z-Ebene und macht damit Abklingen, Aufschwingen,
> Pole und Stabilitaet sichtbar.

## Block 6: Biquads in der z-Ebene

Nach dem reinen IIR kommt der wichtigste praktische Baustein:

$$
y[n]
=
b_0x[n]+b_1x[n-1]+b_2x[n-2]
-a_1y[n-1]-a_2y[n-2].
$$

Die z-Uebertragungsfunktion lautet:

$$
H(z)
=
\frac{
b_0+b_1z^{-1}+b_2z^{-2}
}{
1+a_1z^{-1}+a_2z^{-2}
}.
$$

Multipliziert mit \(z^2\):

$$
H(z)
=
\frac{
b_0z^2+b_1z+b_2
}{
z^2+a_1z+a_2
}.
$$

Damit ist das Biquad in der z-Ebene sehr gut lesbar:

- die Nullstellen sind die Loesungen von
  \(b_0z^2+b_1z+b_2=0\),
- die Pole sind die Loesungen von
  \(z^2+a_1z+a_2=0\),
- die Nullstellen erzeugen Abschwaechungen oder Ausloeschungen,
- die Pole erzeugen Anhebungen, Resonanz und Phasendrehung.

Genau dadurch kann ein Biquad deutlich mehr als ein reines IIR: Der Zaehler
und der Nenner arbeiten zusammen. Im Audiobereich entstehen daraus die
typischen Filterklassen:

- Tiefpass,
- Hochpass,
- Notch,
- Bandpass,
- Low-Shelf,
- High-Shelf,
- Peaking-EQ.

Aktive Bildserie:

- `png_storyboards/06_biquad_filter_z_ebene`

Enthaltene Unterbloecke:

- `06A_low_pass`
- `06B_high_pass`
- `06C_notch`
- `06D_band_pass`
- `06E_low_shelf`
- `06F_high_shelf`
- `06G_peaking_eq`

Jeder Unterblock enthaelt genau fuenf Einzelabbildungen mit derselben
Layoutlogik wie Block 5:

- `01_z_plane_2d.png`: Pol-Nullstellen-Diagramm in der 2D-z-Ebene
- `02_z_plane_3d.png`: \(|H(z)|\) als 3D-z-Ebenenflaeche
- `03_frequency_response.png`: Frequenzgang auf dem Einheitskreis
- `04_frequency_response_log.png`: derselbe Frequenzgang mit logarithmischer
  Frequenzachse in Hz
- `05_frequency_response_log_db.png`: logarithmische Frequenzachse und Betrag
  in dB

Die drei Spektrumsabbildungen uebernehmen die Titel- und
Koeffizientenbox-Logik aus der 7. Vorlesung: Filtertyp und Parameter stehen
im Titel, die normierten Biquad-Koeffizienten stehen direkt im Spektrum.

Aktives Skript:

- `export_block_06_biquad_z_plane_examples.py`

Didaktischer Kern:

> Ein Biquad ist ein kleines, universelles Pol-Nullstellen-System. Die
> Nullstellen druecken den Frequenzgang herunter, die Pole ziehen ihn hoch.
> Durch die richtige Kombination entstehen die typischen Audiofilter.

Stabilitaetsnotiz:

Fuer kausale stabile IIR- und Biquad-Systeme muessen alle Pole innerhalb des
Einheitskreises liegen:

$$
\boxed{
|p_i|<1.
}
$$

Nullstellen duerfen dagegen innerhalb, auf oder ausserhalb des Einheitskreises
liegen. Sie beeinflussen Betrag und Phase, aber nicht die BIBO-Stabilitaet
eines kausalen IIR-Systems.

## Block 7: Peaking-EQ-Sweep

Nach den statischen Biquad-Beispielen wird ein einzelner Peaking-EQ bewegt:
Die Mittenfrequenz wandert mit logarithmisch gebremstem Fortschritt von
tiefen zu hohen Frequenzen. Dadurch bleibt die Bewegung im Hochfrequenzbereich
lesbar. Die Guete variiert deutlich, und der Gain wechselt von Cut zu Boost
und zurueck zu Cut. Dadurch sehen die Studierenden gleichzeitig:

- wie sich der Peak im Spektrum bewegt,
- wie Pole und Nullstellen in der z-Ebene mitwandern,
- wie sich die 3D-z-Ebenenflaeche synchron veraendert.

Aktive Bildserie:

- `png_storyboards/07_peaking_eq_animation`

Enthaltene Animationen:

- `01_spectrum_motion.gif`: Spektrum mit logarithmischer Frequenzachse,
  Betrag in dB und aktuellen Biquad-Koeffizienten
- `02_z_plane_2d_motion.gif`: Pol-Nullstellen-Bewegung in der 2D-z-Ebene
- `03_z_plane_3d_motion.gif`: dieselbe Systemfunktion als 3D-z-Ebenenflaeche

Aktives Skript:

- `export_block_07_peaking_eq_animation.py`

Didaktischer Kern:

> Ein Biquad ist kein statisches Objekt. Wenn sich \(f_0\), \(Q\) und \(G\)
> aendern, bewegen sich Pole und Nullstellen, und der Frequenzgang folgt
> exakt derselben Systemfunktion.

## Block 8: Audioeffekte nach Systemklassen

Nach der z-Ebene wird die Vorlesung kurz wieder auf die Audioeffekt-Ebene
zurueckgefuehrt. Die Studierenden sollen die neue Pol-/Nullstellen-Sprache als
Teil einer groesseren Systemklassifikation lesen:

- Lineare zeitinvariante Systeme (LTI): Gain, Filter, Equalizer, Echo und
  Reverb. Diese Klasse kann mit Impulsantwort, Frequenzgang, Systemfunktion,
  Polen und Nullstellen beschrieben werden.
- Nichtlineare zeitinvariante Systeme (NTI): Verzerrung, Saturation und
  pegelabhaengige Kennlinien ohne explizite Zeitvariation.
- Lineare zeitvariante Systeme (LTV): Tremolo, Wah-wah, Chorus, Flanger,
  Phaser, Doppler, Rotary/Leslie und Vibrato. Die Struktur kann lokal linear
  sein, aber Parameter aendern sich ueber die Zeit.
- Nichtlineare zeitvariante Systeme (NTV): Effekte mit gleichzeitiger
  Pegelabhaengigkeit und Zeitvariation.

Didaktischer Kern:

> Die z-Transformation ist die Sprache fuer LTI-Filter. Viele Audioeffekte
> verlassen diese Klasse, aber die LTI-Sprache bleibt der Referenzpunkt, an dem
> wir Dynamik, Modulation und Nichtlinearitaet spaeter abgrenzen.

Aktive Bildserie:

- `png_storyboards/08_systemklassen_audioeffekte`

## Block 9: Aufgaben zur Filteranalyse

Die Vorlesung endet mit einer Selbstlernphase. Die Aufgaben verlangen nicht nur
Rechnen, sondern das Uebersetzen zwischen Darstellungen:

- Koeffizienten
- Blockdiagramm
- Differenzengleichung
- Systemfunktion \(H(z)\)
- Frequenzgang und Phase
- Pol-/Nullstellen-Diagramm
- Stabilitaet
- Audio-Engineering-Benennung

Wichtige Frequenzkonvention:

$$
0 \leq \frac{\Omega}{\pi} \leq 1.
$$

Dabei gilt:

$$
\frac{\Omega}{\pi}=0
\quad\Rightarrow\quad
\text{DC},
$$

$$
\frac{\Omega}{\pi}=0.5
\quad\Rightarrow\quad
\text{halbe Nyquist-Frequenz},
$$

$$
\frac{\Omega}{\pi}=1
\quad\Rightarrow\quad
\text{Nyquist-Frequenz}.
$$

Die vier Aufgaben aus der Master-Foliendatei:

1. Kurzer Glaetter vor einer Transientenanalyse: FIR-Koeffizienten auswerten,
   \(H(z)\) bestimmen, Nullstellen berechnen und die Wirkung als
   Glattung/Tiefpassnaehe interpretieren.
2. Einfaches IIR-Filter fuer DC-Offset und tieffrequente Stoeranteile:
   Rueckkopplungszweig korrekt einordnen, Pol-/Nullstellenlage und Stabilitaet
   pruefen und die Audio-Wirkung als DC-Blocker beziehungsweise Hochpass lesen.
3. Biquad-Filter gegen einen schmalen hochfrequenten Stoerton: Zaehler- und
   Nennerpolynom trennen, Pole und Nullstellen bestimmen und die
   Notch-/Resonanzwirkung aus der z-Ebene begruenden.
4. Filter aus Pol-/Nullstellen-Lage entwerfen: aus vorgegebenen Nullstellen,
   Polen und globalem Verstaerkungsfaktor ein qualitatives Filterverhalten
   ableiten und als Audioeffekt benennen.

Didaktischer Kern:

> Eine Systemfunktion ist erst dann verstanden, wenn dieselbe Struktur als
> Gleichung, Blockdiagramm, Frequenzgang, z-Ebene und hoerbare Filterwirkung
> gelesen werden kann.

Aktive Bildserie:

- `png_storyboards/09_aufgaben_filteranalyse`
