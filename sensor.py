#
# sensor.py:  Module for reading temperature and pressure from the Honeywell Pressure Sensor
#

import quick2wire.i2c as i2c
from time import sleep

#
# Unit Constants.  Use these to specify the temperature and pressure units to output
#

TempFahrenheit = "fahrenheit"
TempCelsius = "celsius"

PressurePSI = "psi"
PressureInH2O = "inh2o"


class SensorError(Exception):
	def __init__(self, code):
		self.status_code = code
		
	def __str__(self):
		return "SensorError: Status = " + str(self.status_code)
		
		
#
# Class Sensor(i2c_bus, sensor_address)
#
#	Interface to the Honeywell pressure/temperature sensor.  
#
#	Default i2c bus and sensor address for the sum project.  Reuse of this module may require
#	the bus and sensor addresses to be set via i2c_bus and sensor_address
#
class Sensor:
	def __init__(self, i2c_bus = 1, sensor_address = 0x38):
		self.i2c_bus = i2c_bus					# i2c bus number
		self.sensor_address = sensor_address	# sensor i2c address
		self.p_val_min = 1667 					# raw pressure value off sensor when zero differential with current atmospheric
		
				
	#
	# real: read_temperature(t_unit)
	#
	#	Read the temperature off the sensor.  
	#
	#	Default unit is Fahrenheit. Set t_unit to sensor.TempCelsius if required.
	#
	#	Can raise:
	#		RuntimeError if invalid unit is provided or sensor cannot be contacted
	#		SensorError if sensor is contacted, but returns a non-zero status byte
	#
	def read_temperature(self, t_unit = TempFahrenheit):
			(p_val, t_val) = self._read_sensor_data()
			if (t_unit == TempFahrenheit):
				return self._fahrenheit(t_val)
			elif (t_unit == TempCelsius):
				return self._celsius(t_val)
			else:
				raise RuntimeError("Invalid unit to Sensor.read_temp()")
		

	#
	# real: read_pressure(p_unit)
	#
	#	Read the temperature off the sensor.  
	#
	#	Default unit is PSI. Set p_unit to sensor.PressureInH2O (inches of water) if required.
	#
	#	Can raise:
	#		RuntimeError if invalid unit is provided or sensor cannot be contacted
	#		SensorError if sensor is contacted, but returns a non-zero status byte
	#
	def read_pressure(self, p_unit = PressurePSI):
			(p_val, t_val) = self._read_sensor_data()
			if (p_unit == PressurePSI):
				return self._psi(p_val)
			elif (p_unit == PressureInH2O):
				return self._inH2O(p_val)
			else:
				raise RuntimeError("Invalid unit to Sensor.read_pressure()")
	
	
	#
	# (pressure (real), temperature (real): read_pressure_and_temperature(p_unit, t_unit)
	#
	#	Read the pressure and temperature off the sensor.  If you need both, this is the most efficient 
	#	way to get them, as both are read off the sensor in one read operation.
	#
	#	Default pressure unit is PSI. Set p_unit to sensor.PressureInH2O (inches of water) if required.
	#	Default temperature unit is Fahrenheit. Set t_unit to sensor.TempCelsius if required.
	#
	#	Can raise:
	#		RuntimeError if invalid unit is provided or sensor cannot be contacted
	#		SensorError if sensor is contacted, but returns a non-zero status byte
	#	
	def read_pressure_and_temperature(self, p_unit = PressurePSI, t_unit = TempFahrenheit):
		(p_val, t_val) = self._read_sensor_data()
		if (p_unit == PressurePSI):
			p_return = self._psi(p_val)
		elif (p_unit == PressureInH2O):
			p_return = self._inH2O(p_val)
		else:
			raise RuntimeError("Invalid pressure unit to Sensor.read_pressure_and_temperature()")

		if (t_unit == TempFahrenheit):
			t_return = self._fahrenheit(t_val)
		elif (t_unit == TempCelsius):
			t_return = self._celsius(t_val)
		else:
			raise RuntimeError("Invalid temperature unit to Sensor.read_pressure_and_temperature()")

		return (p_return, t_return)


	#
	# <no return>: calibrate_pressure()
	#
	#	Take a sampling of pressure readings and reset the pressure min-value to their average.
	#	This should only be called when you are sure that there is no pressure differential with atmospheric
	#
	#	Process takes ~10s to execute
	#
	def calibrate_pressure(self):
		i = 10
		p_val_sum = 0
		
		while i > 0:
			(p_val, t_val) = self._read_sensor_data()
			p_val_sum = p_val_sum + p_val
			sleep(1)
			i = i - 1
			
		self.p_val_min = p_val_sum / 10
		


	#
	# (raw_pressure (int), raw_temperature (int)) _read_sensor_data()
	#
	#	Read the raw pressure and temperature values off the sensor
	#
	def _read_sensor_data(self):
		try:
			# Read 4 bytes off the sensor
			# See here for info on data format:
			#	http://sensing.honeywell.com/i2c%20comms%20digital%20output%20pressure%20sensors_tn_008201-3-en_final_30may12.pd
			with i2c.I2CMaster(self.i2c_bus) as bus:
				bytes = bus.transaction(
					i2c.reading(self.sensor_address, 4)
					)			
		except IOError:    # Raised when sensor can't be read.  Convert to RuntimeError to pass back a msg 
			raise RuntimeError("Can't read from sensor.  Likely incorrect bus or i2c address.")

		# Check status code
		status = bytes[0][0] >> 6
		if (status != 0):
			raise SensorError(status)
			
		# Convert bytes to raw pressure and temperature values
		pressure_value = ((bytes[0][0] & 0b00111111) << 8) + bytes[0][1]
		temp_value = (bytes[0][2] << 3) + (bytes[0][3] >> 5)
		
		return (pressure_value, temp_value)


	#
	# Utility functions to convert raw sensor value to pressure and temperature readings
	#
	def _psi(self, p_val):
			return (p_val - self.p_val_min) * 5 /(14745 - self.p_val_min)
			
	def _inH2O(self, p_val):
			return self._psi(p_val) * 27.679904843
			
	def _celsius(self, t_val):
		return ((t_val / 2047 * 200) - 50)
		
	def _fahrenheit(self, t_val):
		return self._celsius(t_val) * 9/5 + 32


