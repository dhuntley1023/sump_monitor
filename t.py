import sensor
import time
import sqlite3


s = sensor.Sensor()

while True:
	temperature = s.read_temperature()

	try:
		with sqlite3.connect('temp_monitor.db', 10) as db:
			db.execute("insert into temp_history values (strftime('%Y-%m-%d %H:%M', 'now', 'localtime'), ?);", [temperature])
			db.commit()
		
	except sqlite3.OperationalError:  
		# print("Timed out!")
		pass	# We want to catch the error and just move on.  We'll skip this one.
			
	else:
		# print("Insert ok")
		pass

	time.sleep(60)
