"""
Solar Sense — China Overview (public-facing strategic page).
Positioning for corporate + manufacturing ecosystem.
"""
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="China Overview | Solar Sense", layout="wide")

# ---------------------------------------------------------------------------
# Layout and assets: minimal CSS, image paths
# ---------------------------------------------------------------------------
_ASSET_DIR = Path(__file__).resolve().parent.parent / "image asset"


def _image_path(name: str) -> Path:
    return _ASSET_DIR / name


st.markdown(
    """
    <style>
    .stApp { max-width: 100%; }
    div[data-testid="stVerticalBlock"] > div:has(> div.stMarkdown) {
        margin-bottom: 0.5rem;
    }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; max-width: 900px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
hero_img = _image_path("SolarSensLogo1.png")
if hero_img.exists():
    st.image(str(hero_img), width=260)
st.title("Solar Sense")
st.markdown("**MLPE and module-level signal intelligence for scalable solar infrastructure.**")
st.markdown("*We turn every PV module into an intelligent node for safety, diagnostics, and asset optimization.*")
st.divider()

# ---------------------------------------------------------------------------
# Why Now
# ---------------------------------------------------------------------------
st.subheader("Why Now")
st.markdown(
    "Safety and compliance pressure—including rapid shutdown—is rising. At fleet scale, "
    "O&M cost and downtime from hidden module-level faults are material. Solar fleets need "
    "module-level electrical signatures, not just yield reporting."
)
st.divider()

# ---------------------------------------------------------------------------
# Three columns: Problem | Platform | Value
# ---------------------------------------------------------------------------
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.subheader("The Problem")
    st.markdown(
        """
        - Scale and compliance risk (rapid shutdown, safety)
        - Hidden module-level faults that cut yield and drive O&M cost
        - Lack of electrical-signature visibility at the module
        - Fleets need diagnostics that scale
        """
    )

with col_b:
    st.subheader("The Platform")
    st.markdown(
        """
        - Embedded module-level hardware (MLPE form factor)
        - Real-time V, I, and T telemetry
        - IV-curve signature capture for diagnostics
        - Edge and cloud data pipeline; digital-twin foundations
        - Built for lifecycle and fleet-level analytics
        """
    )

with col_c:
    st.subheader("Value")
    st.markdown(
        """
        - Faster triage and earlier fault detection
        - Fewer truck rolls and less downtime
        - Yield protection across the fleet
        - Data for reliability programs and asset optimization
        """
    )

st.divider()

# ---------------------------------------------------------------------------
# Manufacturing & Integration Readiness
# ---------------------------------------------------------------------------
st.subheader("Manufacturing & Integration Readiness")
st.markdown(
    """
    - Design-for-manufacture mindset with a clear PCB and enclosure pathway
    - Component selection aligned with supply chain stability and availability
    - Cost-down roadmap with defined volume assumptions
    - Integration targets: module manufacturers and power electronics partners
    - We are designing for pilot production and scale; we welcome DFM and supply chain input
    """
)
st.divider()

# ---------------------------------------------------------------------------
# Live Demo
# ---------------------------------------------------------------------------
st.subheader("Live Demo")
demo_img = _image_path("demo1.png")
if demo_img.exists():
    st.image(str(demo_img), width=400)
st.markdown("The platform streams real-time voltage, current, and temperature from the module.")
st.markdown("A live IV curve shows electrical behavior; under shading, the curve distorts and current drops.")
st.markdown("That shift is an electrical behavior signature the system uses for diagnostics and triage.")
st.divider()

# ---------------------------------------------------------------------------
# Roadmap
# ---------------------------------------------------------------------------
st.subheader("Roadmap")
st.markdown(
    "We are de-risking through structured execution: reliability testing, pilot deployments, "
    "and a clear certification pathway (UL/NEC). The roadmap is built for manufacturing and "
    "integration readiness, not speculation."
)
st.divider()

# ---------------------------------------------------------------------------
# What We Are Seeking (3 columns)
# ---------------------------------------------------------------------------
st.subheader("What We Are Seeking")
seek_a, seek_b, seek_c = st.columns(3)

with seek_a:
    st.markdown("**Manufacturing partners**")
    st.markdown(
        """
        - DFM input and design review
        - Pilot production run and volume ramp
        - Supply chain and component collaboration
        - PCB and enclosure manufacturing pathway
        """
    )

with seek_b:
    st.markdown("**Pilot partners**")
    st.markdown(
        """
        - Test sites for module-level diagnostics
        - O&M teams to quantify triage and truck-roll ROI
        - Validation studies (corporate or academic)
        - Data sharing for reliability and signature validation
        """
    )

with seek_c:
    st.markdown("**Strategic investors (hardware-aware)**")
    st.markdown(
        """
        - Hardware and energy infrastructure investors
        - Strategic corporate venture teams
        - Capital that understands DFM and certification pathways
        - Long-term alignment with manufacturing and deployment
        """
    )

st.divider()

# ---------------------------------------------------------------------------
# Footer: founder photo + contact
# ---------------------------------------------------------------------------
footer_img = _image_path("adamaToure.png")
fa, fb = st.columns([1, 4])
with fa:
    if footer_img.exists():
        st.image(str(footer_img), width=90)
with fb:
    st.markdown("**Founder:** Adama Toure  \n**Email:** [adama.toure@sept.energy](mailto:adama.toure@sept.energy)")
