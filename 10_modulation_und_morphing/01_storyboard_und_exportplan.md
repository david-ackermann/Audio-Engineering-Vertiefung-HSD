# Storyboard- und Exportplan Vorlesung 10: Modulation und Morphing

Thema: Modulatoren.

Referenz: Zölzer 2011, Kapitel 3 "Modulators and demodulators",
gedruckte Seiten 83-99.

## Ordnungsentscheidung

Vorlesung 10 folgt der Struktur von Kapitel 3, wird aber didaktisch auf eine
Bachelor-Vorlesung zugeschnitten:

1. Roadmap: von Filter/Delay zu Modulation/Demodulation
2. Ringmodulation, Amplitudenmodulation und Tremolo
3. Single-Side-Band-Modulation im Detail
4. Frequenz-/Phasenmodulation und variable Delayline
5. Applications I: Stereo Phaser und Rotary Speaker

Hinweis: Die ursprünglich geplanten Blöcke Demodulatoren/Envelope-Follower
und Auto-Wah/Morphing wurden nach `../11_demodulation_und_auto_wah/`
verschoben.

Die nicht mehr benötigten Ordner 08 und 09 wurden entfernt.

## Geplante Storyboard-Ordner

- `png_storyboards/01_audio_fx_roadmap/`
- `png_storyboards/02_am_modulation/`
- `png_storyboards/02_am_modulation/02_ringmodulation_am_tremolo/`
- `png_storyboards/02_am_modulation/02a_ringmodulation_sine_carrier/`
- `png_storyboards/02_am_modulation/02b_ringmodulation_audible_low_band/`
- `png_storyboards/02_am_modulation/02c_ringmodulation_musical_unfiltered/`
- `png_storyboards/02_am_modulation/02d_am_modulation_sine_carrier/`
- `png_storyboards/02_am_modulation/02d_am_modulation_sine_carrier_a0_0p5_alpha_1/`
- `png_storyboards/03_single_sideband_modulator/`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/`
- `png_storyboards/03_single_sideband_modulator/03b_ssb_hilbert_phasor_product/`
- `png_storyboards/04_pm_fm_delayline_modulation/`
- `png_storyboards/04_pm_fm_delayline_modulation/04a_angle_modulation_pm_fm/`
- `png_storyboards/05_applications_stereo_phaser_rotary/`
- `png_storyboards/05_applications_stereo_phaser_rotary/05a_stereo_phaser/`

## Block 1: Roadmap Modulation und Demodulation

Ziel:

- Vorlesung 10 als zweiten Teil der Audio-FX-Trilogie rahmen.
- Modulation als "Signal steuert Signal" einführen.
- Demodulation als "Signal wird zu Steuerparameter" einführen.

Bildideen:

- Timeline: VL9 Filter/Delay, VL10 Modulation/Demodulation, VL11 Nichtlinear.
- Zwei einfache Signalflussbilder:
  - Modulation: \(x[n]\), \(m[n]\), Effektparameter, \(y[n]\)
  - Demodulation: \(x[n]\), Analyseblock, \(p[n]\), gesteuerter Effekt
- Vergleichskarte:
  - \(y[n]=x[n]m[n]\)
  - \(y[n]=a[n]x[n]\)
  - \(y[n]=x[n-m[n]]\)

Mögliches Skript:

- `export_block_01_audio_fx_roadmap.py`

Erzeugte PNGs für die Einführungsfolie:

- `png_storyboards/01_audio_fx_roadmap/01_carrier_signal_bonobo_20s.png`
- `png_storyboards/01_audio_fx_roadmap/02_modulation_signal_low_frequency_sine.png`
- `png_storyboards/01_audio_fx_roadmap/03_carrier_times_modulation_product.png`
- `png_storyboards/01_audio_fx_roadmap/04_demodulated_envelope_from_bonobo.png`
- `png_storyboards/01_audio_fx_roadmap/05_demodulated_bass_envelope_from_bonobo.png`
- `png_storyboards/01_audio_fx_roadmap/06_demodulated_zero_crossing_rate_from_bonobo.png`
- `png_storyboards/01_audio_fx_roadmap/07_compressor_output_from_envelope.png`

## Block 2: Ringmodulation, AM und Tremolo

Ziel:

- Multiplikation als Seitenbandgenerator zeigen.
- Ringmodulation und AM unterscheiden.
- Tremolo, Rauigkeit und hörbare Seitenbänder über \(f_m\) einordnen.

Bildideen:

- Sinus mal Sinus im Zeitbereich:
  - Eingang \(x[n]\)
  - Träger \(m[n]\)
  - Ausgang \(y[n]\)
- Spektrum Ringmodulation:
  - Eingangslinie \(f_x\)
  - Ausgangslinien \(f_c-f_x\), \(f_c+f_x\)
  - Hinweis: Originalfrequenz fehlt
- Spektrum AM:
  - Originalfrequenz bleibt
  - Seitenbänder entstehen zusätzlich
- Tremolo-Zeitplot:
  - LFO \(m[n]\)
  - Hüllkurve \(1+\alpha m[n]\)
  - moduliertes Signal
- Wahrnehmungsachse:
  - unter 20 Hz: Tremolo
  - 20-70 Hz: Rauigkeit
  - darüber: Seitenbänder

Mögliches Skript:

- `export_block_02_ringmodulation_am_tremolo.py`

Reaper-JSFX:

- `audio_exports/reaper_jsfx/simple_ringmod_tremolo_am.jsfx`
- Einstellungen: Ringmodulation, Tremolo, AM, SSB USB und SSB LSB
- Parameter: `F_LP_HZ`, `PRESET`, `SIDEBAND`, `F_M_HZ`, `A_OFFSET`,
  `ALPHA`, `OUT_DB`
- `F_LP_HZ` steuert den Tiefpass auf dem Trägersignal vor der Modulation.
- `SIDEBAND=Both` ergibt klassische AM beziehungsweise DSB.
- `SIDEBAND=USB` oder `SIDEBAND=LSB` nutzt das Hilbert-Signal zur
  Auswahl eines einzelnen Seitenbands.
- Die SSB-Presets setzen \(f_m=12\,\mathrm{kHz}\), passend zur Bildserie mit
  bandbegrenztem Bonobo-Träger.

Erwartete Dateien:

- `01_original_carrier_time_20s.png`
- `02_original_carrier_spectrum_twosided.png`
- `03_band_limited_carrier_time_20s.png`
- `04_band_limited_carrier_spectrum_twosided.png`
- `05_modulation_signal_12khz_time_zoom.png`
- `06_modulation_signal_12khz_spectrum_twosided.png`
- `07_ring_modulated_output_time_20s.png`
- `08_ring_modulated_output_spectrum_twosided.png`

Zusätzliches Ringmodulations-Linienbeispiel:

- `export_block_02a_ringmodulation_sine_carrier.py`
- Träger: Sinus mit \(f_c = 1\,\mathrm{kHz}\)
- Modulationssinus: \(f_m = 200\,\mathrm{Hz}\)
- Ringmod-Gain: \(a[n] = m[n]\), also Sinus mit Amplitude \(1\)
- Ausgang: \(y[n] = a[n]x[n]\)
- Didaktische Idee: Ohne DC-Offset hat das Gain-Signal keinen Gleichanteil.
  Deshalb fehlt im Ausgangsspektrum der Carrier bei \(f_c\). Sichtbar bleiben
  nur die Seitenbänder bei \(f_c - f_m\) und \(f_c + f_m\).
- Spektralskalierung: Die Linienspektren sind zweiseitig skaliert. Ein Sinus
  mit Amplitude \(1\) erscheint daher mit Linienhöhe \(0{,}5\) bei
  \(\pm f\). Die Ringmodulations-Ausgangskomponenten haben jeweils
  Zeitsignal-Amplitude \(0{,}5\) und erscheinen deshalb mit Linienhöhe
  \(0{,}25\).

Erwartete Dateien:

- `png_storyboards/02_am_modulation/02a_ringmodulation_sine_carrier/01_carrier_sine_time.png`
- `png_storyboards/02_am_modulation/02a_ringmodulation_sine_carrier/02_carrier_spectrum.png`
- `png_storyboards/02_am_modulation/02a_ringmodulation_sine_carrier/03_modulation_sine_time.png`
- `png_storyboards/02_am_modulation/02a_ringmodulation_sine_carrier/04_modulation_spectrum.png`
- `png_storyboards/02_am_modulation/02a_ringmodulation_sine_carrier/05_ringmod_gain_signal_time.png`
- `png_storyboards/02_am_modulation/02a_ringmodulation_sine_carrier/06_ringmod_gain_spectrum_no_dc.png`
- `png_storyboards/02_am_modulation/02a_ringmodulation_sine_carrier/07_ringmod_output_time.png`
- `png_storyboards/02_am_modulation/02a_ringmodulation_sine_carrier/08_ringmod_output_spectrum_sidebands_only.png`

Zusätzliches hörbares Low-Band-Beispiel:

- `export_block_02b_ringmodulation_audible_low_band.py`
- Träger-Tiefpass: 800 Hz mit 200 Hz Übergangsbereich
- Modulationsfrequenz: 2,4 kHz
- Didaktische Idee: Das stark bandbegrenzte Trägerspektrum wird im hörbaren
  Bereich um die Modulationsfrequenz wiederholt.

Erwartete Dateien:

- `png_storyboards/02_am_modulation/02b_ringmodulation_audible_low_band/01_original_carrier_time_20s.png`
- `png_storyboards/02_am_modulation/02b_ringmodulation_audible_low_band/02_original_carrier_spectrum_twosided.png`
- `png_storyboards/02_am_modulation/02b_ringmodulation_audible_low_band/03_low_passed_carrier_time_20s.png`
- `png_storyboards/02_am_modulation/02b_ringmodulation_audible_low_band/04_low_passed_carrier_spectrum_twosided.png`
- `png_storyboards/02_am_modulation/02b_ringmodulation_audible_low_band/05_modulation_signal_2p4khz_time_zoom.png`
- `png_storyboards/02_am_modulation/02b_ringmodulation_audible_low_band/06_modulation_signal_2p4khz_spectrum_twosided.png`
- `png_storyboards/02_am_modulation/02b_ringmodulation_audible_low_band/07_audible_ring_modulated_output_time_20s.png`
- `png_storyboards/02_am_modulation/02b_ringmodulation_audible_low_band/08_audible_ring_modulated_output_spectrum_twosided.png`

Erwartete Audioexports:

- `audio_exports/02_am_modulation/02b_ringmodulation_audible_low_band/01_original_carrier_20s_48k.wav`
- `audio_exports/02_am_modulation/02b_ringmodulation_audible_low_band/02_low_passed_carrier_800hz_20s_48k.wav`
- `audio_exports/02_am_modulation/02b_ringmodulation_audible_low_band/03_modulation_signal_2p4khz_20s_48k.wav`
- `audio_exports/02_am_modulation/02b_ringmodulation_audible_low_band/04_audible_ring_modulated_output_20s_48k.wav`

Zusätzliches musikalisches Praxisbeispiel:

- `export_block_02c_ringmodulation_musical_unfiltered.py`
- Träger: ungefiltertes Originalsignal
- Modulationsfrequenz: 110 Hz
- Effektvariante 1: reine Ringmodulation, vollständig nass
- Effektvariante 2: musikalischer Wet/Dry-Mix mit 35 % Ringmodulation
- Didaktische Idee: In der Praxis wird Ringmodulation häufig ohne starke
  Vorfilterung eingesetzt; der Klang wird stattdessen über Modulationsfrequenz,
  Wet/Dry-Mix und gegebenenfalls nachgeschalteten EQ gestaltet.

Erwartete Dateien:

- `png_storyboards/02_am_modulation/02c_ringmodulation_musical_unfiltered/01_original_carrier_time_20s.png`
- `png_storyboards/02_am_modulation/02c_ringmodulation_musical_unfiltered/02_original_carrier_spectrum_twosided.png`
- `png_storyboards/02_am_modulation/02c_ringmodulation_musical_unfiltered/03_modulation_signal_110hz_time_zoom.png`
- `png_storyboards/02_am_modulation/02c_ringmodulation_musical_unfiltered/04_modulation_signal_110hz_spectrum_twosided.png`
- `png_storyboards/02_am_modulation/02c_ringmodulation_musical_unfiltered/05_ring_modulated_output_time_20s.png`
- `png_storyboards/02_am_modulation/02c_ringmodulation_musical_unfiltered/06_ring_modulated_output_spectrum_twosided.png`
- `png_storyboards/02_am_modulation/02c_ringmodulation_musical_unfiltered/07_wetdry_output_time_20s.png`
- `png_storyboards/02_am_modulation/02c_ringmodulation_musical_unfiltered/08_wetdry_output_spectrum_twosided.png`

Erwartete Audioexports:

- `audio_exports/02_am_modulation/02c_ringmodulation_musical_unfiltered/01_original_carrier_20s_48k.wav`
- `audio_exports/02_am_modulation/02c_ringmodulation_musical_unfiltered/02_modulation_signal_110hz_20s_48k.wav`
- `audio_exports/02_am_modulation/02c_ringmodulation_musical_unfiltered/03_ring_modulated_full_wet_110hz_20s_48k.wav`
- `audio_exports/02_am_modulation/02c_ringmodulation_musical_unfiltered/04_ring_modulated_wetdry_35pct_110hz_20s_48k.wav`

Zusätzliches AM-Linienbeispiel nach Zölzer Kapitel 3.2.2:

- `export_block_02d_am_modulation_sine_carrier.py`
- Träger: Sinus mit \(f_c = 1\,\mathrm{kHz}\)
- Modulationssinus: \(f_m = 200\,\mathrm{Hz}\)
- AM-Gain: \(a[n] = 1 + \alpha m[n]\) mit \(\alpha = 1\), also Verlauf von \(0\) bis \(2\)
- Ausgang: \(y[n] = a[n]x[n]\)
- Didaktische Idee: Der Offset `1` erzeugt einen Gleichanteil im Spektrum des
  AM-Gain-Signals. Dadurch bleibt im Ausgangsspektrum der Carrier bei \(f_c\)
  erhalten. Der sinusförmige Anteil erzeugt zusätzlich Seitenbänder bei
  \(f_c - f_m\) und \(f_c + f_m\).
- Spektralskalierung: Die Linienspektren sind zweiseitig skaliert. Der
  direkte Carrier mit Zeitsignal-Amplitude \(1\) erscheint mit Linienhöhe
  \(0{,}5\). Der AM-Gain enthält zusätzlich den DC-Anteil \(1\) und
  Sinuslinien der Höhe \(\alpha/2=0{,}5\). Die AM-Ausgangsseitenbänder haben
  Zeitsignal-Amplitude \(\alpha/2=0{,}5\) und erscheinen daher zweiseitig mit
  Linienhöhe \(\alpha/4=0{,}25\).

Erwartete Dateien:

- `png_storyboards/02_am_modulation/02d_am_modulation_sine_carrier/01_carrier_sine_time.png`
- `png_storyboards/02_am_modulation/02d_am_modulation_sine_carrier/02_carrier_spectrum.png`
- `png_storyboards/02_am_modulation/02d_am_modulation_sine_carrier/03_modulation_sine_time.png`
- `png_storyboards/02_am_modulation/02d_am_modulation_sine_carrier/04_modulation_spectrum.png`
- `png_storyboards/02_am_modulation/02d_am_modulation_sine_carrier/05_am_gain_signal_time.png`
- `png_storyboards/02_am_modulation/02d_am_modulation_sine_carrier/06_am_gain_spectrum_dc.png`
- `png_storyboards/02_am_modulation/02d_am_modulation_sine_carrier/07_am_output_time.png`
- `png_storyboards/02_am_modulation/02d_am_modulation_sine_carrier/08_am_output_spectrum_carrier_sidebands.png`

Zusätzliche AM-Linienserie mit DC-Offset \(0{,}5\):

- `export_block_02d_am_modulation_sine_carrier_a0_0p5_alpha_1.py`
- Träger: Sinus mit \(f_c = 1\,\mathrm{kHz}\)
- Modulationssinus: \(f_m = 200\,\mathrm{Hz}\)
- AM-Gain: \(a[n] = 0{,}5 + m[n]\), also der unveränderte Sinus \(-1\) bis \(1\), um \(0{,}5\) angehoben
- Verlauf von \(-0{,}5\) bis \(1{,}5\)
- Ausgang: \(y[n] = a[n]x[n]\)
- Didaktische Idee: Der DC-Offset mischt den trockenen Trägeranteil direkt im
  Gain-Signal hinzu. Gleichzeitig bleibt der volle Ringmodulationsanteil
  erhalten, weil der Sinus nicht mit \(\alpha<1\) skaliert wird.
- Spektralskalierung: Der AM-Gain enthält den DC-Anteil \(0{,}5\) und
  Sinuslinien der Höhe \(0{,}5\). Der Ausgang enthält Carrierlinien der Höhe
  \(0{,}25\) und Seitenbandlinien der Höhe \(0{,}25\).

Erwartete Dateien:

- `png_storyboards/02_am_modulation/02d_am_modulation_sine_carrier_a0_0p5_alpha_1/01_carrier_sine_time.png`
- `png_storyboards/02_am_modulation/02d_am_modulation_sine_carrier_a0_0p5_alpha_1/02_carrier_spectrum.png`
- `png_storyboards/02_am_modulation/02d_am_modulation_sine_carrier_a0_0p5_alpha_1/03_modulation_sine_time.png`
- `png_storyboards/02_am_modulation/02d_am_modulation_sine_carrier_a0_0p5_alpha_1/04_modulation_spectrum.png`
- `png_storyboards/02_am_modulation/02d_am_modulation_sine_carrier_a0_0p5_alpha_1/05_am_gain_signal_time.png`
- `png_storyboards/02_am_modulation/02d_am_modulation_sine_carrier_a0_0p5_alpha_1/06_am_gain_spectrum_dc.png`
- `png_storyboards/02_am_modulation/02d_am_modulation_sine_carrier_a0_0p5_alpha_1/07_am_output_time.png`
- `png_storyboards/02_am_modulation/02d_am_modulation_sine_carrier_a0_0p5_alpha_1/08_am_output_spectrum_carrier_sidebands.png`

Zusätzliche Zeigerprodukt-Serie für Summe und Differenzfrequenz:

- `export_block_02e_phasor_product_animation.py`
- Träger: reeller Kosinus mit zwei gegenläufigen Zeigern
  \(\frac{1}{2}e^{j\omega_x t}\) und \(\frac{1}{2}e^{-j\omega_x t}\)
- Modulator: reeller Kosinus mit zwei gegenläufigen Zeigern
  \(\frac{1}{2}e^{j\omega_m t}\) und \(\frac{1}{2}e^{-j\omega_m t}\)
- Frequenzverhältnis wie im Linienbeispiel: \(\omega_x : \omega_m = 5:1\)
- Didaktische Idee: Das Produkt entsteht aus vier Zeigerprodukten. Deren
  Winkelgeschwindigkeiten addieren sich und ergeben
  \(+\omega_x+\omega_m\), \(+\omega_x-\omega_m\),
  \(-\omega_x+\omega_m\) und \(-\omega_x-\omega_m\). Die paarweise
  konjugierten Zeiger bilden daraus Summen- und Differenzkosinus.

Erwartete Dateien:

- `png_storyboards/02_am_modulation/02e_phasor_product_sum_difference/01_two_signals_conjugate_pairs_preview.png`
- `png_storyboards/02_am_modulation/02e_phasor_product_sum_difference/02_two_signals_conjugate_pairs.gif`
- `png_storyboards/02_am_modulation/02e_phasor_product_sum_difference/03_product_build_00_input_phasors.png`
- `png_storyboards/02_am_modulation/02e_phasor_product_sum_difference/04_product_build_01_sum_positive.png`
- `png_storyboards/02_am_modulation/02e_phasor_product_sum_difference/05_product_build_02_difference_positive.png`
- `png_storyboards/02_am_modulation/02e_phasor_product_sum_difference/06_product_build_03_difference_negative.png`
- `png_storyboards/02_am_modulation/02e_phasor_product_sum_difference/07_product_build_04_sum_negative.png`
- `png_storyboards/02_am_modulation/02e_phasor_product_sum_difference/08_all_product_phasors_preview.png`
- `png_storyboards/02_am_modulation/02e_phasor_product_sum_difference/09_all_product_phasors.gif`
- `png_storyboards/02_am_modulation/02e_phasor_product_sum_difference/10_sum_difference_pairs_preview.png`
- `png_storyboards/02_am_modulation/02e_phasor_product_sum_difference/11_sum_difference_pairs_and_output.gif`

## Block 3: Single-Side-Band-Modulator im Detail

Ziel:

- SSB als Kombination aus direktem Produktzweig und Quadratur-Produktzweig
  verstehen.
- Hilbertfilter, Kompensationsfilter und 90-Grad-Quadratursignale getrennt
  erklären.
- An einem Sinusträger zeigen, dass die Beträge beider Produktzweige gleich
  sind, aber die Phasen das obere oder untere Seitenband auslöschen.

Mögliche Skripte:

- `export_block_03a_single_sideband_audio.py`
- `export_block_03b_ssb_hilbert_compensation_filters.py`
- `export_block_03c_ssb_sine_quadrature_products.py`
- `export_block_03d_ssb_hilbert_phasor_product_animation.py`

Audio-SSB-Beispiel:

- Träger: Bonobo-Audiosignal, 20 s, 48 kHz
- Vorverarbeitung: Bandbegrenzung des Trägers auf ca. 10 kHz wie im
  12-kHz-Ringmodulationsbeispiel
- Modulator: Sinus mit \(f_m = 12\,\mathrm{kHz}\)
- Quadraturpfad: Hilbert-Signal des bandbegrenzten Trägers plus um
  90 Grad verschobener Modulator
- Hilbert-Erklärbilder: endlicher FIR-Hilberttransformator, \(N=129\),
  Gruppenlaufzeit \(D=64\)
- Nichtkausale Hilbert-Erklärbilder: dieselben Koeffizienten auf
  \(n=-64\ldots64\) zentriert, damit die konstante 90-Grad-Phase ohne
  kausale Delayphase sichtbar wird
- Zusatzvergleich: nichtkausale Hilbertfilter mit 512 und 1024 Taps, um den
  verbesserten Amplitudenverlauf bei längeren Filtern zu zeigen
- CF-Erklärbilder: Kompensationsfilter als reine Verzögerung \(z^{-D}\), damit
  Direktsignal und Hilbert-Zweig zeitlich ausgerichtet sind
- USB-Ausgang: positive Träger-Spektralanteile werden nach oben verschoben
- LSB-Ausgang: positive Träger-Spektralanteile werden nach unten gespiegelt
- Didaktische Idee: Ringmodulation erzeugt beide Seitenbandkopien. SSB ergänzt
  einen zweiten Quadraturpfad, sodass nur die obere oder die untere Kopie
  übrig bleibt.
- Keine WAV-Beispiele, nur Abbildungen.
- Sinus-Detailbeispiel: \(f_x=1\,\mathrm{kHz}\), \(f_m=200\,\mathrm{Hz}\),
  Produktlinien bei \(800\,\mathrm{Hz}\) und \(1200\,\mathrm{Hz}\);
  Betrag links, Phase rechts.
- Unterblock `03a_single_sideband_material` enthält die bestehenden
  Audio-, Filter- und Spektrumserien. Die alten Phasor-Diagramme 27 und 28
  wurden entfernt.
- Unterblock `03b_ssb_hilbert_phasor_product` baut die Zeigerproduktserie
  noch einmal auf, ergänzt aber den Hilbert-/Quadraturzweig:
  \(x(t)m(t)\) liefert beide Seitenbänder, \(\hat{x}(t)\hat{m}(t)\)
  wird addiert oder subtrahiert, sodass wahlweise LSB oder USB übrig bleibt.

Erwartete Dateien:

- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/01_original_carrier_time_20s.png`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/02_original_carrier_spectrum_twosided.png`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/03_band_limited_carrier_time_20s.png`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/04_band_limited_carrier_spectrum_twosided.png`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/05_modulation_signal_12khz_time_zoom.png`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/06_modulation_signal_12khz_spectrum_twosided.png`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/07_usb_output_time_20s.png`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/08_usb_output_spectrum_twosided.png`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/09_lsb_output_time_20s.png`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/10_lsb_output_spectrum_twosided.png`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/11_hilbert_filter_impulse_response.png`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/12_hilbert_filter_magnitude_phase.png`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/13_compensation_filter_impulse_response.png`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/14_compensation_filter_magnitude_phase.png`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/15_noncausal_hilbert_filter_impulse_response.png`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/16_noncausal_hilbert_filter_magnitude_phase.png`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/17_noncausal_hilbert_filter_512_taps_impulse_response.png`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/18_noncausal_hilbert_filter_512_taps_magnitude_phase.png`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/19_noncausal_hilbert_filter_1024_taps_impulse_response.png`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/20_noncausal_hilbert_filter_1024_taps_magnitude_phase.png`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/21_direct_product_spectrum_magnitude_phase.png`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/22_quadrature_product_spectrum_magnitude_phase.png`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/23_usb_sine_spectrum_magnitude_phase.png`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/24_lsb_sine_spectrum_magnitude_phase.png`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/25_iir_correction_filter_impulse_response.png`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/26_iir_correction_filter_magnitude_phase.png`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/27_iir_hilbert_filter_impulse_response.png`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/28_iir_hilbert_filter_magnitude_phase.png`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/29_acausal_ideal_hilbert_filter_impulse_response.png`
- `png_storyboards/03_single_sideband_modulator/03a_single_sideband_material/30_acausal_ideal_hilbert_filter_magnitude_phase.png`
- `png_storyboards/03_single_sideband_modulator/03b_ssb_hilbert_phasor_product/01_direct_quadrature_inputs_preview.png`
- `png_storyboards/03_single_sideband_modulator/03b_ssb_hilbert_phasor_product/02_direct_quadrature_inputs.gif`
- `png_storyboards/03_single_sideband_modulator/03b_ssb_hilbert_phasor_product/03_ssb_input_phasors_before_products.png`
- `png_storyboards/03_single_sideband_modulator/03b_ssb_hilbert_phasor_product/04_direct_product_sum_frequency.png`
- `png_storyboards/03_single_sideband_modulator/03b_ssb_hilbert_phasor_product/05_direct_product_difference_frequency.png`
- `png_storyboards/03_single_sideband_modulator/03b_ssb_hilbert_phasor_product/06_quadrature_product_sum_frequency_phase_inverted.png`
- `png_storyboards/03_single_sideband_modulator/03b_ssb_hilbert_phasor_product/07_quadrature_product_difference_frequency.png`
- `png_storyboards/03_single_sideband_modulator/03b_ssb_hilbert_phasor_product/08_direct_and_quadrature_pair_sums_preview.png`
- `png_storyboards/03_single_sideband_modulator/03b_ssb_hilbert_phasor_product/09_direct_and_quadrature_pair_sums.gif`
- `png_storyboards/03_single_sideband_modulator/03b_ssb_hilbert_phasor_product/10_usb_cancellation_preview.png`
- `png_storyboards/03_single_sideband_modulator/03b_ssb_hilbert_phasor_product/11_usb_cancellation_and_output.gif`
- `png_storyboards/03_single_sideband_modulator/03b_ssb_hilbert_phasor_product/12_lsb_cancellation_preview.png`
- `png_storyboards/03_single_sideband_modulator/03b_ssb_hilbert_phasor_product/13_lsb_cancellation_and_output.gif`

## Block 4: PM, FM und Delayline-Modulation

Ziel:

- PM und FM als Winkelmodulation verstehen.
- Momentane Frequenz als Ableitung der Phase erklären.
- Variable Delayline als Phasenmodulation eines Audiosignals lesen.
- Resampling-Faktor für Sinus- und Rampenmodulation einordnen.

Bildideen:

- Winkelmodulation:
  - Trägerphase \(2\pi f_c t\)
  - zusätzlicher Phasenterm \(\varphi(t)\)
- PM versus FM:
  - Sinusmodulator: ähnliche Wirkung mit Zeitverschiebung
  - Puls- oder Rampenmodulator: Unterschied sichtbar machen
- Delayline-Modulation:
  - Schreib-/Leseposition in einer Delayline
  - \(m[n]=M+\mathrm{frac}[n]\)
  - lineare Interpolation zwischen Samples
- Rückgriff auf Vorlesung 9:
  - sinusförmige Delayline-Modulation nur als bekannte mathematische Brücke
  - keine erneute Vibrato-Bildserie
- Rampenmodulation:
  - konstantes \(\alpha\)
  - Pitch steigt oder sinkt, Länge ändert sich

Mögliches Skript:

- `export_block_04_pm_fm_delayline_modulation.py`
- `export_block_04b_pm_fm_phase_animation.py`
- `export_block_04c_fm_phase_derivation.py`

Erwartete Dateien:

- `png_storyboards/04_pm_fm_delayline_modulation/04a_angle_modulation_pm_fm/01_input_carrier.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04a_angle_modulation_pm_fm/02_pm_sine_modulator.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04a_angle_modulation_pm_fm/03_pm_sine_signal.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04a_angle_modulation_pm_fm/04_pm_sine_phase.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04a_angle_modulation_pm_fm/05_fm_sine_modulator.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04a_angle_modulation_pm_fm/06_fm_sine_signal.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04a_angle_modulation_pm_fm/07_fm_sine_phase.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04a_angle_modulation_pm_fm/08_pm_triangle_modulator.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04a_angle_modulation_pm_fm/09_pm_triangle_signal.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04a_angle_modulation_pm_fm/10_pm_triangle_phase.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04a_angle_modulation_pm_fm/11_fm_triangle_modulator.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04a_angle_modulation_pm_fm/12_fm_triangle_signal.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04a_angle_modulation_pm_fm/13_fm_triangle_phase.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04a_angle_modulation_pm_fm/14_pm_rectangle_modulator.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04a_angle_modulation_pm_fm/15_pm_rectangle_signal.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04a_angle_modulation_pm_fm/16_pm_rectangle_phase.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04a_angle_modulation_pm_fm/17_fm_rectangle_modulator.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04a_angle_modulation_pm_fm/18_fm_rectangle_signal.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04a_angle_modulation_pm_fm/19_fm_rectangle_phase.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04b_pm_fm_phase_animation/01_pm_sine_phase_modulation_preview.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04b_pm_fm_phase_animation/02_pm_sine_phase_modulation.gif`
- `png_storyboards/04_pm_fm_delayline_modulation/04b_pm_fm_phase_animation/03_pm_triangle_phase_modulation_preview.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04b_pm_fm_phase_animation/04_pm_triangle_phase_modulation.gif`
- `png_storyboards/04_pm_fm_delayline_modulation/04b_pm_fm_phase_animation/05_pm_rectangle_phase_modulation_preview.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04b_pm_fm_phase_animation/06_pm_rectangle_phase_modulation.gif`
- `png_storyboards/04_pm_fm_delayline_modulation/04b_pm_fm_phase_animation/07_fm_sine_frequency_modulation_preview.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04b_pm_fm_phase_animation/08_fm_sine_frequency_modulation.gif`
- `png_storyboards/04_pm_fm_delayline_modulation/04b_pm_fm_phase_animation/09_fm_triangle_frequency_modulation_preview.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04b_pm_fm_phase_animation/10_fm_triangle_frequency_modulation.gif`
- `png_storyboards/04_pm_fm_delayline_modulation/04b_pm_fm_phase_animation/11_fm_rectangle_frequency_modulation_preview.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04b_pm_fm_phase_animation/12_fm_rectangle_frequency_modulation.gif`
- `png_storyboards/04_pm_fm_delayline_modulation/04b_pm_fm_phase_animation/13_pm_constant_phase_0_preview.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04b_pm_fm_phase_animation/14_pm_constant_phase_0.gif`
- `png_storyboards/04_pm_fm_delayline_modulation/04b_pm_fm_phase_animation/15_pm_constant_phase_minus_pi_over_2_preview.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04b_pm_fm_phase_animation/16_pm_constant_phase_minus_pi_over_2.gif`
- `png_storyboards/04_pm_fm_delayline_modulation/04c_fm_phase_derivation/01_fm_derivation_modulator_m_n.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04c_fm_phase_derivation/02_fm_derivation_instantaneous_frequency.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04c_fm_phase_derivation/03_fm_derivation_discrete_angular_frequency_omega_i.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04c_fm_phase_derivation/04_fm_derivation_omega_i_before_sum.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04c_fm_phase_derivation/05_fm_derivation_accumulated_phase_phi_fm.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04c_fm_phase_derivation/06_fm_derivation_triangle_accumulated_phase_phi_fm.png`
- `png_storyboards/04_pm_fm_delayline_modulation/04c_fm_phase_derivation/07_fm_derivation_rectangle_accumulated_phase_phi_fm.png`

## Block 5: Applications I: Stereo Phaser und Rotary Speaker

Ziel:

- Stereo Phaser als SSB-Anwendung nach Wardle/Zölzer erklären.
- Den Zusammenhang zwischen Frequency Shifter, SSB und Phaser zeigen.
- Rotary Speaker als Kombination aus Delayline-Modulation,
  Amplitudenmodulation und Stereo-Mischung vorbereiten.
- Vibrato nicht erneut behandeln; das wurde in Vorlesung 9 über fractional
  delay eingeführt.

Bildideen:

- SSB-Stereo-Phaser:
  - Eingang \(x[n]\)
  - Allpass-Hilbert-Paar \(x_0[n]\), \(x_{90}[n]\)
  - langsamer Quadraturoszillator \(\cos(\omega_m n)\),
    \(\sin(\omega_m n)\)
  - linker Ausgang als eine SSB-Richtung
  - rechter Ausgang als entgegengesetzte SSB-Richtung
- Frequenzgang über die Zeit:
  - eingefrorene Momentaufnahmen \(Y_L/X\) und \(Y_R/X\)
  - mehrere wandernde Kerben
  - links und rechts bewegen sich gegensinnig
- Rotary Speaker:
  - zwei gegenphasig modulierte Delaylines
  - Amplitudenmodulation \(1+\sin\) und \(1-\sin\)
  - Stereo-Mischung

Mögliches Skript:

- `export_block_05_stereo_phaser_rotary_applications.py`

Reaper-JSFX:

- `audio_exports/reaper_jsfx/simple_ssb_stereo_phaser.jsfx`
- Parameter: `RATE_HZ`, `D_GAIN`, `E_GAIN`, `OUT_DB`
- `RATE_HZ` ist die subsonische SSB-Verschiebefrequenz.
- Links wird das SSB-Signal mit einer Vorzeichenrichtung addiert,
  rechts mit der Gegenrichtung.
- Bei langsamer Rate entsteht ein Stereo-Phaser; bei höherer Rate nähert sich
  der Klang einem Frequency-Shifter.

Erwartete Dateien:

- `png_storyboards/05_applications_stereo_phaser_rotary/05a_stereo_phaser/01_stereo_phaser_response_overlap_cos1.png`
- `png_storyboards/05_applications_stereo_phaser_rotary/05a_stereo_phaser/02_stereo_phaser_response_stereo_offset.png`
- `png_storyboards/05_applications_stereo_phaser_rotary/05a_stereo_phaser/03_stereo_phaser_response_sweep.gif`
- `png_storyboards/05_applications_stereo_phaser_rotary/05a_stereo_phaser/04_after_allpass_1_mag_phase.png`
- `png_storyboards/05_applications_stereo_phaser_rotary/05a_stereo_phaser/05_after_allpass_2_mag_phase.png`
- `png_storyboards/05_applications_stereo_phaser_rotary/05a_stereo_phaser/06_allpass_quadrature_pair_cos1.png`
- `png_storyboards/05_applications_stereo_phaser_rotary/05a_stereo_phaser/07_yl_cos1_mag_phase.png`
- `png_storyboards/05_applications_stereo_phaser_rotary/05a_stereo_phaser/08_yr_cos1_mag_phase.png`
- `png_storyboards/05_applications_stereo_phaser_rotary/05a_stereo_phaser/09_yl_cos45_mag_phase.png`
- `png_storyboards/05_applications_stereo_phaser_rotary/05a_stereo_phaser/10_yr_cos45_mag_phase.png`
- `png_storyboards/05_applications_stereo_phaser_rotary/05a_stereo_phaser/11_yl_cos90_mag_phase.png`
- `png_storyboards/05_applications_stereo_phaser_rotary/05a_stereo_phaser/12_yr_cos90_mag_phase.png`
- `png_storyboards/05_applications_stereo_phaser_rotary/05a_stereo_phaser/13_modulator_pair_cos0.png`
- `png_storyboards/05_applications_stereo_phaser_rotary/05a_stereo_phaser/14_modulator_pair_cos45.png`
- `png_storyboards/05_applications_stereo_phaser_rotary/05a_stereo_phaser/15_modulator_pair_cos90.png`
- `png_storyboards/05_applications_stereo_phaser_rotary/05a_stereo_phaser/16_allpass1_times_cos_cos0_mag_phase.png`
- `png_storyboards/05_applications_stereo_phaser_rotary/05a_stereo_phaser/17_allpass2_times_sin_cos0_mag_phase.png`
- `png_storyboards/05_applications_stereo_phaser_rotary/05a_stereo_phaser/18_allpass1_times_cos_cos45_mag_phase.png`
- `png_storyboards/05_applications_stereo_phaser_rotary/05a_stereo_phaser/19_allpass2_times_sin_cos45_mag_phase.png`
- `png_storyboards/05_applications_stereo_phaser_rotary/05a_stereo_phaser/20_allpass1_times_cos_cos90_mag_phase.png`
- `png_storyboards/05_applications_stereo_phaser_rotary/05a_stereo_phaser/21_allpass2_times_sin_cos90_mag_phase.png`
- `png_storyboards/05_applications_stereo_phaser_rotary/05a_stereo_phaser/22_phasor_hilbert_positive_frequency.png`
- `png_storyboards/05_applications_stereo_phaser_rotary/05a_stereo_phaser/23_phasor_hilbert_negative_frequency.png`
- `png_storyboards/05_applications_stereo_phaser_rotary/05a_stereo_phaser/24_cosine_modulator_start.png`
- `png_storyboards/05_applications_stereo_phaser_rotary/05a_stereo_phaser/25_cosine_modulator_animation.gif`

## Ausgelagerte Blöcke

Die ursprünglich geplanten Blöcke 6 und 7 liegen jetzt in:

- `../11_demodulation_und_auto_wah/` als Block 1: Demodulatoren und Envelope-Follower
- `../11_demodulation_und_auto_wah/` als Block 2: Applications: Sidechain Auto-Wah und Morphing

## Bild- und Plotvorgaben

- Plotstil aus Vorlesung 7-9 weiterverwenden.
- Spektren bei Ringmodulation/AM als einfache Linienplots zeigen, damit die
  Seitenbandlogik nicht in FFT-Details untergeht.
- Für Audiofrequenzen Hz-Achsen verwenden, wenn es um Hörwirkung geht.
- Für allgemeine Theorie zusätzlich normierte Kreisfrequenz \(\Omega\) zeigen.
- Modulatoren farblich konsistent violett darstellen.
- Audiosignale grün darstellen.
- Analyse-/Steuersignale orange oder blau darstellen.
- Blockdiagramme schlicht halten: Multiplikation, Summe, Delayline,
  Detektor und Averager als wiedererkennbare Symbole.

## Geplante Exportskripte

- `export_block_01_audio_fx_roadmap.py`
- `export_block_02_ringmodulation_am_tremolo.py`
- `export_block_02a_ringmodulation_sine_carrier.py`
- `export_block_02b_ringmodulation_audible_low_band.py`
- `export_block_02c_ringmodulation_musical_unfiltered.py`
- `export_block_02d_am_modulation_sine_carrier.py`
- `export_block_03a_single_sideband_audio.py`
- `export_block_03b_ssb_hilbert_compensation_filters.py`
- `export_block_03c_ssb_sine_quadrature_products.py`
- `export_block_03d_ssb_hilbert_phasor_product_animation.py`
- `export_block_04_pm_fm_delayline_modulation.py`
- `export_block_05_stereo_phaser_rotary_applications.py`

## Offene Produktionsfragen

- Welche Hörbeispiele sollen genutzt werden: Stimme, Gitarre, Synth,
  perkussiver Sound oder Rauschen?
- Soll Ringmodulation mit Sinus, Stimme und komplexem Instrument gezeigt
  werden?
- Soll PM/FM zunächst mit Sinusträgern oder direkt an einer Delayline gezeigt
  werden?
