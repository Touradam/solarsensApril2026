# Solar Sense — Live Dashboard

Real-time module-level telemetry and IV-curve dashboard (simulated or serial). Ready for Streamlit Cloud deployment.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with GitHub.
3. New app: select this repo, branch `main`, main file path **app.py**.
4. Click Deploy. Streamlit runs `streamlit run app.py` by default.

Optional: add your Solar Sense logo as `assets/SolarSensLogo1.png` or `image asset/SolarSensLogo1.png` so the dashboard header shows it.
