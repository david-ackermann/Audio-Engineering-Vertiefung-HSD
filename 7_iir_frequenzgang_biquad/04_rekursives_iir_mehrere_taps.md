# Von der Impulsantwort zum Biquad

Dieses Dokument ist fuer Vorlesung 7 bewusst ohne z-Transformation formuliert.
Die zentrale Groesse ist zunaechst der Frequenzgang

$$
H(e^{j\Omega}).
$$

Die z-Transformation, die z-Ebene sowie Pole und Nullstellen werden erst in
Vorlesung 8 eingefuehrt.

## 1. Frequenzgang aus der Impulsantwort

Aus Vorlesung 6 ist bekannt: Ein LTI-System ist vollstaendig durch seine
Impulsantwort `h[n]` beschrieben.

Wenn das Eingangssignal `x[n]` durch das System laeuft, entsteht:

$$
y[n]
=
\sum_{m=-\infty}^{\infty} h[m]\,x[n-m]
$$

Das ist die Faltung.

Setzt man als Eingang eine komplexe Schwingung ein,

$$
x[n]=e^{j\Omega n},
$$

dann folgt:

$$
y[n]
=
\sum_{m=-\infty}^{\infty}
h[m]\,e^{j\Omega(n-m)}
$$

Den Term kann man aufteilen:

$$
y[n]
=
e^{j\Omega n}
\sum_{m=-\infty}^{\infty}
h[m]\,e^{-j\Omega m}
$$

Der zweite Faktor haengt nicht mehr von `n` ab. Er ist nur noch eine komplexe
Zahl fuer die gewaehlte Frequenz `Omega`.

Definition:

$$
H(e^{j\Omega})
=
\sum_{m=-\infty}^{\infty}
h[m]\,e^{-j\Omega m}
$$

Damit gilt:

$$
y[n]
=
H(e^{j\Omega})\,e^{j\Omega n}
$$

Didaktische Lesart:

> Ein LTI-System aendert bei einer Sinusschwingung nicht die Frequenz, sondern
> nur Amplitude und Phase. Genau diese Aenderung beschreibt
> `H(e^{j\Omega})`.

## 2. Bekannter Fall: einpoliges IIR

Das bisherige Einstiegsbeispiel lautet:

$$
y[n]
=
b_0x[n]
+
p\,y[n-1]
$$

Bei einem Dirac-Impuls als Eingang ergibt sich:

$$
h[0]=b_0
$$

$$
h[1]=b_0p
$$

$$
h[2]=b_0p^2
$$

und allgemein:

$$
h[n]=b_0p^n
\qquad n\ge 0
$$

Der Frequenzgang ist die Summe ueber die Impulsantwort:

$$
H(e^{j\Omega})
=
\sum_{n=0}^{\infty} b_0p^n e^{-j\Omega n}
$$

`b_0` ausklammern:

$$
H(e^{j\Omega})
=
b_0
\sum_{n=0}^{\infty}
\left(p e^{-j\Omega}\right)^n
$$

Das ist eine geometrische Reihe mit

$$
q=p e^{-j\Omega}.
$$

Fuer

$$
|p|<1
$$

konvergiert sie:

$$
\sum_{n=0}^{\infty}q^n
=
\frac{1}{1-q}
$$

also:

$$
H(e^{j\Omega})
=
\frac{b_0}{1-p e^{-j\Omega}}
$$

Das ist die bekannte Uebertragungsfunktion im Frequenzbereich fuer das
einpolige IIR.

## 3. Reines rekursives IIR mit mehreren Feedback-Taps

Jetzt wird die Rueckfuehrung erweitert:

$$
y[n]
=
b_0x[n]
-
\sum_{r=1}^{M}a_r y[n-r]
$$

Ausgeschrieben:

$$
y[n]
=
b_0x[n]
-
a_1y[n-1]
-
a_2y[n-2]
-
\ldots
-
a_My[n-M]
$$

Der Zusammenhang mit dem bisherigen `p` ist fuer `M=1`:

$$
y[n]=b_0x[n]+p\,y[n-1]
$$

und

$$
y[n]=b_0x[n]-a_1y[n-1].
$$

Damit gilt:

$$
p=-a_1.
$$

### Impulsantwort-Rekursion

Fuer den Frequenzgang betrachten wir wieder die Impulsantwort. Setze also

$$
x[n]=\delta[n].
$$

Dann ist der Ausgang die Impulsantwort:

$$
y[n]=h[n].
$$

Die Rekursion wird zu:

$$
h[n]
=
b_0\delta[n]
-
\sum_{r=1}^{M}a_r h[n-r]
$$

Jetzt wird der Frequenzgang als Summe ueber die Impulsantwort gebildet:

$$
H(e^{j\Omega})
=
\sum_{n=-\infty}^{\infty} h[n]e^{-j\Omega n}
$$

Setze die Impulsantwort-Rekursion ein:

$$
H(e^{j\Omega})
=
\sum_n
\left(
b_0\delta[n]
-
\sum_{r=1}^{M}a_r h[n-r]
\right)
e^{-j\Omega n}
$$

Der erste Term ist:

$$
\sum_n b_0\delta[n]e^{-j\Omega n}
=
b_0
$$

Fuer den Rueckfuehrungsteil muessen wir einen Schritt genauer hinschauen.
In der Summe taucht nicht direkt `h[n]` auf, sondern eine verschobene
Impulsantwort:

$$
h[n-r]
$$

Das bedeutet:

- bei `r=1`: die Impulsantwort ist um ein Sample nach rechts verschoben,
- bei `r=2`: die Impulsantwort ist um zwei Samples nach rechts verschoben,
- allgemein: `h[n-r]` ist eine um `r` Samples verzoegerte Kopie von `h[n]`.

Wir nennen diese verschobene Folge kurz

$$
g_r[n]=h[n-r].
$$

Gesucht ist nun der Frequenzgang dieser verschobenen Folge:

$$
\sum_n h[n-r]e^{-j\Omega n}
$$

Dazu machen wir einen Indexwechsel. Setze

$$
m=n-r.
$$

Dann ist

$$
n=m+r.
$$

Wichtig: Wenn `n` ueber alle ganzzahligen Samples laeuft, dann laeuft auch
`m` ueber alle ganzzahligen Samples. Wir duerfen die Summe also umschreiben:

$$
\sum_n h[n-r]e^{-j\Omega n}
=
\sum_m h[m]e^{-j\Omega (m+r)}.
$$

Jetzt wird der Exponent aufgeteilt:

$$
e^{-j\Omega (m+r)}
=
e^{-j\Omega m}e^{-j\Omega r}.
$$

Der Faktor \(e^{-j\Omega r}\) haengt nicht von `m` ab. Deshalb darf er vor
die Summe gezogen werden:

$$
\sum_m h[m]e^{-j\Omega (m+r)}
=
e^{-j\Omega r}
\sum_m h[m]e^{-j\Omega m}.
$$

Die verbleibende Summe ist jetzt wieder die Summe, mit der wir den
Frequenzgang der urspruenglichen Impulsantwort definiert haben.

Das `H` kommt also nicht aus einer neuen Rechnung. Es ist nur die Abkuerzung
fuer diese ganze Summe:

$$
H(e^{j\Omega})
:=
\sum_m h[m]e^{-j\Omega m}.
$$

Man kann es so lesen:

- `h[m]` ist die Impulsantwort im Zeitbereich,
- \(e^{-j\Omega m}\) ist die komplexe Testschwingung fuer die Frequenz
  \(\Omega\),
- die Summe misst, wie stark die Impulsantwort diese Frequenz gewichtet,
- das Ergebnis nennen wir Frequenzgang \(H(e^{j\Omega})\).

Damit ist

$$
\sum_m h[m]e^{-j\Omega m}
=
H(e^{j\Omega}).
$$

Damit folgt:

$$
\sum_n h[n-r]e^{-j\Omega n}
=
e^{-jr\Omega}H(e^{j\Omega})
$$

Didaktisch ist das ein sehr wichtiger Schritt:

> Eine Verzoegerung um `r` Samples veraendert den Betrag des Frequenzgangs
> nicht. Sie multipliziert den Frequenzgang nur mit einem frequenzabhaengigen
> Phasenfaktor \(e^{-jr\Omega}\).

Passende Bildserie fuer die Vorlesung:

- `png_storyboards/04_verschobene_impulsantwort/04A_shifted_ir_frequency_response`
- `png_storyboards/04_verschobene_impulsantwort/04B_weighted_shifted_spectra`

Die Serie zeigt fuer `r=0` bis `r=4`, dass der Betrag gleich bleibt, waehrend
die Phase mit jedem zusaetzlichen Sample um `-Omega` staerker faellt. Dazu
zeigt sie pro `r` die verschobene Impulsantwort im Zeitbereich und die Phase
jeweils als Einzelplot. Der Betrag wird ebenfalls pro `r` als eigenes Bild
gezeigt; die Kurve aendert sich dabei nicht, nur der Titel zeigt den aktuellen
Index.

Fuer `r=1` ist der Faktor

$$
e^{-j\Omega}.
$$

Fuer `r=2` ist der Faktor

$$
e^{-j2\Omega}.
$$

Fuer `r` Samples ist der Faktor allgemein

$$
e^{-jr\Omega}.
$$

Das ist dieselbe Verschiebungsregel, die die Studierenden bereits aus der DFT
kennen: Eine Verschiebung im Zeitbereich wird im Frequenzbereich zu einem
Phasenfaktor. In Vorlesung 7 benutzen wir diese Regel aber noch ohne
z-Transformation.

Damit:

$$
H(e^{j\Omega})
=
b_0
-
\sum_{r=1}^{M}
a_r e^{-jr\Omega}H(e^{j\Omega})
$$

Alle Terme mit `H(e^{j\Omega})` auf eine Seite:

$$
H(e^{j\Omega})
+
\sum_{r=1}^{M}
a_r e^{-jr\Omega}H(e^{j\Omega})
=
b_0
$$

Ausklammern:

$$
H(e^{j\Omega})
\left(
1+\sum_{r=1}^{M}a_r e^{-jr\Omega}
\right)
=
b_0
$$

Also:

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

Didaktischer Punkt:

> Mehrere Feedback-Taps machen den Nenner komplexer. Dadurch koennen
> Resonanzen und komplexere Kurven entstehen. Da der Zaehler aber nur `b_0`
> ist, gibt es keine gezielte Ausloeschung durch Eingangskopien.

## 4. Warum Feedforward noetig wird

Ein reines rekursives Filter kann Frequenzen unterschiedlich stark verstaerken
oder abschwaechen. Aber es besitzt keinen Zaehlerausdruck, der fuer eine
bestimmte Frequenz exakt null werden kann.

Beispiel Hochpass-Idee:

Ein Hochpass soll konstante Signale entfernen. Fuer ein konstantes Signal gilt:

$$
x[n]=C
$$

Ein Differenzglied leistet genau das:

$$
y[n]=x[n]-x[n-1]
$$

Denn:

$$
y[n]=C-C=0
$$

Das ist kein Feedback-Effekt. Das ist Feedforward:

$$
b_0x[n]+b_1x[n-1]
$$

mit

$$
b_0=1,\qquad b_1=-1.
$$

Merksatz:

> Feedback erzeugt Speicher und Resonanz. Feedforward erzeugt gezielte
> Ausloeschung durch Vergleich von Eingangskopien.

## 5. Kombination aus Feedforward und Feedback

Die allgemeine rekursive Filtergleichung kombiniert beide Seiten:

$$
y[n]
=
\sum_{k=0}^{N-1}b_kx[n-k]
-
\sum_{r=1}^{M}a_r y[n-r]
$$

Impulsantwort-Rekursion:

$$
h[n]
=
\sum_{k=0}^{N-1}b_k\delta[n-k]
-
\sum_{r=1}^{M}a_r h[n-r]
$$

Wieder wird der Frequenzgang als Summe ueber die Impulsantwort gebildet:

$$
H(e^{j\Omega})
=
\sum_n h[n]e^{-j\Omega n}.
$$

Jetzt wird die Impulsantwort-Rekursion eingesetzt:

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

Nun wird nur die Summe getrennt. Das ist der wichtige didaktische
Zwischenschritt:

$$
H(e^{j\Omega})
=
\sum_n
\sum_{k=0}^{N-1}b_k\delta[n-k]e^{-j\Omega n}
-
\sum_n
\sum_{r=1}^{M}a_r h[n-r]e^{-j\Omega n}.
$$

Weil `b_k` und `a_r` nicht vom Summationsindex `n` abhaengen, duerfen sie vor
die jeweilige innere Summe:

$$
H(e^{j\Omega})
=
\sum_{k=0}^{N-1}b_k
\sum_n \delta[n-k]e^{-j\Omega n}
-
\sum_{r=1}^{M}a_r
\sum_n h[n-r]e^{-j\Omega n}.
$$

Jetzt kann man beide Teile getrennt lesen.

### Feedforward-Teil

Der neue Teil ist der Feedforward-Zweig. Er enthaelt nur verschobene
Dirac-Impulse:

$$
\sum_n \delta[n-k]e^{-j\Omega n}.
$$

Die Folge \(\delta[n-k]\) ist nur bei \(n=k\) ungleich null. Deshalb bleibt in
der Summe genau ein Term uebrig:

$$
\sum_n \delta[n-k]e^{-j\Omega n}
=
e^{-jk\Omega}.
$$

Fuer die ersten Werte sieht man das direkt:

$$
k=0:\quad
\sum_n \delta[n]e^{-j\Omega n}=1
$$

$$
k=1:\quad
\sum_n \delta[n-1]e^{-j\Omega n}=e^{-j\Omega}
$$

$$
k=2:\quad
\sum_n \delta[n-2]e^{-j\Omega n}=e^{-j2\Omega}
$$

Damit liefert der komplette Feedforward-Teil:

$$
\sum_{k=0}^{N-1}b_k e^{-jk\Omega}.
$$

Das ist genau der FIR-Frequenzgang aus Vorlesung 6.

### Feedback-Teil

Den Feedback-Teil kennen wir bereits aus der Herleitung des rein rekursiven
Filters. Fuer eine um `r` Samples verschobene Impulsantwort gilt:

$$
\sum_n h[n-r]e^{-j\Omega n}
=
e^{-jr\Omega}H(e^{j\Omega}).
$$

Damit wird der Feedback-Teil:

$$
\sum_{r=1}^{M}a_r
\sum_n h[n-r]e^{-j\Omega n}
=
\sum_{r=1}^{M}a_r e^{-jr\Omega}H(e^{j\Omega}).
$$

Jetzt die beiden bekannten Bausteine verwenden:

$$
H(e^{j\Omega})
=
\sum_{k=0}^{N-1} b_k e^{-jk\Omega}
-
\sum_{r=1}^{M} a_r e^{-jr\Omega} H(e^{j\Omega}).
$$

Alle Terme mit \(H(e^{j\Omega})\) auf die linke Seite:

$$
H(e^{j\Omega})
+
\sum_{r=1}^{M} a_r e^{-jr\Omega} H(e^{j\Omega})
=
\sum_{k=0}^{N-1} b_k e^{-jk\Omega}.
$$

Ausklammern:

$$
H(e^{j\Omega})
\left(
1+
\sum_{r=1}^{M} a_r e^{-jr\Omega}
\right)
=
\sum_{k=0}^{N-1} b_k e^{-jk\Omega}.
$$

Damit:

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

- Der Zaehler entsteht aus Eingangskopien `x[n-k]`.
- Der Nenner entsteht aus Ausgangskopien `y[n-r]`.
- Der Zaehler kann gezielte Ausloeschungen erzeugen.
- Der Nenner kann Resonanz, Steilheit und Ausschwingen erzeugen.

Damit wird klar, warum die Kombination aus Feedforward und Feedback fuer
Audiofilter so wichtig ist.

## 6. Biquad als Praxisform

Die wichtigste praktische Form fuer viele Audiofilter ist das Biquad:

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

Der Frequenzgang lautet:

$$
H(e^{j\Omega})
=
\frac{
b_0+b_1e^{-j\Omega}+b_2e^{-j2\Omega}
}{
1+a_1e^{-j\Omega}+a_2e^{-j2\Omega}
}
$$

Warum diese Form so wichtig ist:

- nur fuenf freie Koeffizienten bei normiertem Nenner,
- sehr effizient in Echtzeit,
- stabil gut kontrollierbar,
- in Ketten kombinierbar,
- reicht fuer viele typische Audiofilter.

## 7. Typische Filter mit Biquads

### Tiefpass

Ein Tiefpass laesst tiefe Frequenzen durch und daempft hohe Frequenzen.

Kurvenidee:

$$
|H(e^{j0})|\approx 1
$$

und

$$
|H(e^{j\pi})|\approx 0
$$

Beim Biquad entsteht das durch passende Kombination von Feedforward und
Feedback: Der Zaehler sorgt fuer die hohe Frequenzdaempfung, der Nenner
bestimmt Steilheit und gegebenenfalls Resonanz.

### Hochpass

Ein Hochpass daempft tiefe Frequenzen und laesst hohe Frequenzen durch.

Kurvenidee:

$$
|H(e^{j0})|\approx 0
$$

Das braucht Feedforward, weil konstante Signale nur durch Differenzbildung von
Eingangskopien exakt entfernt werden koennen.

### Bandpass

Ein Bandpass laesst einen mittleren Frequenzbereich durch und daempft darunter
und darueber.

Beim Biquad kann der Nenner eine Resonanz im Zielbereich erzeugen, waehrend der
Zaehler tiefe und hohe Bereiche abschwaecht.

### Notch

Ein Notch unterdrueckt einen engen Frequenzbereich.

Das zentrale Prinzip ist eine gezielte Ausloeschung bei einer Frequenz. Diese
Ausloeschung kommt aus dem Feedforward-Teil. Der Feedback-Teil kann die Kerbe
schmaler und kontrollierter machen.

### Low-Shelf

Ein Low-Shelf hebt oder senkt tiefe Frequenzen gegenueber hohen Frequenzen.

Typisch fuer Audio:

- Bass anheben,
- Bass absenken,
- tonale Korrektur ohne schmalen Peak.

### High-Shelf

Ein High-Shelf hebt oder senkt hohe Frequenzen gegenueber tiefen Frequenzen.

Typisch fuer Audio:

- Brillanz erhoehen,
- scharfe Hoehen absenken,
- tonale Korrektur im oberen Frequenzbereich.

### Peaking-EQ

Ein Peaking-EQ hebt oder senkt einen Bereich um eine Mittenfrequenz.

Typische Parameter:

- Mittenfrequenz,
- Gain,
- Guete beziehungsweise Bandbreite.

Das ist fuer parametrische Equalizer besonders wichtig.

## 8. Uebergang zu Vorlesung 8

Bis hierhin reicht fuer Vorlesung 7:

1. Frequenzgang als Summe ueber die Impulsantwort verstehen.
2. Einpoliges IIR sauber herleiten.
3. Mehrere Feedback-Taps als reinen Nenner verstehen.
4. Feedforward als Quelle gezielter Ausloeschung motivieren.
5. Biquad als praktische Standardform vorstellen.

Vorlesung 8 kann dann erklaeren, warum diese Strukturen in der z-Ebene als
geometrische Objekte erscheinen:

- `z^{-1}` als Delay-Sprache,
- Systemfunktion `H(z)`,
- Pole,
- Nullstellen,
- Biquad-Design in der z-Ebene.
