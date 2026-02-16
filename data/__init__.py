"""
Data layer for Solar Sense: simulation, serial I/O, IV curve, health score.
No Streamlit imports; pure logic for testability and reuse.
"""
from data.simulator import generate_sample
from data.serial_reader import read_serial_line, parse_telemetry_line
from data.iv_curve import compute_iv_curve
from data.health_score import compute_health_score

__all__ = [
    "generate_sample",
    "read_serial_line",
    "parse_telemetry_line",
    "compute_iv_curve",
    "compute_health_score",
]
