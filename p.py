import sensor
import time
import sqlite3
from twilio.rest import TwilioRestClient


def send_text_msg(m):
	ACCOUNT_SID = "AC9079652eae20b65630a4f3b5002f8aca" 
	AUTH_TOKEN = "b143c5168050ea776e3b60614331b89d" 
 
	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
 
	client.messages.create(
		to="408-832-4061", 
		from_="+16692216493", 
		body=m  
	)


s = sensor.Sensor()

samples = []
sum = 0.0
count = 0

last_minute_depth = -100.0
pump_active = False

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
	#print("Sending msg: depth = " + str(depth_avg));
	#send_text_msg("Current depth: " + str(depth_avg));

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


	depth_diff = depth_avg - last_minute_depth
	last_minute_depth = depth_avg

	if (depth_diff <= -0.20) and (not pump_active):
		send_text_msg("Sump Pump Activated...");
		pump_active = True

	if (depth_diff >= 0.0) and pump_active:
		#send_text_msg("Sump Pump Turned Off");
		pump_active = False

