# Block 6: Delay-basierte Audioeffekte

Ziel: Vibrato, Flanger, Chorus, Slapback und Echo ueber Delayzeit,
Modulation, Mix und Feedback unterscheiden.

Geplante Bildideen:

- Eingangssignal im Zeitbereich und als Spektrum, jeweils in Schwarz
- Sägezahn-Spektrogramm ohne Modulation als Ausgangspunkt
- Simple-Chorus-Spektrogramm als Einstieg:
  \(y[n]=l\,x[n]+g_1x[n-M_1[n]]+g_2x[n-M_2[n]]\),
  mit \(l=0{,}50\), \(g_1=g_2=0{,}35\),
  \(M_1=12\pm2\,\mathrm{ms}\), \(M_2=20\pm3\,\mathrm{ms}\),
  beide Delayzeiten mit unabhängiger Lowpass-Noise-Modulation
- Modulations-Bildserie:
  erst Sinusmodulation, dann zusätzlich Lowpass-Noise-Modulation;
  beide violett, Sinus durchgezogen, Lowpass-Noise gestrichelt
- Vibrato-Spektrogramm mit variabler Delayline nach DAFX:
  \(BL=0\), \(FF=1\), \(FB=0\), \(D[n]=0\dots3\,\mathrm{ms}\),
  \(MOD=5\,\mathrm{Hz}\) Sinus
- Flanger-Spektrogramm mit DAFX-Parametern:
  \(BL=0{,}7\), \(FF=0{,}7\), \(FB=0{,}7\),
  \(D[n]=0\dots2\,\mathrm{ms}\), \(MOD=1\,\mathrm{Hz}\) Sinus
- Chorus-Spektrogramm mit praktischem Preset:
  \(BL=0{,}7\), \(FF=0{,}7\), \(FB=-0{,}7\),
  \(DELAY=20\,\mathrm{ms}\), \(DEPTH=6\,\mathrm{ms}\),
  Lowpass-Noise nur als Modulationsquelle
- Doubler-Spektrogramm mit DAFX-Parametern:
  \(BL=0{,}7\), \(FF=0{,}7\), \(FB=0\),
  \(DELAY=100\,\mathrm{ms}\), \(DEPTH=100\,\mathrm{ms}\),
  Lowpass-Noise
- Chorus und Doubler nutzen dieselbe Lowpass-Noise-Logik wie das JSFX:
  neuer Zufallszielwert mit \(20\,\mathrm{Hz}\), geglättet mit \(1\,\mathrm{Hz}\)
- Flanger-Frequenzgang-Animation als eingefrorene Momentaufnahme des zeitvarianten Kammfilters
- Chorus-Frequenzgang-Animation als eingefrorene Momentaufnahme einer einzelnen Delay-Voice
- Doubler-Frequenzgang-Animation als eingefrorene Momentaufnahme der verzögerten Kopie
- Keine Vibrato-Frequenzgang-Animation: Vibrato wird über Tonhöhenbewegung im Spektrogramm erklärt
- Delayzeitbereiche der Effekte
- variable Delayzeit \(M[n]\)
- Flanger/Chorus-Vergleich
- Slapback- und Echo-Impulsantworten

Erzeugte Abbildungen:

- `00a_sawtooth_input_time.png`
- `00b_sawtooth_input_spectrum.png`
- `01_sawtooth_spectrogram_static.png`
- `02_simple_two_voice_chorus_spectrogram.png`
- `03a_modulation_sine.png`
- `03b_modulation_sine_lowpass_noise.png`
- `04_sawtooth_vibrato_spectrogram.png`
- `05_sawtooth_flanger_spectrogram.png`
- `06_flanger_magnitude_response_start.png`
- `07_flanger_magnitude_response_sweep.gif`
- `08_sawtooth_chorus_spectrogram.png`
- `09_sawtooth_doubler_spectrogram.png`
- `10_chorus_magnitude_response_start.png`
- `11_chorus_magnitude_response_sweep.gif`
- `12_doubler_magnitude_response_start.png`
- `13_doubler_magnitude_response_sweep.gif`

Einzelskripte fuer Frequenzgang-Animationen:

- `export_block_06_flanger_frequency_response.py`
- `export_block_06_chorus_frequency_response.py`
- `export_block_06_doubler_frequency_response.py`
