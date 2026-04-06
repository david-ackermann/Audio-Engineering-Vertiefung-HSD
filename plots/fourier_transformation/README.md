# Fourier Transformation

Interactive teaching app for visualizing Fourier analysis with cosine and sine components, window functions, complex coefficients, magnitude spectrum, and phase spectrum.

[![Open in Binder (JupyterLab)](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/david-ackermann/Audio-Engineering-Vertiefung-HSD/HEAD?urlpath=lab/tree/plots/fourier_transformation/fourier_phasor_notebook.ipynb)
[![Open as Voila app](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/david-ackermann/Audio-Engineering-Vertiefung-HSD/HEAD?urlpath=voila/render/plots/fourier_transformation/fourier_phasor_notebook.ipynb)

## Files

- `fourier_phasor_interactive.py`: main interactive Matplotlib application
- `fourier_phasor_notebook.ipynb`: notebook and Voila entry point
- `requirements.txt`: local wrapper that points to the shared Binder environment

## Fast local workflow

1. Install the dependencies:

```powershell
pip install -r requirements.txt
```

2. Start Jupyter:

```powershell
jupyter lab
```

3. Open `fourier_phasor_notebook.ipynb` and run the code cell.

The notebook uses `%matplotlib widget`, so the figure stays interactive directly inside Jupyter.

## Online use for students

JupyterLab version:

https://mybinder.org/v2/gh/david-ackermann/Audio-Engineering-Vertiefung-HSD/HEAD?urlpath=lab/tree/plots/fourier_transformation/fourier_phasor_notebook.ipynb

Voila app version:

https://mybinder.org/v2/gh/david-ackermann/Audio-Engineering-Vertiefung-HSD/HEAD?urlpath=voila/render/plots/fourier_transformation/fourier_phasor_notebook.ipynb

The first Binder launch can take a while because the environment has to be built once on the server side.

