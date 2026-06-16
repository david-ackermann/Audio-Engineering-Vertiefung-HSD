# Detailauffrischung: z-Transformation, Delay-Operator und Systemfunktion

Dieses Dokument ist nicht als Studierendenfolie gedacht. Es ist eine mathematisch dichtere Auffrischung fuer die Vorbereitung von Vorlesung 8.

Ziel:

- verstehen, was die z-Transformation formal ist,
- verstehen, warum ein Delay als `z^{-1}` geschrieben wird,
- die Beziehung zwischen Zeitbereich, z-Ebene und Frequenzgang auffrischen,
- Systemfunktionen aus Differenzengleichungen sicher herleiten,
- Pole, Nullstellen, Stabilitaet und Frequenzgang sauber einordnen.

Didaktischer Hinweis fuer die Vorlesung:

Die formale Definition kommt in diesem Dokument frueh, weil es als
Auffrischung fuer die Vorbereitung gedacht ist. In der Vorlesung selbst wird
jedoch zuerst aus dem Zeitbereich gestartet: \(y[n]=x[n-1]\), dann Delay als
Phasenfaktor \(e^{-j\Omega}\), danach erst \(z^{-1}\) und die z-Ebene.

## 1. Ausgangspunkt: diskrete Signale

Ein zeitdiskretes Signal ist eine Folge:

$$
x[n], \qquad n\in\mathbb{Z}.
$$

In der digitalen Signalverarbeitung arbeiten wir oft mit kausalen Folgen, also Folgen mit:

$$
x[n]=0 \quad \text{fuer } n<0.
$$

Die z-Transformation ist eine Transformation solcher Folgen in eine komplexe Funktion der Variablen `z`.

## 2. Definition der z-Transformation

Die bilaterale z-Transformation ist definiert als:

$$
X(z)
=
\mathcal{Z}\{x[n]\}
=
\sum_{n=-\infty}^{\infty}x[n]z^{-n}.
$$

Die Variable `z` ist komplex:

$$
z = r e^{j\Omega}.
$$

Damit gilt:

$$
z^{-n}
=
\left(r e^{j\Omega}\right)^{-n}
=
r^{-n} e^{-j\Omega n}.
$$

Man kann die z-Transformation daher als verallgemeinerte Fourier-Transformation lesen:

- `e^{-j\Omega n}` ist der rotierende komplexe Schwingungsanteil,
- `r^{-n}` ist eine zusaetzliche exponentielle Gewichtung.

Die DTFT entsteht als Spezialfall auf dem Einheitskreis:

$$
r=1
\quad \Rightarrow \quad
z=e^{j\Omega}.
$$

Dann:

$$
X(e^{j\Omega})
=
\sum_{n=-\infty}^{\infty}x[n]e^{-j\Omega n}.
$$

Das ist die Fourier-Transformierte einer diskreten Folge.

## 3. Was bedeutet `z^{-1}`?

Kurzfassung:

> `z^{-1}` ist im Systemkontext der algebraische Ausdruck fuer ein Delay um ein Sample.

Genauer:

Wenn:

$$
X(z)=\sum_{n=-\infty}^{\infty}x[n]z^{-n},
$$

dann hat die um ein Sample verzoegerte Folge:

$$
x[n-1]
$$

die z-Transformation:

$$
\mathcal{Z}\{x[n-1]\}
=
z^{-1}X(z).
$$

### Herleitung der Delay-Eigenschaft

Wir starten mit:

$$
\mathcal{Z}\{x[n-k]\}
=
\sum_{n=-\infty}^{\infty}x[n-k]z^{-n}.
$$

Substitution:

$$
m=n-k
\quad \Rightarrow \quad
n=m+k.
$$

Dann:

$$
\sum_{n=-\infty}^{\infty}x[n-k]z^{-n}
=
\sum_{m=-\infty}^{\infty}x[m]z^{-(m+k)}
$$

$$
=
z^{-k}\sum_{m=-\infty}^{\infty}x[m]z^{-m}
$$

Also:

$$
\mathcal{Z}\{x[n-k]\}
=
z^{-k}X(z).
$$

Fuer `k=1`:

$$
x[n-1]
\quad \longleftrightarrow \quad
z^{-1}X(z).
$$

Damit ist `z^{-1}` die algebraische Darstellung eines Sample-Delays.

## 4. `z^{-1}` als Operator

In Blockdiagrammen wird ein Delay oft als Operator verstanden:

$$
D\{x[n]\}=x[n-1].
$$

Im z-Bereich entspricht dieser Operator der Multiplikation mit `z^{-1}`:

$$
D
\quad \longleftrightarrow \quad
z^{-1}.
$$

Deshalb schreibt man digitale Filter oft als Polynome in `z^{-1}`:

$$
H(z)=b_0+b_1z^{-1}+b_2z^{-2}+\dots
$$

Das ist nichts anderes als:

$$
y[n]=b_0x[n]+b_1x[n-1]+b_2x[n-2]+\dots
$$

Didaktisch:

> Jede Potenz `z^{-k}` steht fuer einen um `k` Samples verzoegerten Signalpfad.

## 5. `z^{-1}` auf dem Einheitskreis

Auf dem Einheitskreis gilt:

$$
z=e^{j\Omega}.
$$

Daher:

$$
z^{-1}=e^{-j\Omega}.
$$

Ein Delay um ein Sample multipliziert eine komplexe Sinusschwingung also mit:

$$
e^{-j\Omega}.
$$

Das ist ein Phasenversatz von:

$$
-\Omega.
$$

Ein Delay um `k` Samples ergibt:

$$
z^{-k}=e^{-j\Omega k}.
$$

Das ist ein Phasenversatz von:

$$
-\Omega k.
$$

Genau deshalb hat ein reines Delay:

$$
y[n]=x[n-D]
$$

die Systemfunktion:

$$
H(z)=z^{-D}
$$

und den Frequenzgang:

$$
H(e^{j\Omega})=e^{-j\Omega D}.
$$

Betrag:

$$
|H(e^{j\Omega})|=1.
$$

Phase:

$$
\varphi(\Omega)=-\Omega D.
$$

Interpretation:

- Ein ideales Delay aendert den Betrag nicht.
- Es erzeugt eine lineare Phase.
- Die Gruppenlaufzeit ist `D` Samples.

## 6. Zusammenhang zwischen z-Transformation und DTFT

Die z-Transformation:

$$
X(z)=\sum_n x[n]z^{-n}
$$

wird mit:

$$
z=re^{j\Omega}
$$

zu:

$$
X(re^{j\Omega})
=
\sum_n x[n]r^{-n}e^{-j\Omega n}.
$$

Die DTFT ist der Spezialfall:

$$
r=1.
$$

Also:

$$
X(e^{j\Omega})
=
\sum_n x[n]e^{-j\Omega n}.
$$

Wichtig:

> Der Frequenzgang eines digitalen Systems ist die Systemfunktion auf dem Einheitskreis.

Also:

$$
H(e^{j\Omega})
=
H(z)\big|_{z=e^{j\Omega}}.
$$

## 6a. Komme ich von `H(e^{j\Omega})` zu `H(z)`?

Didaktisch: ja, genau das ist der sinnvolle Anschluss an Vorlesung 6.

Mathematisch muss man aber praezise formulieren:

> `H(e^{j\Omega})` ist die Auswertung von `H(z)` auf dem Einheitskreis. `H(z)` ist die allgemeinere Beschreibung.

Also:

$$
H(e^{j\Omega})
=
H(z)\big|_{z=e^{j\Omega}}.
$$

Oder umgekehrt als didaktische Generalisierung:

$$
e^{j\Omega}
\quad \longrightarrow \quad
z.
$$

und damit:

$$
e^{-j\Omega}
\quad \longrightarrow \quad
z^{-1}.
$$

### Beispiel FIR

Aus Vorlesung 6 ist fuer ein FIR-Filter bekannt:

$$
H(e^{j\Omega})
=
\sum_{k=0}^{N-1}b_ke^{-j\Omega k}.
$$

Da auf dem Einheitskreis gilt:

$$
z=e^{j\Omega},
$$

folgt:

$$
z^{-k}=e^{-j\Omega k}.
$$

Daher kann man die z-Form schreiben als:

$$
H(z)
=
\sum_{k=0}^{N-1}b_kz^{-k}.
$$

Didaktisch:

> In Vorlesung 7 war `e^{-j\Omega}` der frequenzabhaengige Phasenfaktor eines Delays. In Vorlesung 8 wird daraus der allgemeine Delay-Baustein `z^{-1}`.

### Beispiel einpoliges IIR

Wenn man im Frequenzbereich bereits geschrieben hat:

$$
H(e^{j\Omega})
=
\frac{b_0}{1-pe^{-j\Omega}},
$$

dann ist die zugehoerige z-Schreibweise:

$$
H(z)
=
\frac{b_0}{1-pz^{-1}}.
$$

Auch hier ist die Ersetzung:

$$
e^{-j\Omega}
\rightarrow
z^{-1}.
$$

### Wichtige Einschraenkung

Streng mathematisch kann man aus einem beliebigen Frequenzgang `H(e^{j\Omega})` nicht eindeutig eine Systemfunktion `H(z)` rekonstruieren, wenn keine weiteren Annahmen gemacht werden.

Gruende:

- `H(e^{j\Omega})` beschreibt nur Werte auf dem Einheitskreis.
- `H(z)` beschreibt eine Funktion in der komplexen Ebene.
- Verschiedene Systeme koennen auf dem Einheitskreis denselben Betrag haben.
- Allpass-Faktoren koennen die Phase aendern, ohne den Betrag zu aendern.
- Aus `|H(e^{j\Omega})|` allein folgt `H(z)` erst recht nicht eindeutig.

Eindeutig wird es erst, wenn man zusaetzliche Annahmen macht, z.B.:

- FIR mit bekannter Ordnung,
- IIR mit bekannter rationaler Struktur,
- Kausalitaet,
- Stabilitaet,
- Minimum-Phase,
- bekannte Differenzengleichung.

Fuer die Vorlesung ist deshalb diese Formulierung sauber:

> Wir kennen aus Vorlesung 7 den Frequenzgang `H(e^{j\Omega})` fuer rekursive Filter. Jetzt verallgemeinern wir diese Sicht zu `H(z)`, indem wir den Einheitskreis verlassen und `e^{-j\Omega}` als Spezialfall von `z^{-1}` lesen.

Noch kuerzer:

> `H(e^{j\Omega})` ist die Kurve, die wir sehen. `H(z)` ist die Struktur, aus der diese Kurve entsteht.

## 7. Region of Convergence, ROC

Die z-Transformation ist nicht nur der algebraische Ausdruck, sondern auch der Bereich, in dem die Summe konvergiert.

Definition:

$$
X(z)
=
\sum_{n=-\infty}^{\infty}x[n]z^{-n}
$$

konvergiert nur fuer bestimmte Werte von `z`. Dieser Bereich heisst Region of Convergence:

$$
\mathrm{ROC}.
$$

Warum wichtig?

- Die gleiche algebraische Formel kann zu verschiedenen Zeitfolgen gehoeren, wenn die ROC unterschiedlich ist.
- Kausalitaet und Stabilitaet lassen sich ueber die ROC einordnen.

## 8. Beispiel: rechtsseitige Exponentialfolge

Betrachte:

$$
x[n]=a^n u[n].
$$

Dann:

$$
X(z)
=
\sum_{n=0}^{\infty}a^n z^{-n}
=
\sum_{n=0}^{\infty}(az^{-1})^n.
$$

Das ist eine geometrische Reihe:

$$
\sum_{n=0}^{\infty}q^n
=
\frac{1}{1-q},
\qquad |q|<1.
$$

Hier:

$$
q=az^{-1}.
$$

Also:

$$
X(z)
=
\frac{1}{1-az^{-1}},
\qquad |az^{-1}|<1.
$$

Die Konvergenzbedingung:

$$
|az^{-1}|<1
$$

ist:

$$
\frac{|a|}{|z|}<1
$$

also:

$$
|z|>|a|.
$$

Damit:

$$
x[n]=a^n u[n]
\quad \longleftrightarrow \quad
X(z)=\frac{1}{1-az^{-1}},
\qquad \mathrm{ROC}: |z|>|a|.
$$

Interpretation:

- Der Pol liegt bei `z=a`.
- Die ROC liegt ausserhalb des Polradius.
- Das ist typisch fuer kausale rechtsseitige Folgen.

## 9. Kausalitaet und Stabilitaet

Fuer rationale Systemfunktionen gilt bei kausalen LTI-Systemen:

- Die Impulsantwort ist rechtsseitig.
- Die ROC liegt ausserhalb des aeussersten Pols.

Ein kausales LTI-System ist BIBO-stabil, wenn:

$$
\sum_{n=-\infty}^{\infty}|h[n]|<\infty.
$$

Im z-Bereich bedeutet das:

> Der Einheitskreis muss in der ROC liegen.

Fuer kausale rationale Systeme folgt daraus:

> Alle Pole muessen innerhalb des Einheitskreises liegen.

Also:

$$
|p_i|<1
\quad \text{fuer alle Pole } p_i.
$$

Das ist die bekannte Stabilitaetsbedingung fuer kausale IIR-Filter.

## 10. Systemfunktion eines LTI-Systems

Ein LTI-System ist durch seine Impulsantwort `h[n]` beschrieben.

Zeitbereich:

$$
y[n]=x[n]\ast h[n].
$$

Also:

$$
y[n]=\sum_{m=-\infty}^{\infty}x[m]h[n-m].
$$

Die z-Transformation der Faltung ergibt Multiplikation:

$$
Y(z)=X(z)H(z).
$$

Daraus:

$$
H(z)=\frac{Y(z)}{X(z)}.
$$

`H(z)` ist die Systemfunktion oder Transferfunktion.

## 11. FIR-Systeme

Ein FIR-Filter:

$$
y[n]=\sum_{k=0}^{N-1}b_kx[n-k].
$$

z-Transformation:

$$
Y(z)
=
\sum_{k=0}^{N-1}b_kz^{-k}X(z).
$$

Ausklammern:

$$
Y(z)
=
\left(
\sum_{k=0}^{N-1}b_kz^{-k}
\right)X(z).
$$

Systemfunktion:

$$
H(z)
=
\frac{Y(z)}{X(z)}
=
\sum_{k=0}^{N-1}b_kz^{-k}.
$$

Das ist ein Polynom in `z^{-1}`.

Beispiel:

$$
y[n]=x[n]-x[n-1].
$$

Dann:

$$
H(z)=1-z^{-1}.
$$

Nullstelle:

$$
1-z^{-1}=0
$$

$$
z^{-1}=1
$$

$$
z=1.
$$

Da `z=1` auf dem Einheitskreis der digitalen Frequenz `\Omega=0` entspricht, wird DC ausgeloescht.

## 12. Einpoliges IIR-System

Zeitbereich:

$$
y[n]=b_0x[n]+p\,y[n-1].
$$

z-Transformation:

$$
Y(z)=b_0X(z)+p z^{-1}Y(z).
$$

Umstellen:

$$
Y(z)-p z^{-1}Y(z)=b_0X(z)
$$

$$
Y(z)(1-pz^{-1})=b_0X(z)
$$

Systemfunktion:

$$
H(z)
=
\frac{Y(z)}{X(z)}
=
\frac{b_0}{1-pz^{-1}}.
$$

Der Nenner verschwindet bei:

$$
1-pz^{-1}=0.
$$

Also:

$$
pz^{-1}=1
$$

$$
z=p.
$$

Das System hat einen Pol bei:

$$
z=p.
$$

Fuer kausale Stabilitaet:

$$
|p|<1.
$$

## 13. Frequenzgang des einpoligen IIR

Setze:

$$
z=e^{j\Omega}.
$$

Dann:

$$
H(e^{j\Omega})
=
\frac{b_0}{1-pe^{-j\Omega}}.
$$

Betrag:

$$
|H(e^{j\Omega})|
=
\frac{|b_0|}
{|1-pe^{-j\Omega}|}.
$$

Nennerbetrag:

$$
|1-pe^{-j\Omega}|^2
=
(1-pe^{-j\Omega})(1-pe^{j\Omega})
$$

$$
=
1-p e^{j\Omega}-p e^{-j\Omega}+p^2
$$

mit:

$$
e^{j\Omega}+e^{-j\Omega}=2\cos(\Omega)
$$

folgt:

$$
|1-pe^{-j\Omega}|^2
=
1-2p\cos(\Omega)+p^2.
$$

Also:

$$
|H(e^{j\Omega})|
=
\frac{|b_0|}
{\sqrt{1-2p\cos(\Omega)+p^2}}.
$$

Bei DC:

$$
\Omega=0,\qquad \cos(0)=1
$$

$$
|H(e^{j0})|
=
\frac{|b_0|}{|1-p|}.
$$

Bei Nyquist:

$$
\Omega=\pi,\qquad \cos(\pi)=-1
$$

$$
|H(e^{j\pi})|
=
\frac{|b_0|}{|1+p|}.
$$

Fuer:

$$
0<p<1
$$

ist:

$$
|1-p|<|1+p|.
$$

Also:

$$
|H(e^{j0})|>|H(e^{j\pi})|.
$$

Das System ist tiefpassartig.

Fuer:

$$
-1<p<0
$$

wird Nyquist staerker als DC. Das System wirkt hochfrequenzbetonend.

## 14. Allgemeines rekursives Filter

Zeitbereich:

$$
y[n]
=
\sum_{k=0}^{N-1}b_kx[n-k]
-
\sum_{r=1}^{M}a_ry[n-r].
$$

z-Transformation:

$$
Y(z)
=
\sum_{k=0}^{N-1}b_kz^{-k}X(z)
-
\sum_{r=1}^{M}a_rz^{-r}Y(z).
$$

Alle `Y(z)`-Terme auf eine Seite:

$$
Y(z)
+
\sum_{r=1}^{M}a_rz^{-r}Y(z)
=
\sum_{k=0}^{N-1}b_kz^{-k}X(z).
$$

Ausklammern:

$$
Y(z)
\left(
1+\sum_{r=1}^{M}a_rz^{-r}
\right)
=
X(z)
\left(
\sum_{k=0}^{N-1}b_kz^{-k}
\right).
$$

Systemfunktion:

$$
H(z)
=
\frac{Y(z)}{X(z)}
=
\frac{
\sum_{k=0}^{N-1}b_kz^{-k}
}{
1+\sum_{r=1}^{M}a_rz^{-r}
}.
$$

Definiere:

$$
B(z)=\sum_{k=0}^{N-1}b_kz^{-k}
$$

und:

$$
A(z)=1+\sum_{r=1}^{M}a_rz^{-r}.
$$

Dann:

$$
H(z)=\frac{B(z)}{A(z)}.
$$

## 15. Pole und Nullstellen

Nullstellen sind die Loesungen von:

$$
B(z)=0.
$$

An diesen Orten ist:

$$
H(z)=0.
$$

Pole sind die Loesungen von:

$$
A(z)=0.
$$

An diesen Orten wird:

$$
H(z)
$$

singulaer, sofern nicht gleichzeitig eine exakt gleiche Nullstelle kuerzt.

Merksatz:

- Nullstellen kommen aus dem Zaehler.
- Pole kommen aus dem Nenner.
- Nullstellen erzeugen Ausloeschungen.
- Pole erzeugen starke Reaktionen, Resonanz und Stabilitaetsfragen.

## 16. Warum Nullstellen auf dem Einheitskreis Kerben erzeugen

Der Frequenzgang ist:

$$
H(e^{j\Omega}).
$$

Wenn eine Nullstelle genau auf dem Einheitskreis liegt:

$$
z_0=e^{j\Omega_0},
$$

dann gilt bei:

$$
\Omega=\Omega_0
$$

im Zaehler:

$$
B(e^{j\Omega_0})=0.
$$

Also:

$$
H(e^{j\Omega_0})=0.
$$

Das ist eine ideale Kerbe im Frequenzgang.

## 17. Notch-Beispiel

Eine reelle Filterstruktur mit einer Kerbe bei `\Omega_0` braucht ein komplex-konjugiertes Nullstellenpaar:

$$
z_1=e^{j\Omega_0},
\qquad
z_2=e^{-j\Omega_0}.
$$

Zaehler:

$$
B(z)
=
(1-z_1z^{-1})(1-z_2z^{-1}).
$$

Einsetzen:

$$
B(z)
=
(1-e^{j\Omega_0}z^{-1})(1-e^{-j\Omega_0}z^{-1}).
$$

Ausmultiplizieren:

$$
B(z)
=
1
-
(e^{j\Omega_0}+e^{-j\Omega_0})z^{-1}
+
z^{-2}.
$$

Mit:

$$
e^{j\Omega_0}+e^{-j\Omega_0}
=
2\cos(\Omega_0)
$$

folgt:

$$
B(z)
=
1-2\cos(\Omega_0)z^{-1}+z^{-2}.
$$

FIR-Notch:

$$
H_{\mathrm{notch,FIR}}(z)
=
1-2\cos(\Omega_0)z^{-1}+z^{-2}.
$$

Schaerferer IIR-Notch mit Polradius `r<1`:

$$
H_{\mathrm{notch}}(z)
=
\frac{
1-2\cos(\Omega_0)z^{-1}+z^{-2}
}{
1-2r\cos(\Omega_0)z^{-1}+r^2z^{-2}
}.
$$

Interpretation:

- Nullstellen auf dem Einheitskreis erzeugen die Ausloeschung.
- Pole mit gleichem Winkel und Radius `r<1` machen den Uebergang schmaler.
- Je naeher `r` an `1`, desto schmaler und resonanter die Struktur.

## 18. Warum Pole Resonanzen erzeugen

Ein Pol bei:

$$
z_p=re^{j\Omega_0}
$$

liegt nahe am Einheitskreis, wenn:

$$
r\approx 1.
$$

Der Frequenzgang wird auf dem Einheitskreis ausgewertet:

$$
z=e^{j\Omega}.
$$

Wenn der laufende Punkt `e^{j\Omega}` nahe am Pol vorbeikommt, wird der Nenner klein. Dadurch wird:

$$
|H(e^{j\Omega})|
$$

gross.

Das ergibt eine Resonanz nahe:

$$
\Omega=\Omega_0.
$$

Zeitbereichsinterpretation:

- Polradius klein: schnelles Abklingen.
- Polradius gross: langsames Abklingen.
- Polradius nahe `1`: lange Resonanz.
- Polradius groesser oder gleich `1`: nicht stabil fuer kausale Systeme.

## 19. Biquad

Ein Biquad ist eine rationale Systemfunktion zweiter Ordnung:

$$
H(z)
=
\frac{
b_0+b_1z^{-1}+b_2z^{-2}
}{
1+a_1z^{-1}+a_2z^{-2}
}.
$$

Zeitbereich:

$$
y[n]
=
b_0x[n]+b_1x[n-1]+b_2x[n-2]
-a_1y[n-1]-a_2y[n-2].
$$

Es hat:

- bis zu zwei Nullstellen,
- bis zu zwei Pole,
- eine kompakte Echtzeitstruktur,
- genug Freiheitsgrade fuer viele Standard-Audiofilter.

Typische Biquad-Filter:

- Tiefpass,
- Hochpass,
- Bandpass,
- Notch,
- Low-Shelf,
- High-Shelf,
- Peaking-EQ.

## 20. Wichtige Vorzeichenkonvention

Es gibt zwei haeufige Schreibweisen.

Diese Konvention ist der Grund, warum der einpolige Einstiegsparameter `p` nicht einfach global in `a_1` umbenannt werden sollte.

Einstiegsform:

$$
y[n]=b_0x[n]+p\,y[n-1]
$$

Standardform:

$$
y[n]=b_0x[n]-a_1y[n-1]
$$

Vergleich:

$$
p=-a_1.
$$

Also:

- `p` ist der direkte Rueckfuehrungsfaktor im anschaulichen Einstiegsmodell,
- `a_1` ist der Nennerkoeffizient in der Standard-DSP-Schreibweise,
- bei der ueblichen Minus-Schreibweise haben beide entgegengesetztes Vorzeichen.

Beispiel:

$$
y[n]=b_0x[n]+0.5\,y[n-1]
$$

entspricht:

$$
y[n]=b_0x[n]-(-0.5)y[n-1].
$$

Also:

$$
p=0.5
\quad \Rightarrow \quad
a_1=-0.5.
$$

Schreibweise A:

$$
y[n]
=
\sum_{k=0}^{N-1}b_kx[n-k]
-
\sum_{r=1}^{M}a_ry[n-r].
$$

Dann:

$$
H(z)
=
\frac{
\sum_{k=0}^{N-1}b_kz^{-k}
}{
1+\sum_{r=1}^{M}a_rz^{-r}
}.
$$

Schreibweise B:

$$
y[n]
=
\sum_{k=0}^{N-1}b_kx[n-k]
+
\sum_{r=1}^{M}\alpha_ry[n-r].
$$

Dann:

$$
H(z)
=
\frac{
\sum_{k=0}^{N-1}b_kz^{-k}
}{
1-\sum_{r=1}^{M}\alpha_rz^{-r}
}.
$$

Beide sind gleichwertig, wenn:

$$
\alpha_r=-a_r.
$$

In Python/SciPy wird oft die Nennerform:

$$
A(z)=a_0+a_1z^{-1}+a_2z^{-2}+\dots
$$

mit `a_0=1` verwendet. Die Filtergleichung lautet dann:

$$
y[n]
=
\frac{1}{a_0}
\left(
\sum_k b_kx[n-k]
-
\sum_{r=1}^{M}a_ry[n-r]
\right).
$$

Bei `a_0=1` entspricht das der Schreibweise A.

## 21. Mentales Modell

Zeitbereich:

- `z^{-1}` bedeutet ein Sample Delay.
- `z^{-k}` bedeutet `k` Sample Delay.
- `b_k` gewichten Eingangskopien.
- `a_r` gewichten zurueckgefuehrte Ausgangskopien.

z-Ebene:

- `z` ist ein komplexer Ort.
- `H(z)` beschreibt das System als Funktion dieses Ortes.
- Der Einheitskreis `z=e^{j\Omega}` liefert den Frequenzgang.
- Nullstellen loeschen.
- Pole verstaerken und speichern.

Frequenzbereich:

- Tiefpass: hoher Betrag bei kleinen `\Omega`, kleiner Betrag bei grossen `\Omega`.
- Hochpass: kleiner Betrag bei kleinen `\Omega`, hoher Betrag bei grossen `\Omega`.
- Notch: Nullstelle auf dem Einheitskreis bei der Stoerfrequenz.
- Resonanz: Pol nahe am Einheitskreis bei der Resonanzfrequenz.

## 22. Typische Denkfallen

### Denkfalle 1: `z^{-1}` ist keine Frequenz

`z^{-1}` ist nicht selbst eine Frequenz. Es ist ein Delay-Faktor beziehungsweise ein komplexer Faktor. Erst auf dem Einheitskreis wird daraus:

$$
z^{-1}=e^{-j\Omega}.
$$

Dann beschreibt es einen frequenzabhaengigen Phasenfaktor.

### Denkfalle 2: Die z-Transformation ist nicht nur die DTFT

Die DTFT ist die z-Transformation auf dem Einheitskreis. Die z-Transformation enthaelt zusaetzlich die radiale Dimension `r` und damit Informationen ueber Konvergenz, Pole und Stabilitaet.

### Denkfalle 3: Pole und Nullstellen sind keine Frequenzen

Pole und Nullstellen sind Punkte in der komplexen z-Ebene. Frequenzen liegen auf dem Einheitskreis:

$$
z=e^{j\Omega}.
$$

Ein Pol oder eine Nullstelle hat eine Frequenzrichtung ueber seinen Winkel, aber auch einen Radius.

### Denkfalle 4: Reines IIR bedeutet nicht automatisch Hochpass oder Tiefpass

Reine Rueckfuehrung erzeugt Nennerstrukturen. Je nach Koeffizienten entstehen glaettende oder resonante Kurven. Exakte Ausloeschungen brauchen Zaehlerstrukturen, also Feedforward.

## 23. Minimaler roter Faden fuer die Vorlesung

Fuer Studierende reicht folgender roter Faden:

1. Delay im Zeitbereich: `x[n-1]`.
2. z-Schreibweise: `x[n-1] \leftrightarrow z^{-1}X(z)`.
3. FIR: Eingangskopien werden ein Polynom in `z^{-1}`.
4. IIR: Ausgangskopien erzeugen einen Nenner.
5. Allgemein:

   $$
   H(z)=\frac{B(z)}{A(z)}.
   $$

6. Nullstellen:

   $$
   B(z)=0.
   $$

7. Pole:

   $$
   A(z)=0.
   $$

8. Frequenzgang:

   $$
   H(e^{j\Omega}).
   $$

Das ist der didaktische Kern. Alles Weitere ist Design- und Vertiefungswissen.
