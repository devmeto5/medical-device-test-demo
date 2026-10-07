"""Run tests, export readable case evidence, and fail the process on failure."""
import csv
from pathlib import Path
import unittest
from monitor import evaluate
from test_monitor import CASES, SEQUENCE

def main():
    directory = Path(__file__).resolve().parent / "reports"
    directory.mkdir(exist_ok=True)
    suite = unittest.defaultTestLoader.loadTestsFromName("test_monitor")
    with (directory / "unittest.txt").open("w", encoding="utf-8") as stream:
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    rows = []
    for case_id, temperature, connected, stopped, previous, expected in CASES:
        actual = evaluate(temperature, connected, stopped, previous)
        rows.append([case_id, repr(temperature), connected, stopped, previous,
                     *expected, *actual, actual == expected])
    previous = False
    for step, (temperature, expected) in enumerate(SEQUENCE, 1):
        actual = evaluate(temperature, True, False, previous)
        rows.append([f"TC-18.step-{step}", temperature, True, False, previous,
                     *expected, *actual, actual == expected])
        previous = actual[0]
    with (directory / "cases.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["case_id", "temperature_c", "sensor_connected", "emergency_stop",
                         "previous_heater", "expected_heater", "expected_status",
                         "actual_heater", "actual_status", "passed"])
        writer.writerows(rows)
    print((directory / "unittest.txt").read_text(encoding="utf-8"))
    print(f"Case evidence: {directory / 'cases.csv'}")
    return 0 if result.wasSuccessful() and all(row[-1] for row in rows) else 1

if __name__ == "__main__":
    raise SystemExit(main())
