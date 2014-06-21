import sensor
import time
import sqlite3


s = sensor.Sensor()

while True:
	depth = s.read_pressure(sensor.PressureInH2O)

	try:
		with sqlite3.connect('sump.db', 10) as db:
			db.execute("insert into samples values (strftime('%Y-%m-%d %H:%M', 'now', 'localtime'), ?);", [depth])
			db.commit()
		
	except sqlite3.OperationalError:  
		# print("Timed out!")
		pass	# We want to catch the error and just move on.  We'll skip this one.
			
	else:
		# print("Insert ok")
		pass

	time.sleep(60)
