"""Show the controller responding to simulated samples."""
from monitor import evaluate

previous = False
print("Temperature | Heater | Status")
for temperature in [35, 36, 36.5, 37, 36.5, 35, 40, 61]:
    previous, status = evaluate(temperature, True, False, previous)
    print(f"{temperature:11.1f} | {str(previous):6} | {status}")
