# 7 Vom IIR im Zeitbereich zum Biquad

Vorlesung 7 startet im Zeitbereich mit dem vorhandenen IIR-Block und bleibt bis zum Biquad im Frequenzgang
`H(e^{j\Omega})`. Die z-Transformation, die z-Ebene sowie Pole und Nullstellen werden in Vorlesung 8 verschoben.

## Ordnerstatus

Physisch sind aktuell diese Storyboard-Ordner vorhanden:

- `png_storyboards/01_iir/`
- `png_storyboards/02_frequenzgang_iir/`
- `png_storyboards/03_rekursives_iir_mehrere_taps/`
- `png_storyboards/04_verschobene_impulsantwort/`
- `png_storyboards/05_feedforward_dirac_baustein/`
- `png_storyboards/06_biquad_audiofilter/`

Alle anderen alten Storyboard-Bloecke wurden aus der aktiven Ordnerstruktur entfernt. Weitere Bloecke bleiben vorerst nur im Lehrkonzept beschrieben.

## Dramaturgie

1. FIR aus Vorlesung 6 kurz reaktivieren.
2. Reines IIR im Zeitbereich zeigen.
3. Filterkurven reiner Rueckfuehrung betrachten.
4. Verschiebung der Impulsantwort im Frequenzgang zeigen.
5. Feedforward-Dirac-Baustein als FIR-Term sichtbar machen.
6. Grenzen reiner Rueckfuehrung herausarbeiten.
7. FIR-Feedforward und IIR-Feedback kombinieren.
8. Biquad als praktische Standardform vorstellen.
9. Typische Filterkurven als Biquad-Anwendungen vorstellen.
10. z-Transformation, Pole und Nullstellen als Anschluss fuer Vorlesung 8 motivieren.

## Kernbotschaft

Ein reines IIR kann glaetten, speichern, ausschwingen und resonante Kurven erzeugen. Fuer gezielte Ausloeschungen, echte Hochpaesse und Notches braucht man aber Eingangskopien und damit einen Feedforward-Anteil.

Notation:

- `p` bleibt der direkte Rueckfuehrungsfaktor im einpoligen Einstiegsbeispiel.
- `b_k` gewichtet Eingangskopien im Feedforward-Zweig und laeuft ueber `k=0...N-1`.
- `a_r` gewichtet Ausgangskopien im Feedback-Zweig und laeuft ueber `r=1...M`.
- Fuer den einpoligen Fall mit ueblicher Minus-Schreibweise gilt `p=-a_1`.

In Vorlesung 7 wird die allgemeine Uebertragungsfunktion zunaechst im Frequenzbereich geschrieben:

$$
H(e^{j\Omega})
=
\frac{
\sum_{k=0}^{N-1}b_k e^{-jk\Omega}
}{
1+\sum_{r=1}^{M}a_r e^{-jr\Omega}
}.
$$

Die z-Schreibweise `H(z)=B(z)/A(z)` folgt erst in Vorlesung 8.

## Zentrale Dateien

- `00_lehrkonzept_iir_frequenzgang_biquad.md`
- `01_storyboard_und_exportplan.md`
- `03_frequenzgang_aus_rekursion.md`
- `04_rekursives_iir_mehrere_taps.md`
- `export_block_01_iir.py`
- `export_block_02A_geometric_series.py`
- `export_block_02B_iir_magnitude_examples.py`
- `export_block_03_recursive_iir_examples.py`
- `export_block_03B_iir_impulse_response_build.py`
- `export_block_03C_iir_ir_superposition.py`
- `export_block_04_shifted_ir_frequency_response.py`
- `export_block_04B_weighted_shifted_spectra.py`
- `export_block_05_feedforward_dirac_term.py`
- `export_block_06_biquad_audio_filter_examples.py`
- `png_storyboards/`
- `audio_exports/`
- `notebooks/`

## Aktive Storyboards

- `png_storyboards/01_iir/01A_dirac_impuls`
- `png_storyboards/01_iir/01B_stabil_impulsantwort`
- `png_storyboards/01_iir/01C_grenzstabil_impulsantwort`
- `png_storyboards/01_iir/01D_instabil_impulsantwort`
- `png_storyboards/01_iir/01E_iir_p_plus_05`
- `png_storyboards/01_iir/01F_iir_p_minus_05`
- `png_storyboards/02_frequenzgang_iir/02A_geometric_series`
- `png_storyboards/02_frequenzgang_iir/02B_iir_magnitude_examples`
- `png_storyboards/03_rekursives_iir_mehrere_taps/03A_recursive_iir_frequency_examples` mit Log/dB- und linearer Magnitude-Darstellung
- `png_storyboards/03_rekursives_iir_mehrere_taps/03B_impulse_response_build`
- `png_storyboards/03_rekursives_iir_mehrere_taps/03C_ir_superposition`
- `png_storyboards/04_verschobene_impulsantwort/04A_shifted_ir_frequency_response`
- `png_storyboards/04_verschobene_impulsantwort/04B_weighted_shifted_spectra`
- `png_storyboards/05_feedforward_dirac_baustein/05A_shifted_dirac_fir_term`
- `png_storyboards/06_biquad_audiofilter/06A_typical_audio_filters` mit sieben Filterklassen, je drei Betragsbildern, einer Phasenabbildung und einer Gruppenlaufzeit-Abbildung pro Klasse; alle Achsenflaechen sind pixelgenau gleich positioniert
- `png_storyboards/06_biquad_audiofilter/06B_biquad_cascades` mit Tiefpass-Kaskade, Hochpass-Kaskade und DAW-artiger EQ-Kaskade; Einzelstufen grau, Gesamtkaskade gruen
