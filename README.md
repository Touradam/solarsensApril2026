# Solar Sense Website

Static marketing site (GitHub Pages) and Streamlit live dashboard.

## Website (GitHub Pages)

Open `index.html` locally or deploy via GitHub Pages (workflow in `.github/workflows/`).

Pages: `index.html`, `journey.html`, `market_analysis.html`, `solarsense-pro.html`

## Live dashboard (Streamlit)

```bash
pip install -r requirements.txt
streamlit run app.py
```

Deploy on [Streamlit Community Cloud](https://share.streamlit.io): repo `main`, entry file `app.py`.

Optional logo: `assets/SolarSensLogo1.png`

## Repo layout

| Path | Purpose |
|------|---------|
| `*.html`, `styles.css`, `pro-styles.css` | Static site |
| `assets/` | Images and `motion.js` used by the site |
| `app.py`, `data/` | Streamlit dashboard |
| `docs/market_opportunity_analysis.md` | Market analysis source (also embedded in page) |
| `Archive/` | Local-only retired files (gitignored) |
