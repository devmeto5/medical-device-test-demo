"""Requirement-based cases. Uses Python's standard library only."""
import json
import unittest
from monitor import evaluate, evaluate_json

# ID, temperature, sensor connected, emergency stop, prior heater, expected pair.
CASES = [
    ("TC-01", 35, True, False, False, (True, "HEATING")),
    ("TC-02", 36, True, False, False, (False, "IDLE")),
    ("TC-03", 36, True, False, True, (True, "HEATING")),
    ("TC-04", 36.5, True, False, False, (False, "IDLE")),
    ("TC-05", 36.5, True, False, True, (True, "HEATING")),
    ("TC-06", 37, True, False, True, (False, "IDLE")),
    ("TC-07", 39.999, True, False, True, (False, "IDLE")),
    ("TC-08", 40, True, False, True, (False, "OVER_TEMPERATURE")),
    ("TC-09", 60, True, False, True, (False, "OVER_TEMPERATURE")),
    ("TC-10", 60.001, True, False, True, (False, "SENSOR_FAULT")),
    ("TC-11", 0, True, False, False, (True, "HEATING")),
    ("TC-12", -0.001, True, False, True, (False, "SENSOR_FAULT")),
    ("TC-13", 35, False, False, True, (False, "SENSOR_FAULT")),
    ("TC-14a", float("nan"), True, False, True, (False, "SENSOR_FAULT")),
    ("TC-14b", float("inf"), True, False, True, (False, "SENSOR_FAULT")),
    ("TC-14c", float("-inf"), True, False, True, (False, "SENSOR_FAULT")),
    ("TC-15", 35, True, True, True, (False, "EMERGENCY_STOP")),
    ("TC-16", 35, False, True, True, (False, "EMERGENCY_STOP")),
    ("TC-17", 61, True, False, True, (False, "SENSOR_FAULT")),
]
SEQUENCE = [
    (35, (True, "HEATING")),
    (36.5, (True, "HEATING")),
    (37, (False, "IDLE")),
    (36.5, (False, "IDLE")),
    (35, (True, "HEATING")),
]


class MonitorTests(unittest.TestCase):
    def test_TC_18_state_sequence(self):
        previous = False
        for temperature, expected in SEQUENCE:
            with self.subTest(temperature=temperature, previous=previous):
                actual = evaluate(temperature, True, False, previous)
                self.assertEqual(actual, expected)
                previous = actual[0]

    def test_labview_json_contract(self):
        for case_id, temperature, connected, stopped, previous, expected in CASES:
            with self.subTest(case=case_id):
                result = json.loads(evaluate_json(temperature, connected, stopped, previous))
                self.assertEqual(result, {"heater_enabled": expected[0], "status": expected[1]})

    def test_demo_recovery_is_not_latched(self):
        previous, _ = evaluate(41, True, False, True)
        self.assertEqual(evaluate(35, True, False, previous), (True, "HEATING"))


def make_test(case):
    def test(self):
        case_id, temperature, connected, stopped, previous, expected = case
        self.assertEqual(evaluate(temperature, connected, stopped, previous), expected, case_id)
    return test


for case in CASES:
    setattr(MonitorTests, "test_" + case[0].replace("-", "_"), make_test(case))

if __name__ == "__main__":
    unittest.main(verbosity=2)
