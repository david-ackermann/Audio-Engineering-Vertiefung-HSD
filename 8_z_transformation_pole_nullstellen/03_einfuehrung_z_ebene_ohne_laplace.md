# Einfuehrung in die z-Ebene ohne Laplace-Transformation

Dieses Dokument ist als Vorbereitungs- und Erklaerdokument fuer Vorlesung 8
gedacht. Es beantwortet vor allem die didaktische Frage:

> Was ist eigentlich die z-Ebene, wenn ich sie nicht ueber die
> Laplace-Transformation einfuehren moechte?

Kurzantwort:

> Die z-Ebene ist die komplexe Ebene, in der wir digitale Systeme nicht nur auf
> dem Frequenzkreis betrachten, sondern auch radial nach innen und aussen. Der
> Frequenzgang ist der Schnitt durch diese Ebene entlang des Einheitskreises.

## 1. Sollte man ueber die Laplace-Transformation gehen?

Fuer diese Vorlesung: eher nein.

Die Laplace-Transformation ist mathematisch eng verwandt mit der
z-Transformation. Fuer Studierende, die sie bereits kennen, kann man sagen:

> Die z-Transformation ist die diskrete Schwester der Laplace-Transformation.

Aber als Einstieg in die Vorlesung ist dieser Weg didaktisch unguenstig, wenn
Laplace nicht bekannt ist. Dann muesste man erst eine zweite, kontinuierliche
Transformation erklaeren, bevor man zur eigentlich benoetigten diskreten
Transformation kommt.

Fuer deine Vorlesung ist der bessere Weg:

1. Die Studierenden sehen zuerst ein Delay im Zeitbereich:
   \(y[n]=x[n-1]\).
2. Fuer einen Sinus wird daraus ein frequenzabhaengiger Phasenversatz.
3. Fuer komplexe Exponentialsignale wird das Delay zum Faktor
   \(e^{-j\Omega}\).
4. Dieser Faktor wird zu \(z^{-1}\) verallgemeinert.
5. Dadurch entsteht \(H(z)\).
6. Die z-Ebene erklaert dann Frequenzgang, Pole, Nullstellen und Stabilitaet.

So bleibt der Einstieg im bereits bekannten diskreten Denken.

## 2. Ausgangspunkt: Delay im Zeitbereich

Der didaktische Ausgangspunkt ist nicht sofort die vollstaendige
Systemfunktion, sondern der einfachste digitale Baustein:

$$
y[n]=x[n-1].
$$

Das ist ein Delay um ein Sample.

Fuer einen komplexen Sinus

$$
x[n]=e^{j\Omega n}
$$

folgt:

$$
y[n]
=
x[n-1]
=
e^{j\Omega(n-1)}
=
e^{-j\Omega}e^{j\Omega n}.
$$

Da

$$
x[n]=e^{j\Omega n}
$$

gilt:

$$
y[n]=e^{-j\Omega}x[n].
$$

Der Faktor

$$
e^{-j\Omega}
$$

ist also der Frequenzbereichs-Faktor eines Ein-Sample-Delays. Sein Betrag ist
1, seine Phase ist \(-\Omega\).

Allgemeiner steht

$$
e^{-jk\Omega}
$$

fuer eine Verzoegerung um \(k\) Samples.

Das ist noch keine z-Transformation. Das ist nur die bekannte Aussage:

> Eine Verschiebung im Zeitbereich wird fuer Sinusschwingungen zu einem
> Phasenfaktor.

## 3. Der entscheidende Schritt: \(e^{-j\Omega}\) wird zu \(z^{-1}\)

In der z-Schreibweise ersetzen wir den Frequenzfaktor

$$
e^{-j\Omega}
$$

durch den allgemeineren Faktor

$$
z^{-1}.
$$

Also:

$$
e^{-j\Omega}
\quad\longrightarrow\quad
z^{-1}.
$$

Damit wird aus

$$
e^{-jk\Omega}
$$

der Ausdruck

$$
z^{-k}.
$$

Der Frequenzgang

$$
H(e^{j\Omega})
$$

wird dadurch zur Systemfunktion

$$
H(z).
$$

## 4. Was ist \(z\)?

\(z\) ist eine komplexe Zahl.

Jede komplexe Zahl kann in Polarkoordinaten geschrieben werden als:

$$
z = r e^{j\Omega}.
$$

Dabei ist:

- \(r\) der Radius, also der Abstand vom Ursprung,
- \(\Omega\) der Winkel,
- \(e^{j\Omega}\) ein Punkt auf dem Einheitskreis.

Wenn \(r=1\), dann liegt \(z\) auf dem Einheitskreis:

$$
z = e^{j\Omega}.
$$

Genau dort liegt der bekannte Frequenzgang.

## 5. Was ist die z-Ebene?

Die z-Ebene ist die komplexe Ebene aller moeglichen Werte von \(z\).

Sie hat:

- eine Realachse,
- eine Imaginaerachse,
- den Ursprung \(z=0\),
- den Einheitskreis \(|z|=1\).

Grafisch:

```text
              Im{z}
                ^
                |
          .-----|-----.
       .        |        .
     .          |          .
----.-----------+-----------.----> Re{z}
     .          |          .
       .        |        .
          '-----|-----'
                |

        Kreis: |z| = 1
```

Der Einheitskreis ist didaktisch der wichtigste Teil:

> Auf dem Einheitskreis liest man den Frequenzgang.

Also:

$$
H(e^{j\Omega})
=
H(z)\big|_{z=e^{j\Omega}}.
$$

## 6. Warum braucht man mehr als den Einheitskreis?

Der Frequenzgang zeigt nur, wie das System auf Sinusschwingungen im stationaeren
Zustand reagiert.

Er beantwortet:

> Welche Frequenz wird wie stark verstaerkt oder abgeschwaecht, und welche
> Phase bekommt sie?

Aber der Frequenzgang allein zeigt nicht direkt:

- warum ein IIR stabil oder instabil ist,
- warum ein Filter ausschwingt,
- warum ein Pol Resonanz erzeugt,
- warum eine Nullstelle eine Ausloeschung erzeugt,
- wie Biquad-Koeffizienten geometrisch wirken.

Dafuer braucht man die ganze z-Ebene.

Die z-Ebene zeigt nicht nur den Winkel \(\Omega\), sondern auch den Radius
\(r\).

## 7. Winkel bedeutet Frequenz

Ein Punkt auf dem Einheitskreis hat die Form:

$$
z=e^{j\Omega}.
$$

Der Winkel \(\Omega\) entspricht der normierten Kreisfrequenz.

Einige wichtige Punkte:

$$
\Omega=0
\quad\Rightarrow\quad
z=1
$$

Das ist DC, also Gleichanteil.

$$
\Omega=\pi
\quad\Rightarrow\quad
z=-1
$$

Das ist die Nyquist-Frequenz.

Positive und negative Frequenzen liegen als obere und untere Haelfte des
Einheitskreises.

## 8. Radius bedeutet Abklingen oder Anwachsen

Der Radius \(r\) ist der neue Teil gegenueber dem normalen Frequenzgang.

Schreibe:

$$
z=r e^{j\Omega}.
$$

Dann gilt:

$$
z^{-n}
=
r^{-n} e^{-j\Omega n}.
$$

Der Faktor \(e^{-j\Omega n}\) beschreibt die Schwingung.

Der Faktor \(r^{-n}\) beschreibt eine radiale Gewichtung.

Noch anschaulicher ist die Wirkung bei Polen:

- Polradius kleiner als 1: abklingender Speicher
- Polradius gleich 1: nicht abklingender Speicher
- Polradius groesser als 1: wachsender Speicher

Das passt direkt zur Impulsantwort:

$$
h[n]=b_0 p^n.
$$

Wenn:

$$
|p|<1,
$$

dann klingt die Impulsantwort ab.

Wenn:

$$
|p|>1,
$$

dann waechst die Impulsantwort.

In der z-Ebene ist \(p\) die Polposition.

## 9. Einpoliges IIR als erstes Beispiel

Zeitbereich:

$$
y[n]=b_0x[n]+p\,y[n-1].
$$

Impulsantwort:

$$
h[n]=b_0p^n,\qquad n\ge 0.
$$

Frequenzgang:

$$
H(e^{j\Omega})
=
\frac{b_0}{1-p e^{-j\Omega}}.
$$

Jetzt ersetzen wir:

$$
e^{-j\Omega}
\quad\longrightarrow\quad
z^{-1}.
$$

Dann wird daraus:

$$
H(z)
=
\frac{b_0}{1-pz^{-1}}.
$$

Der Nenner ist:

$$
1-pz^{-1}.
$$

Ein Pol liegt dort, wo der Nenner null wird:

$$
1-pz^{-1}=0.
$$

Umstellen:

$$
pz^{-1}=1
$$

$$
z^{-1}=\frac{1}{p}
$$

$$
z=p.
$$

Das einpolige IIR hat also einen Pol bei:

$$
z=p.
$$

Damit wird die Stabilitaetsaussage geometrisch:

$$
|p|<1
\quad\Rightarrow\quad
\text{Pol innerhalb des Einheitskreises}
$$

und:

$$
|p|>1
\quad\Rightarrow\quad
\text{Pol ausserhalb des Einheitskreises}.
$$

## 10. Was macht ein Pol?

Ein Pol ist eine Stelle, an der der Nenner der Systemfunktion null wird.

Da

$$
H(z)=\frac{B(z)}{A(z)}
$$

gilt:

$$
A(z)=0
\quad\Rightarrow\quad
H(z)\to\infty.
$$

Anschaulich:

> Ein Pol ist eine Stelle, an der das System stark reagiert.

Liegt ein Pol nahe am Einheitskreis, dann wird der Frequenzgang in der Naehe
dieses Winkels gross.

Deshalb erzeugen Pole:

- Resonanz,
- langes Ausschwingen,
- Speicherwirkung,
- Stabilitaetsfragen.

## 11. Was macht eine Nullstelle?

Eine Nullstelle ist eine Stelle, an der der Zaehler null wird:

$$
B(z)=0.
$$

Dann gilt:

$$
H(z)=0.
$$

Anschaulich:

> Eine Nullstelle ist eine Stelle, an der das System ausloescht.

Liegt eine Nullstelle direkt auf dem Einheitskreis, dann wird die zugehoerige
Frequenz vollstaendig ausgeloescht.

Beispiel:

$$
H(z)=1-z^{-1}.
$$

Nullstelle:

$$
1-z^{-1}=0
$$

$$
z=1.
$$

Die Nullstelle liegt bei \(z=1\), also bei \(\Omega=0\). Das bedeutet:

> DC wird ausgeloescht.

Das ist ein einfacher Hochpass beziehungsweise Differenzfilter.

## 12. Warum ist der Einheitskreis so wichtig?

Ein digitales Audiosignal wird normalerweise als Summe diskreter Frequenzen
gedacht:

$$
e^{j\Omega n}.
$$

Diese Frequenzen entsprechen Punkten auf dem Einheitskreis:

$$
z=e^{j\Omega}.
$$

Wenn man wissen will, wie ein Filter klingt, betrachtet man also:

$$
H(z)
\quad\text{auf}\quad
|z|=1.
$$

Darum ist der Frequenzgang:

$$
H(e^{j\Omega})
=
H(z)\big|_{z=e^{j\Omega}}.
$$

Die z-Ebene ist mehr als der Frequenzgang:

- Der Einheitskreis zeigt das hoerbare Frequenzverhalten.
- Die Pole und Nullstellen in der ganzen Ebene erklaeren, warum dieses
  Verhalten entsteht.

## 13. Didaktische Kurzform fuer die Vorlesung

Eine moegliche Erklaerung fuer die Folie:

> Bisher haben wir Filter auf dem Frequenzkreis betrachtet:
>
> \[
> z=e^{j\Omega}.
> \]
>
> Das ist der Einheitskreis. Wenn wir nicht nur Punkte auf diesem Kreis
> zulassen, sondern alle komplexen Punkte \(z\), entsteht die z-Ebene. In
> dieser Ebene sehen wir, wo ein Filter ausloescht und wo es stark reagiert.
> Ausloeschungen heissen Nullstellen, starke Reaktionen heissen Pole.

Noch kuerzer:

> Die z-Ebene ist die Landkarte des digitalen Filters. Der Frequenzgang ist
> der Rundgang auf dem Einheitskreis.

## 14. Biquad in der z-Ebene

Der Biquad aus Vorlesung 7:

$$
y[n]
=
b_0x[n]+b_1x[n-1]+b_2x[n-2]
-a_1y[n-1]-a_2y[n-2]
$$

wird in der z-Ebene zu:

$$
H(z)
=
\frac{
b_0+b_1z^{-1}+b_2z^{-2}
}{
1+a_1z^{-1}+a_2z^{-2}
}.
$$

Der Zaehler:

$$
B(z)=b_0+b_1z^{-1}+b_2z^{-2}
$$

liefert die Nullstellen.

Der Nenner:

$$
A(z)=1+a_1z^{-1}+a_2z^{-2}
$$

liefert die Pole.

Ein Biquad kann also maximal:

- zwei Nullstellen,
- zwei Pole

haben.

Damit lassen sich viele typische Audiofilter geometrisch erklaeren:

- Tiefpass,
- Hochpass,
- Bandpass,
- Notch,
- Low-Shelf,
- High-Shelf,
- Peaking-EQ.

## 15. Wie wuerde man es mit Laplace verbinden?

Nur als Hintergrund fuer dich:

Bei kontinuierlichen Systemen arbeitet man mit der Laplace-Variable:

$$
s=\sigma+j\omega.
$$

Bei zeitdiskreten Systemen arbeitet man mit:

$$
z=r e^{j\Omega}.
$$

Die Verbindung entsteht durch Abtastung:

$$
z=e^{sT}.
$$

Dabei ist \(T\) die Abtastperiode.

Wenn:

$$
s=\sigma+j\omega,
$$

dann:

$$
z=e^{(\sigma+j\omega)T}
=
e^{\sigma T}e^{j\omega T}.
$$

Also:

$$
r=e^{\sigma T}
$$

und:

$$
\Omega=\omega T.
$$

Das ist mathematisch schoen, aber fuer deine Vorlesung nicht notwendig.

Didaktisch reicht:

> Die z-Ebene ist die komplexe Ebene der digitalen Systemfunktion. Der
> Einheitskreis ist der Frequenzgang. Der Radius erklaert Abklingen,
> Anwachsen und Stabilitaet.

## 16. Empfohlene Vorlesungsdramaturgie

Nicht so starten:

1. Laplace-Transformation
2. \(s\)-Ebene
3. Abbildung \(z=e^{sT}\)
4. z-Ebene

Das ist fuer diese Zielgruppe zu indirekt.

Besser:

1. Delay im Zeitbereich:

   $$
   y[n]=x[n-1]
   $$

2. Delay eines komplexen Sinus:

   $$
   e^{j\Omega(n-1)}
   =
   e^{-j\Omega}e^{j\Omega n}
   $$

3. Delay-Faktor:

   $$
   e^{-j\Omega}
   $$

4. Allgemeiner Delay-Operator:

   $$
   z^{-1}
   $$

5. Systemfunktion:

   $$
   H(z)
   $$

6. Frequenzgang als Einheitskreis:

   $$
   H(e^{j\Omega})=H(z)\big|_{z=e^{j\Omega}}
   $$

7. Pole und Nullstellen als Erklaerung der Filterkurven.

## 17. Merksaetze

- \(z\) ist eine komplexe Zahl.
- Die z-Ebene ist die komplexe Ebene aller \(z\)-Werte.
- Der Einheitskreis \(|z|=1\) ist der Ort des Frequenzgangs.
- Der Winkel auf dem Einheitskreis entspricht der Frequenz.
- Der Radius beschreibt Abklingen, Anwachsen und Stabilitaet.
- Nullstellen kommen aus dem Zaehler und erzeugen Ausloeschungen.
- Pole kommen aus dem Nenner und erzeugen Resonanz und Speicherwirkung.
- Fuer stabile kausale IIR-Filter muessen alle Pole innerhalb des
  Einheitskreises liegen.
