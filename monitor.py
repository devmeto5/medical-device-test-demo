"""Educational temperature controller; thresholds are fictional."""
import json
import math


def evaluate(temperature_c, sensor_connected=True, emergency_stop=False,
             previous_heater=False):
    """Return (heater_enabled, status); caller owns the previous state."""
    if emergency_stop:
        return False, "EMERGENCY_STOP"
    if not sensor_connected or not math.isfinite(temperature_c) or not 0 <= temperature_c <= 60:
        return False, "SENSOR_FAULT"
    if temperature_c >= 40:
        return False, "OVER_TEMPERATURE"
    if temperature_c < 36:
        return True, "HEATING"
    if temperature_c >= 37:
        return False, "IDLE"
    return bool(previous_heater), "HEATING" if previous_heater else "IDLE"


def evaluate_json(temperature_c, sensor_connected, emergency_stop, previous_heater):
    """LabVIEW Python Node entry point: four scalar inputs, one JSON string."""
    heater, status = evaluate(temperature_c, sensor_connected, emergency_stop, previous_heater)
    return json.dumps({"heater_enabled": heater, "status": status})
