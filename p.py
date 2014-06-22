import sensor
import time
import sqlite3


s = sensor.Sensor()

samples = []
sum = 0.0
count = 0

while True:
	for i in range(60):
		depth = s.read_pressure(sensor.PressureInH2O)
		samples.append(depth)
		sum = sum + depth
		count = count + 1
		if count > 60:
			sum = sum - samples.pop(0)
			count = count - 1
		# print(depth, sum, count)
		time.sleep(1)

	depth_avg = sum / count

	try:
		# print(depth_avg)
		with sqlite3.connect('sump.db', 10) as db:
			db.execute("insert into samples values (strftime('%Y-%m-%d %H:%M', 'now', 'localtime'), ?);", [depth_avg])
			db.commit()
		
	except sqlite3.OperationalError:  
		# print("Timed out!")
		pass	# We want to catch the error and just move on.  We'll skip this one.
			
	else:
		# print("Insert ok")
		pass
