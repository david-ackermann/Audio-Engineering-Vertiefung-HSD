# TEMP Konzept Block 4: Diskrete Kreisfrequenz vor der DFT

Arbeitsstand: temporaere Konzeptdatei fuer die weitere Ausarbeitung im Laufe des Tages.

Dieses Dokument ist bewusst nicht in `00_konzept_dft_und_leakage.md` eingearbeitet. Es sammelt die detaillierte didaktische Linie fuer den neuen Block 4 zwischen Block 3C und der DFT-Analyzerlogik.

Ausgangspunkt: Vorschlag `c:\Users\ackerm_d\Downloads\diskrete_kreisfrequenz_dft_vorlesungsbaustein.md`

## Rolle im Vorlesungsfluss

Block 3C endet mit:

- endlicher Beobachtungsblock mit $N$ Samples
- Beobachtungsdauer $T_\mathrm{obs} = N / f_s$
- Frequenzraster $\Delta f = f_s / N$
- Binfrequenzen $f_k = k f_s / N$

Der neue Block 4 soll verhindern, dass die DFT-Formel zu frueh kommt. Vor der Summenformel muss klar werden:

- Ein diskretes Signal wird ueber Sample-Indizes $n$ betrachtet.
- Die zentrale Frage ist nicht zuerst "Welche Frequenz in Hz?", sondern "Um welchen Winkel dreht sich der Zeiger pro Sample?"
- Die DFT-Bins sind diskrete Kreisfrequenzen auf dem Einheitskreis.
- Der Bereich oberhalb $\pi$ ist in der DFT die negative Frequenzseite, nicht eine neue positive Audiofrequenz.

Kernsatz:

> Erst den Zeiger erklaeren, dann die Formel. Erst den Kreis erklaeren, dann die Frequenzachse. Erst $N = 8$ zeigen, dann generalisieren.

## Lernziele

Nach Block 4 sollen die Studierenden sagen koennen:

- $\Omega$ ist der Phasenzuwachs pro Sample.
- $\Omega$ hat die anschauliche Einheit rad/sample.
- $\Omega = 2\pi f / f_s$ verbindet eine Frequenz in Hz mit der diskreten Sampleachse.
- Diskrete Kreisfrequenzen sind modulo $2\pi$ definiert.
- $\pi$ ist die Nyquist-Grenze, nicht die Periodizitaet.
- DFT-Bin $k$ bedeutet $k$ volle Umdrehungen im $N$-Sample-Block.
- Daraus folgt $\Omega_k = 2\pi k / N$.
- Die rohe Frequenzachse ist $f_k = k f_s / N$.
- Bins oberhalb $N/2$ entsprechen negativen Frequenzen.
- Fuer reelle Signale gilt die Spiegelbeziehung $X[N-k] = X[k]^*$.

## Zeitrahmen

Der Vorschlag ist fuer 20 bis 30 Minuten ausgelegt. In der 120-Minuten-Vorlesung ist wahrscheinlich ein kompakterer Block sinnvoll:

| Zeit | Abschnitt | Ziel | Material |
|---:|---|---|---|
| 0-3 min | Einstieg | Perspektivwechsel von Hz zu Zeigerschritt | Tafel / kurze verbale Frage |
| 3-7 min | $\Omega$ als Phasenzuwachs | rad/sample anschaulich machen | Einheitskreis / Phasor |
| 7-11 min | Zusammenhang zu Hz | $\Omega = 2\pi f / f_s$ herleiten | Formel + einfaches Zahlenbeispiel |
| 11-15 min | Periodizitaet modulo $2\pi$ | $\Omega$ und $\Omega + 2\pi$ als gleiche Folge zeigen | Plot Periodizitaet |
| 15-20 min | DFT-Bins | $\Omega_k = 2\pi k / N$ aus $k$ Umdrehungen in $N$ Samples | Einheitskreis $N=8$ |
| 20-25 min | Nyquist und negative Frequenzen | Bins oberhalb $\pi$ als negative Seite lesen | Mapping-Tabelle / Frequenzachse |
| 25-30 min | Reelle Signale und Spiegelbins | konjugierte Symmetrie vorbereiten | Paarbildung $k$ und $N-k$ |

Kompakte 15-Minuten-Variante:

| Zeit | Abschnitt | Muss-Inhalt |
|---:|---|---|
| 0-4 min | Zeigerschritt | $\Omega$ = Winkel pro Sample |
| 4-7 min | Hz-Bezug | $\Omega = 2\pi f / f_s$ |
| 7-10 min | DFT-Bins | $\Omega_k = 2\pi k / N$ |
| 10-13 min | Modulo und Nyquist | $2\pi$ Periodizitaet, $\pi$ Nyquist |
| 13-15 min | Negative Seite | $N-k$ als Spiegelbin |

## Didaktische Dramaturgie

### 1. Einstieg

Leitfrage:

> Wir betrachten heute nicht zuerst Frequenz in Hertz, sondern die Frage: Um welchen Winkel dreht sich ein komplexer Zeiger von einem Sample zum naechsten?

Didaktischer Zweck:

- Frequenz nicht sofort als Hz-Achse denken.
- DFT-Bins geometrisch vorbereiten.
- Den DFT-Exponentialterm spaeter als bekannte Zeigerfolge wiedererkennen.

### 2. $\Omega$ einfuehren

Definition:

$$
x[n] = e^{j\Omega n}
$$

Sprechsatz:

> $\Omega$ ist nicht die Frequenz in Hertz. $\Omega$ ist der Winkelzuwachs pro Sample.

Beispiele:

- $\Omega = \pi / 4$: pro Sample 45 Grad weiter.
- $\Omega = \pi / 2$: pro Sample 90 Grad weiter.
- $\Omega = \pi$: pro Sample 180 Grad weiter, also $1, -1, 1, -1, \dots$.

### 3. Von kontinuierlich zu diskret

Herleitung:

$$
x_c(t) = e^{j2\pi f t}
$$

$$
t = nT_s = \frac{n}{f_s}
$$

$$
x[n] = x_c(nT_s)
$$

$$
x[n] = e^{j2\pi f n / f_s}
$$

$$
x[n] = e^{j\Omega n}
$$

Damit:

$$
\Omega = 2\pi\frac{f}{f_s}
$$

Rueckrichtung:

$$
f = \frac{\Omega}{2\pi}f_s
$$

Merksatz:

> Hz fragt: Wie oft pro Sekunde? rad/sample fragt: Wie weit dreht sich der Zeiger von Sample zu Sample?

### 4. Einheit rad/sample

Aus der kontinuierlichen Kreisfrequenz:

$$
\omega = 2\pi f \qquad [\mathrm{rad/s}]
$$

$$
\Omega = \omega T_s = \frac{\omega}{f_s}
$$

Anschaulich:

$$
\frac{\mathrm{rad}}{\mathrm{s}} \cdot \frac{\mathrm{s}}{\mathrm{sample}}
= \frac{\mathrm{rad}}{\mathrm{sample}}
$$

Didaktischer Hinweis:

Radiant ist formal dimensionslos. Trotzdem ist $\mathrm{rad/sample}$ als Sprechweise sinnvoll, weil sie den Winkelzuwachs pro Abtastschritt sichtbar macht.

### 5. Periodizitaet modulo $2\pi$

Zentrale Gleichung:

$$
e^{j(\Omega + 2\pi)n}
= e^{j\Omega n} e^{j2\pi n}
= e^{j\Omega n}
$$

weil fuer ganzzahliges $n$ gilt:

$$
e^{j2\pi n} = 1
$$

Kernsatz:

> Im diskreten Fall ist $\Omega$ nur modulo $2\pi$ eindeutig.

Abgrenzung:

- $2\pi$ ist die Periodizitaet des diskreten Frequenzraums.
- $\pi$ ist die Nyquist-Grenze.
- $\pi$ ist nicht die Periodizitaet, denn $e^{j(\Omega + \pi)n} = e^{j\Omega n}(-1)^n$.

### 6. DFT-Bins aus Kreisbewegungen

Intuition:

> Bin $k$ bedeutet: Der komplexe Zeiger macht $k$ volle Umlaeufe innerhalb von $N$ Samples.

Herleitung:

$$
\Omega_k N = 2\pi k
$$

$$
\Omega_k = \frac{2\pi k}{N}
$$

Binabstand:

$$
\Delta\Omega = \frac{2\pi}{N}
$$

Hz-Achse:

$$
f_k = \frac{\Omega_k}{2\pi}f_s = k\frac{f_s}{N}
$$

$$
\Delta f = \frac{f_s}{N}
$$

Wichtig fuer die Formulierung:

> $f_k = k f_s / N$ ist zuerst die rohe DFT-Achse von 0 bis fast $f_s$. Oberhalb der Nyquist-Grenze lesen wir sie als negative Frequenzseite.

### 7. Beispiel $N = 8$, $f_s = 8000\,\mathrm{Hz}$

Binabstand:

$$
\Delta\Omega = \frac{2\pi}{8} = \frac{\pi}{4}
$$

$$
\Delta f = \frac{8000}{8} = 1000\,\mathrm{Hz}
$$

| $k$ | $\Omega_k$ | rohe Frequenz | signierte Interpretation | Spiegelbin |
|---:|---:|---:|---:|---:|
| 0 | $0$ | 0 Hz | DC | 0 |
| 1 | $\pi/4$ | 1000 Hz | $+1000\,\mathrm{Hz}$ | 7 |
| 2 | $\pi/2$ | 2000 Hz | $+2000\,\mathrm{Hz}$ | 6 |
| 3 | $3\pi/4$ | 3000 Hz | $+3000\,\mathrm{Hz}$ | 5 |
| 4 | $\pi$ | 4000 Hz | Nyquist | 4 |
| 5 | $5\pi/4$ | 5000 Hz | $-3000\,\mathrm{Hz}$ | 3 |
| 6 | $3\pi/2$ | 6000 Hz | $-2000\,\mathrm{Hz}$ | 2 |
| 7 | $7\pi/4$ | 7000 Hz | $-1000\,\mathrm{Hz}$ | 1 |

Erklaerung fuer $k = 7$:

$$
\Omega_7 = \frac{7\pi}{4} = -\frac{\pi}{4} + 2\pi
$$

$$
e^{j(7\pi/4)n} = e^{-j(\pi/4)n}
$$

Sprechsatz:

> $7\pi / 4$ sieht aus wie ein grosser positiver Schritt, ist aber dieselbe diskrete Folge wie $-\pi / 4$.

### 8. Nyquist-Bin

Nyquist-Frequenz:

$$
f_\mathrm{Nyquist} = \frac{f_s}{2}
$$

$$
\Omega_\mathrm{Nyquist}
= 2\pi\frac{f_s/2}{f_s}
= \pi
$$

Bei $\Omega = \pi$:

$$
e^{j\pi n} = (-1)^n = 1, -1, 1, -1, \dots
$$

Didaktischer Punkt:

- Zwei Samples pro Periode.
- Hoechste eindeutig darstellbare positive Frequenz.
- Bei geradem $N$ ist Bin $N/2$ sein eigener Spiegelpartner.

### 9. Reelle Signale und Spiegelbins

Cosinus-Zerlegung:

$$
\cos(\Omega n)
= \frac{1}{2}e^{j\Omega n}
+ \frac{1}{2}e^{-j\Omega n}
$$

Spiegelbin:

$$
\Omega_{N-k}
= \frac{2\pi(N-k)}{N}
= 2\pi - \frac{2\pi k}{N}
\equiv -\Omega_k \pmod{2\pi}
$$

Fuer reelle Signale:

$$
X[N-k] = X[k]^*
$$

$$
|X[N-k]| = |X[k]|
$$

$$
\angle X[N-k] = -\angle X[k]
$$

Sprechsatz:

> Die obere Haelfte der DFT ist bei reellen Signalen nicht zusaetzlicher positiver Inhalt, sondern der konjugierte negative Frequenzpartner der unteren Haelfte.

## Folienlogik

### Folie 1: Drei Frequenzbegriffe

| Begriff | Symbol | Bedeutung | Einheit |
|---|---:|---|---|
| Frequenz | $f$ | Perioden pro Sekunde | Hz |
| kontinuierliche Kreisfrequenz | $\omega$ | Phase pro Sekunde | rad/s |
| diskrete Kreisfrequenz | $\Omega$ | Phase pro Sample | rad/sample |

Einblendfolge:

$$
\omega = 2\pi f
$$

$$
T_s = \frac{1}{f_s}
$$

$$
\Omega = \omega T_s
$$

$$
\Omega = 2\pi\frac{f}{f_s}
$$

### Folie 2: Vom kontinuierlichen Signal zur diskreten Folge

Einblendfolge:

$$
x_c(t)=e^{j2\pi f t}
$$

$$
x[n]=x_c(nT_s)
$$

$$
x[n]=e^{j2\pi f nT_s}
$$

$$
x[n]=e^{j2\pi (f/f_s)n}
$$

$$
x[n]=e^{j\Omega n}
$$

Visual: kontinuierliche Sinus- oder Zeigerbewegung, darunter Samples, daneben Einheitskreis.

### Folie 3: $\Omega$ als Zeigerschritt

Visual:

- Einheitskreis
- Punkte fuer $n = 0, 1, 2, \dots$
- Beispiel $\Omega = \pi/4$

Sprechsatz:

> Von Sample zu Sample wird mit $e^{j\Omega}$ multipliziert. Das ist eine Drehung um $\Omega$.

### Folie 4: Periodizitaet modulo $2\pi$

Formeln:

$$
e^{j(\Omega + 2\pi)n}
= e^{j\Omega n} e^{j2\pi n}
= e^{j\Omega n}
$$

Visual:

- $0$ und $2\pi$ am selben Kreispunkt
- $7\pi / 4$ geometrisch wie $-\pi / 4$

### Folie 5: DFT-Bins als Kreisraster

Intuition:

$$
\text{Bin } k = k \text{ Umlaeufe in } N \text{ Samples}
$$

Formeln:

$$
\Omega_k N = 2\pi k
$$

$$
\Omega_k = \frac{2\pi k}{N}
$$

$$
\Delta\Omega = \frac{2\pi}{N}
$$

### Folie 6: DFT-Formel vorbereiten

Noch nicht als Hauptblock ausformulieren, aber als Anschluss vorbereiten:

$$
X[k] = \sum_{n=0}^{N-1} x[n] e^{-j\Omega_k n}
$$

Deutung des Minuszeichens:

> Die Analysefunktion rotiert entgegengesetzt. Wenn im Signal die passende positive Rotation steckt, wird sie durch Multiplikation mit der Gegenrotation zu einem Gleichanteil.

Optional:

$$
x[n] = e^{j\Omega_k n}
$$

$$
x[n]e^{-j\Omega_k n} = 1
$$

### Folie 7: Positive, Nyquist- und negative Frequenzen

Fuer gerades $N$:

$$
k = 0 \quad \Rightarrow \quad \text{DC}
$$

$$
1 \leq k < N/2 \quad \Rightarrow \quad \text{positive Frequenzen}
$$

$$
k = N/2 \quad \Rightarrow \quad \text{Nyquist}
$$

$$
N/2 < k < N \quad \Rightarrow \quad \text{negative Frequenzen}
$$

Signierte Achse:

$$
\tilde{\Omega}_k =
\begin{cases}
\Omega_k, & 0 \leq k \leq N/2 \\
\Omega_k - 2\pi, & N/2 < k < N
\end{cases}
$$

$$
\tilde{f}_k =
\begin{cases}
k f_s / N, & 0 \leq k \leq N/2 \\
(k-N) f_s / N, & N/2 < k < N
\end{cases}
$$

### Folie 8: Reelle Signale und Spiegelbins

Zeigen:

$$
\Omega_{N-k} = 2\pi - \Omega_k \equiv -\Omega_k \pmod{2\pi}
$$

$$
X[N-k] = X[k]^*
$$

Paarbildung fuer $N=8$:

- Bin 1 <-> Bin 7
- Bin 2 <-> Bin 6
- Bin 3 <-> Bin 5
- Bin 4 ist Nyquist
- Bin 0 ist DC

## Plot- und Skriptbezug

Bereits vorhandene/angelegte Skripte fuer Block 4:

- `export_block_04a0_kontinuierlicher_phasor_helix.py`
- `export_block_04a_diskrete_kreisfrequenz_phasor_animation.py`
- `export_block_04a2_cos_sin_basisfunktionen.py`
- `export_block_04b_dft_bins_omega_raster.py`

Bereits vorhandene Ausgabeordner:

- `png_storyboards/04_diskrete_kreisfrequenz/04A/04A1_kontinuierlicher_phasor_helix`
- `png_storyboards/04_diskrete_kreisfrequenz/04A/04A2_dft_basis_als_diskreter_phasor`
- `png_storyboards/04_diskrete_kreisfrequenz/04A/04A3_cos_sin_basisfunktionen`
- $png_storyboards/04_diskrete_kreisfrequenz/04B/04B1_dft_bins_omega_raster$
- `png_storyboards/04_diskrete_kreisfrequenz/04B/04B2_n32_k16_positive_spectrum`

Moegliche Zuordnung:

| Konzeptteil | passendes Material |
|---|---|
| $\Omega$ als Zeigerschritt | 04A Phasor-Animation |
| DFT-Bin-Raster und konjugierte Seite | 04B Bin-Raster auf der $\Omega$-Achse |

## Typische Missverstaendnisse

### Missverstaendnis 1: Bin 6 bei $N = 8$ ist eine hoehere positive Frequenz als Bin 3

Korrektur:

$$
\Omega_6 = \frac{3\pi}{2} \equiv -\frac{\pi}{2} \pmod{2\pi}
$$

Bin 6 ist der negative Frequenzpartner von Bin 2.

### Missverstaendnis 2: Der Bereich $0$ bis $\pi$ reicht immer

Korrektur:

- Fuer einseitige Magnitudenspektren reeller Signale oft ja.
- Fuer die vollstaendige komplexe DFT, Phase und Rekonstruktion braucht man die negative Seite.

### Missverstaendnis 3: $\pi$ ist die Periodizitaet

Korrektur:

- $\pi$ ist Nyquist.
- Periodizitaet ist $2\pi$.

### Missverstaendnis 4: Negative Frequenzen sind physikalisch neue Toene

Korrektur:

- Negative Frequenzen beschreiben Drehrichtung komplexer Exponentialfunktionen.
- Reelle Audiosignale enthalten positive und negative komplexe Frequenzanteile paarweise.

## Kontrollfragen

1. Was bedeutet $\Omega = \pi/2$?
   - Der Zeiger dreht sich pro Sample um 90 Grad weiter.

2. Welche Frequenz in Hz entspricht $\Omega = \pi$?
   - $f = f_s / 2$, also Nyquist.

3. Was ist bei $N = 8$ der Spiegelbin von $k = 3$?
   - $N-k = 5$.

4. Warum ist $k = 8$ bei einer 8-Punkt-DFT kein neuer Bin?
   - $\Omega_8 = 2\pi \equiv 0 \pmod{2\pi}$, also wieder Bin 0.

5. Warum gilt bei reellen Signalen $X[N-k] = X[k]^*$?
   - Die negative Frequenzseite ist der konjugierte Partner der positiven Frequenzseite.

## Kurze Uebungsaufgaben

### Aufgabe 1

Gegeben:

$$
N = 16, \qquad f_s = 48000\,\mathrm{Hz}, \qquad k = 3
$$

Bestimmen:

$$
\Omega_k = \frac{2\pi \cdot 3}{16} = \frac{3\pi}{8}
$$

$$
f_k = \frac{3 \cdot 48000}{16} = 9000\,\mathrm{Hz}
$$

### Aufgabe 2

Gegeben:

$$
N = 16, \qquad k = 14
$$

Interpretation:

$$
\Omega_{14} = \frac{2\pi \cdot 14}{16} = \frac{7\pi}{4}
$$

$$
\frac{7\pi}{4} \equiv -\frac{\pi}{4} \pmod{2\pi}
$$

Der positive Spiegelbin ist:

$$
N-k = 2
$$

### Aufgabe 3

Ein reelles Signal hat bei einer 8-Punkt-DFT Energie in Bin $k = 2$.

Erwarteter Spiegelbin:

$$
N-k = 8-2 = 6
$$

$$
X[6] = X[2]^*
$$

$$
|X[6]| = |X[2]|
$$

## Arbeitscheckliste fuer die spaetere Integration

- [ ] Entscheiden, ob Block 4 auf 15, 20 oder 30 Minuten ausgelegt wird.
- [ ] Entscheiden, ob die DFT-Formel in Block 4 nur vorbereitet oder schon eingefuehrt wird.
- [ ] Folienreihenfolge final festlegen.
- [ ] Bestehende 04A-Grafiken auf didaktische Reihenfolge pruefen.
- [ ] Plotbeschriftungen auf deutsche Schreibweise und Vorlesungsstil vereinheitlichen.
- [ ] Entscheiden, ob $\mathrm{rad/sample}$ als Einheit explizit in den Abbildungen stehen soll.
- [ ] Nyquist-Sonderfall $k=N/2$ fuer gerade $N$ klar markieren.
- [ ] Reelle Spiegelbins nur vorbereiten oder bereits formal mit $X[N-k]=X[k]^*$ beweisen?
- [ ] Kontrollfragen am Ende des Blocks einbauen.
- [ ] Nach der Ausarbeitung relevante Teile in `00_konzept_dft_und_leakage.md` uebernehmen.

## Offene didaktische Entscheidungen

### Entscheidung A: Wie stark soll Block 4 schon die DFT-Formel beruehren?

Option 1: Nur vorbereiten

- Vorteil: Kreisfrequenz bleibt sauberer eigener Begriff.
- Nachteil: DFT-Anschluss muss in Block 5 erneut aufgebaut werden.

Option 2: DFT-Formel am Ende kurz zeigen

- Vorteil: Direkter Anschluss an Block 5.
- Nachteil: Gefahr, dass der neue Block wieder zur DFT-Formel kippt.

Pragmatischer Vorschlag:

> Block 4 endet mit der Formel $X[k] = \sum_n x[n]e^{-j\Omega_k n}$ nur als Ausblick. Die eigentliche Analyzerlogik bleibt Block 5.

### Entscheidung B: Wie viel negative Frequenzen vor der DFT?

Option 1: Nur geometrisch

- $\pi < \Omega < 2\pi$ entspricht Uhrzeigersinn.
- Spiegelbins werden nur benannt.

Option 2: Schon formal

- $\Omega_{N-k} \equiv -\Omega_k \pmod{2\pi}$
- $X[N-k] = X[k]^*$

Pragmatischer Vorschlag:

> Geometrie im Hauptfluss, formale Symmetrie als kurze Sicherung oder Zusatzfolie.

### Entscheidung C: Welche Beispielwerte?

Der Vorschlag nutzt:

- $N = 8$
- $f_s = 8000\,\mathrm{Hz}$

Vorteile:

- Binabstand ist 1000 Hz.
- Kreisraster hat 45-Grad-Schritte.
- Nyquist liegt bei 4000 Hz.

Moegliche Anpassung fuer Audio:

- $f_s = 48000\,\mathrm{Hz}$, $N = 8$ waere rechnerisch weniger griffig.
- $f_s = 48000\,\mathrm{Hz}$, $N = 16$ ist audio-naeher, aber fuer den ersten Kreis unuebersichtlicher.

Pragmatischer Vorschlag:

> Erst $N=8, f_s=8000\,\mathrm{Hz}$ als didaktisches Rechenbeispiel, spaeter Transfer auf reale Audio-Sampleraten.

