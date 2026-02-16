"""
Serial telemetry reader: parse lines and read from port.
Format: timestamp_ms,voltage,current,temp
Graceful on errors; never raise to crash the app.
"""
from typing import Optional

# Optional import so app runs without pyserial installed
try:
    import serial
    SERIAL_AVAILABLE = True
except ImportError:
    SERIAL_AVAILABLE = False
    serial = None


def parse_telemetry_line(line: str) -> Optional[tuple[int, float, float, float]]:
    """
    Parse one line: timestamp_ms,voltage,current,temp
    Returns (ts_ms, V, I, T) or None on parse error.
    """
    line = line.strip()
    if not line:
        return None
    try:
        parts = line.split(",")
        if len(parts) != 4:
            return None
        ts_ms = int(parts[0].strip())
        v = float(parts[1].strip())
        i = float(parts[2].strip())
        t = float(parts[3].strip())
        return (ts_ms, v, i, t)
    except (ValueError, AttributeError):
        return None


def read_serial_line(port: str, baud_rate: int, timeout_s: float = 0.5) -> Optional[tuple[int, float, float, float]]:
    """
    Open port, read one line, parse and return (ts_ms, V, I, T).
    Returns None on any error (no data, parse fail, open fail).
    Does not hold port open; opens and closes per read to avoid state.
    """
    if not SERIAL_AVAILABLE:
        return None
    try:
        with serial.Serial(port=port, baudrate=baud_rate, timeout=timeout_s) as ser:
            line = ser.readline()
            if not line:
                return None
            decoded = line.decode("utf-8", errors="ignore")
            return parse_telemetry_line(decoded)
    except Exception:
        return None


def list_serial_ports() -> list[str]:
    """Return list of available serial port names if detectable."""
    if not SERIAL_AVAILABLE:
        return []
    try:
        import serial.tools.list_ports
        return [p.device for p in serial.tools.list_ports.comports()]
    except Exception:
        return []
