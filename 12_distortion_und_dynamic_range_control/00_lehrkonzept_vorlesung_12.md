# Lehrkonzept Vorlesung 12: Verzerrung, Sättigung und Dynamic Range Control

Diese Vorlesung setzt die gekürzte Vorlesung 11 fort. Dort wurden
Nichtlinearitäten, Harmonische, Intermodulation und Aliasing vorbereitet. Jetzt
werden daraus konkrete Audioeffekte entwickelt.

Referenz: Zölzer, DAFX, Kapitel 4.

## Lernziele

Die Studierenden sollen nach der Vorlesung erklären können,

- wie eine statische Kennlinie den Klang verändert,
- warum Clipping Obertöne und Intermodulation erzeugt,
- warum Soft Clipping anders klingt als Hard Clipping,
- wie Sättigung, Overdrive, Distortion und Fuzz didaktisch zusammenhängen,
- wie Exciter und Enhancer gezielt neue Spektralanteile hinzufügen,
- wie ein Dynamikprozessor aus Detektor, Zeitkontrolle, Kennlinie und Gain-Computer aufgebaut ist,
- wie sich Limiter, Compressor, Expander, Noise Gate und De-Esser unterscheiden.

## Anschluss an Vorlesung 11

Aus Vorlesung 11 werden drei zentrale Ergebnisse übernommen:

1. Eine Nichtlinearität erzeugt neue Frequenzen.
2. Bei mehreren Eingangstönen entstehen Intermodulationsprodukte.
3. In digitalen Systemen müssen erzeugte Frequenzen oberhalb Nyquist vor dem Downsampling entfernt werden.

Für diese Vorlesung ist deshalb die Grundkette wichtig:

`x[n] \rightarrow f(\cdot) \rightarrow y[n]`

mit einer statischen Kennlinie `f`.

---

## Block 1: Verzerrung und Sättigung

Storyboard-Ordner:

`png_storyboards/01_distortion_saturation/`

Unterordner:

- `01a_clipper_saturation_overdrive`
- `01b_harmonic_subharmonic_generation`
- `01c_exciter_enhancer`

### 1A: Clipper, Sättigung und Overdrive

Der Hard Clipper ist der einfachste Einstieg, weil die Kennlinie direkt sichtbar
ist:

`y[n]=\mathrm{clip}(g\,x[n],-T,T)`

Parameter:

- `g`: Eingangsverstärkung beziehungsweise Drive
- `T`: Clipping-Schwelle
- `x[n]`: Eingangssignal
- `y[n]`: Ausgangssignal

Bei kleinem Pegel ist das System fast linear:

`|g\,x[n]|<T \Rightarrow y[n]=g\,x[n]`

Bei großem Pegel wird das Signal begrenzt:

`g\,x[n]>T \Rightarrow y[n]=T`

`g\,x[n]<-T \Rightarrow y[n]=-T`

Didaktisch wichtig:

- Im Zeitbereich wird die Wellenform abgeflacht.
- Im Spektrum entstehen zusätzliche Obertöne.
- Bei mehreren Eingangstönen entstehen zusätzlich IMD-Produkte.
- Je härter die Kennlinie, desto stärker die hohen Spektralanteile.

Soft Clipping kann als glatter Übergang eingeführt werden:

`y[n]=\tanh(g\,x[n])`

oder normiert:

`y[n]=\frac{\tanh(g\,x[n])}{\tanh(g)}`

Der Unterschied zum Hard Clipper:

- keine harte Ecke in der Kennlinie,
- weniger stark ausgeprägte hohe Obertöne,
- oft musikalisch weicherer Klang.

Overdrive, Distortion und Fuzz können als Varianten derselben Grundidee
erklärt werden:

`Eingangsgain \rightarrow Nichtlinearität \rightarrow Klangfilter \rightarrow Ausgangspegel`

### 1B: Harmonic und Subharmonic Generation

Harmonic Generation nutzt Nichtlinearitäten gezielt, um neue Obertöne zu
erzeugen. Eine einfache Potenzkennlinie zeigt den Mechanismus:

`y[n]=a_1x[n]+a_2x^2[n]+a_3x^3[n]+\dots`

Geradzahlige Terme erzeugen bei symmetrischen Signalen DC- und geradzahlige
Anteile, ungeradzahlige Terme erzeugen ungeradzahlige Anteile. Bei realem
Programmmaterial erscheinen diese Anteile als spektrale Verdichtung.

Subharmonic Generation ist schwieriger, weil eine reine statische Kennlinie
keine echten Subharmonischen erzeugt. Dafür braucht man meist zusätzliche
Signalverarbeitung, zum Beispiel:

- Periodenerkennung,
- Frequenzteilung,
- Pitch-Tracking,
- nichtlineare Rectifier-Strukturen mit anschließender Filterung.

Das kann als kurzer Ausblick behandelt werden.

### 1C: Exciter und Enhancer

Ein Exciter erzeugt neue hochfrequente Anteile und mischt sie dosiert hinzu:

`y[n]=x[n]+\mu h[n]`

Dabei ist `h[n]` ein künstlich erzeugter Hochfrequenzanteil.

Eine typische Kette:

`x[n] \rightarrow Hochpass \rightarrow Nichtlinearität \rightarrow Pegel/Dosierung \rightarrow +`

Parameter:

- Hochpassfrequenz
- Drive der Nichtlinearität
- Mix-Faktor `\mu`
- Ausgangspegel

Ein Enhancer kann breiter verstanden werden: Er verändert wahrgenommene Präsenz,
Brillanz, Stereo- oder Basswirkung. Wichtig ist, den Begriff nicht nur als
Equalizer zu erklären, sondern als psychoakustisch motivierte Bearbeitung.

---

## Block 2: Dynamic Range Control

Storyboard-Ordner:

`png_storyboards/02_dynamic_range_control/`

Unterordner:

- `02a_time_control_sidechain`
- `02b_limiter`
- `02c_compressor_expander`
- `02d_noise_gate_de_esser`

### Grundstruktur eines Dynamikprozessors

Ein Dynamikprozessor besteht aus:

1. Detektor
2. Zeitkontrolle
3. statischer Pegelkennlinie
4. Gain-Computer
5. Anwendung des Gains auf das Audiosignal

Signalfluss:

`x[n] \rightarrow Detektor \rightarrow Zeitkontrolle \rightarrow Kennlinie \rightarrow g[n]`

`y[n]=g[n]x[n]`

Der Detektor kann aus Vorlesung 11 übernommen werden:

`d[n]=|x[n]|`

oder RMS-artig:

`d[n]=x^2[n]`

mit anschließender Mittelung.

### Pegel in dB

Für Dynamikprozessoren ist die dB-Darstellung meist didaktisch klarer:

`L_x[n]=20\log_{10}(|x[n]|+\epsilon)`

Eine statische Kennlinie wird dann als Eingangspiegel `L_x` zu Ausgangspegel
`L_y` gezeichnet.

### Limiter

Ein Limiter verhindert, dass der Ausgangspegel eine Schwelle überschreitet:

`L_y=\min(L_x,T)`

Der Gain in dB ist:

`G=L_y-L_x`

und linear:

`g=10^{G/20}`

Wichtig: Ein idealer Limiter ist nicht dasselbe wie ein Clipper. Der Limiter
regelt den Pegel über einen Gain, während der Clipper die Wellenform direkt
abschneidet.

### Compressor

Für einen Compressor mit Threshold `T` und Ratio `R` gilt oberhalb des Threshold:

`L_y=T+\frac{L_x-T}{R}`

unterhalb des Threshold:

`L_y=L_x`

Je größer `R`, desto stärker wird der Pegel oberhalb der Schwelle reduziert.
Ein Limiter ist der Grenzfall sehr großer Ratio.

### Expander

Ein Expander vergrößert Pegelunterschiede. Unterhalb der Schwelle kann gelten:

`L_y=T+R(L_x-T)`

mit `R>1`.

Dadurch werden leise Signale noch leiser. Das ist die Grundlage für Noise Gate
und Downward Expansion.

### Noise Gate

Ein Gate ist ein starker Expander:

`L_x<T \Rightarrow g \ll 1`

`L_x\geq T \Rightarrow g \approx 1`

Didaktisch wichtig sind Hysterese, Attack, Hold und Release, weil ein Gate ohne
Zeitlogik schnell flattert.

### De-Esser

Ein De-Esser ist ein frequenzselektiver Dynamikprozessor. Der Sidechain hört auf
den Sibilanzbereich, typischerweise mehrere Kilohertz:

`x[n] \rightarrow Bandpass/Hochpass \rightarrow Detektor \rightarrow Gain`

Der berechnete Gain wird dann breitbandig oder nur in einem Hochfrequenzband auf
das Signal angewendet.

---

## Block 3: Transfer aus Vorlesung 11

Storyboard-Ordner:

`png_storyboards/03_transfer_from_lecture_11/`

Dieser Block bleibt als Reserve und Übergang. Er kann verwendet werden, um zu
Beginn der Vorlesung 12 die Kernaussagen aus Vorlesung 11 kurz zu wiederholen:

- Nichtlinearität erzeugt neue Frequenzen.
- IMD ist bei Musiksignalen meist wichtiger als reine Harmonische.
- Oversampling und Tiefpassfilterung sind bei digitalen Verzerrern technisch zentral.

Danach kann direkt mit Clipper, Soft Clipping und Sättigung begonnen werden.
