"""
Simulated solar panel telemetry: V, I, T with optional shading effect.
Pure functions; no Streamlit or I/O.
"""
import time
import random

# Shading effect factors (current drops significantly, voltage slightly)
SHADING_CURRENT_FACTOR = 0.25
SHADING_VOLTAGE_FACTOR = 0.92

# Nominal operating ranges (realistic panel)
VOC_NOMINAL = 38.0   # Open-circuit voltage (V)
ISC_NOMINAL = 9.2   # Short-circuit current (A)
T_BASE = 25.0       # Base temperature (C)
T_NOISE = 2.0       # Temperature variation
V_NOISE = 0.3       # Voltage small variation
I_NOISE = 0.15      # Current small variation


def generate_sample(shading: bool = False) -> tuple[int, float, float, float]:
    """
    Generate one telemetry sample: (timestamp_ms, voltage, current, temp).
    When shading is True, current drops significantly and voltage slightly.
    """
    ts_ms = int(time.time() * 1000)
    v = VOC_NOMINAL * (0.85 + 0.1 * random.random())  # Operating point below Voc
    if shading:
        v *= SHADING_VOLTAGE_FACTOR
    v += (random.random() - 0.5) * 2 * V_NOISE

    i = ISC_NOMINAL * (0.80 + 0.15 * random.random())
    if shading:
        i *= SHADING_CURRENT_FACTOR
    i += (random.random() - 0.5) * 2 * I_NOISE
    i = max(0.0, i)

    t = T_BASE + (random.random() - 0.5) * 2 * T_NOISE

    return ts_ms, round(v, 3), round(i, 3), round(t, 2)
