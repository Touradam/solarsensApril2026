"""
IV curve computation from Voc, Isc and shading.
Simple single-diode style shape; curve visibly changes under shading.
"""
import numpy as np

# Number of points along the curve
N_POINTS = 80


def compute_iv_curve(
    voc: float,
    isc: float,
    shading: bool,
    n_points: int = N_POINTS,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Return (V_array, I_array) for IV curve plot.
    voc: open-circuit voltage (V), isc: short-circuit current (A).
    Shading reduces Isc and slightly reduces Voc; shape changes (flatter knee).
    """
    if voc <= 0 or isc <= 0:
        return np.array([0.0]), np.array([0.0])

    # Voltage from 0 to Voc
    v = np.linspace(0.0, voc, n_points)

    # Simple approximation: I = Isc * (1 - (V/Voc)^k); k controls knee sharpness
    # Higher k = sharper knee; under shading we use lower k for flatter knee
    k = 4.0 if not shading else 2.2
    i = isc * (1.0 - np.power(np.clip(v / voc, 0, 1), k))
    i = np.maximum(i, 0.0)

    return v, i
