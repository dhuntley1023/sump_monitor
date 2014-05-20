import quick2wire.i2c as i2c
import time

class SensorUnits:
	TempFahrenheit = "fahrenheit"
	TempCelsius = "celsius"
	
	PressurePSI = "psi"
	PressureInH2O = "inh2o"


class SensorError(Exception):
	def __init__(self, code):
		self.status_code = code
		
	def __str__(self):
		return "SensorError: Status = " + str(self.status_code)
		
		
class Sensor:
	def __init__(self, i2c_bus = 1, i2c_address = 0x38):
		self.i2c_bus = i2c_bus
		self.i2c_address = i2c_address
		
	def _read_sensor_data(self):
		iodir_register = self.i2c_bus
		address = self.i2c_address
		
		with i2c.I2CMaster() as bus:
			bytes = bus.transaction(
				i2c.reading(address, 4)
				)
				
		status = bytes[0][0] >> 6
		
		if (status != 0):
			raise(SensorError(status))
			
		pressure_value = ((bytes[0][0] & 0b00111111) << 8) + bytes[0][1]
		temp_value = (bytes[0][2] << 3) + (bytes[0][3] >> 5)
		
		# print(bytes[0][0], bytes[0][1], bytes[0][2], bytes[0][3])
		return (pressure_value, temp_value)

	def read_temp(self, t_unit = SensorUnits.TempFahrenheit):
			(p_val, t_val) = self._read_sensor_data()
			if (t_unit == SensorUnits.TempFahrenheit):
				return self._fahrenheit(t_val)
			elif (t_unit == SensorUnits.TempCelsius):
				return self._celsius(t_val)
			else:
				raise(RuntimeError("Invalid unit to Sensor.read_temp()"))
		
	def read_pressure(self, p_unit = SensorUnits.PressurePSI):
			(p_val, t_val) = self._read_sensor_data()
			if (p_unit == SensorUnits.PressurePSI):
				return self._psi(p_val)
			elif (p_unit == SensorUnits.PressureInH2O):
				return self._inH2O(p_val)
			else:
				raise(RuntimeError, "Invalid unit to Sensor.read_temp()")
		
	def read_pressure_and_temp(self, p_unit = SensorUnits.PressurePSI, t_unit = SensorUnits.TempFahrenheit):
		(p_val, t_val) = self._read_sensor_data()
		if (p_unit == SensorUnits.PressurePSI):
			p_return = self._psi(p_val)
		elif (p_unit == SensorUnits.PressureInH2O):
			p_return = self._inH2O(p_val)
		else:
			raise(RuntimeError, "Invalid unit to Sensor.read_pressure_and_temp()")

		if (t_unit == SensorUnits.TempFahrenheit):
			t_return = self._fahrenheit(t_val)
		elif (t_unit == SensorUnits.TempCelsius):
			t_return = self._celsius(t_val)
		else:
			raise(RuntimeError, "Invalid unit to Sensor.read_pressure_and_temp()")

		return (p_return, t_return)


	def _psi(self, p_val):
			return (p_val - 1667) * 5 /(14745 - 1667)
			
	def _inH2O(self, p_val):
			return self._psi(p_val) * 27.679904843
			
	def _celsius(self, t_val):
		return ((t_val / 2047 * 200) - 50)
		
	def _fahrenheit(self, t_val):
		return self._celsius(t_val) * 9/5 + 32


