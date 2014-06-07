from sensor import Sensor, SensorError, PressureInH2O
import time

s = Sensor()
print("Calibrating sensor...")
s.calibrate_pressure()

print("Reading...")
while True:
	try:
		(pressure, temp) = s.read_pressure_and_temperature(p_unit = PressureInH2O)
		print("PSI DIFF = %.2f" % (pressure))
		print("TEMP (F) = %.2f" % (temp))
		print()

	except SensorError as e:
		print("Exception reading sensor: ", e)

	time.sleep(2)
