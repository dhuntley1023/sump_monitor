import quick2wire.i2c as i2c
import time
import sqlite3

address = 0x38
iodir_register = 0x01

conn = sqlite3.connect('temp.db', 15) #Increased timeout to 15s as temporary workaround for long-selects
c = conn.cursor()

while True:
	with i2c.I2CMaster() as bus:
		bytes = bus.transaction(
			i2c.reading(address, 4)
			)
	
	temp_highbyte = bytes[0][2] << 3
	temp_lowbyte =  bytes[0][3] >> 5
	temp_val = temp_highbyte + temp_lowbyte

	temperature = (((temp_val / 2047 * 200) - 50) * 9/5 + 32)
#	print(temperature)

# // print("%.3f, %d, %d" % (temperature, temp_highbyte, temp_lowbyte))

	c.execute("insert into temperature values (datetime('now', 'localtime'), ?);", [temperature])
	conn.commit()

	time.sleep(15)
