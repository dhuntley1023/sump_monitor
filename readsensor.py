import quick2wire.i2c as i2c
import time

address = 0x38
iodir_register = 0x01

while True:
	with i2c.I2CMaster() as bus:
		bytes = bus.transaction(
			i2c.reading(address, 3)
			)
	
	pressure_val = (bytes[0][0] << 8) + bytes[0][1]
	print("PSI DIFF =", (pressure_val - 1667) * 5 /(14745 - 1667))
	
	temp_val = bytes[0][2]
	print("TEMP (C) =", ((temp_val << 3) / 2047 * 200) - 50)
	
	print()
	
	time.sleep(1)
