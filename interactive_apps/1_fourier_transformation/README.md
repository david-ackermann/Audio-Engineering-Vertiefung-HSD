# Fourier Transformation Interactive App

Interaktive Lehr-App für Vorlesung 1 zur Visualisierung von Fourier-Analyse, Cosinus- und Sinusanteilen, komplexen Köffizienten sowie Betrag und Phase.

[![Open in Binder (JupyterLab)](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/david-ackermann/Audio-Engineering-Vertiefung-HSD/HEAD?urlpath=lab/tree/interactive_apps/1_fourier_transformation/fourier_phasor_notebook.ipynb)
[![Open as Voila app](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/david-ackermann/Audio-Engineering-Vertiefung-HSD/HEAD?urlpath=voila/render/interactive_apps/1_fourier_transformation/fourier_phasor_notebook.ipynb)

## Dateien

- `fourier_phasor_interactive.py`
  Schmale Binder-Huelle für das Vorlesungsmodul.
- `fourier_phasor_notebook.ipynb`
  Notebook- und Voila-Einstiegspunkt.
- `requirements.txt`
  Lokale Abhängigkeiten für diese App.

## Bezug zum Projekt

Die fachliche Kernlogik liegt nicht hier, sondern in:

- `../../1_fourier_transformation/fourier_phasor_core.py`

Damit bleiben Vorlesungslogik und App-Huelle getrennt.

## Lokaler Ablauf

1. Abhängigkeiten installieren:

```powershell
pip install -r requirements.txt
```

2. Jupyter starten:

```powershell
jupyter lab
```

3. `fourier_phasor_notebook.ipynb` öffnen und ausführen.
