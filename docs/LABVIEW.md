# LabVIEW integration guide

## Status

The Python module and its JSON contract are tested independently. The steps below have not been executed in LabVIEW. This repository does not contain a generated VI.

## Prerequisites

Install LabVIEW with Python Node support (introduced in LabVIEW 2018) and a Python version supported by your specific LabVIEW release. Match the architecture and compatibility requirements in [NI's integration guide](https://www.ni.com/en/support/documentation/supplemental/18/installing-python-for-calling-python-code.html). This project's standalone tests use Python 3.10 or newer; choose a combination supported by both.

## Build a small demonstration VI

1. Add a numeric DBL control named `Temperature C`.
2. Add Boolean controls named `Sensor Connected`, `Emergency Stop`, and `Previous Heater`.
3. Add a string indicator named `Result JSON`.
4. On the block diagram, use **Open Python Session**, **Python Node**, and **Close Python Session**. Wire the session and error connections through them in that order.
5. Configure the Python Node's module path to the absolute path of `monitor.py`, function name to `evaluate_json`, and return type to a string.
6. Wire the four inputs in this exact order: temperature (DBL), sensor connected (Boolean), emergency stop (Boolean), previous heater (Boolean).
7. Wire the returned string to `Result JSON`. Display or handle LabVIEW errors, and ensure the session closes.
8. With 35, True, False, False, expect JSON containing `"heater_enabled": true` and `"status": "HEATING"`. Compare parsed values, not JSON spacing or key order.

For repeated samples, retain the returned heater state in a shift register and pass it into the next call. Do not continuously pass False: that would lose the hysteresis state.

## What this verifies

Calling this function from LabVIEW demonstrates integration with the Python simulation. It does not test a separate controller implemented in LabVIEW.

To test an independently implemented LabVIEW controller, build a VI with the same four inputs and two outputs, drive it with the cases in `TEST_PLAN.md`, and compare both outputs against the listed expected values. Use a For Loop for independent cases and retain state only for the TC-18 sequence. Count failures and save actual results. Keep those results separate from the Python simulation reports.

Do not connect this exercise to a real heater or medical device.
