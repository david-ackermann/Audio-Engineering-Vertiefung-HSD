# Audio-Effekte als Leitfaden für Vorlesungen 5 bis 11

## Ziel

Die Vorlesungen 5 bis 11 sollen ab jetzt deutlicher als Audio-Engineering-Strecke funktionieren:

> Erst hören, dann strukturieren, dann rechnen.

Die Studierenden sollen digitale Signalverarbeitung nicht als abstrakte Formelwelt erleben, sondern als Sprache, mit der vertraute Audioeffekte gebaut, gehört, verglichen und erklärt werden können. Die Literatur stützt genau diese Dramaturgie: Ein digitaler Audioeffekt wird als System mit Eingang, Ausgang und steuerbaren Parametern verstanden; technische Grundbausteine sind Gewichtung, Addition, Delay, Filter, Faltung, Modulation, Dynamikbearbeitung und nichtlineare Kennlinien.

## Quellenbasis

Seitenangaben beziehen sich auf die PDF-Seiten der lokalen Dateien.

- Leitquelle ab Vorlesung 5 ist Zölzer, `DAFX - Digital Audio Effects` (2011). Die Effektgruppen werden zuerst über Wahrnehmung eingeführt und danach technisch gelesen.
- Fuer den neuen Audio-FX-Block gilt die konkrete Zuordnung: Vorlesung 9 nutzt Kapitel 2 `Filters and delays`, Vorlesung 10 nutzt Kapitel 3 `Modulators and demodulators`, Vorlesung 11 nutzt Kapitel 4 `Nonlinear processing`.
- Zölzer und Lerch, `Digitale Audio-Effekte` (2025): kompakte deutschsprachige Rahmung für Bachelor-Studierende. Besonders geeignet für Grundoperationen, Impulsantwort, Faltung, FIR/IIR, Filtertypen, Delay/Kammfilter, Tremolo, Vibrato, Chorus, Flanger, Phaser, Dynamik, Faltungshall und nichtlineare Effekte. Relevante PDF-Seiten: 1-21.
- Zölzer, `DAFX - Digital Audio Effects` (2011): breites Referenzwerk für Effektklassen und Audio-Demos. Abschnitt 1.2.2 ist ab jetzt die Leitstruktur für die Wahrnehmungsklassifikation: Lautheit `L`, Dauer/Rhythmus `D`, Tonhöhe/Harmonie `P`, Klangfarbe/Qualität `T`, räumliche Eigenschaften `S` und mehrdimensionale Effekte. Relevante PDF-Seiten: 26-33, 66-70, 201-233, 234-238, 294-296, 485-486.
- Zölzer, `Digital Audio Signal Processing` (2008): solide DSP-Basis mit Audio-Fokus. Besonders geeignet für Equalizer, FIR/FFT-Faltung, Raumimpulsantworten, Comb/Allpass-Reverb und Dynamikbearbeitung. Relevante PDF-Seiten: 129-132, 171-182, 205-218, 240-245.

## Didaktisches Grundmuster

Jede Effekt-Vorlesung sollte im selben Rhythmus laufen:

1. Hören: trockenes Signal, Effekt A/B, dann ein extremer Parameterfall.
2. Wahrnehmen: Welches DAFX-Attribut ändert sich primär: Lautheit `L`, Dauer/Rhythmus `D`, Tonhöhe/Harmonie `P`, Klangfarbe/Qualität `T` oder räumliche Eigenschaften `S`?
3. Beobachten: Zeitverlauf, Spektrum, Spektrogramm, Impulsantwort oder Frequenzgang.
4. Benennen: Welche Grundoperation ist beteiligt: Gain, Summe, Delay, Filter, Faltung, Modulation, Feedback, Nichtlinearität?
5. Modellieren: eine kleine Gleichung oder ein Blockdiagramm.
6. Parametrisieren: ein bis drei Parameter, die im Plugin wiedererkannt werden.
7. Prüfen: Studierende sagen voraus, was beim Parameterwechsel zu hören und zu sehen sein wird.

Die Mathematik bleibt dabei knapp und funktionsbezogen. Bachelor-tauglich heißt hier:

- wenige Standardgleichungen sehr sicher können
- keine langen allgemeinen Herleitungen, wenn ein Beispiel die Struktur zeigt
- Pole/Nullstellen, z-Ebene und STFT-Phasen nur als Lesewerkzeuge einführen
- immer eine Audio-Entscheidung anschließen: klingt heller, räumlicher, bewegter, dichter, härter, komprimierter?

## DAFX-Wahrnehmungsklassifikation nach Abschnitt 1.2.2

Diese Einordnung ist ab jetzt die verbindliche Landkarte für die Audioeffekt-Vorlesungen. DAFX unterscheidet Hauptattribute und Nebenattribute: Das Hauptattribut beschreibt die beabsichtigte dominante Wahrnehmungsänderung; Nebenattribute können absichtlich oder als Artefakt mitverändert werden. Die Klassifikation ist nicht streng ausschließend, sondern eine Hör- und Kommunikationshilfe.

Kürzel:

| Kürzel | DAFX-Attribut | Deutsche Lesart |
|---|---|---|
| `L` | Loudness | Lautheit, Dynamik, Nuance, Akzent |
| `D` | Duration and rhythm | Dauer, Tempo, Rhythmus |
| `P` | Pitch and harmony | Tonhöhe, Chroma, Melodie, Intonation, Harmonie |
| `T` | Timbre and quality | Klangfarbe, Qualität, Textur, Helligkeit, Formanten |
| `S` | Spatial qualities | Ortung, Entfernung, Bewegung, Direktivität, Raum |

Steuerungskürzel: `A` steht für adaptive Steuerung, `cross-A` für cross-adaptive Steuerung und `LFO` für Low-Frequency Oscillator.

### Effekte mit Hauptattribut Lautheit `L`

| Effektname nach DAFX | Hauptattribut | Nebenattribute | Steuerung |
|---|---|---|---|
| compressor, limiter, expander, noise gate | `L` | `T` | `A` |
| gain/amplification | `L` | - | - |
| normalization | `L` | - | - |
| tremolo | `L` | - | `LFO` |
| violoning (attack smoothing) | `L` | `T` | `A` |

### Effekte mit Hauptattribut Dauer/Rhythmus `D`

| Effektname nach DAFX | Hauptattribut | Nebenattribute | Steuerung |
|---|---|---|---|
| time inversion | `D` | `P`, `L`, `T` | - |
| time-scaling | `D` | - | - |
| time-scaling with formant preservation | `D` | - | - |
| time-scaling with vibrato preservation | `D` | - | - |
| time-scaling with attack preservation | `D` | - | `A` |
| rhythm/swing change | `D` | `T` | `A` |

### Effekte mit Hauptattribut Tonhöhe/Harmonie `P`

| Effektname nach DAFX | Hauptattribut | Nebenattribute | Steuerung |
|---|---|---|---|
| pitch-shifting without formant preservation | `P` | `T` | - |
| pitch-shifting with formant preservation | `P` | - | - |
| pitch change | `P` | - | `A` |
| pitch discretization (auto-tune) | `P` | `T` | `A` |
| harmonizer/smart harmony | `P` | - | `A` |
| (in-)harmonizer | `P` | - | `A` |

### Effekte mit Hauptattribut räumliche Eigenschaften `S`

| Effektname nach DAFX | Hauptattribut | Nebenattribute | Steuerung |
|---|---|---|---|
| distance change | `S` | `L`, `T` | - |
| directivity | `S` | `P`, `T` | - |
| Doppler effect | `S` | `L`, `P` | - |
| echo | `S` | `L` | - |
| granular delay | `S` | `L`, `D`, `P`, `T` | `A` |
| reverberation | `S` | `L`, `D`, `T` | - |
| panning (2D, 3D) | `S` | - | - |
| spectral panning | `S` | `L`, `T` | - |
| rotary/Leslie | `S` | `P`, `T` | `LFO` |

### Effekte mit Hauptattribut Klangfarbe/Qualität `T`

| DAFX-Untergruppe | Effektname nach DAFX | Hauptattribut | Nebenattribute | Steuerung |
|---|---|---|---|---|
| spectral envelope | filter | `T` | `L` | - |
| spectral envelope | arbitrary resolution filter | `T` | `L` | - |
| spectral envelope | comb filter | `T` | `L`, `P` | - |
| spectral envelope | resonant filter | `T` | `L`, `P` | - |
| spectral envelope | equalizer | `T` | `L` | - |
| spectral envelope | wah-wah | `T` | `L`, `P` | - |
| spectral envelope | auto-wah (sensitive wah) | `T` | `L`, `D`, `P` | `LFO` |
| spectral envelope | envelope shifting | `T` | `L` | - |
| spectral envelope | envelope scaling | `T` | `L` | - |
| spectral envelope | envelope warping | `T` | `L` | - |
| spectral envelope | spectral centroid change | `T` | `L` | - |
| phase | chorus | `T` | - | random |
| phase | flanger | `T` | `P` | `LFO` |
| phase | phaser | `T` | `P` | `LFO` |
| spectral structure | spectrum shifting | `T` | `P` | - |
| spectral structure | adaptive ring modulation | `T` | `P` | `A` |
| spectral structure | texture change | `T` | - | - |
| spectrum and envelope | distortion | `T` | `L`, `P` | - |
| spectrum and envelope | fuzz | `T` | `L`, `P` | - |
| spectrum and envelope | overdrive | `T` | `L`, `P` | - |
| spectrum and envelope | spectral (in-)harmonizer | `T` | - | - |
| spectrum and envelope | mutation | `T` | `L`, `P` | `cross-A` |
| spectrum and envelope | spectral interpolation | `T` | `L`, `P` | `cross-A` |
| spectrum and envelope | vocoding | `T` | `L`, `P` | `cross-A` |
| spectrum and envelope | cross-synthesis | `T` | `L`, `P` | `cross-A` |
| spectrum and envelope | voice morphing | `T` | `L`, `P` | `cross-A` |
| spectrum and envelope | timbral metamorphosis | `T` | `L`, `P` | `cross-A` |
| spectrum and envelope | timbral morphing | `T` | `L`, `P` | `cross-A` |
| spectrum and envelope | whispering/hoarseness | `T` | `L` | - |
| spectrum and envelope | de-esser | `T` | `L` | `A` |
| spectrum and envelope | declicking | `T` | `L` | - |
| spectrum and envelope | denoising | `T` | `L` | - |
| spectrum and envelope | exciter | `T` | `L` | - |
| spectrum and envelope | enhancer | `T` | `L` | - |

### Effekte mit mehreren Hauptattributen

| Effektname nach DAFX | Hauptattribute | Nebenattribute | Steuerung |
|---|---|---|---|
| spectral compressor | `L`, `T` | - | - |
| gender change | `P`, `T` | `L` | `A` |
| intonation change | `L`, `P` | - | `A` |
| martianisation | `P`, `T` | `L` | `A` |
| prosody change | `L`, `D`, `P` | - | `A` |
| resampling | `D`, `T` | `L`, `P` | - |
| ring modulation | `P`, `T` | - | - |
| robotization | `P`, `T` | `L` | - |
| spectral tremolo | `L`, `T` | `D` | `LFO` |
| spectral warping | `T`, `P` | `L` | - |
| time shuffling | `L`, `D`, `P`, `T` | - | - |
| vibrato | `L`, `P` | `T`, `D` | `LFO` |

## Gemeinsames Demo-Material

Für alle kommenden Vorlesungen sollte ein kleiner, wiederkehrender Demo-Satz genutzt werden:

- `audio_samples/nachhallfrei/sprache/Speech_GrimmStoryExcerptGermanFemale.wav`: Sprache, gut für Verständlichkeit, Nähe, EQ, Kompression, Reverb, Distortion
- `audio_samples/nachhallfrei/drums/Conga_ITA.wav`: perkussive Transienten, gut für Attack, Körper, Raum, Delay, Reverb
- `audio_samples/nachhallfrei/drums/Drums_UltraVioletApology.wav`: Drumloop, gut für Punch, Groove, Kompression, Gate, Parallelkompression
- `audio_samples/nachhallfrei/instrumente/Cello.wav`: gehaltenes Instrument, gut für Klangfarbe, Wärme, EQ, Chorus, Phaser, Hall
- `audio_samples/nachhallfrei/instrumente/Strings_Streichquartett_mono.wav`: Monostreicher, gut für Breite, Stereo-Delay, Chorus, künstliche Räumlichkeit
- `audio_samples/nachhallfrei/instrumente/Bonobo_Kerala.wav`: musikalischer Kontext, gut für Vorher-Nachher-Vergleiche mit EQ, Dynamik, Raum und Modulation
- `audio_samples/nachhallfrei/testsignale/sweep.wav`: Sweep, gut für Frequenzgang, Filterbewegung, Nichtlinearität und Systemmessung
- später zusätzlich Raumimpulsantworten für Faltungshall und IR-Vergleich

Wichtig: Jede Demo sollte mit Dry/Wet, Parameterwerten und einer kleinen Visualisierung reproduzierbar sein.

## Vorlesung 5: Systeme, Faltung und Frequenzgang-Anschluss

### Audio-Hook

Vorlesung 5 startet nicht sofort mit Systemtheorie. Nach Orga und Wiederholung steht zuerst ein 30- bis 40-minütiger Überblick über Audioeffekte als Klangwerkzeuge. Der Block soll hörbar und sortierend sein:

- Was verändert der Effekt am Klang?
- Welche Parameter kann man anfassen?
- Welche grobe Systemklasse steckt dahinter?

Trockenes Sprach-, Gitarren-, Synth- oder Snare-Signal zuerst unverarbeitet hören, danach mehrere kurze Wet-Beispiele:

- EQ/Filter
- Slapback-Delay
- kurze oder lange Raumimpulsantwort
- Chorus, Flanger oder Phaser
- Compressor
- Distortion/Saturation

Danach wird die Landkarte sortiert:

- `L` Lautheit: compressor, limiter, expander, noise gate, gain/amplification, normalization, tremolo, violoning
- `D` Dauer/Rhythmus: time inversion, time-scaling, time-scaling with formant/vibrato/attack preservation, rhythm/swing change
- `P` Tonhöhe/Harmonie: pitch-shifting, pitch change, pitch discretization, harmonizer/smart harmony, (in-)harmonizer
- `S` räumliche Eigenschaften: distance change, directivity, Doppler effect, echo, granular delay, reverberation, panning, spectral panning, rotary/Leslie
- `T` Klangfarbe/Qualität: filter, equalizer, wah-wah, chorus, flanger, phaser, distortion, fuzz, overdrive, vocoding, cross-synthesis, exciter, enhancer
- mehrere Hauptattribute: spectral compressor, gender change, intonation change, martianisation, prosody change, resampling, ring modulation, robotization, spectral tremolo, spectral warping, time shuffling, vibrato

Nach dieser Wahrnehmungslandkarte folgt noch kein Detailblock zu einer einzelnen Effektklasse. Stattdessen wird dieselbe DAFX-Liste in grobe Systemklassen übersetzt:

| Systemklasse | Leitfrage | Typische DAFX-Effekte | Warum diese Klasse wichtig ist |
|---|---|---|---|
| lineare zeitinvariante Systeme | Bleibt die Wirkung unabhängig von Startzeit und Pegel gleich? | filter, equalizer, echo mit festen Parametern, reverberation über feste Impulsantwort, comb filter | Einstieg in Systembegriff, Impulsantwort und Faltung; Frequenzgang als Anschluss |
| zeitvariante lineare Systeme | Bleibt das System linear, aber ein Parameter bewegt sich in der Zeit? | tremolo, chorus, flanger, phaser, vibrato, rotary/Leslie | erklärt Modulation, LFO und bewegte Klangfarbe |
| nichtlineare Systeme | Entstehen durch Pegel oder Kennlinie neue Spektralanteile oder Pegelabhängigkeiten? | distortion, fuzz, overdrive, compressor, limiter, expander, noise gate | erklärt Kennlinien, Obertöne, Dynamik und Grenzen der LTI-Sicht |

Blockbasierte Analyse/Transformation/Synthese wie time-scaling, pitch-shifting oder Phase-Vocoder-Effekte kommt später als Erweiterung dazu. Für Vorlesung 5 reicht die erste klare Sortierung: LTI, zeitvariante lineare Systeme, nichtlineare Systeme.

Der eigentliche Übergang in die Systemtheorie lautet:

> Wir beginnen mit der einfachsten und wichtigsten Klasse: lineare zeitinvariante Systeme. Dort reichen Impulsantwort, Faltung und Frequenzgang erstaunlich weit.

Wenn diese Orientierung viel Raum braucht, ist das fachlich sinnvoll. Da Block 3 in der fünften Sitzung nicht mehr vorgestellt werden konnte, endet Vorlesung 5 beim gesicherten Stand aus Impulsantwort und Faltung. Impulsantwort und Frequenzgang werden als erster Fachblock in Vorlesung 6 nachgeholt; Delay, FIR und FIR-Differenzengleichungen folgen danach.

### Audio-Hook für den LTI-Einstieg

Nach der DAFX-Landkarte und der Systemklassenbrücke werden die LTI-Beispiele genauer gehört:

- Direktpfad
- einfaches Feedback-Echo
- kurze Raumimpulsantwort
- lange Raumimpulsantwort

Leitfrage:

> Warum reicht eine Impulsantwort, um den Klang eines linearen Systems vorherzusagen?

### Lernkern

- System als Abbildung $x[n]\to y[n]$
- Impuls $\delta[n]$ als Klick-Testsignal
- Impulsantwort $h[n]$ als Systemsignatur
- Faltung als Summe verschobener und gewichteter Impulsantworten
- Frequenzgang als zweite Sicht auf dieselbe LTI-Systemwirkung (verschoben nach Vorlesung 6, Block 1)

### Effektbezug

- Raum und Lautsprecher über Impulsantworten
- Faltungshall als direkte Anwendung von $x[n]*h[n]$
- EQ/Filter über Betrag und Phase des Frequenzgangs ab Vorlesung 6
- Echo als anschauliche Impulsantwort, ohne Delay-Struktur schon vollständig auszubauen

### Literaturanker

- Zölzer/Lerch 2025, PDF p1-5: Grundoperationen, Impulsantwort, Faltung, FIR/IIR.
- Zölzer 2008, PDF p205-208: Raumimpulsantwort als direkte Audioanwendung.
- DAFX 2011, PDF p20-22: Audioeffekt als System mit Eingang, Ausgang und Kontrollparametern.

### Bachelor-Grenze

Kein ROC, keine allgemeine z-Transformations-Theorie. $z^{-1}$ und $H(z)$
werden in Vorlesung 5 nicht eingefuehrt; die z-Sprache beginnt erst in
Vorlesung 8.

## Vorlesung 6: Frequenzgang, Delay, Speicher und FIR

### Audio-Hook

Zu Beginn wird der nicht mehr gehaltene Block aus Vorlesung 5 nachgeholt:

- Impulsantwort eines festen LTI-Systems zeigen
- Frequenzgang $H(e^{j\Omega})$ daraus lesen
- DFT-Rasterwerte $H_N[k]$ für verschiedene Längen vergleichen
- Spektrum eines Rechtecksignals mit $H_N[k]$ gewichten

Eine kurze Musik- oder Sprachspur sowie ein Klick durch Delay-Strukturen hören:

- reines Delay
- Feedforward-Delay als Slapback oder kurzer Comb-Filter
- Zwei-Tap-FIR als Tiefpass und Hochpass
- k-Tap-FIR, FIR-Notch und FIR-Tiefpass-Design

Danach dieselben Feedforward-Strukturen als Blockdiagramm, Koeffizientenfolge und FIR-Differenzengleichung zeigen.

### Lernkern

- Impulsantwort und Frequenzgang als nachgeholte LTI-Zweitsicht
- Delay als elementarer Speicherbaustein
- Feedforward nutzt vergangene Eingangswerte
- FIR-Koeffizienten sind die endliche Impulsantwort
- Differenzengleichung als FIR-Bauplan
- Tap-Anzahl, Fensterung und Gruppenlaufzeit als Entwurfsentscheidung
- Feedback/IIR erst in Vorlesung 7

### Effektbezug

- Slapback-Delay
- Comb-Filter durch Direktsignal plus kurze verzögerte Kopie
- Zwei-Tap-Tiefpass und Zwei-Tap-Hochpass
- FIR-Notch
- linearphasiger FIR-Tiefpass

### Literaturanker

- Zölzer/Lerch 2025, PDF p6-13: Filtertypen, FIR/IIR als späterer Anschluss, Delay/Kammfilter.
- Zölzer 2008, PDF p171-182: FIR-Realisierung und FFT-Faltung als Ausblick.
- DAFX 2011, PDF p66-70: Filter und Delays als zentrale Effektgrundlage.

### Bachelor-Grenze

Kein Feedback/IIR, keine z-Transformation, keine Pol-Nullstellen-Analyse. Die Vorlesung bleibt bei FIR, Koeffizienten, Frequenzgang und Gruppenlaufzeit.

## Vorlesung 7: IIR im Zeitbereich, Frequenzgang und Biquad

### Audio-Hook

Ein trockenes Signal und einen Sweep durch einfache Filter hören:

- Stabilitaet im Zeitbereich: stabile und instabile Impulsantwort
- einpoliges IIR mit $p=0.5$ und $p=-0.5$, wobei `p` hier nur der direkte Rueckfuehrungsfaktor im Einstiegsbeispiel ist
- reine Rueckfuehrung: glaettende und resonante Kurven
- Feedforward-Differenz: konstante Anteile verschwinden
- Filtertypen: Tiefpass, Hochpass, Bandpass, Notch, Low-Shelf, High-Shelf, Peaking-EQ
- Biquad: dieselben Filtertypen als kompakte praktische Standardform lesen

Danach die Strukturen weiterhin als Frequenzgang $H(e^{j\Omega})$ und Impulsantwort lesen. Beim Uebergang zur Standardform gilt fuer den einpoligen Fall `p=-a_1`; z-Transformation, Pole und Nullstellen folgen erst in Vorlesung 8.

### Lernkern

- Feedback/IIR als rekursive Erweiterung der FIR-Differenzengleichung
- `p` als anschaulicher Einstiegsparameter, `a_r` als Standardnotation des Feedback-Zweigs in der allgemeinen Filtergleichung
- einpoliges IIR aus Impulsantwort und geometrischer Reihe zu $H(e^{j\Omega})$ fuehren
- reine Rueckfuehrung als begrenzte Filterklasse verstehen
- Feedforward-`b_k` als notwendige Erweiterung fuer Hochpass, Notch und gezielte Ausloeschungen lesen
- allgemeine rekursive Filterform als Kombination aus FIR- und IIR-Anteil verstehen
- Biquad als praktische LTI-Filterform fuer typische Audiofilter einfuehren

### Effektbezug

- Notch-Filter
- Resonator
- parametrischer EQ als Biquad-Struktur
- PEQ-Zielkurve als linearphasiges FIR
- Comb-Filter als Brücke zu Vorlesung 8

### Literaturanker

- Zölzer/Lerch 2025, PDF p6-13: Filtertypen, FIR/IIR, Allpass, Equalizer, Delay/Kammfilter.
- Zölzer 2008, PDF p129-132: Equalizer-Grundtypen und grafische/parametrische Denkweise.
- DAFX 2011, PDF p66-70: Filter und Delays als zentrale Effektgrundlage.
- Zölzer 2008, PDF p171-182: FIR-Realisierung und FFT-Faltung als Ausblick.

### Bachelor-Grenze

Keine z-Transformation in Vorlesung 7. ROC, inverse z-Transformation, bilineare Transformation und Pol-/Nullstellen-Entwurf bleiben aussen vor. Ziel ist: $H(e^{j\Omega})$ aus Impulsantwort und Differenzengleichung lesen, Filtertypen hoeren und den Biquad als praktische Standardform einordnen.

## Vorlesung 8: z-Transformation, Pole/Nullstellen und Systemklassen

### Audio-Hook

Der Audio-Bezug kommt ueber Filter, Equalizer und Analyzer-Logik: Ein Biquad
aus Vorlesung 7 wird nicht nur als Frequenzgang, sondern als Struktur in der
z-Ebene gelesen. Pol- und Nullstellenlagen werden damit zur geometrischen
Erklaerung fuer Ausloeschung, Resonanz, Stabilitaet und Filterbenennung.

### Lernkern

- z-Transformation als Erweiterung von \(H(e^{j\Omega})\) zu \(H(z)\)
- \(z^{-1}\) als kompakte Schreibweise fuer ein Sample Delay
- Einheitskreis als Ort des Frequenzgangs
- freier Radius \(r\) als Erweiterung von stationaeren zu abklingenden oder
  anwachsenden Analysekernen
- Systemfunktion fuer FIR, IIR und Biquad aufstellen
- Nullstellen aus dem Zaehler und Pole aus dem Nenner bestimmen
- Pol-/Nullstellenlage mit Betrag, Phase, Stabilitaet und Audio-Wirkung
  verbinden
- abschliessend Audioeffekte nach Systemklassen einordnen: LTI, NTI, LTV und
  NTV

### Effektbezug

- LTI: Gain, Filter, Equalizer, Echo und Reverb koennen ueber Impulsantwort,
  Frequenzgang und Systemfunktion beschrieben werden.
- NTI: Saturation und Verzerrung brauchen Kennlinien statt nur \(H(z)\).
- LTV: Tremolo, Wah-wah, Chorus, Flanger, Phaser, Doppler, Rotary/Leslie und
  Vibrato brauchen zeitveraenderliche Parameter.
- NTV: Effekte mit Nichtlinearitaet und Zeitvariation verlassen die reine
  LTI-Sprache deutlich.

### Literaturanker

- Zoelzer/Lerch 2025, PDF p6-13: Filtertypen, FIR/IIR, Allpass, Equalizer,
  Delay/Kammfilter.
- DAFX 2011, PDF p29-31: Wahrnehmungsnahe Einordnung von Equalization, Echo,
  Reverb, Vibrato, Chorus und Flanging.
- DAFX 2011, PDF p66-70: Delay- und Filtergrundlagen.

### Bachelor-Grenze

ROC, inverse z-Transformation, bilineare Transformation und formaler
Pol-/Nullstellen-Entwurf bleiben aussen vor. Entscheidend ist, eine gegebene
Systemfunktion als Frequenzgang, z-Ebene und Audio-Wirkung lesen zu koennen.
## Vorlesung 9: Filter und Delay-basierte Audioeffekte

### Audio-Hook

Eine trockene Gitarren-, Vocal- oder Synth-Spur wird nacheinander durch
vertraute Plugin-Werkzeuge geschickt:

- Lowpass/Highpass
- Peak-EQ
- Allpass/Phaser
- FIR-Comb und IIR-Comb
- Wah-Wah
- Vibrato, Flanger, Chorus, Slapback und Echo

Die Studierenden sollen hoeren: Manche Effekte formen nur das Spektrum,
manche bewegen Parameter ueber die Zeit, manche erzeugen Interferenz durch
verzogerte Kopien.

### Lernkern

- Vorlesung 9 folgt Zoelzer 2011, Kapitel 2 "Filters and delays".
- Filtertypen werden ueber Betrag, Phase und Parameter gelesen.
- Ein Peak-EQ ist ein Biquad mit Koeffizienten aus \(f_c\), \(Q\) und \(G\).
- Ein Allpass veraendert nicht den Betrag, sondern die Phase.
- Ein Comb-Filter entsteht aus direkter und verzogerter Kopie oder aus
  Feedback in einer Delayline.
- Zeitvariante Filter- und Delay-Effekte entstehen, wenn Filterfrequenz oder Delayzeit
  langsam bewegt werden.
- Delay-basierte Effekte unterscheiden sich durch Delayzeit, Modulation, Mix
  und Feedback.

### Effektbezug

- TP/HP/BP/BR/Shelving/Peak: klassische Filter- und EQ-Werkzeuge.
- Allpass: Phasenwerkzeug und Grundlage fuer Phaser-Strukturen.
- Wah-Wah: bewegter Bandpass.
- Phaser: bewegte Phasenausloeschungen durch Allpass-/Notch-Strukturen.
- Vibrato: variable Delayzeit ohne dominanten Dry-Anteil.
- Flanger: kurze modulierte Delayline plus Dry-Signal und oft Feedback.
- Chorus: mehrere oder weicher modulierte Delaykopien.
- Slapback/Echo: laengere feste Delays mit wahrnehmbarer Wiederholung.

### Literaturanker

- Zoelzer 2011, Kapitel 2.2: Basic filters
- Zoelzer 2011, Kapitel 2.3: Equalizers
- Zoelzer 2011, Kapitel 2.4: Time-varying filters
- Zoelzer 2011, Kapitel 2.5: Basic delay structures
- Zoelzer 2011, Kapitel 2.6: Delay-based audio effects
- Zoelzer 2011, Abb. 2.34: Reservekontext fuer Standard effects with
  variable-length delay line, nicht als eigener VL9-Block durchgefuehrt

### Bachelor-Grenze

Kein allgemeines FIR-Filterdesign, keine Faltung, keine Multiband-Delays und
kein Natural-sounding-Comb-Filter. Fractional Delay nur als notwendige Idee
fuer variable Delayzeiten, nicht als Filterentwurfsproblem.

Rueckblick zu Vorlesung 9: Die eigenen Vertiefungsbloecke zu Fractional Delay
Lines und zur Standardstruktur wurden nicht benoetigt. Die gehaltene Spur
endet nach den zeitvarianten Delay-Effekten mit Aufgaben.

## Vorlesung 10: Modulation und Morphing

Vorlesung 10 folgt Zölzer 2011, Kapitel 3. Das detaillierte Einzelkonzept
liegt in `10_modulation_und_morphing/00_lehrkonzept_vorlesung_10.md`.

Der Schwerpunkt liegt auf Ringmodulation, Amplitudenmodulation, Tremolo,
Single-Side-Band-Modulation, Frequenz-/Phasenmodulation sowie Detektoren und
Demodulatoren als Steuersignalerzeuger. Anwendungen sind Auto-Wah, Rotary
Speaker, SSB-Effekte und Amplituden-Morphing. Der Modulation Vocoder steht am
Ende als optionaler Ausblick.

## Vorlesung 11: Nichtlineare Effekte

Vorlesung 11 folgt Zoelzer 2011, Kapitel 4. Der Schwerpunkt liegt auf
Dynamikprozessoren, Saturation, Distortion, Excitern und Enhancern. Die zentrale
Sprache sind Kennlinien, Envelope-Follower, harmonische Verzerrung,
Intermodulation und Aliasing-Risiko.

## Querlogik: Effekte nach Systemklasse

Die DAFX-Klassifikation oben ist die primäre Lehrlandkarte nach Wahrnehmung. Die folgende Tabelle ist nur die technische Zweitsicht, um nach dem Hören zu Blockdiagramm, Gleichung und Implementierung zu wechseln.

| Systemklasse | Hörbares Beispiel | Technische Sprache | Vorlesung |
|---|---|---|---|
| LTI mit kurzer IR | EQ, Lautsprecher, kurzer Raum | $h[n]$, $H(e^{j\Omega})$, ab Vorlesung 8 $H(z)$ | 5-9 |
| LTI mit Delay | Echo, Comb | $z^{-M}$, Feedforward, Feedback | 6, 9 |
| LTI mit langer IR | Faltungshall | lange FIR, FFT-Faltung | späterer Ausblick |
| Zeitvariant | Wah-Wah, Vibrato, Chorus, Flanger, Phaser | LFO, $D[n]$, Parameterbewegung | 9-10 |
| Modulierend/demodulierend | Tremolo, Ringmodulation, AM, FM/PM, Envelope-Follower | Träger, Seitenbänder, Detektion | 10 |
| Pegelabhängig | Compressor, Gate, Limiter | Kennlinie, Envelope, Attack/Release | 11 |
| Nichtlinear | Distortion, Saturation, Exciter/Enhancer | Kennlinie, Obertöne, Aliasing | 11 |
| Blockbasiert | Pitch-Shift, Time-Stretch | STFT, Analyse/Transformation/Synthese | späterer Ausblick |

## Mini-Aufgaben als wiederkehrendes Format

### Höraufgabe

Studierende hören Dry/Wet und markieren:

- welches DAFX-Hauptattribut verändert sich primär: `L`, `D`, `P`, `T` oder `S`?
- welche Nebenattribute werden hörbar mitverändert?
- wirkt der Effekt statisch oder zeitlich bewegt?
- entsteht ein längerer Nachklang?
- klingt es linear oder werden neue Obertöne erzeugt?

### Strukturaufgabe

Zu einem Effekt wird eine einfache Gleichung oder ein Blockdiagramm zugeordnet:

- $y[n]=x[n]+g x[n-M]$ für Feedforward-Delay
- $y[n]=x[n]+g y[n-M]$ für Feedback-Delay
- $y[n]=g[n]x[n]$ für Amplitudenmodulation und Tremolo in Vorlesung 10
- $y[n]=x[n-D(n)]$ für Vibrato
- $y[n]=x[n]+g x[n-D(n)]$ für Flanger

### Parameteraufgabe

Studierende sagen voraus, was passiert, wenn ein Parameter steigt:

- Cutoff größer: Grenzfrequenz wandert nach oben
- `Q` größer: Resonanz oder Kerbe wird schmaler und ausgeprägter
- EQ-Gain größer: Anhebung wird stärker
- Delay Time größer: Echoabstand größer, Comb-Kerben enger
- Feedback größer: längerer Nachklang, Stabilitätsfrage
- LFO Rate größer: Bewegung schneller
- Depth größer: Modulation stärker
- Wet-Anteil größer: Effektanteil wird dominanter

## Konsequenz für Storyboards und Python-Demos

Jeder neue Block sollte mindestens drei Exporttypen bekommen:

- Hör-/Systembild: Dry -> Effekt -> Wet mit Parameteranzeige
- Mechanikbild: Blockdiagramm oder Kopien/Delays/Faltung
- Analysebild: Impulsantwort, Frequenzgang, Spektrogramm oder Kennlinie

Die Python-Demos sollten nach Möglichkeit WAV-Dateien exportieren, nicht nur PNGs. Für die Vorlesung ist der Ablauf dann:

1. WAV hören
2. Plot ansehen
3. Gleichung lesen
4. Parameter verändern
5. erneutes WAV hören

## Was bewusst nicht Schwerpunkt wird

- tiefe allgemeine Filterentwurfsverfahren
- umfassende z-Transformations- und ROC-Theorie
- mathematisch vollständige Phase-Vocoder-Herleitung
- professionelle Reverb-FDN-Optimierung
- Machine-Learning-Audioeffekte als Kernstoff

Diese Themen können als Ausblick genannt werden, aber der Kern bleibt:

> Audioeffekte als gut hörbare Beispiele für digitale Systeme.
