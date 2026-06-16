# Storyboard- und Exportplan Vorlesung 8

## Ordnungsentscheidung

Vorlesung 8 startet aus dem Zeitbereich. Die Storyboards folgen deshalb nicht
zuerst der abstrakten z-Ebene, sondern dieser Progression:

1. Delay im Zeitbereich
2. Delay als Phasenversatz
3. komplexe Exponentialsignale als natuerliche LTI-Testsignale
4. Frequenzbereichsschreibweise
   \(Y(e^{j\Omega})=e^{-j\Omega}X(e^{j\Omega})\)
5. z-Ebene und Einheitskreis:
   \(z=e^{j\Omega}\)
6. Kehrwert des Zeigers:
   \(z^{-1}=e^{-j\Omega}\)
7. Systemfunktionen fuer FIR und IIR
8. \(H(z)\) auf dem Einheitskreis und in der z-Ebene auswerten
9. z-Transformation als Erweiterung der DTFT mit freiem Radius
10. Pole, Nullstellen und Stabilitaet
11. bewegter Peaking-EQ: Spektrum, 2D-z-Ebene und 3D-z-Ebene synchron
12. Audioeffekte nach Systemklassen
13. Aufgaben zur Filteranalyse

## Geplante Storyboard-Ordner

- `png_storyboards/01_delay_phase_zeitbereich/`
- `png_storyboards/02_komplexe_exponentialsignale_lti/`
- `png_storyboards/03_z_ebene_zeiger_z/`
- `png_storyboards/04_systemfunktion_fir_iir/`
- `png_storyboards/05_z_transformation_analysekern/`
- `png_storyboards/06_biquad_filter_z_ebene/`
- `png_storyboards/07_peaking_eq_animation/`
- `png_storyboards/08_systemklassen_audioeffekte/`
- `png_storyboards/09_aufgaben_filteranalyse/`

## Block 1: Delay im Zeitbereich und Phasenversatz

Aktive Bildserie:

- `png_storyboards/01_delay_phase_zeitbereich/01A_sinus_durch_delay`
- `png_storyboards/01_delay_phase_zeitbereich/01B_phasenfaktor_multiplikation`
- `png_storyboards/01_delay_phase_zeitbereich/01C_phasor_kreisfrequenz`

Ziel:

- \(y[n]=x[n-D]\) als reinen Delay-Baustein zeigen,
- Eingang und Ausgang getrennt darstellen,
- den Zeitversatz bei DC, halber Nyquist-Frequenz und Nyquist zeigen,
- daraus den linearen Phasengang \(\varphi(\Omega)=-D\Omega\) ableiten,
- die Gruppenlaufzeit \(\tau_g=D\) vorbereiten.

Aktives Skript:

- `export_block_01A_fir_delay_phase_examples.py`
- `export_block_01B_phase_factor_multiplication.py`
- `export_block_01C_phasor_frequency_points.py`

Bildidee:

- Eingang: Samples schwarz, zugehoeriger Sinus grau
- Ausgang: Samples blau, zugehoeriger verzogerter Sinus grau
- Referenz im Ausgang: Eingangssinus hellgrau gestrichelt
- Beispiele fuer \(D=1\) und \(D=2\)
- Zeitbereichsplots nutzen dieselbe Achsendarstellung wie Vorlesung 7,
  Block 1E: \(n=0,\dots,7\), identische y-Achse und feste Canvasgroesse
- Legenden werden nach allen Kurven und Markern hinzugefuegt
- Phasengang ueber \(\Omega/\pi\) als Aufbau-Serie ohne Textannotation im Plot:
  Punkt bei \(0\), dann Teilgerade von \(0\) bis \(0.5\), danach kompletter
  linearer Phasengang
- Fuer \(D=2\) wird die bereits bekannte Phase von \(D=1\) grau hinterlegt,
  danach wird die neue gruene Phase mit demselben Linienaufbau gezeigt

### Block 1B: Phasenfaktor als komplexe Multiplikation

Ziel:

- den Delay-Faktor \(e^{-jD\Omega}\) als Zeiger auf dem Einheitskreis zeigen,
- die Multiplikation \(y[n]=e^{-jD\Omega}x[n]\) geometrisch darstellen,
- sichtbar machen, dass der Betrag unveraendert bleibt und nur der Winkel
  addiert wird,
- fuer \(D=1\) und \(D=2\) die Faelle DC, halbe Nyquist-Frequenz und
  Nyquist zeigen.

Aktives Skript:

- `export_block_01B_phase_factor_multiplication.py`

Bildidee:

- schwarzer Zeiger: Eingang \(x[n]\),
- orangefarbener Zeiger: Phasenfaktor \(e^{-jD\Omega}\),
- blauer Zeiger: Ausgang \(y[n]\),
- orangefarbener Drehbogen: Winkelverschiebung durch den Phasenfaktor.

### Block 1C: Phasor fuer diskrete Kreisfrequenzen

Ziel:

- DC, halbe Nyquist-Frequenz und Nyquist als Zeiger mit Betrag 1 in der
  komplexen Ebene zeigen,
- den Phasenwinkel \(\Omega\) als schwarzen Pfeilbogen ausserhalb des
  Einheitskreises markieren,
- dieselbe Achsendarstellung wie in Block 1B nutzen.

Aktives Skript:

- `export_block_01C_phasor_frequency_points.py`

## Block 2: Komplexe Exponentialsignale und Frequenzbereich

Geplanter Storyboard-Ordner:

- `png_storyboards/02_komplexe_exponentialsignale_lti/02A_normierte_kreisfrequenz`
- `png_storyboards/02_komplexe_exponentialsignale_lti/02B_phasenfaktor_multiplikation`
- `png_storyboards/02_komplexe_exponentialsignale_lti/02D_eigenfunktion_lti`

Ziel:

- \(\Omega\) als normierte Kreisfrequenz in rad/Sample einfuehren,
- den Unterschied zu \(\Omega_k\) aus der DFT deutlich machen:
  \(\Omega\) darf beliebig sein, \(\Omega_k\) ist nur das DFT-Raster,
- \(e^{j\Omega n}\) als rotierenden Zeiger darstellen,
- zeigen, dass ein Delay daraus nur den Faktor \(e^{-jD\Omega}\) macht,
- daraus \(Y(e^{j\Omega})=e^{-j\Omega}X(e^{j\Omega})\) als
  Frequenzbereichsschreibweise motivieren,
- zeigen, dass ein LTI-System die Frequenz erhaelt und nur mit
  \(H(e^{j\Omega})\) multipliziert.

Aktives Skript:

- `export_block_02A_normierte_kreisfrequenz.py`
- `export_block_02B_phase_factor_multiplication_animation.py`

Export:

- Eingangsserie: `01_x_input_start_n0.png`, `02_x_input_motion.gif`,
  `03_x_input_end_n16.png`
- Ausgangsserie: `04_y_delay_start_n0.png`, `05_y_delay_motion.gif`,
  `06_y_delay_end_n16.png`
- Aufbau: links Phasor auf dem Einheitskreis, rechts Helix ueber \(n\)
- Eingangs-Phasor und Eingangs-Helix schwarz, Ausgangs-Phasor und
  Ausgangs-Helix blau
- Beim Ausgang gilt ein kausales Delay-System mit Ruhezustand:
  \(y[0]=0\), danach \(y[n]=x[n-1]\)
- Die kombinierten Phasor-/Helix-Abbildungen werden nach dem Export
  zusaetzlich pixelgenau in `phasor/` und `helix/` getrennt.
- PNGs und GIFs werden nach dem Cropping auf identische Pixelgroesse gepolstert.

### Block 2B: Phasenfaktor direkt am komplexen Eingangssignal

Ziel:

- fuer eine konkrete Frequenz \(x[n]=e^{j\Omega n}\) zeigen,
  dass ein Delay nur mit \(e^{-j\Omega}\) multipliziert,
- die Multiplikation \(y[n]=e^{-j\Omega}x[n]\) in der komplexen Ebene
  sichtbar machen,
- fuer \(\Omega=\pi/2\) und \(\Omega=\pi\) zeigen, dass der Ausgang ein
  phasenverschobenes komplexes Exponentialsignal bleibt.
- Eingang \(x[n]\) schwarz, Ausgang \(y[n]\) blau, Phasenfaktor
  \(e^{-j\Omega}\) gruen als Systemanteil.
- In den Input-Phasor-Abbildungen zeigt ein schwarzer Pfeilbogen die
  Kreisfrequenz \(\Omega\), also den Winkelzuwachs pro Sample.

Export:

- `01_half_nyquist_input_start_n0.png`
- `02_half_nyquist_input_motion.gif`
- `03_half_nyquist_input_end_n16.png`
- `04_half_nyquist_output_start_n0.png`
- `05_half_nyquist_output_motion.gif`
- `06_half_nyquist_output_end_n16.png`
- `07_nyquist_input_start_n0.png`
- `08_nyquist_input_motion.gif`
- `09_nyquist_input_end_n16.png`
- `10_nyquist_output_start_n0.png`
- `11_nyquist_output_motion.gif`
- `12_nyquist_output_end_n16.png`
- `13_half_nyquist_output_d2_start_n0.png`
- `14_half_nyquist_output_d2_motion.gif`
- `15_half_nyquist_output_d2_end_n16.png`
- `16_nyquist_output_d2_start_n0.png`
- `17_nyquist_output_d2_motion.gif`
- `18_nyquist_output_d2_end_n16.png`
- Zusaetzlich liegen pixelgenau getrennte Phasor- und Helix-Versionen in
  den Unterordnern `phasor/` und `helix/`.

Moegliche Bildfolge:

1. normierte Kreisfrequenz:
   \(\Omega=2\pi f/f_s\)
2. rotierender komplexer Zeiger fuer mehrere Samples
3. Delay um ein Sample als Rueckdrehen des Zeigers
4. Betrag des Delay-Faktors bleibt 1
5. Winkel des Delay-Faktors ist \(-\Omega\)
6. LTI-System: Eingang \(e^{j\Omega n}\), Ausgang
   \(H(e^{j\Omega})e^{j\Omega n}\)

## Block 3: z-Ebene und Zeiger \(z\)

Aktive Bildserie:

- `png_storyboards/03_z_ebene_zeiger_z/01_z_plane_unit_circle.png`
- `png_storyboards/03_z_ebene_zeiger_z/02_z_vector_r1_omega.png`
- `png_storyboards/03_z_ebene_zeiger_z/03_inverse_vector_z_minus_1.png`

Ziel:

- die z-Ebene als komplexe Ebene mit Einheitskreis einfuehren,
- \(z=e^{j\Omega}\) als Zeiger auf dem Einheitskreis zeigen,
- einen konkreten Zeiger auf dem Einheitskreis darstellen und symbolisch als
  \(z=e^{j\Omega}\) beschriften,
- die Kreisfrequenz \(\Omega\) als Pfeilbogen zeigen,
- den zuvor gezeigten Zeiger grau stehen lassen und den Kehrwert
  \(z^{-1}=e^{-j\pi/4}\) als aktiven gruenen Systemzeiger zeigen,
- vorbereiten, dass \(z^{-1}\) genau dem Delay-Phasenfaktor entspricht.

Aktives Skript:

- `export_block_03_z_ebene_zeiger_z.py`

Export:

- `01_z_plane_unit_circle.png`
- `02_z_vector_r1_omega.png`
- `03_inverse_vector_z_minus_1.png`

Bildidee:

- Darstellung der z-Ebene wie in der bisherigen 3C-Serie,
- erstes Bild: Einheitskreis ohne Zeiger,
- zweites Bild: schwarzer Zeiger \(z=e^{j\Omega}\) mit Pfeilbogen \(\Omega\),
- drittes Bild: \(z\) grau, Kehrwert \(z^{-1}=e^{-j\Omega}\) gruen.

## Block 4: Systemfunktion aus FIR und IIR

Aktive Bildserie:

- `png_storyboards/04_systemfunktion_fir_iir/04A1_fir_three_tap_notch`
- `png_storyboards/04_systemfunktion_fir_iir/04A2_fir_three_tap_inside_zeros`
- `png_storyboards/04_systemfunktion_fir_iir/04C_iir_two_delay_resonator`
- `png_storyboards/04_systemfunktion_fir_iir/04D_biquad_highpass`

Ziel:

- aus dem Delay-Operator erste Systemfunktionen aufbauen,
- ein Drei-Tap-FIR-Notch mit
  \(H(z)=0.5+0.5z^{-2}\) zeigen,
- die Koeffizienten \(b_0=0.5\), \(b_1=0\), \(b_2=0.5\) als normiertes
  Notch-Beispiel bei \(\Omega_0=\pi/2\) einfuehren,
- ein zweites Drei-Tap-FIR mit veraenderten Koeffizienten zeigen:
  \(H(z)=1-0.6z^{-1}+0.36z^{-2}\),
- an diesem zweiten FIR zeigen, dass die Nullstellen jetzt bei
  \(z=0.6e^{\pm j\pi/3}\) liegen und damit nicht auf dem Einheitskreis,
- ein reines IIR mit zwei Ausgangsdelays zeigen:
  \(H(z)=1/(1-0.9z^{-1}+0.81z^{-2})\),
- ein Biquad-Hochpassbeispiel zeigen:
  \(H(z)=
  (0.68931-1.37861z^{-1}+0.68931z^{-2})/
  (1-1.27963z^{-1}+0.47759z^{-2})\),
- am Biquad zeigen, dass Zaehler-Nullstellen und Nenner-Pole gemeinsam den
  Frequenzgang formen,
- fuer alle Systeme die Impulsantwort in Gruen zeigen,
- den 2D-Frequenzgang ueber \(\Omega/\pi\) von \(0\) bis \(1\), also bis
  Nyquist, zuerst linear zeigen,
- den 2D-Frequenzgang ueber \(\Omega/\pi\) von \(0\) bis \(1\), also bis
  Nyquist, in dB zeigen,
- das Startbild des 2D-Frequenzgang-GIFs als eigenes PNG zeigen,
- denselben Frequenzgang als GIF in Gruen aufbauen, waehrend der komplette
  Frequenzgang hellgrau sichtbar bleibt,
- den 2D-Frequenzgang anschliessend auf \(0\leq\Omega/\pi\leq2\) erweitern:
  \(0\) bis \(1\) bleibt Gruen, \(1\) bis \(2\) wird Blau,
- mit denselben Frequenzpunkten ein zweites GIF in der z-Ebene zeigen: noch
  ohne Flaeche, nur die Frequenzgangkurve auf dem Einheitskreis; der
  vollstaendige Einheitskreis bleibt unten grau, der abgefahrene Abschnitt
  wird orange,
- danach den ganzen Einheitskreis als 3D-Standbild zeigen:
  \(0\leq\Omega/\pi\leq1\) Gruen, \(1\leq\Omega/\pi\leq2\) Blau; der
  zugehoerige \(r=1\)-Kreis wird unten in Orange hervorgehoben,
- eine 3D-Standbildserie mit kleiner werdendem Radius
  \(r=0.8,0.6,0.4,0.2,0\) zeigen; der jeweils aktive Kreis wird unten in
  Orange hervorgehoben, bereits gezeigte Radiuswerte bleiben transparent,
- ein weiteres 3D-Standbild mit allen zusaetzlichen Radiuskurven zeigen,
- danach \(|H(z)|\) fuer \(r\neq1\) als Flaechen-/Zeltdarstellung zeigen,
  inklusive der Frequenzgangkurve auf dem Einheitskreis,
- danach die z-Ebene in 2D zeigen: beim FIR mit Nullstellen und formalem
  Delay-Pol bei \(z=0\), beim IIR mit Polstellen.

Aktives Skript:

- `export_block_04_systemfunktion_fir_iir.py`

Hinweis:

Beim FIR liegen die Nullstellen bei \(e^{\pm j\pi/2}=\pm j\). Bei
\(f_s=48\,\mathrm{kHz}\) entspricht das einem Notch bei \(12\,\mathrm{kHz}\).
Beim zweiten FIR liegen die Nullstellen bei \(0.6e^{\pm j\pi/3}\); dadurch
entsteht keine ideale Ausloeschung, sondern eine breitere Frequenzgangformung.
Beim IIR liegen die Pole bei \(0.9e^{\pm j\pi/3}\); dadurch entsteht eine
abklingende Resonanzantwort.
Beim Biquad liegen die Nullstellen doppelt bei \(z=1\), die Pole bei
\(0.6398\pm j0.2612\); dadurch entsteht ein Hochpassverhalten.

Export pro Beispiel:

- `01_impulse_response.png`
- `02_frequency_response_linear.png`
- `03_frequency_response_full.png`
- `04_frequency_response_build_start.png`
- `05_frequency_response_build.gif`
- `06_frequency_response_full_two_periods.png`
- `07_frequency_response_unit_circle_start.png`
- `08_frequency_response_unit_circle_build.gif`
- `09_frequency_response_unit_circle_end.png`
- Im GIF wird unten nicht nur der abgefahrene Kreisabschnitt orange gezeigt,
  sondern auch ein orangefarbener Zeiger vom Ursprung zur aktuellen
  Projektion auf den Einheitskreis.
- `10_frequency_response_full_unit_circle.png`
- `11_frequency_response_radius_r_0_8.png`
- `12_frequency_response_radius_r_0_6.png`
- `13_frequency_response_radius_r_0_4.png`
- `14_frequency_response_radius_r_0_2.png`
- `15_frequency_response_radius_r_0_0.png`
- `16_frequency_response_radius_curves.png`
- `17_z_plane_surface.png`
- `18_frequency_response_on_surface.png`
- `19_surface_with_poles_zeros.png`
- `20_z_plane_poles_zeros_2d.png`

## Block 5: z-Transformation als Erweiterung der DTFT

Aktive Bildserie:

- `png_storyboards/05_z_transformation_analysekern/05A_r_1_unit_circle`
- `png_storyboards/05_z_transformation_analysekern/05B_r_less_1_decay`
- `png_storyboards/05_z_transformation_analysekern/05C_r_greater_1_growth`
- `png_storyboards/05_z_transformation_analysekern/05D_r_pole_radius`

Ziel:

- die DTFT als Einheitskreisfall \(r=1\) einordnen,
- den freien Radius \(z=re^{j\Omega}\) einfuehren,
- zeigen, dass \(r<1\) abklingende und \(r>1\) wachsende Zeitanteile
  beschreibt,
- den Polradius des Biquad-Hochpasses aus Block 4D als zusaetzlichen
  Analysefall zeigen,
- nur in `05A` fuer jeden diskreten Analysekern den 2D-Frequenzgang aus
  Block 4D zeigen: vollstaendig grau, bis zur aktuellen Zeigerposition gruen,
- fuer jeden diskreten Analysekern die dazugehoerige Auswertung der
  Biquad-Systemantwort als 3D-Kurve ohne Flaeche zeigen,
- die z-Transformation als Weg von \(h[n]\) nach \(H(z)\) einordnen.

Aktives Skript:

- `export_block_05_z_transformation_analysis_kernel.py`

## Block 6: Biquad-Filter in der z-Ebene

Aktive Storyboard-Ordner:

- `png_storyboards/06_biquad_filter_z_ebene/06A_low_pass`
- `png_storyboards/06_biquad_filter_z_ebene/06B_high_pass`
- `png_storyboards/06_biquad_filter_z_ebene/06C_notch`
- `png_storyboards/06_biquad_filter_z_ebene/06D_band_pass`
- `png_storyboards/06_biquad_filter_z_ebene/06E_low_shelf`
- `png_storyboards/06_biquad_filter_z_ebene/06F_high_shelf`
- `png_storyboards/06_biquad_filter_z_ebene/06G_peaking_eq`

Ziel:

- das Biquad als Kombination aus Zaehler-Nullstellen und Nenner-Polen lesen,
- die typischen Audiofilter aus Vorlesung 7 in der z-Ebene zeigen,
- sichtbar machen, warum ein Biquad deutlich universeller ist als ein
  rein rekursiver IIR-Baustein.

Jede Serie nutzt dieselbe pixelgenaue Layoutlogik wie Block 5:

1. `01_z_plane_2d.png`: Pol-Nullstellen-Diagramm in der 2D-z-Ebene
2. `02_z_plane_3d.png`: \(|H(z)|\) als 3D-z-Ebenenflaeche
3. `03_frequency_response.png`: Frequenzgang auf dem Einheitskreis
4. `04_frequency_response_log.png`: derselbe Frequenzgang mit
   logarithmischer Frequenzachse in Hz
5. `05_frequency_response_log_db.png`: logarithmische Frequenzachse und
   Betrag in dB

Die drei Spektrumsabbildungen nutzen die Titel- und Koeffizientenbox-Logik
aus der 7. Vorlesung. Die Koeffizientenbox steht wie dort standardmaessig
oben rechts, beim High-Shelf unten links.

Hinweis:

Es werden keine GIFs erzeugt. Es gibt keine Zeiger- oder Helix-Darstellungen
in diesem Block.

Aktives Skript:

- `export_block_06_biquad_z_plane_examples.py`

## Block 7: Peaking-EQ-Sweep

Aktiver Storyboard-Ordner:

- `png_storyboards/07_peaking_eq_animation`

Ziel:

- den Peaking-EQ als bewegtes Pol-Nullstellen-System zeigen,
- Spektrum, 2D-z-Ebene und 3D-z-Ebene mit derselben Parameterfolge koppeln,
- die Frequenz logarithmisch gebremst von tief nach hoch fahren, damit die
  Bewegung im Hochfrequenzbereich lesbar bleibt,
- sichtbar machen, dass \(f_0\), \(Q\) und \(G\) direkt die Lage von Polen,
  Nullstellen und die Flaeche \(|H(z)|\) veraendern,
- den Gain als Cut-Boost-Cut-Verlauf und die Guete mit staerkerer Spreizung
  zeigen.

Bildserie:

1. `01_spectrum_motion.gif`: logarithmisches dB-Spektrum des wandernden
   Peaking-EQs mit aktuellen Biquad-Koeffizienten
2. `02_z_plane_2d_motion.gif`: synchroner Pol-Nullstellen-Plot
3. `03_z_plane_3d_motion.gif`: synchroner 3D-z-Plan mit Systemflaeche

Alle drei GIFs haben dieselbe Framezahl, dieselbe Bildrate und dieselbe
Parameterfolge.

Aktives Skript:

- `export_block_07_peaking_eq_animation.py`

## Block 8: Audioeffekte nach Systemklassen

Geplanter Storyboard-Ordner:

- `png_storyboards/08_systemklassen_audioeffekte`

Ziel:

- LTI-, NTI-, LTV- und NTV-Systeme als Abschlussrahmen einordnen,
- zeigen, dass z-Transformation und Pol-/Nullstellen-Sprache vor allem fuer
  LTI-Systeme die passende Beschreibung liefern,
- Audioeffekte wie Gain, Filter, Equalizer, Echo, Reverb, Tremolo, Wah-wah,
  Chorus, Flanger, Phaser, Doppler, Rotary/Leslie, Vibrato und Ringmodulation
  systematisch einsortieren.

Bildidee:

- Tabelle oder Matrix mit Systemklassen:
  - LTI: Gain, Filter, Equalizer, Echo, Reverb
  - NTI: Saturation, Verzerrung, pegelabhaengige Kennlinie
  - LTV: Tremolo, Wah-wah, Chorus, Flanger, Phaser, Vibrato, Rotary/Leslie
  - NTV: zeitvariante nichtlineare Effekte
- Ruhiger Abschluss: Die z-Ebene erklaert LTI-Filter; Vorlesung 9 erweitert
  den Blick auf Systeme, die zeitvariant, pegelabhaengig oder blockbasiert
  sind.

## Block 9: Aufgaben zur Filteranalyse

Geplanter Storyboard-Ordner:

- `png_storyboards/09_aufgaben_filteranalyse`

Ziel:

- Aufgaben aus der Master-Foliendatei als Selbstlernphase dokumentieren,
- Filter aus Koeffizienten, Blockdiagramm, Differenzengleichung,
  Systemfunktion, Frequenzgang und Pol-/Nullstellenlage lesen,
- die technische Analyse mit einer Audio-Engineering-Benennung verbinden.

Uebungen:

1. Kurzer Glaetter vor einer Transientenanalyse
2. Einfaches IIR-Filter fuer DC-Offset und tieffrequente Stoeranteile
3. Biquad-Filter gegen einen schmalen hochfrequenten Stoerton
4. Filter aus verbal beschriebener Pol-/Nullstellen-Lage entwerfen

## Exportskripte

Vorhanden und angepasst:

- `export_block_01A_fir_delay_phase_examples.py`
- `export_block_02A_normierte_kreisfrequenz.py`
- `export_block_02B_phase_factor_multiplication_animation.py`
- `export_block_03_z_ebene_zeiger_z.py`
- `export_block_04_systemfunktion_fir_iir.py`
- `export_block_05_z_transformation_analysis_kernel.py`
- `export_block_06_biquad_z_plane_examples.py`
- `export_block_07_peaking_eq_animation.py`

Vorgeschlagene weitere Namen:

- `export_block_02B_complex_exponentials_lti.py`
- `export_block_08_systemklassen_audioeffekte.py`
- `export_block_09_aufgaben_filteranalyse.py`
- `export_block_09A_exercises_live_demo.py`
