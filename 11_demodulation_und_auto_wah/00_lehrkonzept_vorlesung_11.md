# Lehrkonzept Vorlesung 11: Demodulation, Auto-Wah und Nichtlinearitäten

Diese Fassung ist die gekürzte Version der Vorlesung 11. Die Vorlesung endet
jetzt bei Intermodulation und Aliasing. Musikalische Verzerrung, Sättigung und
Dynamic Range Control werden in Vorlesung 12 weitergeführt.

Referenz: Zölzer, DAFX, Kapitel 3.3 und Kapitel 4.1/4.1.1.

## Lernziele

Die Studierenden sollen nach der Vorlesung erklären können,

- wie aus einem Audiosignal ein Steuersignal gewonnen wird,
- warum Detektor, Mittelung und Skalierung getrennte Bausteine sind,
- wie ein Sidechain-Auto-Wah aus einem Envelope ein Filter steuert,
- worin sich lineare und nichtlineare Systeme grundsätzlich unterscheiden,
- warum statische Nichtlinearitäten harmonische Verzerrungen erzeugen,
- warum bei zwei Sinussignalen Intermodulationsprodukte entstehen,
- warum nichtlineare digitale Systeme Aliasing erzeugen und wie Oversampling hilft.

## Gesamtstruktur

- Block 1: Demodulatoren und Envelope Follower
- Block 2: Anwendung Auto-Wah
- Block 3: Einstieg in nichtlineare Systeme
- Block 4: Intermodulationsverzerrungen
- Block 5: Aliasing und Oversampling

---

## Block 1: Demodulatoren und Envelope Follower

Storyboard-Ordner:

`png_storyboards/01_demodulators_envelope_followers/`

### Didaktische Idee

Der Block schließt an Vorlesung 10 an: Dort wurde ein Modulator als Signal
verstanden, das ein Trägersignal verändert. Jetzt wird der umgekehrte Weg
betrachtet. Ein Demodulator extrahiert aus einem Audiosignal ein Steuersignal.
Dieses Steuersignal kann anschließend wieder als Modulator für einen Effekt
dienen.

Die Studierenden sollen die Kette als drei getrennte Schritte verstehen:

1. Detektion: Aus dem Audiosignal wird eine positive Größe.
2. Mittelung: Aus der schnellen Audioschwingung wird ein langsames Steuersignal.
3. Skalierung: Das Steuersignal wird auf einen musikalisch sinnvollen Bereich abgebildet.

### Detektoren

Eingangssignal:

`x[n]`

Detektorsignal:

`d[n]`

Typische Detektoren:

Half-wave detector:

`d[n]=\max(x[n],0)`

Full-wave detector:

`d[n]=|x[n]|`

Squarer:

`d[n]=x^2[n]`

Instantaneous envelope:

`d[n]=\sqrt{x^2[n]+\hat{x}^2[n]}`

Hier ist `\hat{x}[n]` die Hilbert-Transformierte von `x[n]`. Bei einem idealen
analytischen Signal ist das die Quadraturkomponente. Für einen reinen Sinus ist
die Hüllkurve dadurch konstant. Für reale Audiosignale ist sie eine sehr gute
Schätzung der momentanen Amplitude, aber praktisch immer durch Filterlänge,
Bandbegrenzung und Randartefakte begrenzt.

### Mittelung und Zeitkonstante

Nach der Detektion enthält `d[n]` oft noch schnelle Schwankungen. Deshalb wird
geglättet:

`y[n]=(1-\alpha)d[n]+\alpha y[n-1]`

mit

`\alpha=e^{-\frac{1}{\tau f_s}}`

Dabei ist:

- `f_s`: Abtastfrequenz
- `\tau`: Zeitkonstante in Sekunden
- `\alpha`: rekursiver Glättungsfaktor
- `y[n]`: gemitteltes Detektorsignal

Die Zeitkonstante beschreibt die Reaktionsgeschwindigkeit. Nach einer
Zeitkonstante hat ein Sprung etwa `1-e^{-1}\approx 63,2\,\%` seines Zielwerts
erreicht.

### Attack und Release

Für Audiosignale reicht eine einzige Zeitkonstante oft nicht aus. Ein
Kompressor soll Pegelanstiege schnell erkennen, aber Pegelabfälle langsamer
freigeben. Deshalb werden Attack und Release getrennt:

`\alpha_A=e^{-\frac{1}{\tau_A f_s}}`

`\alpha_R=e^{-\frac{1}{\tau_R f_s}}`

Fallunterscheidung:

`d[n]>y[n-1] \Rightarrow y[n]=(1-\alpha_A)d[n]+\alpha_A y[n-1]`

`d[n]\leq y[n-1] \Rightarrow y[n]=(1-\alpha_R)d[n]+\alpha_R y[n-1]`

Typische Parameter, die in den Abbildungen verwendet werden:

- schneller Envelope Follower: `\tau_A=5\,\mathrm{ms}`, `\tau_R=100\,\mathrm{ms}`
- RMS-artige Messung: längere Zeitkonstanten, damit kurze Peaks weniger stark dominieren

---

## Block 2: Anwendung Auto-Wah

Storyboard-Ordner:

`png_storyboards/02_applications_auto_wah_morphing/`

Reaper-Plugin:

`audio_exports/reaper_jsfx/simple_sidechain_auto_wah.jsfx`

### Didaktische Idee

Das Auto-Wah zeigt, warum Demodulation musikalisch nützlich ist. Aus einem
Sidechain-Signal `s[n]` wird ein Envelope gewonnen. Dieser Envelope steuert die
Mittenfrequenz eines Bandpassfilters.

Wichtig: Das Sidechain-Signal ist nicht selbst im Ausgang zu hören. Es steuert
nur den Modulator beziehungsweise die Filterfrequenz.

### Signalkette

Sidechain:

`s[n]`

Detektor:

`d[n]=|s[n]|` oder `d[n]=s^2[n]`

Envelope:

`e[n]=(1-\alpha)d[n]+\alpha e[n-1]`

Skalierung auf einen Bereich `0...1`:

`\tilde{e}[n]=\mathrm{clip}(g\,e[n],0,1)`

Logarithmische Abbildung auf die Bandpass-Mittenfrequenz:

`f_c[n]=f_{\min}\left(\frac{f_{\max}}{f_{\min}}\right)^{\tilde{e}[n]}`

Damit bewegt sich die Mittenfrequenz musikalisch gleichmäßiger als bei einer
linearen Frequenzinterpolation.

### Parameter

- `f_min`: tiefste Wah-Frequenz
- `f_max`: höchste Wah-Frequenz
- `Q`: Resonanz beziehungsweise Bandpassgüte
- `\tau_A`: Attack-Zeit des Envelope Followers
- `\tau_R`: Release-Zeit des Envelope Followers
- `sidechain gain`: Pegelanpassung vor Detektor und Mittelung
- `wet mix`: Anteil des gefilterten Signals

---

## Block 3: Einstieg in nichtlineare Systeme

Storyboard-Ordner:

`png_storyboards/03_nonlinear_processing_intro/`

Unterordner:

- `03A_delay_clipper_helix`
- `03B_harmonic_decomposition`
- `03C_real_cos_harmonic_decomposition`

### Didaktische Idee

Der Einstieg greift Vorlesung 8 wieder auf. Dort wurde ein lineares System am
Beispiel einer Verzögerung betrachtet. Ein komplexes Exponentialsignal bleibt
nach einem linearen zeitinvarianten System ein komplexes Exponentialsignal mit
geänderter Amplitude und Phase.

Für ein lineares System gilt:

`x[n]=e^{j\Omega n}`

`y[n]=H(e^{j\Omega})e^{j\Omega n}`

Die Frequenz bleibt erhalten. Nur Betrag und Phase ändern sich.

Jetzt wird hinter die Verzögerung ein Hard Clipper gesetzt. Dadurch ist das
System nichtlinear. Ein einzelnes Eingangsspektrum bleibt nicht mehr auf einer
Frequenz, sondern erzeugt neue Spektralanteile.

### Statische Nichtlinearität

Eine speicherlose Nichtlinearität kann als Kennlinie beschrieben werden:

`y[n]=f(x[n])`

Lokal kann diese Kennlinie über eine Taylor-Reihe angenähert werden:

`f(x)=a_0+a_1x+a_2x^2+a_3x^3+a_4x^4+\dots`

Für Audiosignale ist das sehr anschaulich:

- `a_1x`: linearer Anteil, ursprüngliche Frequenzen bleiben erhalten
- `a_2x^2`: geradzahlige Verzerrungsanteile und DC-Anteile
- `a_3x^3`: ungeradzahlige Verzerrungsanteile
- höhere Potenzen: weitere Obertöne und weitere Intermodulationsprodukte

Ein idealer Hard Clipper ist nicht glatt. Deshalb hat er keine einfache
Taylor-Reihe über den gesamten Bereich. Für das Verständnis der entstehenden
Frequenzen ist die Potenzreihen-Idee trotzdem didaktisch sehr hilfreich.

### Warum entstehen harmonische Verzerrungen?

Wenn das Eingangssignal periodisch mit Grundperiode `N_0` ist, dann ist auch
`f(x[n])` periodisch mit derselben Grundperiode:

`x[n+N_0]=x[n]`

`y[n+N_0]=f(x[n+N_0])=f(x[n])=y[n]`

Jedes periodische Signal mit dieser Grundperiode kann in Harmonische der
Grundfrequenz zerlegt werden. Deshalb erzeugt ein statischer Clipper bei einem
einzelnen Sinus harmonische Obertöne.

Bei einem realen Cosinus müssen immer positive und negative Frequenzanteile
gemeinsam gedacht werden:

`\cos(\Omega_0 n)=\frac{1}{2}e^{j\Omega_0 n}+\frac{1}{2}e^{-j\Omega_0 n}`

Die Harmonischen erscheinen deshalb wieder als konjugiert-komplexe Paare.

---

## Block 4: Intermodulationsverzerrungen

Storyboard-Ordner:

`png_storyboards/04_imd/`

Unterordner:

- `04A_single_sine`
- `04B_two_sine_mixture`

### Didaktische Idee

Bei einem einzelnen Sinus sind die neuen Frequenzen Harmonische. Bei zwei
Sinussignalen entstehen zusätzlich Summen- und Differenzfrequenzen. Das ist für
Musiksignale wichtig, weil reale Signale fast immer mehrere Teiltöne enthalten.

### Quadrat eines Zweiton-Signals

Eingang:

`x[n]=\cos(\Omega_1 n)+\cos(\Omega_2 n)`

Quadrat:

`x^2[n]=\cos^2(\Omega_1 n)+\cos^2(\Omega_2 n)+2\cos(\Omega_1 n)\cos(\Omega_2 n)`

Mit

`\cos^2(\Omega n)=\frac{1}{2}+\frac{1}{2}\cos(2\Omega n)`

und

`2\cos(\Omega_1 n)\cos(\Omega_2 n)=\cos((\Omega_1-\Omega_2)n)+\cos((\Omega_1+\Omega_2)n)`

ergibt sich:

`x^2[n]=1+\frac{1}{2}\cos(2\Omega_1 n)+\frac{1}{2}\cos(2\Omega_2 n)+\cos((\Omega_1-\Omega_2)n)+\cos((\Omega_1+\Omega_2)n)`

Damit entstehen beim Quadrat-Term:

- ein DC-Anteil,
- zweite Harmonische der beiden Eingangstöne,
- Differenzfrequenz `\Omega_1-\Omega_2`,
- Summenfrequenz `\Omega_1+\Omega_2`.

Diese Rechnung ist der zentrale mathematische Einstieg in IMD.

### Höhere Potenzen

Für den kubischen Term entstehen Produkte wie:

- `2\Omega_1-\Omega_2`
- `2\Omega_2-\Omega_1`
- `2\Omega_1+\Omega_2`
- `2\Omega_2+\Omega_1`
- `3\Omega_1`
- `3\Omega_2`

Im Spektrum sind diese Linien oft musikalisch auffälliger als reine
Harmonische, weil sie nicht zwingend harmonisch zur ursprünglichen Tonhöhe
liegen.

---

## Block 5: Aliasing und Oversampling

Storyboard-Ordner:

`png_storyboards/05_aliasing/`

Unterordner:

- `05A_48khz`
- `05B_96khz`
- `05C_192khz`
- `05D_384khz`

Reaper-Plugin:

`audio_exports/reaper_jsfx/simple_oversampling_sine_clipper.jsfx`

### Didaktische Idee

Nichtlineare Systeme erzeugen neue Frequenzen. In einem digitalen System können
diese Frequenzen oberhalb der Nyquist-Frequenz liegen. Alles oberhalb Nyquist
wird nicht einfach abgeschnitten, sondern in den darstellbaren Bereich
zurückgefaltet.

### Digitale Frequenzen sind periodisch

Im zeitdiskreten System sind Frequenzen modulo `f_s` beziehungsweise modulo
`2\pi` äquivalent:

`e^{j\Omega n}=e^{j(\Omega+2\pi k)n}`

Deshalb kann eine erzeugte analoge Frequenz `f` als Alias im Bereich
`0...f_s/2` erscheinen:

`f_\mathrm{alias}=|f-k f_s|`

Dabei wird `k` so gewählt, dass `f_\mathrm{alias}` im Nyquist-Bereich liegt.

### Oversampling-Kette

Die praktische Lösung ist:

1. Upsampling um Faktor `L`
2. Nichtlinearität bei höherer Abtastrate anwenden
3. Tiefpassfilter vor dem Downsampling
4. Downsampling zurück auf die Projektabtastrate

Als Blockformel:

`x[n] \rightarrow \uparrow L \rightarrow f(\cdot) \rightarrow H_\mathrm{TP}(z) \rightarrow \downarrow L \rightarrow y[n]`

Der Tiefpass nach der Nichtlinearität ist entscheidend. Er entfernt die bei der
höheren Abtastrate erzeugten Obertöne oberhalb der Ziel-Nyquist-Frequenz, bevor
sie beim Downsampling aliasen können.

### Übergang zur Vorlesung 12

Vorlesung 12 startet genau an dieser Stelle: Wenn klar ist, welche neuen
Frequenzen eine Nichtlinearität erzeugt und warum Oversampling nötig wird,
können Clipper, Sättigung, Overdrive, Distortion, Fuzz und anschließend Dynamic
Range Control musikalisch und technisch sauber eingeführt werden.
