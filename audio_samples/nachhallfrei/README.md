# Nachhallfreie Audiosamples

Dieser Ordner ist für trockene, nachhallfreie Audiosamples gedacht, die in den kommenden Vorlesungen mit Audioeffekten bearbeitet werden.

## Ziel

Die Samples sollen als gemeinsamer Ausgangspunkt für DAFX-orientierte Hör- und Plot-Demos dienen. Jedes Beispiel sollte erst trocken gehört werden, danach mit einem Effekt, und anschließend über Wahrnehmung und Systemstruktur erklärt werden.

## Unterordner

- `sprache/`: kurze Sprachphrasen für EQ, Kompressor, Gate, Reverb, Distortion
- `drums/`: kurze Drumloops oder Einzelschläge für Kompression, Transienten, Reverb, Delay
- `instrumente/`: Gitarre, E-Piano, Synth, Bass oder gehaltene Töne für Chorus, Flanger, Phaser, Vibrato
- `testsignale/`: Impuls, Klick, Sinus, Sweep, Rauschen für Systemmessung, Frequenzgang und Impulsantworten

## Aktuelle Startsammlung

| Datei | Erste Wahrnehmungsfrage | Naheliegende DAFX-Bezüge |
|---|---|---|
| `sprache/Speech_GrimmStoryExcerptGermanFemale.wav` | Wie verändern sich Verständlichkeit, Präsenz und Nähe? | EQ, Kompressor, Gate, Reverb, Distortion |
| `drums/Conga_ITA.wav` | Wie werden Attack, Körper und Raum wahrgenommen? | Kompressor, Transient Shaping, Delay, Reverb |
| `drums/Drums_UltraVioletApology.wav` | Wie verändern sich Groove, Punch und Räumlichkeit? | Kompressor, Gate, Parallelkompression, Reverb |
| `instrumente/Cello.wav` | Wie verändern sich Klangfarbe, Wärme und Schwebung? | EQ, Chorus, Phaser, Faltungshall |
| `instrumente/Strings_Streichquartett_mono.wav` | Wie entsteht Breite aus einem trockenen Monosignal? | Chorus, Stereo-Delay, Reverb, künstliche Räumlichkeit |
| `testsignale/sweep.wav` | Was verrät ein Sweep über ein System? | Frequenzgang, Filter, Nichtlinearität, Messung |
| `instrumente/Bonobo_Kerala.wav` | Wie wirken Effekte in einem musikalischen Kontext? | EQ, Dynamik, Raum, Modulation, Vorher-Nachher-Vergleich |

## Benennung

Dateinamen bleiben bewusst ASCII und klein geschrieben:

- `voice_dry_01.wav`
- `drum_loop_dry_01.wav`
- `guitar_chord_dry_01.wav`
- `synth_note_dry_01.wav`
- `impulse_01.wav`
- `sine_440hz_01.wav`
- `sweep_20hz_20khz_01.wav`

## Technische Empfehlung

- WAV, mono oder stereo
- 48 kHz, 24 Bit oder 32 Bit float
- kurze Ausschnitte: 3 bis 12 Sekunden
- keine Normalisierung auf 0 dBFS; lieber Headroom lassen
- Zielpegel ungefähr zwischen -18 dBFS und -12 dBFS RMS, Peaks unter -3 dBFS
- möglichst ohne Hall, Delay, Chorus, Kompression oder Mastering-Limiter

## Wahrnehmungsnotizen

Zu jedem wichtigen Sample sollte später eine kurze Notiz ergänzt werden:

- Was hört man trocken?
- Welche Effekte eignen sich besonders?
- Welche Wahrnehmungsdimension steht im Vordergrund?
- Gibt es Störgeräusche, Raumanteil oder starke Transienten?

Beispiel:

| Datei | Wahrnehmung trocken | Geeignete Effekte | Hinweis |
|---|---|---|---|
| `voice_dry_01.wav` | Sprache, trocken, mittlere Dynamik | EQ, Kompressor, Reverb, Saturation | gut für Dry/Wet-Vergleich |
| `drum_loop_dry_01.wav` | Transienten, deutliche Peaks | Kompressor, Gate, Delay, Reverb | gut für Attack/Release |
| `guitar_chord_dry_01.wav` | gehaltene Akkorde | Chorus, Flanger, Phaser | gut für Modulation |

## Git-Hinweis

Kleine Demo-WAVs können im Projekt bleiben. Sehr große Rohaufnahmen sollten nicht ohne Entscheidung ins Repository gelegt werden.
