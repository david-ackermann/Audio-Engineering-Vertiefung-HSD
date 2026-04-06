# Audio Engineering Vertiefung HSD

Collection of Binder-ready interactive plots and notebooks for the course.

## Repository structure

```text
binder/
  requirements.txt
plots/
  fourier_transformation/
    README.md
    requirements.txt
    fourier_phasor_interactive.py
    fourier_phasor_notebook.ipynb
```

## Current interactive plots

### Fourier Transformation

- JupyterLab:
  `https://mybinder.org/v2/gh/david-ackermann/Audio-Engineering-Vertiefung-HSD/HEAD?urlpath=lab/tree/plots/fourier_transformation/fourier_phasor_notebook.ipynb`
- Voila:
  `https://mybinder.org/v2/gh/david-ackermann/Audio-Engineering-Vertiefung-HSD/HEAD?urlpath=voila/render/plots/fourier_transformation/fourier_phasor_notebook.ipynb`

## How to add another interactive plot later

1. Create a new folder under `plots/`, for example `plots/sampling` or `plots/filter_design`.
2. Put the notebook entry file and the supporting Python files into that folder.
3. Add a local `requirements.txt` with:

```text
-r ../../binder/requirements.txt
```

4. If the new plot needs additional Python packages, extend `binder/requirements.txt`.
5. Add the new Binder links to this root `README.md`.

## Binder link pattern

- JupyterLab:
  `https://mybinder.org/v2/gh/<user>/<repo>/HEAD?urlpath=lab/tree/plots/<topic>/<notebook>.ipynb`
- Voila:
  `https://mybinder.org/v2/gh/<user>/<repo>/HEAD?urlpath=voila/render/plots/<topic>/<notebook>.ipynb`


