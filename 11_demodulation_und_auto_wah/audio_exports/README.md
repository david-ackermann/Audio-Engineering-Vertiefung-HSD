# Audio-Exports und Reaper-JSFX Vorlesung 11

## Reaper-JSFX

- `reaper_jsfx/simple_sidechain_auto_wah.jsfx`
  - Anwendung zu Block 2: Sidechain-Envelope steuert die Mittenfrequenz eines Bandpassfilters.
- `reaper_jsfx/simple_oversampling_sine_clipper.jsfx`
  - Anwendung zu Block 5: Sinusgenerator, Hard Clipper, Oversampling und Lowpass vor dem Downsampling.

## Didaktische Zuordnung

Das Auto-Wah gehört zur Demodulation: Aus dem Sidechain-Signal \(s[n]\) wird ein
Envelope \(e[n]\) gewonnen, der anschließend einen Modulator beziehungsweise eine
Filtersteuerung antreibt.

Der Oversampling-Clipper gehört zum Aliasing-Block: Vor der Nichtlinearität wird
das Signal hochgesampelt, nach der Nichtlinearität wird tiefpassgefiltert und
anschließend wieder auf die Projektabtastrate zurückgeführt.
