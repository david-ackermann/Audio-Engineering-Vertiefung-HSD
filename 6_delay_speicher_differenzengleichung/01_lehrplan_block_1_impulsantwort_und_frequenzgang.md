# Block 1: Impulsantwort und Frequenzgang

## Ziel des Blocks

Dieser Block eröffnet Vorlesung 6. Er war ursprünglich als Block 3 der fünften Vorlesung geplant, wurde dort aus Zeitgründen aber nicht mehr vorgestellt. Die Studierenden haben aus Vorlesung 5 bis hierhin gesehen:

- Ein System bildet $x[n]$ auf $y[n]$ ab.
- Ein LTI-System kann durch seine Impulsantwort $h[n]$ beschrieben werden.
- Die Ausgangsfolge entsteht durch diskrete Faltung:

  $$
  y[n]=x[n]*h[n]=\sum_m h[m]x[n-m]
  $$

Jetzt wird die zweite Sicht auf dieselbe Systemwirkung sauber nachgeholt:

> Die Impulsantwort beschreibt das System im Zeitbereich. Der Frequenzgang beschreibt dasselbe System im Frequenzbereich.

## Didaktischer Kern

Die Studierenden kennen aus den bisherigen Vorlesungen bereits DFT-Bins, Spektren und Folgen wie $X[k]$. Neu ist jetzt nicht die DFT an sich, sondern die Interpretation:

- Bisher: $X[k]$ beschreibt ein Signal.
- Jetzt: $H(e^{j\Omega})$ beschreibt ein System.
- Für Plots auf DFT-Bins darf weiterhin $H[k]$ verwendet werden.
- Sauber ist:

  $$
  H[k] := H(e^{j\Omega_k}),
  \qquad
  \Omega_k=\frac{2\pi k}{N}
  $$

Damit ist $H[k]$ die bekannte diskrete Plot-Darstellung, während $H(e^{j\Omega})$ die allgemeine Frequenzgang-Funktion des diskreten Systems ist.

## Notationsentscheidung für die Folien

### Empfehlung

Auf der ersten Folie des Blocks explizit beide Schreibweisen nebeneinander setzen:

$$
H(e^{j\Omega})=\sum_m h[m]e^{-j\Omega m}
$$

und

$$
H[k]=H(e^{j\Omega_k}),
\qquad
\Omega_k=\frac{2\pi k}{N}
$$

Dann in den Plots weiter mit $H[k]$ arbeiten, wenn die x-Achse der DFT-Binindex $k$ ist.

### Warum das sinnvoll ist

$H(e^{j\Omega})$ ist der Frequenzgang als Funktion über der normierten digitalen Kreisfrequenz $\Omega$. Das ist der korrekte Systembegriff.

$H[k]$ ist die abgetastete Darstellung dieses Frequenzgangs an den Frequenzstützstellen der DFT. Das ist die korrekte Plot- und Folienlogik, wenn die Achse mit Binindex $k$ beschriftet ist.

### Didaktischer Merksatz

> $X[k]$ ist ein abgetastetes Signalspektrum. $H[k]$ ist ein abgetasteter Frequenzgang. Beide leben auf denselben DFT-Bins, beschreiben aber unterschiedliche Dinge: Signal vs. System.

## Neue Storyline für Block 1

Der Block soll nicht abstrakt mit der Formel starten, sondern aus einer konkreten Beobachtung entstehen:

1. Ein LTI-System hat eine feste Impulsantwort $h[n]$.
2. Aus dieser Impulsantwort kann ich für eine gewählte DFT-Länge $N$ eine Folge von Frequenzgangwerten $H_N[k]$ berechnen.
3. Ein Eingangssignal $x[n]$ hat für dieselbe DFT-Länge $N$ ein Spektrum $X_N[k]$.
4. Wenn beide Folgen auf demselben Frequenzraster liegen, wirkt das System im Frequenzbereich binweise:

   $$
   Y_N[k]=H_N[k]\cdot X_N[k]
   $$

5. Die inverse DFT von $Y_N[k]$ liefert wieder eine Ausgangsfolge $y[n]$. Diese ist nach dem Tiefpass nicht mehr rechteckförmig, sondern geglättet.
6. Wenn die Beobachtungslänge geändert wird, passt das alte $H[k]$ nicht mehr als vollständige Bin-für-Bin-Beschreibung. Das System ist nicht anders geworden, aber das DFT-Raster ist anders.

Wichtig ist deshalb die sprachliche Korrektur:

> Nicht: Ich passe $h[n]$ an die Länge des Eingangssignals an.

> Besser: Ich taste dieselbe Systemantwort auf dem zur DFT-Länge passenden Frequenzraster ab.

Das System bleibt gleich. Die Impulsantwort $h[n]$ bleibt gleich. Nur die Darstellung als DFT-Bins ändert sich mit $N$.

Für ein gewähltes $N$ gilt:

$$
\Omega_k=\frac{2\pi k}{N}
$$

$$
H_N[k]=H(e^{j\Omega_k})
$$

und damit:

$$
Y_N[k]=H_N[k]\cdot X_N[k]
$$

Der zentrale Satz für die Folie:

> $H[k]$ ist keine allgemeine Systembeschreibung, sondern eine Abtastung von $H(e^{j\Omega})$ auf einem bestimmten DFT-Raster. Wenn sich $N$ ändert, ändert sich dieses Raster.

Die allgemeine, von $N$ unabhängige Beschreibung ist:

$$
H(e^{j\Omega})
=
\sum_{m=-\infty}^{\infty} h[m]e^{-j\Omega m}
$$

Bei endlicher Impulsantwort:

$$
H(e^{j\Omega})
=
\sum_{m=0}^{M-1} h[m]e^{-j\Omega m}
$$

Für jedes beliebige $N$ wird daraus:

$$
H_N[k]
=
H\left(e^{j\frac{2\pi k}{N}}\right)
$$

Kurz gesagt:

> $H(e^{j\Omega})$ beschreibt das System unabhängig von der Beobachtungslänge. $H_N[k]$ ist die passende DFT-Abtastung davon für ein konkretes $N$.

Für die Folie zur DFT-Multiplikation muss außerdem klar sein:

> Wenn über DFT und inverse DFT gerechnet wird, entsteht zunächst eine zirkuläre Faltung der Länge $N$. Damit sie der linearen Faltung entspricht, muss ausreichend aufgefüllt werden.

$$
N \geq N_x + N_h - 1
$$

## Ablaufvorschlag für 35 bis 45 Minuten

| Zeit | Inhalt | Tafel/Folie | Ziel |
|---:|---|---|---|
| 0-5 min | Rückblick auf Faltung | $y[n]=\sum_m h[m]x[n-m]$ | Zeitbereich reaktivieren |
| 5-10 min | System vs. Signal klären | $x[n]\rightarrow h[n]\rightarrow y[n]$ | $h[n]$ als Systemeigenschaft festigen |
| 10-18 min | Frequenzgang aus der Impulsantwort | $H(e^{j\Omega})=\sum_m h[m]e^{-j\Omega m}$ | Systemfunktion einführen |
| 18-25 min | DFT-Raster und Zero Padding | $H_N[k]=H(e^{j2\pi k/N})$ | $H[k]$ als N-abhängige Abtastung verstehen |
| 25-35 min | Spektrale Gewichtung eines Rechtecksignals | $Y_N[k]=H_N[k]X_N[k]$ | Systemwirkung als Bin-für-Bin-Gewichtung sehen |
| 35-42 min | Längeres Rechtecksignal und anderes Raster | $N=32$ vs. $N=64$ | zeigen, warum altes $H[k]$ nicht direkt passt |
| 42-45 min | Abschluss und Ausblick | $H(e^{j\Omega})$ unabhängig von $N$ | Übergang zu Block 2: Delay/Speicher |

Wenn nur 15 Minuten verfügbar sind, sollte der Block auf drei Aussagen reduziert werden:

1. $h[n]$ ist die Zeitbereichsbeschreibung.
2. $H(e^{j\Omega})$ ist die Frequenzbereichsbeschreibung.
3. $H[k]$ sind die DFT-Binwerte dieses Frequenzgangs.

## Folienvorschlag

### Folie 1: Rückblick aus Vorlesung 5

Titel:

> LTI-System im Zeitbereich

Inhalt:

$$
y[n]=x[n]*h[n]
$$

$$
y[n]=\sum_m h[m]x[n-m]
$$

Sprechtext:

> Wir haben ein LTI-System bisher vollständig im Zeitbereich beschrieben. Die Impulsantwort sagt, welche Antwort ein einzelner Sample-Anstoß erzeugt. Ein beliebiges Eingangssignal setzt sich aus vielen solchen Anstößen zusammen. Deshalb entsteht der Ausgang als Summe verschobener und skalierter Kopien von $h[n]$.

### Folie 2: Die neue Frage

Titel:

> Was macht dasselbe System mit Frequenzen?

Visualisierung:

- links: Impulsantwort $h[n]$
- rechts: Frequenzgang $H(e^{j\Omega})$

Sprechtext:

> Ein LTI-System verändert Sinusanteile nicht in ihrer Frequenz. Es ändert ihre Amplitude und Phase. Genau diese frequenzabhängige Änderung ist der Frequenzgang.

Kernsatz:

> Gleiche Frequenz rein, gleiche Frequenz raus, aber mit anderem Betrag und anderer Phase.

### Folie 3: Frequenzgang als Transformation der Impulsantwort

Titel:

> Aus $h[n]$ wird $H(e^{j\Omega})$

Formel:

$$
H(e^{j\Omega})=\sum_m h[m]e^{-j\Omega m}
$$

Erläuterung:

- $h[n]$: System im Zeitbereich
- $H(e^{j\Omega})$: System im Frequenzbereich
- $\Omega$: digitale Kreisfrequenz in rad/Sample

Sprechtext:

> Das sieht aus wie die Fourier-Transformation einer diskreten Folge. Genau das ist der Punkt: Die Impulsantwort ist eine Folge, und ihr Frequenzinhalt beschreibt, wie das System auf Frequenzen wirkt.

### Folie 4: Warum nicht einfach $H[k]$?

Titel:

> Von der Funktion zum Plot: $H(e^{j\Omega})$ und $H[k]$

Formeln:

$$
\Omega_k=\frac{2\pi k}{N}
$$

$$
H[k]=H(e^{j\Omega_k})
$$

Sprechtext:

> Bisher haben wir Spektren meistens als DFT-Folgen über dem Binindex $k$ gezeichnet. Das bleibt für Plots völlig in Ordnung. Neu ist nur: Beim System gibt es zunächst eine Frequenzgang-Funktion $H(e^{j\Omega})$. Wenn wir diese Funktion auf unseren DFT-Bins auswerten, erhalten wir die Folge $H[k]$.

Korrektursatz:

> $H[k]$ ist nicht falsch. Es ist die abgetastete Darstellung von $H(e^{j\Omega})$.

### Folie 5: Tiefpass als Beispiel

Titel:

> Beispiel: Tiefpass auf DFT-Bins

Visualisierung:

- $h_\mathrm{TP}[n]$ im Zeitbereich
- $|H_N[k]|$ für verschiedene DFT-Längen $N$
- zuerst nur die DFT-Stützstellen zeigen
- danach die gemeinsame Hüllkurve $|H(e^{j\Omega})|$ ergänzen

Sprechtext:

> Im Zeitbereich sehen wir dieselbe ausklingende Impulsantwort. Im Frequenzbereich sehen wir zunächst nur einzelne DFT-Bins. Wenn $N$ größer wird, wird das Frequenzraster feiner. Das System ist aber nicht anders geworden: Die Punkte liegen auf derselben Systemantwort $H(e^{j\Omega})$.

Wichtig:

Nicht zu tief in Filterdesign gehen. Der Fokus ist: Zeitform und Frequenzwirkung gehören zusammen, und $H[k]$ ist nur eine Rasterdarstellung.

### Folie 6: Systemwirkung im Frequenzbereich

Titel:

> Ein System gewichtet das Spektrum

Formeln:

$$
y[n]=x[n]*h[n]
$$

$$
Y(e^{j\Omega})=X(e^{j\Omega})H(e^{j\Omega})
$$

Für ein gewähltes DFT-Raster:

$$
\Omega_k=\frac{2\pi k}{N}
$$

$$
H_N[k]=H(e^{j\Omega_k})
$$

$$
Y_N[k]=H_N[k]X_N[k]
$$

Sprechtext:

> Im Zeitbereich ist die Systemwirkung Faltung. Im Frequenzbereich wird daraus eine binweise Gewichtung. Ein Rechtecksignal hat bestimmte Frequenzanteile. Der Tiefpass multipliziert jeden passenden Bin mit seiner Systemantwort. Nach der inversen DFT ist das Signal geglättet und nicht mehr rechteckförmig.

Didaktischer Hinweis:

Die DFT-Form $Y_N[k]=H_N[k]X_N[k]$ gilt für ein gemeinsames DFT-Raster. Wenn über DFT und inverse DFT gerechnet wird, entsteht zunächst zirkuläre Faltung. Für lineare Faltung muss ausreichend aufgefüllt werden:

$$
N\geq N_x+N_h-1
$$

### Folie 7: Warum $H(e^{j\Omega})$ nötig ist

Titel:

> Dasselbe System, anderes Raster

Visualisierung:

- längeres periodisches Rechtecksignal $x[n]$
- $X_N[k]$ für größeres $N$
- altes $H[k]$ für kleineres $N$ passt nicht zu jedem neuen Bin
- danach $H_N[k]=H(e^{j2\pi k/N})$ für das neue Raster zeigen

Sprechtext:

> Wenn das Eingangssignal länger betrachtet wird, entstehen mehr DFT-Bins. Das alte $H[k]$ ist deshalb nicht falsch, aber es passt nicht mehr als vollständiger Multiplikator zu jedem neuen Bin. Die Impulsantwort bleibt gleich. Wir werten nur dieselbe Systemantwort auf einem feineren Raster aus.

Merksatz:

> $H(e^{j\Omega})$ beschreibt das System unabhängig von der Beobachtungslänge. $H_N[k]$ ist die passende DFT-Abtastung davon für ein konkretes $N$.

### Folie 8: Signal oder System?

Titel:

> Nicht verwechseln: Signal und System

Tabelle:

| Größe | Beschreibt | Beispiel |
|---|---|---|
| $x[n]$ | Eingangssignal im Zeitbereich | Audiosignal |
| $X[k]$ | Eingangsspektrum auf DFT-Bins | Frequenzanteile des Signals |
| $h[n]$ | Impulsantwort des Systems | Raum, Lautsprecher, Filter |
| $H_N[k]$ | Frequenzgang auf DFT-Bins | Wirkung des Systems auf Frequenzen |
| $y[n]$ | Ausgangssignal im Zeitbereich | bearbeitetes Signal |
| $Y[k]$ | Ausgangsspektrum | Frequenzanteile nach dem System |

Sprechtext:

> Ein Spektrum beschreibt ein Signal. Ein Frequenzgang beschreibt ein System. Beide können über denselben Binindex gezeichnet werden, aber sie beantworten unterschiedliche Fragen.

### Folie 9: Abschlussfolie

Titel:

> Drei Sichten auf dasselbe LTI-System

Inhalt:

$$
h[n]
\quad\Longleftrightarrow\quad
H(e^{j\Omega})
$$

$$
y[n]=x[n]*h[n]
\quad\Longleftrightarrow\quad
Y(e^{j\Omega})=X(e^{j\Omega})H(e^{j\Omega})
$$

Merksätze:

- $h[n]$ beschreibt das System im Zeitbereich.
- $H(e^{j\Omega})$ beschreibt das System im Frequenzbereich.
- $H_N[k]$ sind Frequenzgangwerte auf den DFT-Bins einer gewählten Länge $N$.
- Der nächste Block baut daraus konkrete DSP-Strukturen: Delay, Speicher und Differenzengleichung.

## Formelsammlung für die Folien

Frequenzgang:

```latex
\[
H(e^{j\Omega})=\sum_m h[m]e^{-j\Omega m}
\]
```

DFT-Bins:

```latex
\[
\Omega_k=\frac{2\pi k}{N}
\]
```

Abgetasteter Frequenzgang:

```latex
\[
H[k]=H(e^{j\Omega_k})
\]
```

Zeitbereich:

```latex
\[
y[n]=x[n]*h[n]=\sum_m h[m]x[n-m]
\]
```

Frequenzbereich:

```latex
\[
Y(e^{j\Omega})=X(e^{j\Omega})H(e^{j\Omega})
\]
```

DFT-Bin-Darstellung:

```latex
\[
Y[k]=X[k]H[k]
\]
```

Gruppenlaufzeit:

```latex
\[
\tau_g[k]
=
-\left.
\frac{d\varphi(\Omega)}{d\Omega}
\right|_{\Omega=\Omega_k}
\]
```

Phase:

```latex
\[
\varphi[k]=\arg\{H(e^{j\Omega_k})\}
\]
```

## Empfohlene Schreibweise in deiner bestehenden Folie

Die vorhandene Schreibweise mit $H[k]$ ist nicht falsch, wenn die Achse als DFT-Binindex $k$ dargestellt ist. Ich würde aber eine Brückenfolie davor setzen und danach präziser schreiben:

$$
H_\mathrm{TP}[k]=H_\mathrm{TP}(e^{j\Omega_k})
$$

Dann bleibt die bestehende Darstellung mit $H[k]$, $X[k]$ und $Y[k]$ verständlich und fachlich sauber.

Für die Blocküberschrift oder die neue Theorieformel sollte dagegen $H(e^{j\Omega})$ stehen, weil dort der Frequenzgang als Systemfunktion eingeführt wird.

## Kurzantwort zur Notationsfrage

Nein, es ist kein Problem, dass jetzt erstmals $H(e^{j\Omega})$ auftaucht. Es ist sogar sinnvoll, weil damit klar wird:

- $H(e^{j\Omega})$ ist der Frequenzgang des diskreten Systems als Funktion.
- $H[k]$ sind Werte dieses Frequenzgangs an den DFT-Bins.
- Die Studierenden kennen $k$ schon; du nutzt $k$ jetzt als Abtastgitter für eine Systemfunktion.

Ich würde also nicht komplett auf $H[k]$ verzichten. Ich würde nur einmal sauber definieren:

$$
H[k] := H(e^{j\Omega_k})
$$

Danach kannst du für geplottete Abbildungen weiter $H[k]$ verwenden.
