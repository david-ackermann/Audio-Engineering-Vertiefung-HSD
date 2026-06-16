# Audioexports Vorlesung 10

Hier werden Hörbeispiele und Reaper-JSFX für Modulation, Demodulation und
Morphing abgelegt.

## Reaper-JSFX

### `reaper_jsfx/simple_ringmod_tremolo_am.jsfx`

Ein didaktischer Stereo-JSFX für Ringmodulation, Tremolo, AM und SSB.

Parameter:

- `F_LP_HZ`: Tiefpass-Grenzfrequenz des Trägers vor der Modulation.
- `PRESET`: Manual, Ringmodulation, Tremolo, AM, SSB USB oder SSB LSB.
- `SIDEBAND`: Both, USB oder LSB.
- `F_M_HZ`: Modulationsfrequenz \(f_m\) in Hz.
- `A_OFFSET`: Gleichanteil \(a_0\) der Amplitudensteuerung.
- `ALPHA`: Modulationstiefe beziehungsweise Modulationsgrad \(\alpha\).
- `OUT_DB`: Ausgangspegel in dB.

Grundgleichung:

$$
m[n]=\sin(2\pi f_m n/f_s),\qquad a[n]=a_0+\alpha m[n],\qquad y[n]=a[n]x[n].
$$

Für SSB wird zusätzlich ein Hilbert-Pfad des bandbegrenzten Trägers genutzt.
`USB` und `LSB` wählen jeweils nur ein Seitenband aus.

### `reaper_jsfx/simple_pm_fm_oscillator.jsfx`

Ein einfacher Oszillator für PM und FM mit Sinus-, Dreieck- oder
Rechteckmodulator.

Wichtige Parameter:

- `MODE`: PM oder FM.
- `MOD_SHAPE`: Sine, Triangle oder Rectangle.
- `F_C_HZ`: Trägerfrequenz \(f_c\).
- `F_M_HZ`: Modulationsfrequenz \(f_m\).
- `BETA_RAD`: PM-Modulationsindex \(\beta\).
- `DELTA_F_HZ`: FM-Frequenzhub \(\Delta f\).

### `reaper_jsfx/simple_pm_fm_delayline_effect.jsfx`

Ein vereinfachter Delayline-Effekt für PM-/FM-ähnliche Bewegung auf einem
Eingangssignal.

Parameter:

- `MODE`: PM delayline oder FM delayline.
- `MOD_SHAPE`: Sine, Triangle oder Rectangle.
- `F_M_HZ`: Modulationsfrequenz \(f_m\).
- `DELTA`: normierte Modulationstiefe.
- `OUT_DB`: Ausgangspegel.

### `reaper_jsfx/simple_ssb_stereo_phaser.jsfx`

Ein SSB-/Hilbert-basierter Stereo-Phaser nach der Idee von Wardle/Zölzer.
Der Effekt nutzt zwei Allpass-Hilbert-Zweige und mischt das direkte Signal
mit zwei entgegengesetzten SSB-Richtungen.

Parameter:

- `RATE_HZ`: subsonische SSB-Verschiebefrequenz \(f_m\).
- `D_GAIN`: direkter Anteil \(d\).
- `E_GAIN`: SSB-Anteil \(e\).
- `OUT_DB`: Ausgangspegel.

Didaktische Gleichung:

$$
y_L[n]=d\,x[n]+e\left(x_0[n]\cos(\omega_m n)-x_{90}[n]\sin(\omega_m n)\right)
$$

$$
y_R[n]=d\,x[n]+e\left(x_0[n]\cos(\omega_m n)+x_{90}[n]\sin(\omega_m n)\right)
$$

Bei langsamer `RATE_HZ` entstehen wandernde Phaser-Kerben, die sich links und
rechts gegensinnig bewegen. Bei höherer `RATE_HZ` nähert sich der Klang einem
Frequency-Shifter.

### `reaper_jsfx/simple_rotary_loudspeaker.jsfx`

Ein didaktischer Rotary-Loudspeaker-/Leslie-Simulator nach der einfachen
Zölzer/Disch-Topologie aus Fig. 3.13: zwei gegensinnig modulierte Delaylines
erzeugen den Doppler-Anteil, synchrone Amplitudenmodulation modelliert die
Richtwirkung, und eine ungleiche Mischung erzeugt das Stereo-Bild. Es gibt
bewusst keine getrennte Horn-/Drum-Frequenzaufteilung.

Parameter:

- `SPEED`: Manual, Chorale oder Tremolo.
- `F_ROT_HZ`: Rotationsfrequenz \(f_m\).
- `BASE_DELAY_MS`: Grundverzögerung \(M\).
- `DEPTH_MS`: Doppler-Modulationstiefe \(D\) der Delaylines.
- `AM_DEPTH`: Intensitätsmodulation durch die Richtwirkung.
- `CROSS_GAIN`: ungleiche Stereo-Mischung \(c\), Standardwert \(0{,}7\).
- `RAMP_MS`: Trägheit beim Umschalten der Rotationsgeschwindigkeit.
- `OUT_DB`: Ausgangspegel.

Didaktische Kerngleichungen:

$$
d_A[n]=M+D\sin(\omega_m n),\qquad d_B[n]=M-D\sin(\omega_m n)
$$

$$
u_A[n]=\left(1-\alpha\sin(\omega_m n)\right)x[n-d_A[n]]
$$

$$
u_B[n]=\left(1+\alpha\sin(\omega_m n)\right)x[n-d_B[n]]
$$

$$
y_L[n]=u_A[n]+c\,u_B[n],\qquad y_R[n]=c\,u_A[n]+u_B[n]
$$
