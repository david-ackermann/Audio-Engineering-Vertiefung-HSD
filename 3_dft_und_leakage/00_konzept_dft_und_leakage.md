# Konzept Vorlesung 3: Digitale Analyse, DFT und iDFT

## Ziel der Vorlesung

Die Studierenden sollen am Ende verstehen:

- dass ein digitales Audiosystem nicht $x(t)$, sondern eine diskrete Folge $x[n]$ verarbeitet
- wie Abtastfrequenz, Blocklaenge und Beobachtungsdauer gemeinsam das Frequenzraster bestimmen
- wie Nyquist-Grenze und Aliasbildung praktisch zu deuten sind
- warum ein FFT-basierter Analyzer immer auf endlichen Bloecken arbeitet
- was Frequenzbins und der Binabstand $\Delta f = f_s / N$ bedeuten
- wie die diskrete Kreisfrequenz $\Omega_k$ den DFT-Bin als Kreisbewegung beschreibt
- wie die DFT einen Block an diskreten Frequenzstellen ausliest
- wie die iDFT aus diesen Binwerten denselben Zeitblock rekonstruiert

Leakage wird am Ende nur als offene Anschlussfrage motiviert: Was passiert, wenn die analysierte Schwingung nicht genau auf ein DFT-Bin passt? Die ausfuehrliche Behandlung ist jetzt Block 1 der vierten Vorlesung.

## Didaktische Rolle im Gesamtaufbau

Vorlesung 3 baut die digitale Ein-Block-Analyse auf. Sie verschiebt die Perspektive von der kontinuierlichen Fourier-Sicht auf die Arbeitsweise realer digitaler Audiowerkzeuge.

Die fachliche Kette lautet:

- aus dem kontinuierlichen Signal $x(t)$ wird die diskrete Folge $x[n]$
- aus der Abtastung folgen Alias-Mehrdeutigkeit und periodische Spektralkopien
- aus dem endlichen Beobachtungsblock folgen $T_{\mathrm{obs}}$, $\Delta f$ und die Binfrequenzen $f_k$
- aus $k$ und $N$ folgt die diskrete Kreisfrequenz $\Omega_k = 2 \pi k / N$
- aus dem Beobachtungsblock wird per DFT/FFT ein Spektralbild
- aus den Binwerten fuehrt die iDFT wieder zum lokalen Zeitblock

Mitgenommen werden muessen insbesondere:

- $x[n]$ als diskrete Folge
- Aliasbildung als periodische Frequenzmehrdeutigkeit modulo $f_s$
- $T_{\mathrm{obs}}$ und $\Delta f$ als Folge des endlichen Beobachtungsblocks
- DFT-Bins als diskretes Frequenzraster
- DFT und FFT als Messlogik, nicht als neues Signal
- iDFT als Rueckweg zum betrachteten Block

## Anschluss an Vorlesung 2

Vorlesung 2 hat die kontinuierliche Sicht auf Beobachtung und Fensterung aufgebaut:

$$
x_{\mathrm{obs}}(t) = x(t) w(t)
$$

$$
X_{\mathrm{obs}}(f) = (X \ast W)(f)
$$

Vorlesung 3 fuegt nun die digitale Sicht hinzu: Abtastung, diskrete Folge, DFT-Raster und Blockanalyse.

Ein geeigneter Uebergangssatz ist:

> Vorlesung 2 erklaert die kontinuierliche Spektralform. Vorlesung 3 erklaert, wie Abtastung und DFT daraus ein diskretes Analysebild machen.

## Mathematischer Kern

$$
x[n] = x_c(n T_s),    T_s = 1 / f_s
$$

$$
x_s(t) = \sum_n x[n] \delta(t - n T_s)
$$

$$
X_s(f) = f_s \sum_m X(f - m f_s)
$$

$$
x_B[n] = x[n] w[n],    0 \le n \le N - 1
$$

$$
T_{\mathrm{obs}} = N / f_s,    \Delta f = f_s / N = 1 / T_{\mathrm{obs}},    f_k = k f_s / N
$$

$$
\Omega_k = 2 \pi k / N = 2 \pi f_k / f_s
$$

$$
X[k] = \sum_{n=0}^{N-1} x[n] w[n] e^{-j 2 \pi k n / N}
$$

$$
x[n] = (1 / N) \sum_{k=0}^{N-1} X[k] e^{j 2 \pi k n / N}
$$

## Didaktischer roter Faden

1. Einstieg ueber Analyzer, Spektrum und Spektrogramm als Motivation
2. Rueckgriff auf bekannte Fourier-Begriffe und saubere Notation
3. Block 2A: vom kontinuierlichen Signal $x(t)$ zur diskreten Folge $x[n]$
4. Block 3A: Aliasing als Mehrdeutigkeit analoger Frequenzen nach der Abtastung
5. Block 3B: ideale Abtastung eines tiefpassbegrenzten Signals und periodische Spektralkopien
6. Block 3C: endlicher Beobachtungsblock, Beobachtungsdauer $T_{\mathrm{obs}}$ und Binraster $\Delta f$
7. Block 4: diskrete Kreisfrequenz, Phasor und Binfrequenz
8. Block 5: DFT als formale Analyzerlogik
9. Block 6: iDFT als Rueckweg zum Zeitblock
10. Ausblick: Off-Bin-Frequenz und Leakage als Startfrage fuer Vorlesung 4

## Zeitplan fuer 120 Minuten

| Zeit | Abschnitt | Inhalt | mathematischer Fokus | didaktische Funktion |
|---|---|---|---|---|
| 0-10 min | Einstieg | Analyzer, Spektrum, Leitfrage | noch keine neue Formel | Motivation und Anker |
| 10-20 min | Rueckgriff | FT, Phase, Fensterung, Notation $x(t)$, $x_s(t)$, $x[n]$ | Begriffs- und Objektklaerung | saubere Notationsbasis |
| 20-32 min | Block 2A | $x[n] = x_c(n T_s)$, Samples auf der Kurve, diskrete Folge | Abtastung im Zeitbereich | Wechsel von $t$ zu $n$ |
| 32-45 min | Block 3A/3B | Nyquist, Basisbereich, Alias-Familien, periodische Spektralkopien | Frequenz modulo $f_s$, $X_s(f)$ | Mehrdeutigkeit klaeren |
| 45-58 min | Block 3C | endlicher Block, $T_{\mathrm{obs}}$, $\Delta f$, $f_k$ | $T_{\mathrm{obs}} = N / f_s$, $\Delta f = f_s / N$ | Uebergang zum Analyzer |
| 58-74 min | Block 4 | diskrete Kreisfrequenz, Phasor, Binfrequenz und Prueffrequenz | $\Omega_k = 2 \pi k / N$, $f_k = k f_s / N$ | Begriffliche Bruecke vor der DFT |
| 74-88 min | Block 5 | Blocklaenge, Bins, Projektion, FFT als Algorithmus | $X[k]$, diskrete Prueffrequenzen | von der Theorie zur Messlogik |
| 88-96 min | Pause | kurze Unterbrechung | - | Entlastung |
| 96-112 min | Block 6 | Rekonstruktion aus Bin-Werten | iDFT-Gleichung | Analyse und Synthese verbinden |
| 112-120 min | Ausblick | nicht-binzentrierter Ton als offene Frage | Was misst ein Bin, wenn kein Bin exakt passt? | Startpunkt fuer Leakage in Vorlesung 4 setzen |

## Typische Verstaendnishuerden

- DFT und FFT werden leicht verwechselt.
- Das Spektrogramm wird schnell fuer "das Signal selbst" gehalten.
- Frequenzaufloesung wird vorschnell allein der Samplerate zugeschrieben.
- hoehere FFT-Laenge wird mit "mehr wahrer Aufloesung" gleichgesetzt.
- Aliasbildung wird als Verschwinden hoher Frequenzen missverstanden.
- negative Frequenzen und DFT-Bins oberhalb von Nyquist werden zu spaet zusammengefuehrt.

## Demo-, Hoer- und Python-Einsatz

- Hoerdemo: Aliasbildung mit Sweep oder Sinus oberhalb von $f_s / 2$
- Analyzer-Demo: gleicher Block bei verschiedenen $N$ und $f_s$
- Python: DFT-Bins als Pruefschwingungen
- Python: DFT und iDFT desselben endlichen Blocks
- Abschlussdemo: off-bin Ton als nicht mehr sauber von einem einzelnen Bin getroffener Fall

## Geplante Export- und Storyboard-Struktur

- `02_zeitbereich_und_frequenzraster`
- `02_zeitbereich_und_frequenzraster/02a_signal_zu_x_n`
- `03_aliasing`
- `03_aliasing/03A_aliasing`
- `03_aliasing/03B_rechteckzug_zum_dirac_kamm`
- `03_aliasing/03C_frequenzraster_und_aufloesung`
- `04_diskrete_kreisfrequenz`
- `04_diskrete_kreisfrequenz/04A`
- `04_diskrete_kreisfrequenz/04A/04A1_kontinuierlicher_phasor_helix`
- `04_diskrete_kreisfrequenz/04A/04A2_dft_basis_als_diskreter_phasor`
- `04_diskrete_kreisfrequenz/04A/04A3_cos_sin_basisfunktionen`
- `04_diskrete_kreisfrequenz/04B/04B1_dft_bins_omega_raster`
- `04_diskrete_kreisfrequenz/04B/04B2_n32_k16_positive_spectrum`
- `05_dft_analyzerlogik`
- `06_idft_rekonstruktion`

Die Fortsetzung mit Leakage, STFT und iSTFT liegt in `../4_stft_und_istft/`.
