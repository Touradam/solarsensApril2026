"""
Solar Sense — Live Dashboard.
Real-time V/I/T telemetry, IV curve, simulated or serial data. Ready for Streamlit deployment.
"""
import time
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from data.simulator import generate_sample, VOC_NOMINAL, ISC_NOMINAL
from data.serial_reader import read_serial_line
from data.iv_curve import compute_iv_curve
from data.health_score import compute_health_score

# Bounded storage
MAX_TELEMETRY_ROWS = 1000
TABLE_ROWS = 20

# ---------------------------------------------------------------------------
# Page config and logo
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Solar Sense | Live Dashboard",
    layout="wide",
    initial_sidebar_state="auto",
)

# Logo path: prefer "image asset" then "assets" (deployment-friendly)
_root = Path(__file__).resolve().parent
_logo_candidates = [
    _root / "image asset" / "SolarSensLogo1.png",
    _root / "image asset" / "SolarSensLogo1.jpg",
    _root / "assets" / "SolarSensLogo1.png",
    _root / "assets" / "SolarSensLogo1.jpg",
    _root / "assets" / "logo.png",
]
_logo_path = next((p for p in _logo_candidates if p.exists()), None)

if _logo_path:
    st.image(str(_logo_path), width=180)
else:
    st.title("Solar Sense")
st.caption("Live Dashboard — module-level telemetry and IV curve")

st.markdown(
    """
    <style>
    .stApp { max-width: 100%; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Session state init
# ---------------------------------------------------------------------------
if "telemetry_df" not in st.session_state:
    st.session_state.telemetry_df = pd.DataFrame(
        columns=["timestamp_ms", "voltage", "current", "temp"]
    )
if "events" not in st.session_state:
    st.session_state.events = []
if "shading_active" not in st.session_state:
    st.session_state.shading_active = False
if "data_source" not in st.session_state:
    st.session_state.data_source = "Simulated"
if "serial_port" not in st.session_state:
    st.session_state.serial_port = "COM3"
if "baud_rate" not in st.session_state:
    st.session_state.baud_rate = 9600

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Dashboard controls")

    data_source = st.radio(
        "Data source",
        ["Simulated", "Serial"],
        index=0 if st.session_state.data_source == "Simulated" else 1,
    )
    if data_source != st.session_state.data_source:
        st.session_state.data_source = data_source
        st.session_state.telemetry_df = pd.DataFrame(
            columns=["timestamp_ms", "voltage", "current", "temp"]
        )
        st.session_state.events = []
    else:
        st.session_state.data_source = data_source

    refresh_rate = st.slider("Refresh rate (s)", 0.5, 5.0, 1.0, 0.5)
    time_window_s = st.slider("Time window (s)", 10, 300, 60, 10)

    if data_source == "Serial":
        serial_port = st.text_input("Serial port", value=st.session_state.serial_port)
        baud_rate = st.number_input("Baud rate", value=st.session_state.baud_rate, min_value=1200, step=960)
        st.session_state.serial_port = serial_port
        st.session_state.baud_rate = baud_rate

    st.divider()
    if data_source == "Simulated":
        if st.button("Toggle Shading"):
            st.session_state.shading_active = not st.session_state.shading_active
        st.caption("Shading: " + ("ON" if st.session_state.shading_active else "OFF"))

    event_label = st.text_input("Event label", value="")
    if st.button("Mark event"):
        if len(st.session_state.telemetry_df) > 0:
            ts = int(st.session_state.telemetry_df["timestamp_ms"].iloc[-1])
        else:
            ts = int(time.time() * 1000)
        st.session_state.events.append((ts, event_label or "Event"))
        st.rerun()

# ---------------------------------------------------------------------------
# Acquire one new sample and append to state
# ---------------------------------------------------------------------------
if st.session_state.data_source == "Simulated":
    row = generate_sample(shading=st.session_state.shading_active)
else:
    row = read_serial_line(
        st.session_state.serial_port,
        st.session_state.baud_rate,
        timeout_s=min(0.5, refresh_rate * 0.5),
    )

if row is not None:
    new_df = pd.DataFrame(
        [{"timestamp_ms": row[0], "voltage": row[1], "current": row[2], "temp": row[3]}]
    )
    st.session_state.telemetry_df = pd.concat(
        [st.session_state.telemetry_df, new_df], ignore_index=True
    )
    if len(st.session_state.telemetry_df) > MAX_TELEMETRY_ROWS:
        st.session_state.telemetry_df = st.session_state.telemetry_df.tail(
            MAX_TELEMETRY_ROWS
        ).reset_index(drop=True)

# ---------------------------------------------------------------------------
# Current values for KPIs and IV
# ---------------------------------------------------------------------------
df = st.session_state.telemetry_df
if len(df) == 0:
    voltage_now = 0.0
    current_now = 0.0
    temp_now = 0.0
else:
    voltage_now = float(df["voltage"].iloc[-1])
    current_now = float(df["current"].iloc[-1])
    temp_now = float(df["temp"].iloc[-1])

health = compute_health_score(
    current_now,
    st.session_state.shading_active,
)

# ---------------------------------------------------------------------------
# Top row: 4 KPI boxes
# ---------------------------------------------------------------------------
k1, k2, k3, k4 = st.columns(4)
k1.metric("Voltage", f"{voltage_now:.2f} V")
k2.metric("Current", f"{current_now:.2f} A")
k3.metric("Temperature", f"{temp_now:.1f} C")
k4.metric("Health Score", f"{health:.0f}")

# ---------------------------------------------------------------------------
# Time window filter (ms)
# ---------------------------------------------------------------------------
window_ms = time_window_s * 1000
if len(df) > 0:
    t_min = df["timestamp_ms"].max() - window_ms
    df_win = df[df["timestamp_ms"] >= t_min].copy()
else:
    df_win = df

# ---------------------------------------------------------------------------
# Main area: time-series (left 2/3) + IV curve (right 1/3)
# ---------------------------------------------------------------------------
col_ts, col_iv = st.columns([2, 1])

with col_ts:
    st.subheader("Real-time telemetry")
    if len(df_win) < 2:
        st.info("Waiting for data...")
    else:
        fig_ts = go.Figure()
        t_rel = (df_win["timestamp_ms"].astype(float) - df_win["timestamp_ms"].min()) / 1000.0
        fig_ts.add_trace(
            go.Scatter(x=t_rel, y=df_win["voltage"], name="Voltage (V)", line=dict(width=2))
        )
        fig_ts.add_trace(
            go.Scatter(x=t_rel, y=df_win["current"], name="Current (A)", line=dict(width=2))
        )
        fig_ts.add_trace(
            go.Scatter(x=t_rel, y=df_win["temp"], name="Temperature (C)", line=dict(width=2))
        )
        for (ts, label) in st.session_state.events:
            if df_win["timestamp_ms"].min() <= ts <= df_win["timestamp_ms"].max():
                x_val = (ts - df_win["timestamp_ms"].min()) / 1000.0
                fig_ts.add_vline(x=x_val, line_dash="dash", line_color="gray", annotation_text=label or "Event")
        fig_ts.update_layout(
            xaxis_title="Time (s)",
            yaxis_title="Value",
            margin=dict(l=50, r=20, t=20, b=50),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            height=350,
        )
        st.plotly_chart(fig_ts, use_container_width=True)

with col_iv:
    st.subheader("IV curve")
    if len(df) == 0:
        st.info("No data yet")
    else:
        if st.session_state.data_source == "Simulated":
            voc, isc = VOC_NOMINAL, ISC_NOMINAL
        else:
            voc = max(float(df["voltage"].max()), 1.0)
            isc = max(float(df["current"].max()), 0.1)
        v_arr, i_arr = compute_iv_curve(voc, isc, st.session_state.shading_active)
        fig_iv = go.Figure()
        fig_iv.add_trace(go.Scatter(x=v_arr, y=i_arr, mode="lines", name="IV", line=dict(width=2)))
        fig_iv.update_layout(
            xaxis_title="Voltage (V)",
            yaxis_title="Current (A)",
            margin=dict(l=50, r=20, t=20, b=50),
            height=350,
        )
        st.plotly_chart(fig_iv, use_container_width=True)

# ---------------------------------------------------------------------------
# Raw telemetry table (last 20)
# ---------------------------------------------------------------------------
st.subheader("Raw telemetry (last 20 samples)")
if len(df) == 0:
    st.caption("No samples yet.")
else:
    show = df.tail(TABLE_ROWS)[["timestamp_ms", "voltage", "current", "temp"]]
    st.dataframe(show, use_container_width=True, hide_index=True)

# ---------------------------------------------------------------------------
# Auto-refresh
# ---------------------------------------------------------------------------
time.sleep(refresh_rate)
st.rerun()
