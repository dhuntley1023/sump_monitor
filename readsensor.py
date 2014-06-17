from sensor import Sensor, SensorError, PressureInH2O
import time
import sys

s = Sensor()
print("Calibrating sensor...")
#s.calibrate_pressure()

print("Reading...")
while True:
	try:
		(pressure, temp) = s.read_pressure_and_temperature(p_unit = PressureInH2O)
		print("PSI DIFF = %.2f" % (pressure))
		print("TEMP (F) = %.2f" % (temp))
		print()
		sys.stdout.flush()

	except SensorError as e:
		print("Exception reading sensor: ", e)

	time.sleep(2)
