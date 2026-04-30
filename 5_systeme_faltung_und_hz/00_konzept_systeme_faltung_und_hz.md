# Konzept Vorlesung 5: Systeme, Faltung und H(z)

## Ziel der Vorlesung

Die Studierenden sollen am Ende verstehen:

- was ein diskretes System aus einer Eingangsfolge $x[n]$ macht
- warum die Impulsantwort $h[n]$ ein System vollstaendig beschreibt, wenn das System linear und zeitinvariant ist
- wie die diskrete Faltung als Summe verschobener und gewichteter Impulsantworten gelesen wird
- warum Delay $z^{-1}$ der elementare Speicherbaustein digitaler Systeme ist
- wie aus einer Differenzengleichung eine kompakte Systembeschreibung entsteht
- was $H(z) = Y(z) / X(z)$ als Lesesprache bedeutet, ohne schon tief in Pole und Nullstellen einzusteigen

## Didaktische Rolle im Gesamtaufbau

Vorlesung 4 schliesst die Analyseperspektive ab: Ein Signal kann als Folge betrachtet, analysiert und wieder rekonstruiert werden. Vorlesung 5 wechselt die Frage:

> Nicht mehr: Was steckt im Signal? Sondern: Was macht ein System mit dem Signal?

Die fachliche Kette lautet:

- ein System bildet $x[n]$ auf $y[n]$ ab
- ein Impuls testet, wie das System auf einen einzelnen Sample-Anstoss reagiert
- bei linearen zeitinvarianten Systemen reichen verschobene und gewichtete Impulsantworten aus
- daraus entsteht die Faltung $y[n] = (x \ast h)[n]$
- Delays machen Speicher im Zeitbereich sichtbar
- Differenzengleichungen beschreiben Feedforward- und Feedback-Strukturen
- $H(z)$ ist die kompakte Schreibweise dieser Struktur

## Anschluss an Vorlesung 4

Aus Vorlesung 4 nehmen die Studierenden mit:

- $x[n]$ als diskrete Folge
- lokale Analyse und Rekonstruktion aus vollstaendigen Koeffizienten
- Fensterung und Blockdenken als Beobachtungsoperation

Vorlesung 5 verlaesst die Beobachtung und behandelt Wirkung:

- $h[n]$ ist nicht Beobachtungsfenster, sondern Systemantwort
- Faltung ist nicht Fensterung, sondern Systemwirkung
- $H(z)$ beschreibt nicht ein Spektrogramm, sondern das Verhalten eines Systems

## Mathematischer Kern

Impuls und Impulsantwort:

$$
\delta[n] = \begin{cases}
1, & n = 0 \\
0, & n \neq 0
\end{cases}
$$

$$
h[n] = \mathcal{T}\{\delta[n]\}
$$

Lineares zeitinvariantes System:

$$
\mathcal{T}\{a x_1[n] + b x_2[n]\} = a\mathcal{T}\{x_1[n]\} + b\mathcal{T}\{x_2[n]\}
$$

$$
\mathcal{T}\{x[n - n_0]\} = y[n - n_0]
$$

Diskrete Faltung:

$$
y[n] = (x \ast h)[n] = \sum_m x[m] h[n - m]
$$

Feedforward-System:

$$
y[n] = \sum_{k=0}^{M} b_k x[n-k]
$$

Feedback-/IIR-System:

$$
y[n] = \sum_{k=0}^{M} b_k x[n-k] - \sum_{r=1}^{R} a_r y[n-r]
$$

Delay als z-Baustein:

$$
x[n-1] \leftrightarrow z^{-1}
$$

Systemfunktion:

$$
H(z) = Y(z) / X(z)
$$

Feedforward-Beispiel:

$$
H(z) = b_0 + b_1 z^{-1} + b_2 z^{-2} + \dots
$$

Feedback-Beispiel:

$$
H(z) =
\frac{b_0 + b_1 z^{-1} + \dots + b_M z^{-M}}{1 + a_1 z^{-1} + \dots + a_R z^{-R}}
$$

## Didaktischer roter Faden

1. Block 1: Systembegriff, Ein- und Ausgangsfolge, Impuls als Testsignal
2. Block 2: Impulsantwort und diskrete Faltung als Ueberlagerung
3. Block 3: Impulsantwort, Spektrum und Systemwirkung
4. Block 4: Delay, Speicher und Differenzengleichung
5. Block 5: Von der Differenzengleichung zu $H(z)$
6. Block 6: Feedforward und Feedback als Ausblick auf Pole/Nullstellen

## Block 1: Systembegriff und Impulsantwort

### Kerngedanke

> Ein System ist eine Abbildung von $x[n]$ nach $y[n]$. Die Impulsantwort zeigt, was das System aus einem einzelnen Sample-Anstoss macht.

Didaktisch wichtig:

- zuerst mit Folgen und nicht mit Formeln beginnen
- $\delta[n]$ als digitales Klicksignal verstehen
- $h[n]$ als messbare Antwort des Systems lesen
- LTI nur so weit einfuehren, wie es fuer Faltung gebraucht wird

Geplante Storyboards:

- Eingang $x[n]$, Systemblock, Ausgang $y[n]$
- diskreter Impuls $\delta[n]$
- kurze Impulsantworten: Direktpfad, Echo, gedämpfte Antwort

## Block 2: Diskrete Faltung

### Kerngedanke

> Jedes Sample von $x[n]$ startet eine verschobene und skalierte Kopie von $h[n]$. Die Summe aller Kopien ist $y[n]$.

Didaktisch wichtig:

- Faltung als Aufbauprozess zeigen, nicht nur als fertige Summe
- erst wenige Samples, dann die allgemeine Formel
- Zeitverschiebung und Gewichtung sichtbar machen
- Vorzeichenkonvention in $h[n-m]$ nicht ueberbetonen, sondern ueber verschobene Kopien motivieren

Geplante Storyboards:

- einzelne gewichtete Impulsantworten
- schrittweise Summation
- fertiges Ausgangssignal
- Vergleich kurze IR gegen lange IR

## Block 3: Impulsantwort und Frequenzgang

### Kerngedanke

> Dieselbe Systemwirkung kann im Zeitbereich als Faltung und im Frequenzbereich als Gewichtung gelesen werden.

Didaktisch wichtig:

- an Vorlesung 1 bis 4 anschliessen: Zeitfolge und Spektrum sind zwei Sichten
- $h[n]$ hat ein Spektrum, das die Wirkung auf Sinusanteile beschreibt
- hier nur die Frequenzgang-Idee vorbereiten, die genaue Einheitskreis-Auswertung kommt in Vorlesung 6

Geplante Storyboards:

- Impulsantwort oben, Betragsspektrum unten
- Eingangsspektrum, Systemwirkung, Ausgangsspektrum
- einfache Beispiele: Tiefpass-artige, Hochpass-artige und Echo-artige Impulsantwort

## Block 4: Delay, Speicher und Differenzengleichung

### Kerngedanke

> Digitales Systemverhalten entsteht aus Addition, Multiplikation und Delay.

Didaktisch wichtig:

- $x[n-1]$ als ein Sample Speicher zeigen
- Blockdiagramm und Gleichung parallel aufbauen
- Feedforward vor Feedback
- Feedback noch ohne Stabilitaetsdiskussion einfuehren

Geplante Storyboards:

- ein Sample Delay
- Feedforward-Delay $y[n] = x[n] + g x[n-M]$
- Feedback-Delay $y[n] = x[n] + g y[n-M]$
- Differenzengleichung als Ablesung aus dem Blockdiagramm

## Block 5: H(z) als Systemsprache

### Kerngedanke

> $H(z)$ ist eine kompakte Schreibweise fuer Delay-Strukturen.

Didaktisch wichtig:

- $z^{-1}$ direkt an $x[n-1]$ koppeln
- Zaehler als Feedforward-Anteil lesen
- Nenner als Feedback-Anteil lesen
- noch keine ausfuehrliche Pol-Nullstellen-Analyse; diese gehoert in Vorlesung 6

Geplante Storyboards:

- Differenzengleichung links, $H(z)$ rechts
- FIR-Beispiel nur mit Zaehler
- IIR-Beispiel mit Zaehler und Nenner
- Strukturdiagramm und Formel gegeneinander markieren

## Block 6: Feedforward und Feedback als Ausblick

### Kerngedanke

> Feedforward verteilt Energie endlich in der Zeit. Feedback kann Energie wieder in das System zurueckfuehren.

Didaktisch wichtig:

- FIR/IIR begrifflich vorbereiten, aber noch nicht vollstaendig behandeln
- Stabilitaet als offene Frage fuer Vorlesung 6 formulieren
- Pole und Nullstellen nur als naechste Leseschicht von $H(z)$ ankündigen

Geplante Storyboards:

- endliche Impulsantwort bei Feedforward
- ausklingende Antwort bei Feedback
- gleiche Delaystruktur mit verschiedenen $g$
- Abschlussfolie: von $H(z)$ zum Einheitskreis in Vorlesung 6

## Zeitplan fuer 120 Minuten

| Zeit | Abschnitt | Inhalt | mathematischer Fokus | didaktische Funktion |
|---|---|---|---|---|
| 0-8 min | Rueckbezug | Von Analyse/Rekonstruktion zur Systemwirkung | $x[n] \to y[n]$ | Perspektivwechsel setzen |
| 8-25 min | Block 1 | Systembegriff, Impuls, Impulsantwort | $h[n] = \mathcal{T}\{\delta[n]\}$ | Systemantwort anschaulich machen |
| 25-48 min | Block 2 | Faltung als Summe verschobener Impulsantworten | $y[n] = \sum_m x[m] h[n-m]$ | Faltung mechanisch verstehen |
| 48-60 min | Block 3 | Impulsantwort und Frequenzgang | Zeitbereich/Frequenzbereich | bekannte Spektralsicht anbinden |
| 60-68 min | Pause | kurze Unterbrechung | - | Entlastung |
| 68-88 min | Block 4 | Delay, Speicher und Differenzengleichung | $x[n-1]$, $y[n-r]$ | Systemstruktur aus Grundbausteinen lesen |
| 88-108 min | Block 5 | Von der Gleichung zu $H(z)$ | $H(z)=Y(z)/X(z)$ | kompakte Systemsprache aufbauen |
| 108-118 min | Block 6 | Feedforward/Feedback, Ausblick Pole/Nullstellen | Zaehler/Nenner | Vorlesung 6 vorbereiten |
| 118-120 min | Abschluss | drei Merksaetze | Faltung, Delay, $H(z)$ | Verdichten |

## Typische Verstaendnishuerden

- Faltung wird als abstrakte Rechenvorschrift statt als Systemwirkung verstanden.
- Impulsantwort und Fensterfunktion werden verwechselt.
- $h[n]$ wird als Eingangssignal statt als Systemeigenschaft gelesen.
- Delay wird als reine Zeitverschiebung, aber nicht als Speicherbaustein verstanden.
- Differenzengleichung und Blockdiagramm werden getrennt gelernt.
- $z^{-1}$ wirkt wie eine neue Achse statt wie eine Schreibweise fuer ein Sample Delay.
- $H(z)$ wird zu frueh mit Pol-Nullstellen-Geometrie ueberladen.

## Demo-, Hoer- und Python-Einsatz

- Klick oder Clap durch kurze Raum-IR
- trockener Impuls gegen Echo und Raumantwort
- direkte Faltung einer kurzen Folge mit einer kurzen Impulsantwort
- Audiobeispiel: trockenes Signal durch kurze IR falten
- Feedforward- und Feedback-Delay als einfache Audioeffekte
- Gleichung, Blockdiagramm und $H(z)$ fuer dasselbe System nebeneinander

## Geplante Export- und Storyboard-Struktur

- `01_systembegriff_und_impulsantwort`
- `02_diskrete_faltung`
- `03_impulsantwort_und_frequenzgang`
- `04_delay_speicher_differenzengleichung`
- `05_hz_als_systemsprache`
- `06_feedforward_feedback_ausblick`

## Anschluss an Vorlesung 6

Vorlesung 5 endet mit $H(z)$ als algebraischer Systemsprache. Vorlesung 6 wertet diese Sprache geometrisch aus:

- $H(e^{j \Omega})$ als Auswertung auf dem Einheitskreis
- Pole und Nullstellen als Leseschicht von $H(z)$
- Stabilitaet ueber Pol-Lage
- Minimum Phase als strukturelle Eigenschaft
