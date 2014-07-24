from flask import Flask
import sqlite3
import string


app = Flask(__name__)

@app.route("/")
def display_all_temps():
		response = []
		
		response.append('<html><body><table border="1"><tr><td>Timestamp</td><td>Depth</td></tr>')
		
		conn = sqlite3.connect("sump.db")
		cur = conn.cursor()
		
		for row in cur.execute("select sample_time, depth from samples where sample_time > datetime('now', 'localtime', '-120 hours') order by sample_time desc;"):
			sample_time = row[0]
			depth = row[1]
			
			response.append("<tr><td>" + sample_time + "</td><td>" + str(depth) + "</td></tr>")
			
		response.append("</table></body></html>")
		
		cur.close()
		conn.close()
		
		return string.join(response, '')

@app.route("/hourly")
def display_hourly_temps():
		response = []
		
		response.append('<html><body><table border="1"><tr><td>Timestamp</td><td>Depth</td></tr>')
		
		conn = sqlite3.connect("sump.db")
		cur = conn.cursor()
		
		for row in cur.execute('select strftime("%m-%d-%Y %H:00", sample_time) as stime, avg(depth) from samples group by stime order by stime desc;'):
			sample_time = row[0]
			depth = row[1]
			
			response.append("<tr><td>" + sample_time + "</td><td>" + str(depth) + "</td></tr>")
			
		response.append("</table></body></html>")
		
		cur.close()
		conn.close()
		
		return string.join(response, '')

@app.route("/activations")
def display_activations():
		response = []
		
		response.append('<html><body><table border="1"><tr><td>Activation Time</td></tr>')
		
		conn = sqlite3.connect("sump.db")
		cur = conn.cursor()
		
		for row in cur.execute('select activation_time from activations order by activation_time desc;'):
			activation_time = row[0]
			
			response.append("<tr><td>" + activation_time + "</td></tr>")
			
		response.append("</table></body></html>")
		
		cur.close()
		conn.close()
		
		return string.join(response, '')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)

