# Block 2: Komplexe Exponentialsignale und LTI-Systeme

Geplante Bildserien zu \(e^{j\Omega n}\), Delay-Faktor
\(e^{-jD\Omega}\) und LTI-Eigenfunktion
\(y[n]=H(e^{j\Omega})e^{j\Omega n}\).

Aktive Unterbloecke:

- `02A_normierte_kreisfrequenz`
- `02B_phasenfaktor_multiplikation`

Nach Block 2B wird in Block 3 zuerst die z-Ebene mit Einheitskreis und Zeiger
\(z=e^{j\Omega}\) gezeigt. Der Kehrwert dieses Zeigers ist:

$$
e^{-j\Omega}
=
\left(e^{j\Omega}\right)^{-1}
=
z^{-1}.
$$

Block 4 liest diesen Kehrwert dann als Delay-Schreibweise und baut daraus
erste FIR- und IIR-Systemfunktionen. Die Erweiterung auf mehrere
Delay-Samples wird spaeter in Block 6 genutzt:

$$
e^{-jD\Omega}=z^{-D}.
$$

Hier ist \(z=e^{j\Omega}\) nur der Einheitskreis, also der Spezialfall
\(r=1\). Die allgemeinere z-Transformation mit \(z=re^{j\Omega}\) folgt
in Block 5.
