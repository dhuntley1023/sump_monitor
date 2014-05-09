import quick2wire.i2c as i2c
import time

address = 0x38
iodir_register = 0x01

while True:
	with i2c.I2CMaster() as bus:
		bytes = bus.transaction(
			i2c.reading(address, 2)
			)
	
	
	output_val = (bytes[0][0] << 8) + bytes[0][1]
	print(output_val)
	
	time.sleep(1)
