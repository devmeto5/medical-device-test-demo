# Medical Device Test Demo

A small educational QA project: a simulated temperature controller, automated Python tests, and a LabVIEW integration guide.

**Scope:** Python simulation testing. No LabVIEW VI files or real device drivers are included. Thresholds are fictional; this is not a clinically validated device or a compliance demonstration.

## Quick start

Requires Python 3.10 or newer. No third-party Python packages are needed.

From this repository folder:

```sh
python demo.py
python run_tests.py
```

On Windows, use `py` instead of `python` if that is your installed launcher.

The test command returns exit code 0 on success and 1 on test failure. It writes:
- `reports/unittest.txt`: test results.
- `reports/cases.csv`: inputs, expected outputs, actual outputs, and pass/fail for each requirement case and sequence step.

Alternative: `python -m unittest -v`.

## What is tested?

- Normal heating and the 36–37 °C hysteresis band.
- Exact temperature limits and just-outside values.
- Over-temperature shutdown.
- Disconnected sensors, NaN, and infinities.
- Emergency stop and fault precedence.
- State retention across a heating/cooling sequence.
- The JSON interface intended for a LabVIEW Python Node.
- Automatic recovery, which is an explicit simplification of this demo.

There are 18 requirement scenarios (TC-14 has three variants), implemented as 20 requirement test methods, plus two interface/recovery methods: **22 tests total**. The CSV contains 24 rows because TC-18 records five steps.

See [requirements and test cases](docs/TEST_PLAN.md) and [LabVIEW integration](docs/LABVIEW.md).

## Controller behavior

Rules are evaluated in order: emergency stop → sensor validity → over-temperature → heating/hysteresis. The caller passes the previous heater state into each sample. No hardware is accessed.

## Automated checks on GitHub

The workflow runs on pushes, pull requests, and manual dispatch. It executes the Python simulation tests and saves the reports as a workflow artifact. A passing workflow does **not** establish that a LabVIEW VI or physical device passed.

## Files

| File | Purpose |
| --- | --- |
| `monitor.py` | Simulation and JSON entry point |
| `test_monitor.py` | Independent expected results and tests |
| `run_tests.py` | Test runner and CSV evidence |
| `demo.py` | Console walkthrough |
| `docs/TEST_PLAN.md` | Requirements and traceable scenarios |
| `docs/LABVIEW.md` | Manual integration and verification steps |

## Limits

This deliberately small demo omits alarm latching, reset authorization, sensor timing, communication failures, calibration, hardware interlocks, and real device validation. No medical or patient data is used.
