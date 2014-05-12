import quick2wire.i2c as i2c
import time

class Sensor:
	def __init__(self, i2c_bus = 1, i2c_address = 0x38):
		self.i2c_bus = i2c_bus
		self.i2c_address = i2c_address
		
	def read_sensor_data(self):
		iodir_register = self.i2c_bus
		address = self.i2c_address
		
		with i2c.I2CMaster() as bus:
			bytes = bus.transaction(
				i2c.reading(address, 4)
				)
				
		status = bytes[0][0] >> 6
		pressure_value = ((bytes[0][0] & 0b00111111) << 8) + bytes[0][1]
		temp_value = (bytes[0][2] << 3) + (bytes[0][3] >> 5)
		
		print(bytes[0][0], bytes[0][1], bytes[0][2], bytes[0][3])
		return (status, pressure_value, temp_value)

	def psi(self, pval):
			return (pval - 1667) * 5 /(14745 - 1667)
			
	def inches_of_water(self, pval):
			return self.psi(pval) * 27.679904843
			
	def fahrenheit(self, tval):
		return ((tval / 2047 * 200) - 50) * 9/5 + 32
