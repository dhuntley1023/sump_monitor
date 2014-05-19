from flask import Flask
import sqlite3
import string


app = Flask(__name__)

@app.route("/")
def display_all_temps():
		response = []
		
		response.append('<html><body><table border="1"><tr><td>Timestamp</td><td>Temp</td></tr>')
		
		conn = sqlite3.connect("temp.db")
		cur = conn.cursor()
		
		for row in cur.execute("select sample_time, temperature from temperature where sample_time > datetime('now', 'localtime', '-24 hours') order by sample_time;"):
			sample_time = row[0]
			temperature = row[1]
			
			response.append("<tr><td>" + sample_time + "</td><td>" + str(temperature) + "</td></tr>")
			
		response.append("</table></body></html>")
		
		cur.close()
		conn.close()
		
		return string.join(response, '')

@app.route("/hourly")
def display_hourly_temps():
		response = []
		
		response.append('<html><body><table border="1"><tr><td>Timestamp</td><td>Temp</td></tr>')
		
		conn = sqlite3.connect("temp.db")
		cur = conn.cursor()
		
		for row in cur.execute('select strftime("%m-%d-%Y %H:00", sample_time) as stime, avg(temperature) from temperature group by stime order by stime;'):
			sample_time = row[0]
			temperature = row[1]
			
			response.append("<tr><td>" + sample_time + "</td><td>" + str(temperature) + "</td></tr>")
			
		response.append("</table></body></html>")
		
		cur.close()
		conn.close()
		
		return string.join(response, '')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)

