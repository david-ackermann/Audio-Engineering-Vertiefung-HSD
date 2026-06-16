# 8 z-Ebene, z-Transformation, Pole und Nullstellen

Vorlesung 8 fuehrt die z-Ebene aus dem Zeitbereich heraus ein. Der Einstieg
ist ein einzelnes Delay:

$$
y[n]=x[n-1].
$$

Von dort aus wird gezeigt:

1. Delay bedeutet Zeitverschiebung.
2. Bei einem Sinus wird daraus ein Phasenversatz.
3. Fuer komplexe Exponentialsignale wird das Delay zum Faktor
   \(e^{-j\Omega}\).
4. Im Frequenzbereich wird daraus
   \(Y(e^{j\Omega})=e^{-j\Omega}X(e^{j\Omega})\).
5. Die z-Ebene wird zuerst nur mit Einheitskreis und Zeiger
   \(z=e^{j\Omega}\) eingefuehrt.
6. Der Kehrwert \(z^{-1}=e^{-j\Omega}\) wird als kompakte Delay-Schreibweise
   gelesen.
7. Mit \(z^{-1}\) und \(z^{-2}\) werden erste FIR- und IIR-Systemfunktionen
   gelesen.
8. Auf dem Einheitskreis \(z=e^{j\Omega}\) ergibt \(H(z)\) den Frequenzgang.
9. In der ganzen z-Ebene ergibt \(|H(z)|\) die Systemflaeche.
10. Die z-Transformation wird als Erweiterung der DTFT mit freiem Radius
    eingefuehrt.
11. Pole und Nullstellen erklaeren Ausloeschung, Resonanz und Stabilitaet.
12. Audioeffekte werden abschliessend nach Systemklassen eingeordnet.
13. Aufgaben verbinden Koeffizienten, \(H(z)\), Frequenzgang und
    Pol-/Nullstellenlage.

## Zentrale Dateien

- `00_lehrkonzept_z_transformation_pole_nullstellen.md`
- `01_storyboard_und_exportplan.md`
- `02_z_transformation_detail_auffrischung.md`
- `03_einfuehrung_z_ebene_ohne_laplace.md`
- `export_block_01A_fir_delay_phase_examples.py`
- `export_block_01B_phase_factor_multiplication.py`
- `export_block_01C_phasor_frequency_points.py`
- `export_block_02A_normierte_kreisfrequenz.py`
- `export_block_02B_phase_factor_multiplication_animation.py`
- `export_block_02C_delay_ir_frequenzbereich.py`
- `export_block_03_z_ebene_zeiger_z.py`
- `export_block_04_systemfunktion_fir_iir.py`
- `export_block_05_z_transformation_analysis_kernel.py`
- `export_block_06_biquad_z_plane_examples.py`
- `export_block_07_peaking_eq_animation.py`
- `png_storyboards/`
- `notebooks/`
- `audio_exports/`

## Blockstruktur

- `01_delay_phase_zeitbereich`
- `02_komplexe_exponentialsignale_lti`
- `03_z_ebene_zeiger_z`
- `04_systemfunktion_fir_iir`
- `05_z_transformation_analysekern`
- `06_biquad_filter_z_ebene`
- `07_peaking_eq_animation`
- `08_systemklassen_audioeffekte`
- `09_aufgaben_filteranalyse`

## Kernbotschaft

Die z-Transformation ersetzt den bekannten Frequenzgang nicht. Sie erweitert
ihn:

$$
H(e^{j\Omega})=H(z)\big|_{z=e^{j\Omega}}.
$$

Der Frequenzgang ist also \(H(z)\), ausgewertet auf dem Einheitskreis. Die
z-Ebene beschreibt darueber hinaus, ob Anteile wachsen, konstant bleiben oder
abklingen. Genau dadurch werden Pole, Nullstellen, Resonanzen und Stabilitaet
geometrisch sichtbar.
