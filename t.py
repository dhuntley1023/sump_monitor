import quick2wire.i2c as i2c
import time
import sqlite3

address = 0x38
iodir_register = 0x01

while True:
	with i2c.I2CMaster() as bus:
		bytes = bus.transaction(
			i2c.reading(address, 4)
			)
	
	temp_highbyte = bytes[0][2] << 3
	temp_lowbyte =  bytes[0][3] >> 5
	temp_val = temp_highbyte + temp_lowbyte

	temperature = (((temp_val / 2047 * 200) - 50) * 9/5 + 32)

	try:
		with sqlite3.connect('temp.db', 10) as db:
			db.execute("insert into temperature values (datetime('now', 'localtime'), ?);", [temperature])
			db.commit()
		
	except sqlite3.OperationalError:  
		# print("Timed out!")
		pass	# We want to catch the error and just move on.  We'll skip this one.
			
	else:
		# print("Insert ok")
		pass

	time.sleep(15)
