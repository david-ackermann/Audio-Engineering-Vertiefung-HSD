# Lehrkonzept: Systeme, diskrete Faltung und Frequenzgang-Anschluss

**Veranstaltungskontext:** Audio Engineering / Digitale Signalverarbeitung, Bachelor Vertiefung  
**Zielumfang:** ca. 120 Minuten inklusive Orga, Wiederholung und kurzer Pause  
**Aktueller Stand:** Vorlesung 5 endete aus Zeitgründen bei Block 2: diskrete Faltung. Der ursprünglich geplante Block 3 zu Impulsantwort und Frequenzgang wird als Block 1 in Vorlesung 6 nachgeholt. Delay, Speicher und FIR-Differenzengleichung folgen danach in Vorlesung 6; IIR/Biquad folgt in Vorlesung 7, $H(z)$ erst in Vorlesung 8.

## 1. Didaktische Hauptfrage

> Nicht mehr: Was steckt im Signal? Sondern: Was macht ein System mit dem Signal?

Die Studierenden kennen aus den bisherigen Vorlesungen diskrete Folgen, DFT, Leakage, STFT und iSTFT. In Vorlesung 5 wechselt die Perspektive von der Beobachtung eines Signals zur Wirkung eines Systems. Ein Equalizer, ein Raum, ein Lautsprecher, ein Delay oder ein Reverb werden als Systeme gelesen, die aus einem Eingang $x[n]$ einen Ausgang $y[n]$ erzeugen.

Der wichtigste Begriffswechsel:

- Eine Fensterfunktion $w[n]$ ist eine Beobachtungsoperation.
- Eine Impulsantwort $h[n]$ ist eine Systemeigenschaft.
- Faltung beschreibt Systemwirkung, nicht nur eine Rechenoperation.

## 2. Lernziele

Nach Vorlesung 5 sollen die Studierenden:

1. ein diskretes System als Abbildung $x[n]\mapsto y[n]$ beschreiben können,
2. den diskreten Impuls $\delta[n]$ als einzelnes Sample-Testsignal erklären können,
3. die Impulsantwort $h[n]$ als Antwort eines Systems auf $\delta[n]$ deuten können,
4. erklären können, warum eine einzige Impulsantwort nur bei LTI-Systemen das System vollständig beschreibt,
5. die diskrete Faltung

   $$
   y[n]=\sum_m x[m]h[n-m]
   $$

   als Summe verschobener und gewichteter Impulsantworten lesen können,
6. die Dirac-Faltung $x[n]*\delta[n]=x[n]$ als Einstieg in die Faltungsmechanik verstehen,
7. erklären können, dass Impulsantwort und Frequenzgang zwei Sichten auf dasselbe LTI-System sind und dieser Zusammenhang in Vorlesung 6 direkt fortgesetzt wird.

## 3. Audio-Dramaturgie

Vorlesung 5 startet bewusst nicht direkt mit Formeln. Nach 5 Minuten Orga und 10 Minuten Wiederholung folgt ein ruhiger Überblick über Audioeffekte als Klangwerkzeuge. Die Studierenden sollen zuerst hören und sortieren:

- Was verändert sich am Klang?
- Welche Wahrnehmungsdimension ist betroffen?
- Welche grobe Systemklasse steckt dahinter?

DAFX-Wahrnehmungsklassen:

| Kürzel | Wahrnehmung | Beispiele |
|---|---|---|
| `L` | Lautheit, Dynamik, Akzent | gain, compressor, limiter, expander, tremolo |
| `D` | Dauer und Rhythmus | time-scaling, time inversion, rhythm/swing change |
| `P` | Tonhöhe und Harmonie | pitch-shifting, auto-tune, harmonizer |
| `S` | Raum, Ortung, Entfernung, Bewegung | echo, reverb, panning, Doppler, rotary/Leslie |
| `T` | Klangfarbe und Qualität | filter, EQ, wah-wah, chorus, flanger, phaser, distortion |

Danach wird dieselbe Effektlandkarte technisch sortiert:

| Systemklasse | Beispiele | Technische Sprache |
|---|---|---|
| LTI | EQ, Filter, Echo mit festen Parametern, Faltungshall | Impulsantwort, Faltung, Frequenzgang |
| LTV | Tremolo, Chorus, Flanger, Phaser, Vibrato | zeitabhängiger Gain, bewegtes Delay, LFO |
| nichtlinear | Distortion, Saturation, Fuzz, Compressor/Limiter | Kennlinie, Pegelabhängigkeit, Obertöne |
| nichtlinear und zeitvariant | Sidechain-Kompressor, Gate mit Hüllkurve | Envelope-Follower, zeitabhängiges Gain |

Übergangssatz:

> Viele Audioeffekte sehen zuerst sehr verschieden aus. Systemtheorie liefert die Sprache, um ihre gemeinsamen Bausteine zu erkennen. Wir beginnen mit der einfachsten und wichtigsten Klasse: lineare zeitinvariante Systeme.

## 4. Mathematischer Kern

Diskreter Impuls:

$$
\delta[n]=
\begin{cases}
1, & n=0\\
0, & n\neq 0
\end{cases}
$$

Systemabbildung:

$$
y[n]=\mathcal{T}\{x[n]\}
$$

Impulsantwort:

$$
h[n]=\mathcal{T}\{\delta[n]\}
$$

Linearität:

$$
\mathcal{T}\{a x_1[n]+b x_2[n]\}
=
a\mathcal{T}\{x_1[n]\}
+b\mathcal{T}\{x_2[n]\}
$$

Zeitinvarianz:

$$
\mathcal{T}\{x[n-n_0]\}=y[n-n_0]
$$

Diskrete Faltung:

$$
y[n]=(x*h)[n]=\sum_m x[m]h[n-m]
$$

Anschlussformel für Vorlesung 6:

$$
H(e^{j\Omega})=\sum_m h[m]e^{-j\Omega m}
$$

Gruppenlaufzeit an diskreten Frequenzstützstellen:

$$
\tau_g[k]
=
-\left.
\frac{d\varphi(\Omega)}{d\Omega}
\right|_{\Omega=\Omega_k}
$$

mit

$$
\varphi[k]=\arg\{H(e^{j\Omega_k})\},
\qquad
\Omega_k=\frac{2\pi k}{N}.
$$

## 5. Blockstruktur

### Block 0: Audioeffekte als Klanglandkarte

Ziel: Die Studierenden sollen Effekte zuerst als hörbare Klangveränderungen einordnen.

Material:

- trockenes Signal
- EQ/Filter
- Echo oder kurzer Raum
- Modulationseffekt
- Compressor
- Distortion/Saturation

Didaktischer Fokus:

- erst hören, dann benennen
- Wahrnehmungssprache vor Formelsprache
- DAFX-Kategorien als Landkarte
- Systemklassen nur als erste technische Sortierung

### Block 00: Allgemeiner Systembegriff

Kernaussage:

> Ein System ist eine Abbildung von $x[n]$ nach $y[n]$.

Storyboards:

- einfache Eingangsfolge $x[n]$
- dazugehörige Ausgangsfolge $y[n]$
- diskreter Impuls $\delta[n]$
- Impulsantwort $h[n]$
- ideales Spektrum, Phase und Gruppenlaufzeit des diskreten Impulses
- Tiefpass-Impulsantwort in Abb. 8 didaktisch pegelangehoben wie im Faltungsblock; Betrag und Gruppenlaufzeit nutzen die normalisierte IR als einseitige Darstellung bis Nyquist. Bei $N=16$ also $k=0,\dots,8$, die zweite DFT-Hälfte wird nicht geplottet

### Block 1B: Systemklassenbeispiele

Ziel: Die Systemklassen nicht abstrakt, sondern über Effektbeispiele motivieren.

Storyboards:

- geclippter Sinus: nichtlineares System, neue Obertöne
- Tremolo-Gainfolge $g[n]$: zeitvariantes lineares System
- Sidechain-Kompressor: Sidechain-Signal $s[n]$, Hüllkurve $e_s[n]$, Gain $g_s[n]$

### Block 1: Systembegriff und Impulsantwort

Kernaussage:

> Die Impulsantwort zeigt, was das System aus einem einzelnen Sample-Anstoß macht.

Wichtig:

- Eine Impulsantwort kann man bei vielen Systemen messen.
- Eine einzige Impulsantwort beschreibt das System aber nur bei LTI-Systemen vollständig.
- Der Impuls ist ein Testsignal, nicht ein typisches Audiosignal.

### Block 2: Diskrete Faltung

Kernaussage:

> Jedes Sample von $x[n]$ startet eine verschobene und skalierte Kopie von $h[n]$. Die Summe aller Kopien ist $y[n]$.

Didaktische Reihenfolge:

1. Dirac-Faltung mit festem $\delta[m]$ und verschobenem $x[n-m]$.
2. Kommutativität: festes $x[m]$ und verschobener Dirac $\delta[n-m]$.
3. Übergang vom Dirac zur Tiefpass-Impulsantwort $h[n]$.
4. LTI-Lesart: einzelne Kopien $x[m]h[n-m]$ bauen $y[n]$ auf.

### Verschobener Block 3: Impulsantwort und Frequenzgang

Kernaussage:

> Dieselbe Systemwirkung kann im Zeitbereich als Faltung und im Frequenzbereich als komplexe Gewichtung gelesen werden.

Dieser Block war für Vorlesung 5 geplant, wurde aber nicht mehr vorgestellt. Er wird in Vorlesung 6 als Block 1 neu angesetzt und dort mit den vorhandenen Storyboards gerendert.

Didaktischer Fokus:

- $h[n]$ ist die Zeitbereichssicht.
- $H(e^{j\Omega})$ ist die Frequenzbereichssicht.
- Betrag zeigt Verstärkung/Dämpfung.
- Phase zeigt Phasenverschiebung.
- Gruppenlaufzeit zeigt frequenzabhängige Verzögerung.
- $H[k]$ ist nicht die allgemeine Systembeschreibung, sondern eine Abtastung von $H(e^{j\Omega})$ auf einem konkreten DFT-Raster.
- Bei einer DFT-Länge $N$ gilt $H_N[k]=H(e^{j2\pi k/N})$ und damit $Y_N[k]=H_N[k]X_N[k]$.
- Ändert sich $N$, bleibt das System gleich; nur die DFT-Bin-Darstellung der Systemantwort wird neu ausgewertet.
- Bei DFT-Multiplikation ist die Faltung zunächst zirkulär. Für lineare Faltung muss ausreichend aufgefüllt werden: $N\geq N_x+N_h-1$.

Beispiele:

- Dirac: Betrag konstant, Phase null, Gruppenlaufzeit null
- Tiefpass: tiefe Frequenzen bleiben, hohe Frequenzen werden gedämpft
- nichtlinearphasiger Tiefpass: Gruppenlaufzeit ist nicht konstant
- periodisches Rechtecksignal: $X_N[k]$ wird durch $H_N[k]$ binweise gewichtet; $y[n]$ ist geglättet und nicht mehr rechteckförmig
- längeres Rechtecksignal: das alte $H[k]$ passt nicht zu jedem neuen Bin; $H(e^{j\Omega})$ löst dieses Rasterproblem

## 6. Zeitplan für 120 Minuten

| Zeit | Abschnitt | Inhalt | Funktion |
|---|---|---|---|
| 0-5 min | Orga | Ablauf und Material | Ankommen |
| 5-15 min | Wiederholung | DFT/STFT/iSTFT zur Systemsicht | Vorwissen aktivieren |
| 15-40 min | Block 0 | DAFX-Wahrnehmungslandkarte | Audio-Motivation |
| 40-55 min | Block 00 | System, Impuls, Impulsantwort | Grundsprache |
| 55-65 min | Block 1B | Systemklassenbeispiele | LTI/LTV/Nichtlinear unterscheiden |
| 65-72 min | Pause | kurze Unterbrechung | Entlastung |
| 72-88 min | Block 1 | LTI und Impulsantwort | Geltungsbereich klären |
| 88-108 min | Block 2 | diskrete Faltung | Mechanik verstehen |
| 108-118 min | Sicherung | Faltung als Systemwirkung und offene Frequenzsicht | erreichten Stand festigen |
| 118-120 min | Abschluss | Anschluss an Vorlesung 6 | Frequenzgang-Block ankündigen |

Da Block 0 und die Systemklassenbrücke mehr Zeit gebraucht haben, bleibt Block 3 nicht nur ein kurzer Ausblick, sondern wird vollständig in Vorlesung 6 verschoben.

## 7. Typische Verständnishürden

| Fehlkonzept | Korrektursatz |
|---|---|
| Die Impulsantwort ist ein Eingangssignal. | Die Impulsantwort ist die Antwort des Systems auf einen Impuls. |
| Faltung ist nur eine Rechenregel. | Faltung beschreibt, wie ein LTI-System jedes Eingangssample in eine Kopie von $h[n]$ übersetzt. |
| $h[n]$ beschreibt jedes System vollständig. | Eine einzige Impulsantwort beschreibt nur LTI-Systeme vollständig. |
| Frequenzgang ist ein Signalspektrum. | Der Frequenzgang beschreibt das System, nicht ein einzelnes Signal. |
| Betrag reicht zur Systembeschreibung. | Phase und Gruppenlaufzeit können hörbar und technisch wichtig sein. |

## 8. Anschluss an Vorlesung 6

Vorlesung 6 beginnt mit der noch offenen Frage:

> Wie beschreibt dieselbe Impulsantwort die Systemwirkung im Frequenzbereich?

Direkt danach folgt die konstruktive Frage:

> Wie baut man solche Systeme aus digitalen Bausteinen?

Anschlussbegriffe:

- $H(e^{j\Omega})$
- $H_N[k]$
- spektrale Gewichtung $Y_N[k]=H_N[k]X_N[k]$
- Delay als Speicher
- $x[n-1]$ und $x[n-M]$
- Feedforward-Delay
- Feedback-Delay
- Differenzengleichung
- Delay-Operator als Speicherbaustein
- $H(z)$ erst ab Vorlesung 8

Damit wird aus der beschreibenden Sicht von Vorlesung 5 eine konstruktive DSP-Sprache.
