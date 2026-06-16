# Storyboard- und Exportplan Vorlesung 9

Thema: Filter und Delay-basierte Audioeffekte.

Referenz: Zoelzer 2011, Kapitel 2 "Filters and delays".

## Ordnungsentscheidung

Vorlesung 9 wird als konkrete Audio-FX-Vorlesung aufgebaut. Die Reihenfolge
bleibt nah an Kapitel 2:

1. Filtertypen und Parameter wiederholen
2. Allpass am Ende des Filtertypen-Blocks als Phasenfilter einfuehren
3. Equalizer und Peak-EQ vertiefen
4. Comb-Filter als Delay-basierte Filterwirkung aufbauen
5. zeitvariante Filter zeigen: zuerst Wah-Wah, dann Phaser
6. Delay-basierte Audioeffekte unterscheiden

Rueckblick nach der gehaltenen Folienspur: Die eigenen Storyboard-Bloecke 7
und 8 wurden nicht benoetigt. Fractional Delay und die Standardstruktur mit
variabler Delayline bleiben Reserve- beziehungsweise Implementationskontext,
aber nicht Teil der aktiven Produktion fuer Vorlesung 9.

Nicht in dieser Vorlesung:

- allgemeines FIR-Filterdesign
- Faltung und Convolution-FX
- Multiband-Delayeffekte
- Natural sounding comb filter
- tiefe Interpolationsfilter-Theorie
- Modulations-/Demodulationstheorie aus Kapitel 3
- Nichtlinearitaet aus Kapitel 4

## Geplante Storyboard-Ordner

- `png_storyboards/01_audio_fx_roadmap/`
- `png_storyboards/02_filtertypen_parameter/`
- `png_storyboards/03_peak_eq_koeffizienten/`
- `png_storyboards/04_zeitvariante_filter/`
- `png_storyboards/05_kammfilter_fir_iir/`
- `png_storyboards/06_delay_based_fx/`

## Block 1: Audio-FX-Roadmap

Ziel:

- Vorlesung 9 bis 11 als zusammenhaengenden Audio-FX-Block rahmen.
- Kapitelbezug aus Zoelzer 2011 sichtbar machen.

Bildideen:

- Timeline: VL9 Filter/Delay, VL10 Modulation/Demodulation, VL11 Nonlinear.
- Systemklassenkarte: LTI, LTV, NTI, NTV.

Moegliches Skript:

- `export_block_01_audio_fx_roadmap.py`

## Block 2: Filtertypen, Parameter und Allpass

Ziel:

- TP, HP, BP, BR/Notch und Allpass kurz wiederholen.
- Parameter \(f_c\), \(Q\), Bandbreite, Gain und Phase einordnen.

Bildideen:

- je eine eigene Abbildung mit Betrag in dB, logarithmischer Frequenzachse und Phase:
  - lowpass
  - highpass
  - bandpass
  - notch/bandreject
  - allpass magnitude + phase
- Magnitude in Gruen durchgezogen, Phase in Gruen gestrichelt.
- \(f_s=48\,\mathrm{kHz}\), Frequenzachse \(20\,\mathrm{Hz}\) bis \(20\,\mathrm{kHz}\),
  Betragsachse \(-15\,\mathrm{dB}\) bis \(5\,\mathrm{dB}\).
- Frequenzen: Low-pass \(5\,\mathrm{kHz}\), High-pass \(200\,\mathrm{Hz}\),
  Band-pass/Notch/All-pass \(500\,\mathrm{Hz}\).
- Zusatzserie fuer etwas hoehere Guete \(Q=1.25\), mit Referenzguete
  \(Q=1/\sqrt{2}\) in Grau und konstantem Achsenausschnitt.

Moegliches Skript:

- `export_block_02_filtertypen_parameter.py`

Erzeugte Abbildungen:

- `01_low_pass_filter_response.png`
- `02_high_pass_filter_response.png`
- `03_band_pass_filter_response.png`
- `04_band_stop_filter_response.png`
- `05_all_pass_filter_response.png`
- `06_low_pass_high_q_response.png`
- `07_high_pass_high_q_response.png`
- `08_band_pass_high_q_response.png`
- `09_band_stop_high_q_response.png`
- `10_all_pass_high_q_response.png`

## Block 3: Shelving- und Peak-EQ

Ziel:

- Low-Shelf, High-Shelf und Peak-EQ als Biquads aus \(f_c\), \(Q\), \(G\) erklaeren.
- Koeffizientenberechnung zeigen.
- Rueckbezug auf \(H(z)\), Pole/Nullstellen und Frequenzgang.

Bildideen:

- Peak-EQ-Frequenzgang bei 500 Hz zuerst mit vier Gain-Werten \(\pm6\,\mathrm{dB}\) und \(\pm12\,\mathrm{dB}\) bei Referenzguete.
- Peak-EQ-Frequenzgang danach mit erhoehter Guete \(Q=1.25\) und grauer Referenz.
- Low-Shelf-Frequenzgang als Gain-Familie zuerst mit Referenzguete, dann mit erhoehter Guete \(Q=1.25\) und grauer Referenz.
- High-Shelf-Frequenzgang als Gain-Familie zuerst mit Referenzguete, dann mit erhoehter Guete \(Q=1.25\) und grauer Referenz.
- DAW-EQ-Kaskade aus HP, drei Peak-EQs und High-Shelf.
- Summenphase der Kaskade als eigene Abbildung.
- Gruppenlaufzeit der Kaskade als eigene Abbildung mit sichtbaren negativen Werten.
- Koeffizientenbox im Stil von Vorlesung 7/8.
- optional: Pol-/Nullstellenbewegung fuer Boost/Cut.

Moegliches Skript:

- `export_block_03_peak_eq_koeffizienten.py`

Exportierte Dateien:

- `01_peak_eq_gain_variation.png`
- `02_peak_eq_higher_q.png`
- `03_low_shelf_reference_q.png`
- `04_low_shelf_higher_q.png`
- `05_high_shelf_reference_q.png`
- `06_high_shelf_higher_q.png`
- `07_daw_eq_cascade_magnitude.png`
- `08_daw_eq_cascade_phase_response.png`
- `09_daw_eq_cascade_group_delay.png`

## Block 4: Zeitvariante Filter

Ziel:

- Wah-Wah als bewegten Bandpass erklaeren.
- Phaser als zeitvariante Allpass-/Notch-Struktur erklaeren.
- Beide Effekte als Filtereffekte einordnen, nicht als Delay-FX.

Bildideen:

- Wah-Wah:
  - Startstandbild und GIF fuer \(Q=5\)
  - zusaetzliches Startstandbild und GIF fuer \(Q=15\)
  - weitere Serie mit \(Q=15\) und \(MIX=0{,}5\), wobei \(MIX=0\) den reinen Bandpass meint
  - bewegter Bandpasspeak von tiefen zu hoeheren Frequenzen und zurueck
  - TPT-SVF-Bandpass nach dem JSFX-Modell, mit \(1/Q\)-Normalisierung auf 0 dB Maximalpegel
  - eine feste graue Referenzkurve, momentane Antwort in Gruen
  - statischer 2D Pol-/Nullstellenplot und statische 3D z-Ebene an der Referenz
- Phaser aus Allpass-Kaskade:
  - vier Standbilder zum Aufbau:
    - Allpass A: Allpass zweiter Ordnung aus Block 2
    - Allpass B: Allpass zweiter Ordnung mit höherer Frequenz
    - \(A(z)B(z)\): Betrag bleibt flach, Phase addiert sich
    - Dry plus Allpass-Kaskade: Notch entsteht
  - Startstandbild und GIF
  - vier zeitvariable Allpass-Stufen bewegen die Notches wie im Plugin
  - erste Serie ohne Feedback: \(f_b=0\)
  - eine feste graue Referenzkurve, momentane Antwort in Gruen
  - statischer 2D Pol-/Nullstellenplot und statische 3D z-Ebene für den Summenfilter \(d+eA(z)B(z)\)
- Phaser-Feedback-Serie:
  - Startstandbild und GIF, in dem nur \(f_b\) variiert
  - graue Referenz ist \(f_b=0\)
  - \(f_\mathrm{AP}\), \(a\) und \(e\) bleiben konstant
- Phaser-Dry/Wet-Serie:
  - Startstandbild und GIF
  - Wet-Anteil \(e\) wird als didaktische Mix-Tiefensteuerung bewegt
  - Hinweis: In typischen Phasern moduliert der LFO eher \(a[n]\), nicht Dry/Wet
- Spektrogramme für dasselbe bandbegrenzte Rechtecksignal:
  - Wah-Wah zeigt die wandernde Bandpassbetonung über der Zeit
  - Phaser zeigt die zeitvariante Notch-/Phaseninterferenz über der Zeit

Skripte:

- `export_block_04_wah_wah.py`
- `export_block_04_phaser.py`
- `export_block_04_zeitvariante_filter.py`

Erzeugte Spektrogramme:

- `17_square_wah_wah_spectrogram.png`
- `18_square_phaser_spectrogram.png`

## Block 5: Kammfilter FIR und IIR

Ziel:

- Feedforward-Comb und Feedback-Comb unterscheiden.
- Delayzeit \(M\), Feedback \(g\), Kammabstand und Stabilitaet erklaeren.
- Comb als Bruecke verstehen: technisch Delayline, akustisch zunaechst Filterwirkung.

Bildideen:

- Impulsantwort FIR-Comb: direkter Impuls + verzogerter Impuls.
- Betrag FIR-Comb: periodische Kerben/Peaks.
- Impulsantwort IIR-Comb: abklingende Echo-Serie.
- Betrag IIR-Comb: schmale Resonanzen.
- Vergleich: \(g>0\), \(g<0\), groesseres/kleineres \(M\).
- Bildserie Spektrum: initiale Delayzeit in Gruen; danach initiale
  Delayzeit in Grau und neue Delayzeit in Gruen.
- Frequenzachse als normierte Kreisfrequenz \(\Omega/\pi\).
- Positive Filterkoeffizienten durchgezogen, negative gestrichelt.
- Normierung so, dass die maximale Amplitude bei \(0\,\mathrm{dB}\) liegt.
- Systemfunktion nicht in den Spektrum-Plots zeigen, sondern als separate
  z-Ebenen-Darstellung:
  - 2D Pol-/Nullstellendiagramm
  - 3D-Auswertung von \(|H(z)|\)

Moegliches Skript:

- `export_block_05_kammfilter_fir_iir.py`

Erzeugte Dateien:

- `01_fir_comb_initial_delay.png`
- `02_fir_comb_delay_comparison.png`
- `03_iir_comb_initial_delay.png`
- `04_iir_comb_delay_comparison.png`
- `05_fir_comb_z_plane_2d.png`
- `06_fir_comb_z_plane_3d.png`
- `07_iir_comb_z_plane_2d.png`
- `08_iir_comb_z_plane_3d.png`
- `09_fir_comb_dense_z_plane_2d.png`
- `10_iir_comb_dense_z_plane_2d.png`

## Block 6: Delay-basierte Audioeffekte

Ziel:

- Vibrato, Flanger, Chorus, Slapback und Echo ueber Delayzeit,
  Modulation, Mix und Feedback unterscheiden.

Bildideen:

- Eingangssignal:
  - Sägezahn im Zeitbereich in Schwarz
  - Spektrum des Sägezahns in Schwarz, im Frequenzlayout von Block 6
- Simple Chorus als Einstieg vor der Multi-Effect-Struktur:
  - Dry-Anteil plus zwei unabhängig modulierte Delaylines
  - \(y[n]=l\,x[n]+g_1x[n-M_1[n]]+g_2x[n-M_2[n]]\)
  - \(l=0{,}50\), \(g_1=g_2=0{,}35\)
  - \(M_1=12\pm2\,\mathrm{ms}\), \(M_2=20\pm3\,\mathrm{ms}\)
  - beide Delayzeiten werden mit unabhängiger Lowpass-Noise-Modulation bewegt
- Modulations-Bildserie:
  - zuerst Sinusmodulation
  - danach Sinus plus Lowpass-Noise
  - beide violett; Sinus durchgezogen, Lowpass-Noise gestrichelt
- Vibrato:
  - zuerst Sägezahn-Spektrogramm ohne Modulation
  - danach Sägezahn-Spektrogramm mit variabler Delayline
    nach DAFX: \(BL=0\), \(FF=1\), \(FB=0\),
    \(D[n]=0\dots3\,\mathrm{ms}\), Sinus mit \(5\,\mathrm{Hz}\)
  - Spektrogramm statt Frequenzgang, weil sich die Tonhöhe zeitlich ändert
- Chorus, Flanger und Doubling:
  - ebenfalls als Sägezahn-Spektrogramm
  - Flanger nach DAFX Tabelle 2.9: \(BL=0{,}7\), \(FF=0{,}7\), \(FB=0{,}7\),
    \(DELAY=0\,\mathrm{ms}\), \(DEPTH=2\,\mathrm{ms}\),
    \(MOD=1\,\mathrm{Hz}\) Sinus
  - Chorus als praktisches Preset: \(BL=0{,}7\), \(FF=0{,}7\), \(FB=-0{,}7\),
    \(DELAY=20\,\mathrm{ms}\), \(DEPTH=6\,\mathrm{ms}\),
    Lowpass-Noise nur als Modulationsquelle für \(D[n]\)
  - Doubler nach DAFX Tabelle 2.9: \(BL=0{,}7\), \(FF=0{,}7\), \(FB=0\),
    \(DELAY=100\,\mathrm{ms}\), \(DEPTH=100\,\mathrm{ms}\),
    Lowpass-Noise
  - Lowpass-Noise wird wie im JSFX nur zur Delaymodulation verwendet:
    neuer Zufallszielwert mit \(20\,\mathrm{Hz}\), danach \(1\,\mathrm{Hz}\)
    Glättung
  - Flanger zusätzlich als Frequenzgang-Animation des zeitvarianten Kammfilters
  - Chorus zusätzlich als Momentan-Frequenzgang einer einzelnen Delay-Voice
  - Doubler zusätzlich als Momentan-Frequenzgang der verzögerten Kopie
  - Vibrato bewusst nicht als Frequenzgang-Animation, sondern über das Spektrogramm
- Delayzeitbereiche als Achse:
  - Vibrato
  - Flanger
  - Chorus
  - Slapback
  - Echo
- variable Delayzeit \(M[n]\) als LFO-Kurve.
- Spektren/Comb-Kerben fuer Flanger vs Chorus.
- Impulsantworten fuer Slapback und Echo.

Moegliches Skript:

- `export_block_06_delay_based_fx.py`
- `export_block_06_flanger_frequency_response.py`
- `export_block_06_chorus_frequency_response.py`
- `export_block_06_doubler_frequency_response.py`

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

## Reserve: Fractional Delay Lines

Ziel:

- Zoelzer 2011, Kap. 2.5.4 didaktisch einfuehren.
- Erklaeren, warum variable Delayzeiten Werte zwischen zwei Samples brauchen.
- \(D=M+\mathrm{frac}\) als ganzzahligen und fractional Anteil lesen.
- Lineare Interpolation als einfachstes anschauliches Modell zeigen.

Rueckblick: Dieser Block wurde nicht produziert und nicht als eigene Folie
benoetigt. Die Inhalte bleiben als Reserve fuer eine spaetere Vertiefung.

Bildideen:

- Delayline mit Samplepositionen \(M-1\), \(M\), \(M+1\) und Zielpunkt
  \(M+\mathrm{frac}\).
- Aufbau der linearen Interpolation zwischen zwei benachbarten Samples.
- Vergleich: ganzzahliges Delay springt stufig, fractional Delay bewegt sich glatt.
- kurze Verfahrenskarte: linear, allpass, sinc, spline.

## Reserve: Standardstruktur mit variabler Delayline

Ziel:

- Zoelzer 2011, Abb. 2.34 didaktisch lesen.
- BL, FF, FB, MOD[n] und variable Delayline als gemeinsames Modell
  fuer mehrere Effekte erklaeren.

Rueckblick: Dieser Block wurde nicht produziert und nicht als eigene Folie
benoetigt. Die Standardstruktur bleibt als internes Modell im Delay-FX-Block.

Bildideen:

- vereinfachtes Blockdiagramm der Standardstruktur.
- dieselbe Struktur mit Parameter-Presets:
  - Vibrato
  - Flanger
  - Chorus
  - Slapback
  - Echo
- farbliche Hervorhebung:
  - direkter Pfad
  - Feedforward-Pfad
  - Feedback-Pfad
  - Modulationssignal

## Bild- und Plotvorgaben

- Plotstil aus Vorlesung 7 und 8 weiterverwenden.
- Frequenzachsen bevorzugt logarithmisch fuer Audio-Bezug.
- Bei Erklaerung von \(H(z)\) oder Pol-/Nullstellenlage weiterhin die
  z-Ebenen-Logik aus Vorlesung 8 verwenden.
- Koeffizientenboxen im Spektrum wie in Vorlesung 7/8.
- Modulations- und Delaypfade in Blockdiagrammen farblich konsistent halten.

## Exportskripte

Geplante Skripte:

- `export_block_01_audio_fx_roadmap.py`
- `export_block_02_filtertypen_parameter.py`
- `export_block_03_peak_eq_koeffizienten.py`
- `export_block_04_zeitvariante_filter.py`
- `export_block_05_kammfilter_fir_iir.py`
- `export_block_06_delay_based_fx.py`

## Offene Produktionsfragen

- Welche trockenen Audio-Samples werden fuer Hoerbeispiele genutzt?
- Sollen die Effektvergleiche als PNG-Serie oder GIF-Serie entstehen?
- Soll Abb. 2.34 nur konzeptionell nachgebaut oder als eigene didaktische
  Abbildung neu gezeichnet werden?
- Welche Parameterbereiche sollen fuer Flanger/Chorus/Slapback/Echo konkret
  demonstriert werden?
