# Medical Equipment Temperature Monitor — Demo Test Plan

## Purpose

A small educational project demonstrating automated verification of temperature-monitoring logic for a simulated medical equipment heater. All thresholds are invented for the exercise. This project is not validated for clinical use or connected to real equipment.

## Interface

Inputs: temperature in degrees Celsius, sensor-connected flag, emergency-stop flag, previous heater state.

Outputs: heater-enabled flag and status string.

## Demo requirements

Evaluate rules in this order:

1. **REQ-01:** An active emergency stop disables the heater and returns `EMERGENCY_STOP`.
2. **REQ-02:** A disconnected sensor, non-finite temperature, or temperature outside the inclusive range 0–60 °C disables the heater and returns `SENSOR_FAULT`.
3. **REQ-03:** A valid temperature at or above 40 °C disables the heater and returns `OVER_TEMPERATURE`.
4. **REQ-04:** Below 36 °C, enable the heater and return `HEATING`.
5. **REQ-05:** At or above 37 °C, disable the heater and return `IDLE`.
6. **REQ-06:** From 36 °C inclusive to 37 °C exclusive, retain the previous heater state; return `HEATING` or `IDLE` accordingly.

The demo reevaluates these rules on every sample. Faults do not latch. A real device's reset, timing, and alarm requirements are outside this exercise.

## Test cases

Unless specified, the sensor is connected and emergency stop is inactive.

| ID | Requirement | Input / initial condition | Expected result |
| --- | --- | --- | --- |
| TC-01 | REQ-04 | 35 °C, heater off | On, HEATING |
| TC-02 | REQ-06 | 36 °C, heater off | Off, IDLE |
| TC-03 | REQ-06 | 36 °C, heater on | On, HEATING |
| TC-04 | REQ-06 | 36.5 °C, heater off | Off, IDLE |
| TC-05 | REQ-06 | 36.5 °C, heater on | On, HEATING |
| TC-06 | REQ-05 | 37 °C, heater on | Off, IDLE |
| TC-07 | REQ-05 | 39.999 °C, heater on | Off, IDLE |
| TC-08 | REQ-03 | 40 °C, heater on | Off, OVER_TEMPERATURE |
| TC-09 | REQ-03 | 60 °C | Off, OVER_TEMPERATURE |
| TC-10 | REQ-02 | 60.001 °C | Off, SENSOR_FAULT |
| TC-11 | REQ-04 | 0 °C | On, HEATING |
| TC-12 | REQ-02 | -0.001 °C | Off, SENSOR_FAULT |
| TC-13 | REQ-02 | Sensor disconnected at 35 °C | Off, SENSOR_FAULT |
| TC-14 | REQ-02 | NaN, positive infinity, negative infinity (separate cases) | Off, SENSOR_FAULT |
| TC-15 | REQ-01 | Emergency stop active at 35 °C | Off, EMERGENCY_STOP |
| TC-16 | REQ-01 | Emergency stop active and sensor disconnected | Off, EMERGENCY_STOP |
| TC-17 | REQ-02 | 61 °C | Off, SENSOR_FAULT (sensor validity takes precedence) |
| TC-18 | REQ-04–06 | Sequence 35 → 36.5 → 37 → 36.5 → 35 °C, initially off | On → On → Off → Off → On |

## Execution and acceptance

For each case, compare both outputs with the independently specified expected results. Reset state between independent cases; preserve it within TC-18. Record case ID, input, expected output, actual output, and pass/fail. The runner must return a nonzero exit code if any case fails.

Acceptance: all cases pass. Execution against a simulation demonstrates only the simulation's behavior; execution against a LabVIEW VI must be reported separately and requires an actual LabVIEW environment.