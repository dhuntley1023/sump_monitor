from sensor import Sensor
import time

address = 0x38
iodir_register = 0x01

while True:
	(pressure, temp) = Sensor().read_pressure_and_temp()
	print("PSI DIFF = %.4f" % (pressure))
	
	print("TEMP (F) = %.2f" % (temp))
	
	print()
	
	time.sleep(1)
