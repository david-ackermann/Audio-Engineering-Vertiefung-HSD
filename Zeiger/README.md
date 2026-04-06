# Fourier Phasor Explorer

Interactive teaching app for visualizing Fourier analysis with cosine and sine components, window functions, complex coefficients, magnitude spectrum, and phase spectrum.

## Files

- `streamlit_app.py`: browser-based Streamlit app for students
- `fourier_phasor_interactive.py`: desktop Matplotlib version
- `requirements.txt`: Python dependencies

## Run locally

```powershell
streamlit run streamlit_app.py
```

## Deploy with Streamlit Community Cloud

1. Create a new GitHub repository in the browser.
2. Upload these files to the repository.
3. Open Streamlit Community Cloud.
4. Create a new app from your GitHub repository.
5. Select `streamlit_app.py` as the entry file.
6. Share the generated URL with students.

## Suggested structure for future apps

If you want to publish more interactive plots later, you can keep several apps in one repository, for example:

```text
interactive-plots/
  requirements.txt
  fourier/
    streamlit_app.py
    fourier_phasor_interactive.py
  convolution/
    streamlit_app.py
  sampling/
    streamlit_app.py
```

Then each app can be deployed separately by selecting a different entry file in Streamlit Community Cloud.
