# Lehrkonzept Vorlesung 10: Modulation und Morphing

Untertitel: Modulatoren nach Zölzer 2011.

Referenz: Zölzer, U. (Hrsg.): DAFX - Digital Audio Effects, 2nd edition,
2011, Kapitel 3 "Modulators and demodulators", gedruckte Seiten 83-99.

## Einordnung in die Audio-FX-Trilogie

Vorlesung 10 ist der zweite Teil des Audio-FX-Blocks:

| Vorlesung | Referenz in Zölzer 2011 | Schwerpunkt |
|---:|---|---|
| 9 | Kapitel 2: Filters and delays | Filter, EQ, Allpass, Comb, Phaser, Delay-FX |
| 10 | Kapitel 3: Modulators and demodulators | Ringmodulation, AM/SSB, PM/FM, Stereo Phaser, Rotary Speaker |
| 11 | Kapitel 3.3 und weitere Inhalte | Demodulatoren, Envelope-Follower, Auto-Wah |

Vorlesung 9 blieb nah an \(H(z)\), \(H(e^{j\Omega})\), Delayline, Phase,
Mischung und Feedback. Vorlesung 10 verschiebt den Blick: Ein Signal wird
nicht nur gefiltert oder verzögert, sondern durch ein zweites Signal gesteuert.
Dieses zweite Signal kann ein LFO, ein Oszillator, eine Hüllkurve oder ein aus
dem Eingangssignal extrahierter Parameter sein.

Die zentrale didaktische Leitfrage lautet:

> Was passiert, wenn ein Audiosignal durch ein anderes Signal gesteuert,
> verschoben oder analysiert wird?

## Rückgriff auf Vorlesung 9

Vorlesung 10 knüpft an vier Punkte aus Vorlesung 9 an:

1. Zeitvariante Effekte entstehen, wenn Parameter während der Signalverarbeitung
   bewegt werden.
2. Eine Delayline mit variabler Verzögerung kann als Phasenmodulation gelesen
   werden.
3. Ein LFO ist kein Audiosignal im engeren Sinn, sondern häufig ein langsames
   Steuersignal.
4. Viele Effekte werden erst verständlich, wenn Zeitbereich und Spektralbereich
   gemeinsam betrachtet werden.

In Vorlesung 9 wurden Vibrato, Flanger, Chorus und Phaser vor allem über
Effektklassen und hörbare Wirkung erklärt. In Vorlesung 10 wird die
Modulationssprache dahinter explizit gemacht.

## Scope-Entscheidung

Enthalten:

- Ringmodulation als Multiplikation zweier Signale
- Amplitudenmodulation und Tremolo
- Single-Side-Band-Modulation als Auswahl eines Seitenbands
- Wahrnehmungsbereiche von Modulationsfrequenzen: langsam, rau, hörbare
  Seitenbänder
- Frequenz- und Phasenmodulation als Winkelmodulation
- Phasenmodulation von Audiosignalen als zeitvariable Delayline
- Resampling-Faktor bei Sinus- und Rampenmodulation
- Anwendungen vor der Demodulation: Stereo Phaser und Rotary Speaker

Nicht enthalten:

- keine vollständige Nachrichtentechnik und kein AM/FM-Rundfunk im Detail
- keine analoge Schaltungstechnik von Modulatoren
- kein eigenständiger Frequency-Shifter-Effekt im Detail; der Frequency
  Shifter dient nur als Brücke zum SSB-Stereo-Phaser
- kein vollständiger Pitch-Shifter aus späteren Kapiteln
- keine erneute Vibrato-Einführung; Vibrato wurde in Vorlesung 9 über
  fractional delay behandelt und wird hier nur als bekannter Sonderfall
  der Delayline-Modulation referenziert
- keine Demodulatoren und Envelope-Follower im Detail; diese wurden nach
  Vorlesung 11 verschoben
- kein Auto-Wah-Block; dieser wurde nach Vorlesung 11 verschoben
- keine Dynamikprozessoren im Detail; Compressor, Limiter und Gate folgen später
- keine zusätzlichen optionalen Ausblicke; die Vorlesung endet mit den`r`n  Modulator-Anwendungen Stereo Phaser und Rotary Speaker

## Lernziele

Nach der Vorlesung sollen Studierende:

1. Ringmodulation, Amplitudenmodulation und Single-Side-Band-Modulation anhand
   ihrer Gleichungen
   unterscheiden können,
2. die Seitenbandbildung bei Multiplikation im Zeitbereich erklären können,
3. USB und LSB über Quadratur- beziehungsweise Hilbert-Signale erklären können,
4. Tremolo, Rauigkeit und hörbare Seitenbänder über die Modulationsfrequenz
   einordnen können,
5. PM und FM über die Phase eines Trägers beschreiben können,
6. die momentane Frequenz als Ableitung der Phase erklären können,
7. eine zeitvariable Delayline als Phasenmodulator lesen können,
8. Stereo Phaser und Rotary Speaker als Anwendungen von Modulation ohne
   vorherige Demodulation einordnen koennen.

## Zeitplanung und Blockstruktur

| Zeit | Block | Thema | Ziel |
|---:|---|---|---|
| 0-6 min | 1 | Roadmap Modulation/Demodulation | Von Filter/Delay zu Steuer- und Analysepfaden wechseln |
| 6-22 min | 2 | Ringmodulation, AM und Tremolo | Multiplikation, Seitenbänder, Tremolo und Rauigkeit erklären |
| 22-38 min | 3 | Single-Side-Band-Modulation | Hilbertfilter, Quadraturprodukte und USB/LSB-Auslöschung verstehen |
| 38-54 min | 4 | PM/FM und Delayline-Modulation | Winkelmodulation und zeitvariable Verzögerung mathematisch lesen |
| 54-68 min | 5 | Applications I: Stereo Phaser und Rotary Speaker | Modulation als Effektanwendung ohne Demodulation hören und sehen |

## Verwendete Parameter für Folien und Vorbereitung

Diese Übersicht ist als praktische Arbeitsnotiz gedacht. Sie beschreibt die
Werte, mit denen die aktuellen Abbildungen, Animationen und JSFX-Plugins
erzeugt wurden.

### Gemeinsame Notation

| Symbol | Bedeutung |
|---|---|
| \(f_s\) | Abtastrate |
| \(f_m\) | Modulationsfrequenz |
| \(f_c\) | Trägerfrequenz oder Filter-Mittenfrequenz, je nach Kontext |
| \(a_0\) | Gleichanteil beziehungsweise Offset im Amplitudenmodulator |
| \(\alpha\) | Modulationstiefe |
| \(\tau\) | Zeitkonstante eines einpoligen Glätters |
| \(\tau_a\) | Attack-Zeitkonstante |
| \(\tau_r\) | Release-Zeitkonstante |
| \(Q\) | Filtergüte beziehungsweise Resonanz |

Für den einpoligen Averager gilt:

$$
g = \exp\left(-\frac{1}{f_s\tau}\right).
$$

Für den Attack-Release-Averager werden zwei Koeffizienten verwendet:

$$
g_a = \exp\left(-\frac{1}{f_s\tau_a}\right), \qquad g_r = \exp\left(-\frac{1}{f_s\tau_r}\right).
$$

Der schnelle Koeffizient wird beim Anstieg verwendet, der langsamere beim
Abfall. In den Folien bedeutet ein größeres \(\tau\): langsamere Reaktion,
glattere Kurve, aber mehr zeitliche Verzögerung.

### Blockweise Parameter

| Block | Bildserie / Plugin | Genutzte Werte |
|---|---|---|
| 1 | Roadmap mit Bonobo-Audio | `Bonobo_Kerala.wav`, erste \(20\,\mathrm{s}\), Modulator \(f_m=0{,}25\,\mathrm{Hz}\), Hüllkurve \(\tau_a=10\,\mathrm{ms}\), \(\tau_r=180\,\mathrm{ms}\), Bassband \(60-250\,\mathrm{Hz}\), Analysefenster \(4096\) Samples, Hop \(512\) Samples, Kompressor-Demo \(g[n]=g_\mathrm{min}+\frac{1-g_\mathrm{min}}{1+10\,e[n]}\), \(g_\mathrm{min}=0{,}12\) |
| 2 | Ringmodulation mit Audio, hohe Modulationsfrequenz | \(f_s=48\,\mathrm{kHz}\), Bonobo-Träger \(20\,\mathrm{s}\), Tiefpass \(f_\mathrm{TP}=10\,\mathrm{kHz}\), Übergangsbereich \(1\,\mathrm{kHz}\), \(f_m=12\,\mathrm{kHz}\), Spektrum \(-24\) bis \(24\,\mathrm{kHz}\) |
| 2 | Ringmodulation hörbarer Bereich | Bonobo-Träger \(20\,\mathrm{s}\), Tiefpass \(f_\mathrm{TP}=800\,\mathrm{Hz}\), Übergangsbereich \(200\,\mathrm{Hz}\), \(f_m=2{,}4\,\mathrm{kHz}\), Spektrum \(-24\) bis \(24\,\mathrm{kHz}\) |
| 2 | Musikalische Ringmodulation | ungefilterter Bonobo-Träger, \(f_m=110\,\mathrm{Hz}\), Wet/Dry-Beispiel mit Wet-Anteil \(0{,}35\) |
| 2 | Sine-Ringmodulation und AM | \(f_s=48\,\mathrm{kHz}\), \(f_x=1\,\mathrm{kHz}\), \(f_m=200\,\mathrm{Hz}\), Ringmodulation mit \(a_0=0,\alpha=1\), AM-Linienbeispiele mit \(a_0=1,\alpha=1\) und \(a[n]=0{,}5+m[n]\) |
| 3 | SSB mit Audio | Bonobo-Träger \(20\,\mathrm{s}\), Tiefpass \(10\,\mathrm{kHz}\), \(f_m=12\,\mathrm{kHz}\), getrennte Ausgänge für USB und LSB, Hilbert-FIR \(N=129\), Kompensationsfilter \(z^{-64}\) |
| 3 | SSB-Sinus-Quadratur | \(f_x=1\,\mathrm{kHz}\), \(f_m=200\,\mathrm{Hz}\), direkter Produktzweig \(x(t)m_c(t)\), Quadraturzweig \(\hat{x}(t)m_s(t)\), Produktlinien bei \(800\,\mathrm{Hz}\) und \(1200\,\mathrm{Hz}\), Betrag links und Phase rechts |
| 2 | `simple_ringmod_tremolo_am.jsfx` | Tiefpass-Fader `F_LP_HZ`, Presets Ringmodulation, Tremolo, AM, SSB USB, SSB LSB; Ringmodulation \(a_0=0,\alpha=1\), Tremolo \(f_m=5\,\mathrm{Hz},a_0=1,\alpha=0{,}8\), AM \(f_m=110\,\mathrm{Hz},a_0=1,\alpha=0{,}8\) |
| 4 | PM/FM-Standbilder | didaktische Abtastrate \(1000\,\mathrm{Hz}\), Dauer \(6\,\mathrm{s}\), Träger \(f_c=8\,\mathrm{Hz}\), Modulator \(f_m=0{,}5\,\mathrm{Hz}\), \(\beta=1{,}5\pi\), \(\Delta f=\beta f_m\), Modulatorformen Sinus, Dreieck, Rechteck |
| 4 | `simple_pm_fm_delayline_effect.jsfx` | Modus PM/FM, Modulatorform Sinus/Dreieck/Rechteck, \(f_m=5\,\mathrm{Hz}\), Modulationstiefe \(\delta=0{,}4\), Grunddelay \(40\,\mathrm{ms}\), maximale Modulationsdelaytiefe \(20\,\mathrm{ms}\) |
| 5 | Stereo Phaser | Frequenzachse \(20\,\mathrm{Hz}\) bis \(20\,\mathrm{kHz}\), Betrag \(-35\) bis \(5\,\mathrm{dB}\), zwei Allpassketten mit je 6 Abschnitten, Direktsignal \(d=0{,}5\), SSB-Anteil \(e=0{,}5\), Cos-Phasen \(0^\circ\), \(45^\circ\), \(90^\circ\) |
| 5 | `simple_ssb_stereo_phaser.jsfx` | `RATE_HZ=0.35`, `D_GAIN=0.5`, `E_GAIN=0.5`, `OUT_DB=0` |
| 5 | `simple_rotary_loudspeaker.jsfx` | Rotationsfrequenz \(0{,}8\,\mathrm{Hz}\), Grunddelay \(M=10\,\mathrm{ms}\), Delaytiefe \(D=0{,}6\,\mathrm{ms}\), Amplitudentiefe \(\alpha=1\), Cross-Gain \(c=0{,}7\), Ramp-Zeit \(1200\,\mathrm{ms}\), Ausgang \(-3\,\mathrm{dB}\) |

## Block 1: Roadmap Modulation und Demodulation

### Grundidee

Modulation bedeutet: Ein Signal beeinflusst einen Parameter eines anderen
Signals. In der Nachrichtentechnik wird meistens ein niederfrequentes
Informationssignal auf einen hochfrequenten Träger aufgeprägt. In Audioeffekten
ist die Logik ähnlich, aber die Ziele sind andere: Klangveränderung,
Bewegung, Lebendigkeit, Verfremdung oder Analyse eines Eingangssignals.

Zölzer unterscheidet in Kapitel 3 zwei Seiten:

- Modulatoren: Sie erzeugen ein neues Signal, indem ein Signal ein anderes
  steuert oder multipliziert.
- Demodulatoren: Sie extrahieren aus einem Signal eine Steuergröße, zum
  Beispiel die Amplitudenhüllkurve.

### Tafelbild

$$
\text{Modulation:}\qquad x[n] \ \text{wird durch}\ m[n]\ \text{verändert}
$$

$$
\text{Demodulation:}\qquad x[n]\ \longrightarrow\ p[n]
$$

Dabei ist \(p[n]\) ein extrahierter Parameter, zum Beispiel Pegel, Hüllkurve,
momentane Frequenz oder ein Steuersignal für einen Effekt.

### Drei Grundoperationen

Für diese Vorlesung reichen drei mathematische Grundbilder:

1. Multiplikation:

$$
y[n] = x[n]\,m[n]
$$

2. Zeitvariable Skalierung:

$$
y[n] = a[n]\,x[n]
$$

3. Zeitvariable Verzögerung:

$$
y[n] = x[n-m[n]]
$$

Die erste und zweite Form sind eng verwandt. Die dritte Form ist die Brücke
zu Vibrato, Flanger und Pitch-Änderung.

### Didaktischer Merksatz

> Filter verändern die Gewichtung von Frequenzen. Modulatoren erzeugen neue
> spektrale Komponenten oder zeitliche Bewegung, weil Parameter selbst zu
> Signalen werden.

## Block 2: Ringmodulation, Amplitudenmodulation und Tremolo

### Ringmodulation nach Zölzer 2011, Abschnitt 3.2.1

Bei der Ringmodulation wird das Eingangssignal \(x[n]\) mit einem Träger
\(m[n]\) multipliziert:

$$
y[n] = x[n]\cdot m[n].
$$

Wenn der Träger ein Sinus oder Kosinus mit Trägerfrequenz \(f_c\) ist, dann
entstehen im Spektrum zwei verschobene Kopien des Eingangsspektrums:

- Upper Side Band, USB
- Lower Side Band, LSB

Für eine einfache Rechnung ist ein Kosinus hilfreich:

$$
x(t)=A_x\cos(2\pi f_x t), \qquad m(t)=A_c\cos(2\pi f_c t).
$$

Mit der Produktformel

$$
\cos(\alpha)\cos(\beta) = \frac{1}{2}\cos(\alpha+\beta) + \frac{1}{2}\cos(\alpha-\beta)
$$

folgt:

$$
y(t) = \frac{A_xA_c}{2} \cos\bigl(2\pi(f_x+f_c)t\bigr) + \frac{A_xA_c}{2} \cos\bigl(2\pi(f_x-f_c)t\bigr).
$$

Man hört also nicht mehr die ursprüngliche Frequenz \(f_x\), sondern
Summen- und Differenzfrequenzen:

$$
f_\mathrm{USB}=f_c+f_x, \qquad f_\mathrm{LSB}=|f_c-f_x|.
$$

Bei einem periodischen Eingang mit Grundfrequenz \(f_0\) und Harmonischen
\(k f_0\) entstehen Linien bei:

$$
f_{k,\pm}=|k f_0 \pm f_c|.
$$

### Spektrale Interpretation

Multiplikation im Zeitbereich entspricht Faltung im Frequenzbereich:

$$
y[n]=x[n]m[n] \quad\Longleftrightarrow\quad Y(e^{j\Omega}) = \frac{1}{2\pi} X(e^{j\Omega}) * M(e^{j\Omega}).
$$

Wenn \(m[n]\) ein einzelner Sinus ist, besteht \(M(e^{j\Omega})\) aus zwei
Linien bei \(\pm\Omega_c\). Die Faltung mit diesen Linien verschiebt das
Spektrum von \(x[n]\) nach oben und unten.

In normierter Kreisfrequenz:

$$
\Omega_c = 2\pi\frac{f_c}{f_s}.
$$

Bei einem Kosinusträger gilt idealisiert:

$$
Y(e^{j\Omega}) = \frac{1}{2} X(e^{j(\Omega-\Omega_c)}) + \frac{1}{2} X(e^{j(\Omega+\Omega_c)}).
$$

Das ist die zentrale mathematische Aussage dieses Blocks: Ein Modulator
verschiebt Spektren.

### Warum heißt es Ringmodulation?

Historisch kommt der Begriff aus analogen Schaltungen, in denen Dioden in
Ringform angeordnet waren. Für die digitale Signalverarbeitung ist der Name
weniger wichtig als die Operation:

$$
\text{Ringmodulation} = \text{Multiplikation ohne direkten Trägeranteil}.
$$

Der Träger selbst erscheint idealerweise nicht im Ausgang. Das unterscheidet
Ringmodulation von klassischer Amplitudenmodulation.

### Hörwirkung

Bei einfachen Sinustönen ist die Wirkung leicht vorherzusagen. Bei komplexen
Musiksignalen entstehen sehr viele Summen- und Differenzfrequenzen. Weil diese
Frequenzen meist nicht mehr harmonisch zur ursprünglichen Grundfrequenz
geordnet sind, klingt Ringmodulation oft:

- metallisch,
- glockenartig,
- technisch,
- fremd,
- inharmonisch.

### Didaktischer Stolperpunkt

Studierende erwarten bei Ringmodulation oft eine einfache Tonhöhenänderung.
Ringmodulation skaliert Frequenzen aber nicht proportional. Sie erzeugt
Summen- und Differenzfrequenzen. Dadurch bleiben harmonische Abstände meist
nicht erhalten.

## Amplitudenmodulation nach Zölzer 2011, Abschnitt 3.2.2

Bei der Amplitudenmodulation wird das Eingangssignal mit einem zeitvariablen
Faktor multipliziert:

$$
y[n] = \bigl(1+\alpha m[n]\bigr)x[n].
$$

Dabei gilt typischerweise:

- \(m[n]\): Modulator, meist auf Spitzenwert 1 normiert
- \(\alpha\): Modulationstiefe
- \(\alpha=0\): keine Modulation
- \(\alpha=1\): maximale Modulation ohne negatives Vorzeichen, wenn
  \(m[n]\in[-1,1]\)

Wenn \(m[n]\) ein LFO ist, entsteht Tremolo:

$$
m[n]=\sin\left(2\pi f_m\frac{n}{f_s}\right).
$$

Dann ist:

$$
y[n] = \left( 1+\alpha \sin\left(2\pi f_m\frac{n}{f_s}\right) \right)x[n].
$$

### Unterschied zwischen AM und Ringmodulation

AM lässt den ursprünglichen Signalanteil stehen:

$$
y[n] = x[n] + \alpha x[n]m[n].
$$

Der erste Term \(x[n]\) bleibt erhalten. Der zweite Term erzeugt Seitenbänder.

Ringmodulation enthält nur:

$$
y[n] = x[n]m[n].
$$

Der direkte Anteil fehlt. Deshalb ist Ringmodulation stärker verfremdend.

### Sinusrechnung für AM

Für

$$
x(t)=A_x\cos(2\pi f_x t), \qquad m(t)=\cos(2\pi f_m t)
$$

ergibt sich:

$$
y(t) = A_x\cos(2\pi f_x t) + \frac{\alpha A_x}{2} \cos\bigl(2\pi(f_x+f_m)t\bigr) + \frac{\alpha A_x}{2} \cos\bigl(2\pi(f_x-f_m)t\bigr).
$$

Man erhält also:

- Originalkomponente bei \(f_x\)
- unteres Seitenband bei \(|f_x-f_m|\)
- oberes Seitenband bei \(f_x+f_m\)

### Wahrnehmungsbereiche der Modulationsfrequenz

Zölzer beschreibt drei wichtige Bereiche:

| Modulationsfrequenz | Wahrnehmung | Typischer Effekt |
|---:|---|---|
| unter ca. 20 Hz | zeitliche Lautstärkeschwankung | Tremolo |
| ca. 20-70 Hz | Rauigkeit, Körnigkeit | roughness |
| deutlich darüber | getrennte Spektralkomponenten | AM-Klang, Seitenbänder |

Das ist didaktisch sehr wichtig: Dieselbe mathematische Operation kann als
zeitlicher Effekt oder als spektraler Effekt gehört werden. Der Unterschied
liegt in der Modulationsfrequenz.

### Typische Erklärung im Unterricht

> Tremolo ist keine neue Filterstruktur. Tremolo ist Amplitudenmodulation mit
> einem langsamen Modulator. Wenn der Modulator schneller wird, hört man nicht
> mehr nur Lautstärkeschwankung, sondern Rauigkeit und schließlich
> Seitenbänder.

## Block 3: Single-Side-Band-Modulation im Detail

### Single-Side-Band-Modulation nach Zölzer 2011, Abschnitt 3.2.3

Ringmodulation und klassische AM erzeugen bei einem sinusförmigen Modulator
immer zwei Seitenbänder. Die Single-Side-Band-Modulation, kurz SSB, entfernt
eines dieser Seitenbänder. Dafür braucht man zum Eingangssignal ein
Quadratursignal. In der digitalen Signalverarbeitung wird es mit der
Hilbert-Transformation gebildet:

$$
\hat{x}(t)=\mathcal{H}\{x(t)\}.
$$

Für eine einzelne Kosinus-Spektralkomponente gilt ideal:

$$
x(t)=\cos(2\pi f_c t),\qquad \hat{x}(t)=\sin(2\pi f_c t).
$$

Der Modulator wird ebenfalls in zwei um 90 Grad verschobene Komponenten
zerlegt:

$$
m_c(t)=\cos(2\pi f_m t),\qquad m_s(t)=\sin(2\pi f_m t).
$$

Das obere Seitenband entsteht durch:

$$
y_\mathrm{USB}(t)=x(t)m_c(t)-\hat{x}(t)m_s(t).
$$

Das untere Seitenband entsteht durch:

$$
y_\mathrm{LSB}(t)=x(t)m_c(t)+\hat{x}(t)m_s(t).
$$

Für eine einzelne Spektralkomponente kann man den Unterschied direkt über die
Additionstheoreme sehen:

$$
y_\mathrm{USB}(t)=\cos(2\pi f_c t)\cos(2\pi f_m t)-\sin(2\pi f_c t)\sin(2\pi f_m t)=\cos(2\pi(f_c+f_m)t).
$$

$$
y_\mathrm{LSB}(t)=\cos(2\pi f_c t)\cos(2\pi f_m t)+\sin(2\pi f_c t)\sin(2\pi f_m t)=\cos(2\pi(f_c-f_m)t).
$$

Didaktisch ist das der entscheidende Punkt: Ringmodulation erzeugt
\(f_c-f_m\) und \(f_c+f_m\). SSB benutzt ein zweites, phasenverschobenes
Produkt, sodass sich eines der beiden Seitenbänder auslöscht.

Für das Reaper-Plugin ist die gleiche Logik als Seitenbandumschalter gedacht:

$$
\text{Both:}\quad y(t)=a_0x(t)+\alpha x(t)m(t).
$$

$$
\text{USB/LSB:}\quad y(t)=a_0x_d(t)+\alpha\,y_\mathrm{USB/LSB}(t).
$$

Dabei ist \(x_d(t)\) das zeitlich an den Hilbert-Filter angepasste
Direktsignal. Für reine SSB wird \(a_0=0\) gesetzt. Wenn \(a_0=1\) bleibt der
Originalanteil als direkter Träger zusätzlich hörbar. Die Wahl von Sinus oder
Kosinus im LFO verändert nur die Anfangsphase, nicht die Lage des oberen oder
unteren Seitenbands.

Das `CF` im Schaltbild ist deshalb kein Klangfilter im engeren Sinn, sondern
ein Kompensationsfilter. Im idealen Erklärmodell ist es eine Verzögerung
\(z^{-D}\), die die Gruppenlaufzeit des Hilbertfilters ausgleicht. In der
Bildserie wird dafür ein FIR-Hilberttransformator mit \(N=129\) Samples und
\(D=64\) Samples verwendet. Der Hilbertfilter erzeugt den um 90 Grad
verschobenen Quadraturanteil, der CF-Zweig hält den nicht transformierten
Anteil zeitlich synchron.

Zur Erklärung wird zusätzlich die nichtkausale Version desselben
Hilbertfilters gezeigt. Dabei liegen die Koeffizienten um \(n=0\) herum auf
\(n=-64\ldots64\). Diese Darstellung ist nicht direkt implementierbar, zeigt
aber die eigentliche Hilbert-Eigenschaft ohne die zusätzliche lineare
Delayphase: Für positive Frequenzen liegt die Phase näherungsweise bei
\(-\pi/2\), also bei \(-90^\circ\).

Der Betrag ist bei endlicher Filterlänge im Bassbereich nicht ideal. Ein
längerer Hilbertfilter macht den Übergang vom gesperrten DC-Bereich zum
flachen Durchlassbereich steiler. Die Zusatzbilder mit 512 und 1024 Taps
zeigen deshalb, dass der nutzbare Amplitudenbereich nach unten erweitert wird.
Ein echter DC-Anteil bleibt trotzdem ein Sonderfall und wird durch die
Hilberttransformation nicht sinnvoll in ein um 90 Grad verschobenes Signal
überführt.

Die Bildserie im Unterblock verwendet als Träger das Bonobo-Audiosignal aus
Block 2, keinen Sinusträger. Das Signal wird auf ca. 10 kHz bandbegrenzt und
dann mit \(f_m=12\,\mathrm{kHz}\) moduliert. So sehen die Studierenden direkt,
wie aus einem komplexen Audiospektrum entweder die obere oder die untere
Seitenbandkopie entsteht. Die Kosinusrechnung oben ist nur die Erklärung für
eine einzelne Spektralkomponente innerhalb dieses komplexen Signals.

### Sinus-Detailbild: Betrag und Phase der Produktzweige

Für die Detailerklärung des SSB-Modulators wird zusätzlich ein rein
sinusförmiges Beispiel verwendet:

$$
x(t)=\cos(2\pi f_x t), \qquad m_c(t)=\cos(2\pi f_m t).
$$

Mit \(f_x=1\,\mathrm{kHz}\) und \(f_m=200\,\mathrm{Hz}\) entstehen im direkten
Produktzweig:

$$
x(t)m_c(t)=\frac{1}{2}\cos(2\pi(f_x-f_m)t)+\frac{1}{2}\cos(2\pi(f_x+f_m)t).
$$

Das Spektrum enthält also Linien bei \(800\,\mathrm{Hz}\) und
\(1200\,\mathrm{Hz}\). Für die SSB-Logik reicht der Betrag allein aber nicht:
Die Phasen der Produktzweige entscheiden, welches Seitenband sich bei Addition
oder Subtraktion auslöscht.

Der Quadraturzweig verwendet:

$$
\hat{x}(t)=\sin(2\pi f_x t), \qquad m_s(t)=\sin(2\pi f_m t).
$$

Daraus folgt:

$$
\hat{x}(t)m_s(t)=\frac{1}{2}\cos(2\pi(f_x-f_m)t)-\frac{1}{2}\cos(2\pi(f_x+f_m)t).
$$

Wichtig: Im Quadraturzweig werden nicht einfach alle Spektrallinien des
Produkts um \(90^\circ\) verschoben. Die \(90^\circ\)-Verschiebung wirkt
zunächst auf die beiden Einzelsignale \(x(t)\) und \(m_c(t)\). Erst danach
werden diese beiden verschobenen Signale multipliziert. Durch die
Multiplikation entstehen aber neue Frequenzen, nämlich Differenz- und
Summenfrequenz. Für diese neuen Frequenzen entscheidet die
Produktidentität \(\sin(\alpha)\sin(\beta)\), welche Phase entsteht:

$$
\sin(\alpha)\sin(\beta)=\frac{1}{2}\cos(\alpha-\beta)-\frac{1}{2}\cos(\alpha+\beta).
$$

Der Differenzanteil bleibt dadurch gleichphasig. Der Summenanteil bekommt ein
Minuszeichen. Ein Minuszeichen entspricht einer Phasendrehung um
\(\pi\) beziehungsweise \(180^\circ\). Deshalb liegen im direkten Produkt alle
Linien bei \(0^\circ\), während im Quadraturprodukt der Summenanteil bei
\(\pi\) beziehungsweise \(-\pi\) liegt. Genau dieser frequenzabhängige
Phasenunterschied ist die Voraussetzung dafür, dass sich bei Addition oder
Subtraktion gezielt ein Seitenband auslöscht.

Der Betrag ist an beiden Seitenbandfrequenzen wieder gleich, aber der
Summenanteil hat gegenüber dem direkten Produktzweig die Phase \(\pi\). Genau
dieser Vorzeichen- beziehungsweise Phasenunterschied ermöglicht die
Auslöschung:

$$
y_\mathrm{USB}(t)=x(t)m_c(t)-\hat{x}(t)m_s(t)=\cos(2\pi(f_x+f_m)t).
$$

$$
y_\mathrm{LSB}(t)=x(t)m_c(t)+\hat{x}(t)m_s(t)=\cos(2\pi(f_x-f_m)t).
$$

## Block 4: Frequenz- und Phasenmodulation, Delayline-Modulation

### Winkelmodulation nach Zölzer 2011, Abschnitt 3.2.4

Ein winkelmodulierter Träger kann kontinuierlich geschrieben werden als:

$$
x_{PM/FM}(t) = A_c\cos\left(2\pi f_c t+\varphi(t)\right).
$$

Die Phase \(\varphi(t)\) wird durch ein Modulationssignal gesteuert.

Bei Phasenmodulation:

$$
\varphi_{PM}(t) = k_{PM}m(t).
$$

Bei Frequenzmodulation:

$$
\varphi_{FM}(t) = 2\pi k_{FM}\int_{-\infty}^{t}m(\tau)\,d\tau.
$$

Der Unterschied ist:

- PM: Das Modulationssignal steuert direkt die Phase.
- FM: Das Modulationssignal steuert die momentane Frequenz; die Phase ist das
  Integral der Frequenzabweichung.

### Diskrete Foliennotation für PM und FM

Für die Folien sollte \(\varphi[n]\) eindeutig als Phase verwendet werden.
Die diskrete Kreisfrequenz \(\Omega\) ist dabei der Phasenzuwachs pro Sample
in rad/Sample:

$$
\Omega_c = 2\pi\frac{f_c}{f_s}.
$$

$$
\varphi_c[n] = \varphi_0 + \Omega_c n.
$$

\(\varphi_c[n]\) ist die unmodulierte Referenzphase des Trägers. Sie wächst
linear, weil die diskrete Kreisfrequenz \(\Omega_c\) konstant ist. Wichtig:
\(\Omega_c\) ist keine zweite Phase, sondern die Steigung der Phase pro Sample.
\(\varphi_0\) ist der Startwinkel beziehungsweise die Anfangsphase bei
\(n=0\).

Bei Phasenmodulation steuert das Modulationssignal direkt die zusätzliche
Phase:

$$
\Delta\varphi_\mathrm{PM}[n] = \beta m[n].
$$

Die gesamte PM-Phase ist:

$$
\varphi_\mathrm{PM}[n] = \varphi_c[n] + \Delta\varphi_\mathrm{PM}[n]
= \varphi_0 + \Omega_c n + \beta m[n].
$$

Das Ausgangssignal lautet:

$$
y_\mathrm{PM}[n]=\cos\left(\varphi_\mathrm{PM}[n]\right).
$$

Bei Frequenzmodulation steuert das Modulationssignal zuerst die momentane
Frequenz:

$$
f_i[n]=f_c+\Delta f\,m[n].
$$

Daraus folgt die zeitabhängige diskrete Kreisfrequenz:

$$
\Omega_i[n]=2\pi\frac{f_i[n]}{f_s}.
$$

Die FM-Phase entsteht durch Aufsummieren dieser diskreten Kreisfrequenzwerte.
Mit
\(\varphi_\mathrm{FM}[0]=\varphi_0\) gilt:

$$
\varphi_\mathrm{FM}[n+1]=\varphi_\mathrm{FM}[n]+\Omega_i[n].
$$

Äquivalent:

$$
\varphi_\mathrm{FM}[n]=\varphi_0+\sum_{k=0}^{n-1}\Omega_i[k],
\qquad n\geq 1.
$$

Das Ausgangssignal lautet:

$$
y_\mathrm{FM}[n]=\cos\left(\varphi_\mathrm{FM}[n]\right).
$$

Ein häufiger Stolperpunkt: Die Summe
\(\sum_{k=0}^{n}\Omega_i[k]\) ist nicht
falsch, wenn die Startphase entsprechend anders definiert wird. Für die
Generator-Konvention \(\varphi_\mathrm{FM}[0]=\varphi_0\) ist aber die Summe
bis \(n-1\) die klarere Schreibweise.

### Momentane Frequenz

Die momentane Kreisfrequenz ist die Ableitung der Phase:

$$
\omega_i(t) = \frac{d}{dt} \left(2\pi f_c t+\varphi(t)\right) = 2\pi f_c + \frac{d\varphi(t)}{dt}.
$$

Die momentane Frequenz in Hz ist:

$$
f_i(t) = \frac{1}{2\pi}\omega_i(t) = f_c+\frac{1}{2\pi}\frac{d\varphi(t)}{dt}.
$$

Das ist die Brücke zwischen Phase und wahrgenommener Tonhöhenbewegung.

### PM/FM in Audioeffekten versus Synthese

In der klassischen Synthese moduliert ein Signal die Phase oder Frequenz eines
Oszillators. In vielen Audioeffekten liegt aber bereits ein Audiosignal
\(x[n]\) vor. Dann wird nicht ein neuer Kosinus moduliert, sondern die
Zeitposition des Eingangssignals:

$$
y[n]=x[n-m[n]].
$$

Zölzer beschreibt diese Form als Phasenmodulation durch eine zeitvariable
Delayline.

### Zeitvariable Delayline als Phasenmodulator

Eine Verzögerung um \(m[n]\) Samples kann formal über eine zeitvariante
Impulsantwort geschrieben werden:

$$
h[n]=\delta[n-m[n]].
$$

Dann ist:

$$
y[n] = x[n]*h[n] = x[n]*\delta[n-m[n]] = x[n-m[n]].
$$

Für einen eingefrorenen Moment, also wenn \(m[n]\) lokal als konstant gelesen
wird, ergibt sich im Frequenzbereich:

$$
Y(e^{j\Omega}) = X(e^{j\Omega})e^{-j\Omega m[n]}.
$$

Der Betrag bleibt gleich, die Phase wird um \(-\Omega m[n]\) verschoben.
Wenn \(m[n]\) langsam variiert, bewegt sich diese Phase über die Zeit.

### Ganzzahliger und fractional Anteil

Da \(m[n]\) im Allgemeinen nicht ganzzahlig ist, wird zerlegt:

$$
m[n]=M[n]+\mathrm{frac}[n], \qquad M[n]\in\mathbb{Z}, \qquad 0\leq \mathrm{frac}[n]<1.
$$

Der ganzzahlige Anteil wird mit Delay-Speicher realisiert. Der fractional
Anteil benötigt Interpolation. Als einfache lineare Interpolation:

$$
y[n] = (1-\mathrm{frac}[n])x[n-M[n]] + \mathrm{frac}[n]x[n-M[n]-1].
$$

Zölzer verweist hier auf lineare, Lagrange-, Allpass- und Spline-Filter.
Für Vorlesung 10 reicht die Idee: Zeitvariable Phasenmodulation eines
Audiosignals braucht eine variable, meist fractional Delayline.

### Sinusförmige Delayline-Modulation als Rückgriff

Aus Vorlesung 9 ist bekannt: Wenn die Delayzeit sinusförmig bewegt wird,
entsteht eine periodische Tonhöhenschwankung.

$$
m[n] = M + DEPTH\cdot\sin(\omega_M nT).
$$

Dabei ist:

- \(M\): mittlere Verzögerung in Samples
- \(DEPTH\): Modulationstiefe in Samples
- \(\omega_M=2\pi f_M\): Modulationskreisfrequenz
- \(T=1/f_s\): Abtastperiode

Zölzer gibt den Resampling-Faktor:

$$
\alpha[n] = \frac{f_I}{f} = 1 - DEPTH\cdot\omega_M T \cos(\omega_M nT).
$$

Interpretation:

- \(f\): Eingangsfrequenz
- \(f_I\): momentane Ausgangsfrequenz
- \(\alpha[n]\): momentanes Pitch-Verhältnis

Der Mittelwert von \(\alpha[n]\) ist 1. Deshalb bleibt die mittlere Tonhöhe
gleich, aber sie schwankt periodisch um den Originalwert. In Vorlesung 10
dient diese Stelle nur als mathematische Verbindung zwischen variabler
Delayline und Phasenmodulation.

### Rechenbeispiel

Bei \(f_s=48\,\mathrm{kHz}\), \(DEPTH=3\,\mathrm{ms}\) und
\(f_M=5\,\mathrm{Hz}\):

$$
DEPTH_\mathrm{samples} = 0{,}003\cdot48000 = 144.
$$

Die maximale Abweichung des Resampling-Faktors ist:

$$
\Delta\alpha = DEPTH_\mathrm{samples} \cdot 2\pi f_M \cdot \frac{1}{f_s} = 144\cdot2\pi\cdot5/48000 \approx 0{,}094.
$$

Das entspricht einer momentanen Pitch-Schwankung von etwa \(\pm9{,}4\%\).
In Halbtönen:

$$
\Delta s = 12\log_2(1+\Delta\alpha) \approx 1{,}56\ \text{Halbtöne}.
$$

Das wäre bereits eine deutlich hörbare periodische Tonhöhenschwankung. Der
Effekt selbst wird hier nicht erneut als eigener Block behandelt.

### Rampenmodulation und Pitch-Transposition

Für eine rampenförmige Modulation:

$$
m[n]=M\pm SLOPE\cdot n
$$

gilt nach Zölzer:

$$
\alpha = \frac{f_I}{f} = 1\mp SLOPE.
$$

Hier ist \(\alpha\) konstant. Das Signal wird in der Tonhöhe transponiert,
aber die Länge ändert sich um den Faktor:

$$
\frac{1}{\alpha}.
$$

Das ist der Kern vieler Pitch-Transpositionstechniken: Wenn man schneller
durch das Signal liest, steigt die Tonhöhe und die Ausgabe wird kürzer. Wenn
man langsamer liest, sinkt die Tonhöhe und die Ausgabe wird länger.

### Didaktischer Merksatz

> Eine variable Delayline ist nicht nur ein Delay. Sie ist ein Zeitleser.
> Ändert sich die Leseadresse, ändert sich lokal die Tonhöhe.

## Block 5: Applications I: Stereo Phaser und Rotary Speaker

### Warum dieser Block vor den Demodulatoren kommt

Zölzer stellt nach den Modulatoren zunächst Demodulatoren vor und danach
Anwendungen. Für diese Vorlesung ist es didaktisch sinnvoll, zwei Anwendungen
vorzuziehen, die noch keine Demodulation benötigen:

1. Stereo Phaser
2. Rotary Speaker

Beide Effekte zeigen: Modulation ist nicht nur eine abstrakte
Nachrichtentechnik. Sie erzeugt direkt hörbare Bewegung im Raum, in der Phase
und im Spektrum. Erst danach wird die Frage behandelt, wie man aus einem
Audiosignal selbst ein Steuersignal gewinnt.

### Stereo Phaser über SSB nach Wardle und Zölzer

Zölzer beschreibt den Stereo Phaser in Abschnitt 3.4.2 als Anwendung eines
Single-Side-Band-Modulators. Die zugrunde liegende Idee stammt aus Wardles
Hilbert-Transformer-Frequency-Shifter: Ein Frequency Shifter ist ein
SSB-Modulator. Wenn die Verschiebefrequenz sehr klein ist und das verschobene
Signal wieder mit dem Eingang gemischt wird, entsteht kein klassischer
Pitch-Shifter, sondern ein Phaser mit wandernden Kerben.

Das ist für die Vorlesung günstig, weil Block 3 bereits SSB eingeführt hat.
Der Stereo Phaser ist dann kein neuer isolierter Effekt, sondern eine
Anwendung derselben Quadraturidee.

### Quadraturpfad

Wardle und Zölzer verwenden zwei Allpass-Zweige, die ungefähr 90 Grad
Phasendifferenz erzeugen:

$$
x_0[n]=A_0(-z^2)\{x[n]\}
$$

$$
x_{90}[n]=z^{-1}A_1(-z^2)\{x[n]\}
$$

Dabei sind \(A_0\) und \(A_1\) Allpassfilter. Ihr Betrag ist ungefähr eins,
aber ihre Phasen unterscheiden sich über einen großen Frequenzbereich um etwa
\(\pi/2\). Damit stehen zwei Signale in Quadratur zur Verfügung.

Wichtig für Fig. 3.11: Das sichtbare \(90^\circ\)-Symbol sitzt im
Modulatorpfad. Es erzeugt aus

$$
\cos(\omega_m n)
$$

den zweiten Modulator

$$
\sin(\omega_m n).
$$

Der Hilbert-Transformer für das Audiosignal ist dagegen durch die beiden
Allpass-Zweige realisiert. Ein idealer Hilbert-Filter hat

$$
H_\mathcal{H}(e^{j\Omega})=-j\,\operatorname{sgn}(\Omega).
$$

Das heißt:

- positive Frequenzen werden um \(-90^\circ\) gedreht,
- negative Frequenzen werden um \(+90^\circ\) gedreht,
- der Betrag bleibt idealerweise unverändert.

Die Drehung hängt also nicht davon ab, ob die momentane Phase eines Zeigers
positiv oder negativ ist. Sie hängt vom Vorzeichen der Frequenzkomponente ab.

### SSB-Ausgänge für links und rechts

Mit einem sehr langsamen Modulator

$$
c[n]=\cos(\omega_m n)
$$

$$
s[n]=\sin(\omega_m n)
$$

werden zwei entgegengesetzte Seitenbandrichtungen gebildet:

$$
y_L[n]=d\,x[n]+e\left(x_0[n]c[n]-x_{90}[n]s[n]\right)
$$

$$
y_R[n]=d\,x[n]+e\left(x_0[n]c[n]+x_{90}[n]s[n]\right)
$$

Interpretation:

- \(d\): Anteil des direkten Signals
- \(e\): Anteil des SSB-Signals
- \(y_L[n]\): eine Verschieberichtung
- \(y_R[n]\): die entgegengesetzte Verschieberichtung

Bei \(f_m\) im Sub-Audio-Bereich hört man keine stabile neue Tonhöhe. Die
leichte Frequenzverschiebung interferiert stattdessen mit dem direkten Signal.
Dadurch entstehen Kerben, die sich kontinuierlich über die Frequenzachse
bewegen. Weil links und rechts entgegengesetzte SSB-Richtungen nutzen, bewegen
sich die Kerben gegensinnig. Das erzeugt die Stereo-Wirkung.

### Warum das trotzdem ein Phaser ist

Ein statischer Phaser kann als Summe aus Direktsignal und phasenverdrehtem
Allpasspfad gelesen werden:

$$
H(z)=d+eA(z).
$$

Beim SSB-Stereo-Phaser ist der Allpass-/Quadraturpfad zusätzlich langsam
moduliert:

$$
H_L(z,n)=d+e\left(A_0(z)\cos(\omega_m n)-A_1(z)\sin(\omega_m n)\right)
$$

$$
H_R(z,n)=d+e\left(A_0(z)\cos(\omega_m n)+A_1(z)\sin(\omega_m n)\right)
$$

Formal ist das kein zeitinvariantes \(H(z)\), weil \(n\) explizit in der
Gleichung steht. Für die Folie ist es aber sinnvoll, eingefrorene
Momentaufnahmen zu zeigen: Für einen festen Zeitpunkt sieht man einen
Frequenzgang mit Kerben; über die Zeit wandern diese Kerben.

### Reaper-Plugin

Das Reaper-JSFX in diesem Projekt setzt genau diese Struktur um:

`audio_exports/reaper_jsfx/simple_ssb_stereo_phaser.jsfx`

Parameter:

- `RATE_HZ`: langsame SSB-Verschiebefrequenz \(f_m\)
- `D_GAIN`: direkter Anteil \(d\)
- `E_GAIN`: SSB-Anteil \(e\)
- `OUT_DB`: Ausgangspegel

Für die Demonstration ist \(f_m\) langsam, zum Beispiel
\(0{,}2\,\mathrm{Hz}\) bis \(1\,\mathrm{Hz}\). Bei deutlich höheren Werten
kippt der Effekt stärker in Richtung Frequency Shifter beziehungsweise
Ringmodulations-Charakter.

### Rotary Speaker / Leslie

Der Rotary-Speaker-Effekt kombiniert mehrere Modulationen:

1. Doppler-Effekt durch bewegte Schallquelle
2. Amplitudenmodulation durch Richtwirkung
3. Stereo-Bewegung durch zwei unterschiedlich gemischte Pfade

Signalverarbeitung nach Zölzer, hier bewusst in der einfachen Form aus
Fig. 3.13:

- zwei delay-modulierte Pfade A und B
- gegenphasige Delay-Modulationen
- synchrone Amplitudenmodulation mit \(1-\sin(\omega nT)\) und \(1+\sin(\omega nT)\)
- ungleiche Mischung auf linken und rechten Kanal, im Buch mit \(0{,}7\)

Vereinfacht:

$$
d_A[n]=M+D\sin(\omega_M nT), \qquad d_B[n]=M-D\sin(\omega_M nT).
$$

$$
u_A[n]=\left(1-\alpha\sin(\omega_M nT)\right)x[n-d_A[n]]
$$

$$
u_B[n]=\left(1+\alpha\sin(\omega_M nT)\right)x[n-d_B[n]]
$$

$$
y_L[n]=u_A[n]+c\,u_B[n], \qquad y_R[n]=c\,u_A[n]+u_B[n].
$$

Wenn sich das Horn auf den Hörer zubewegt:

- steigt die momentane Tonhöhe,
- steigt die Amplitude.

Wenn es sich wegbewegt:

- sinkt die momentane Tonhöhe,
- sinkt die Amplitude.

Damit ist der Rotary Speaker eine kombinierte Anwendung aus Delayline-
Modulation, Amplitudenmodulation und Stereo-Mischung.

Das zugehörige Reaper-JSFX liegt hier:

`audio_exports/reaper_jsfx/simple_rotary_loudspeaker.jsfx`

Die wichtigsten Parameter sind:

- `SPEED`: Manual, Chorale oder Tremolo
- `F_ROT_HZ`: Rotationsfrequenz \(f_m\)
- `BASE_DELAY_MS`: Grundverzögerung \(M\)
- `DEPTH_MS`: Modulationstiefe \(D\) der Delaylines, also Doppler-Anteil
- `AM_DEPTH`: Modulationstiefe der Richtwirkung
- `CROSS_GAIN`: ungleiche Stereo-Mischung \(c\), Standardwert \(0{,}7\)
- `RAMP_MS`: Trägheit beim Umschalten zwischen Chorale und Tremolo

Damit ist der Application-Block abgeschlossen. Mehr Anwendungen werden hier
nicht eingeführt, damit die Vorlesung wieder zurück zur systematischen
Signalflusslogik gehen kann: Wie gewinnt man aus einem Audiosignal ein
Steuersignal?

## Ausgelagerte Blöcke

Die ursprünglich geplanten Blöcke Demodulatoren/Envelope-Follower und Auto-Wah/Morphing liegen jetzt in ../11_demodulation_und_auto_wah/.

Damit endet Vorlesung 10 inhaltlich mit den Modulatoren und den Anwendungen Stereo Phaser sowie Rotary Speaker.

## Zusammenfassende Kernbotschaften

1. Modulation bedeutet, dass ein Signal einen Parameter eines anderen Signals
   verändert.
2. Multiplikation im Zeitbereich erzeugt Verschiebung und Seitenbänder im
   Frequenzbereich.
3. Ringmodulation unterdrückt den direkten Träger- beziehungsweise
   Originalanteil stärker als AM.
4. SSB löscht durch Quadratur- und Hilbert-Signale entweder das obere oder das
   untere Seitenband aus.
5. Tremolo ist AM mit langsamem Modulator.
6. PM und FM sind Winkelmodulationen; die momentane Frequenz ist die Ableitung
   der Phase.
7. Eine variable Delayline kann als Phasenmodulation eines Audiosignals gelesen
   werden.

## Literaturanker

- Zölzer 2011, Kap. 3.1: Introduction
- Zölzer 2011, Kap. 3.2.1: Ring modulator
- Zölzer 2011, Kap. 3.2.2: Amplitude modulator
- Zölzer 2011, Kap. 3.2.3: Single-side-band modulator
- Zölzer 2011, Kap. 3.2.4: Frequency and phase modulator
- Zölzer 2011, Kap. 3.4.2-3.4.5: Applications ohne erneute
  Vibrato-Behandlung
- Wardle 1998: Hilbert-transformer frequency shifter und SSB-Stereo-Phaser

## Abgrenzung zu Vorlesung 11

Vorlesung 10 endet mit Modulatoren und Anwendungen wie Stereo Phaser und Rotary Speaker. Die Demodulatoren, Envelope-Follower und Auto-Wah liegen jetzt in ../11_demodulation_und_auto_wah/.