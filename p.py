import sensor
import time
import sqlite3
from twilio.rest import TwilioRestClient


def send_text_msg(m):
	ACCOUNT_SID = "AC9079652eae20b65630a4f3b5002f8aca" 
	AUTH_TOKEN = "b143c5168050ea776e3b60614331b89d" 
 
	try:
		client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
		client.messages.create(
			to="408-832-4061", 
			from_="+16692216493", 
			body=m  
		)

	except:
		print("Error sending text message... skipping for now")


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
	print("Depth = " + str(depth_avg));
	#send_text_msg("Current depth: " + str(depth_avg));
	depth_diff = depth_avg - last_minute_depth
	last_minute_depth = depth_avg

	try:
		with sqlite3.connect('sump.db', 30) as db:
			db.execute("insert into samples values (strftime('%Y-%m-%d %H:%M', 'now', 'localtime'), ?);", [depth_avg])
			db.commit()
		
			if (depth_diff <= -0.20) and (not pump_active):
				pump_active = True
				send_text_msg("Sump Pump Activated...");
				db.execute("insert into activations values (strftime('%Y-%m-%d %H:%M', 'now', 'localtime'));")
				db.commit()

			if (depth_diff >= 0.0) and pump_active:
				pump_active = False
				#send_text_msg("Sump Pump Turned Off");

	except sqlite3.OperationalError:  
		# Most likely a timeout
		pass	# We want to catch the error and just move on.  We'll skip this one.




