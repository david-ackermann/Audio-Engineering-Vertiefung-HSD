# Block 4: Systemfunktion aus FIR und IIR

Block 4 zeigt, was man mit einer bereits hergeleiteten Systemfunktion machen
kann.

- `04A1_fir_three_tap_notch`: Drei-Tap-FIR-Notch mit
  \(H(z)=0.5+0.5z^{-2}\). Die Nullstellen liegen bei
  \(z=e^{\pm j\pi/2}\), also bei \(f=f_s/4\).
- `04A2_fir_three_tap_inside_zeros`: Drei-Tap-FIR mit
  \(H(z)=1-0.6z^{-1}+0.36z^{-2}\). Die Nullstellen liegen bei
  \(z=0.6e^{\pm j\pi/3}\), also innerhalb des Einheitskreises.
- `04C_iir_two_delay_resonator`: rein rekursiver Resonator mit
  \(H(z)=1/(1-0.9z^{-1}+0.81z^{-2})\). Die Pole liegen bei
  \(z=0.9e^{\pm j\pi/3}\).
- `04D_biquad_highpass`: Highpass-Biquad mit
  \(H(z)=(0.68931-1.37861z^{-1}+0.68931z^{-2})/
  (1-1.27963z^{-1}+0.47759z^{-2})\). Die Nullstellen liegen doppelt
  bei \(z=1\), die Pole bei \(z\approx0.6398\pm j0.2612\).

Die erste Abbildung zeigt jeweils die Impulsantwort in Gruen. Danach wird
zuerst \(z=e^{j\Omega}\) eingesetzt: Der Frequenzgang bis Nyquist wird
zunaechst linear und danach in dB gezeigt. Der dB-Frequenzgang wird als GIF
aufgebaut; das Startbild des GIFs liegt als eigenes PNG vor. Anschliessend
wird der Frequenzgang auf \(0\leq\Omega/\pi\leq2\) erweitert; der Bereich
oberhalb von Nyquist ist blau.

Danach wird derselbe Frequenzgang in der z-Ebene gezeigt: erst als GIF bis
Nyquist, dann als Standbild ueber den ganzen Einheitskreis. Im GIF bleibt der
vollstaendige Einheitskreis unten grau, der abgefahrene Abschnitt wird orange
aufgebaut; zusaetzlich zeigt ein orangefarbener Zeiger die aktuelle Projektion
auf den Einheitskreis.
Im Standbild ist der \(r=1\)-Kreis unten orange hervorgehoben. Anschliessend
folgt eine Serie mit kleiner werdendem Radius \(r=0.8,0.6,0.4,0.2,0\); der
aktuell zugehoerige Kreis ist unten in der z-Ebene orange hervorgehoben,
bereits gezeigte Werte bleiben transparent sichtbar. Ein weiteres Standbild
fasst die Radiuskurven zusammen. Erst danach wird \(|H(z)|\) in der ganzen
z-Ebene als Flaeche gezeigt. Die gruene und blaue Kurve auf der Flaeche ist
derselbe Ausdruck auf dem Einheitskreis, also der Frequenzgang. Abschliessend
zeigt eine 2D-z-Ebene beim FIR die Nullstellen plus den formalen Delay-Pol
bei \(z=0\), beim IIR die Polstellen.
