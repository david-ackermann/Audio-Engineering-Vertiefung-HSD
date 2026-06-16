# Frequenzgang aus der Impulsantwort

Dieses Dokument beschreibt die didaktisch kurze Herleitung fuer Block 2:

> Wir kennen aus Vorlesung 6: Der Frequenzgang entsteht aus der Impulsantwort. Beim FIR ist die Impulsantwort endlich lang. Beim IIR ist sie theoretisch unendlich lang.

Ziel ist die Formel

$$
H(e^{j\Omega})
=
\frac{b_0}{1-p e^{-j\Omega}}.
$$

Die Herleitung bleibt bewusst nahe am Vorwissen aus FIR und DFT. Die z-Transformation wird hier noch nicht benoetigt.

## 1. Erinnerung: FIR aus Vorlesung 6

Bei einem FIR-Filter ist die Impulsantwort endlich:

$$
h[n]=0
\quad \text{fuer } n\ge N.
$$

Der Frequenzgang ist die Transformation der Impulsantwort:

$$
H(e^{j\Omega})
=
\sum_{n=0}^{N-1} h[n]e^{-j\Omega n}.
$$

Das ist eine endliche Summe. Deshalb kann man den Frequenzgang eines FIR-Filters sehr direkt aus der Impulsantwort berechnen.

Die DFT beziehungsweise FFT liefert davon Frequenzstuetzstellen. Dabei ist
`L` die DFT-Laenge; `N` bleibt hier die Anzahl der FIR-Taps:

$$
H[k]
=
\sum_{n=0}^{N-1} h[n]e^{-j2\pi k n/L}.
$$

Didaktischer Satz:

> Beim FIR ist der Frequenzgang die DFT/DTFT der endlichen Impulsantwort.

## 2. Gleiche Idee beim IIR

Beim IIR gilt dieselbe Grundidee:

$$
H(e^{j\Omega})
=
\sum_{n=0}^{\infty} h[n]e^{-j\Omega n}.
$$

Der Unterschied ist nur:

> Die Impulsantwort endet nicht nach endlich vielen Samples.

Deshalb steht beim IIR keine endliche Summe, sondern eine unendliche Summe.

## 3. Impulsantwort des einfachen IIR

Aus Block 1 kennen wir fuer das System

$$
y[n]=b_0x[n]+p\,y[n-1]
$$

die Impulsantwort fuer \(n\ge 0\):

$$
h[n]=b_0p^n,\qquad n\ge 0.
$$

Dabei beschreibt \(p^n\), wie die Rueckfuehrung von Sample zu Sample weiterlebt.

## 4. Einsetzen in den Frequenzgang

Wir setzen die Impulsantwort in die Frequenzgang-Summe ein:

$$
H(e^{j\Omega})
=
\sum_{n=0}^{\infty} b_0p^n e^{-j\Omega n}.
$$

Der Faktor \(b_0\) ist unabhaengig von \(n\), also kann man ihn ausklammern:

$$
H(e^{j\Omega})
=
b_0\sum_{n=0}^{\infty} p^n e^{-j\Omega n}.
$$

Jetzt fassen wir die beiden Potenzen zusammen:

$$
p^n e^{-j\Omega n}
=
\left(p e^{-j\Omega}\right)^n.
$$

Damit wird

$$
H(e^{j\Omega})
=
b_0\sum_{n=0}^{\infty}
\left(p e^{-j\Omega}\right)^n.
$$

## 5. Geometrische Reihe

Die Summe

$$
\sum_{n=0}^{\infty}
\left(p e^{-j\Omega}\right)^n
$$

ist eine geometrische Reihe.

Allgemein gilt:

$$
\sum_{n=0}^{\infty}q^n
=
\frac{1}{1-q}
\quad \text{fuer } |q|<1.
$$

Hier ist

$$
q=p e^{-j\Omega}.
$$

Also ist

$$
|q|
=
|p e^{-j\Omega}|
=
|p|\cdot |e^{-j\Omega}|.
$$

Da

$$
|e^{-j\Omega}|=1
$$

folgt

$$
|q|=|p|.
$$

Die Reihe konvergiert also fuer

$$
|p|<1.
$$

Das passt genau zur Stabilitaetsidee aus Block 1:

> Wenn die Impulsantwort abklingt, konvergiert die unendliche Summe.

## 6. Ergebnis

Mit

$$
q=p e^{-j\Omega}
$$

wird aus der geometrischen Reihe:

$$
\sum_{n=0}^{\infty}
\left(p e^{-j\Omega}\right)^n
=
\frac{1}{1-p e^{-j\Omega}}.
$$

Damit folgt:

$$
H(e^{j\Omega})
=
b_0\frac{1}{1-p e^{-j\Omega}}.
$$

Also:

$$
\boxed{
H(e^{j\Omega})
=
\frac{b_0}{1-p e^{-j\Omega}}
}
$$

## 7. Was ist \(H(e^{j\Omega})\)?

\(H(e^{j\Omega})\) ist der Frequenzgang des Systems.

Man kann ihn lesen als:

$$
H(e^{j\Omega})
=
\text{komplexe Verstaerkung bei der Frequenz } \Omega.
$$

Der Betrag beschreibt die Amplitudenaenderung:

$$
|H(e^{j\Omega})|
=
\text{Amplitudenfaktor}.
$$

Die Phase beschreibt die Phasenverschiebung:

$$
\arg\{H(e^{j\Omega})\}
=
\text{Phasenverschiebung}.
$$

Fuer die Vorlesung reicht hier als Merksatz:

> Der Frequenzgang sagt fuer jede Frequenz, wie stark sie durch das Filter veraendert wird.

## 8. Didaktische Kurzfassung fuer die Folie

FIR:

$$
H(e^{j\Omega})
=
\sum_{n=0}^{N-1} h[n]e^{-j\Omega n}
$$

IIR:

$$
H(e^{j\Omega})
=
\sum_{n=0}^{\infty} h[n]e^{-j\Omega n}
$$

Mit

$$
h[n]=b_0p^n,\qquad n\ge 0
$$

folgt

$$
H(e^{j\Omega})
=
b_0\sum_{n=0}^{\infty}
\left(p e^{-j\Omega}\right)^n.
$$

Geometrische Reihe:

$$
\sum_{n=0}^{\infty}q^n
=
\frac{1}{1-q}
\quad \text{fuer } |q|<1.
$$

Ergebnis:

$$
\boxed{
H(e^{j\Omega})
=
\frac{b_0}{1-p e^{-j\Omega}}
}
$$

## 9. Alternative Herleitung aus der Rekursion

Man kann dieselbe Formel auch direkt aus der Differenzengleichung herleiten, indem man

$$
x[n]=e^{j\Omega n}
$$

einsetzt und nutzt, dass ein LTI-System diese Frequenz nur in Betrag und Phase veraendert:

$$
y[n]=H(e^{j\Omega})e^{j\Omega n}.
$$

Diese Herleitung ist korrekt, aber abstrakter. Fuer den schnellen Vorlesungsweg ist die Herleitung ueber die bekannte Impulsantwort-Logik naheliegender.

## 10. Ausblick auf Vorlesung 8

Bis hierhin haben wir nur den Frequenzgang betrachtet. Die z-Transformation
wird in Vorlesung 8 direkt am Anfang eingefuehrt.

Didaktischer Anschluss:

- In Vorlesung 7 reicht \(H(e^{j\Omega})\).
- In Vorlesung 8 wird daraus \(H(z)\).
- Dann koennen dieselben Filterkurven geometrisch ueber Einheitskreis, Pole
  und Nullstellen gelesen werden.
