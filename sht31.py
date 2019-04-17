import machine
import sys
import utime
from machine import Pin, I2C


class SHT31_Sensor:
	'''
	Represents a temperature and humidity sensor.
	'''
	def __init__(self, freq, sdapin, sclpin):
		self.i2c = I2C(freq=freq, sda=Pin(sdapin), scl=Pin(sclpin)) 
		addrs = self.i2c.scan()
		if not addrs:
			raise Exception('no SHT31 found at bus on SDA pin %d SCL pin %d' % (sdapin, sclpin))
		self.addr = addrs.pop()	
		print ('Device address')
		print("%x" % self.addr)

	def read_temp_humd(self, fahreheit = True):
		status = self.i2c.writeto(self.addr,b'\x24\x00')
		print ('Status')
		print (status)

		utime.sleep (1) ## delay (20 slow)
		databytes = self.i2c.readfrom(self.addr, 6)  # read 6 bytes

		len(databytes)  # 6
		print (databytes) # b'^0\xce\x9b~1'
		for x in databytes: print ("%x" % x)    
		print ()

		# Temperature CRC
		dataset = [databytes[0],databytes[1]]
		for x in dataset: print ("%x" % x)    
		print ()

		cal_crc = self.generate_crc_from_array(dataset)
		print ("Calculated CRC = %x" % cal_crc)
		if (databytes[2] == cal_crc):
			print ("CRC is good.")
		else:
			print ("CRC is bad.")

		#Humidity CRC
		dataset = [databytes[3],databytes[4]]
		for x in dataset: print ("%x" % x)    
		print ()

		cal_crc = self.generate_crc_from_array(dataset)
		print ("Calculated CRC = %x" % cal_crc)
		if (databytes[5] == cal_crc):
			print ("CRC is good.")
		else:
			print ("CRC is bad.")

		temperature_raw = databytes[0] << 8 | databytes[1]

		temperature_raw  # 24112
		print ("%x" % temperature_raw)  #5e30

		temperatureC = (175.0 * float(temperature_raw) / 65535.0) - 45
		print ("Temp : %d C" % temperatureC)  # 19.38697 C

		temperatureF = (315.0 * float(temperature_raw) / 65535.0) - 49
		print ("Temp : %d F" % temperatureF)  # 66.89655 F

		humidity_raw = databytes[3] << 8  | databytes[4]
		humidityP    = (100.0 * float(humidity_raw) / 65535.0)
		print ("Humidity : %d %%" % humidityP)   # 60.74007

		if fahreheit:
			sensor_data = [temperatureF,humidityP]
		else:
			sensor_data = [temperatureC,humidityP]

		return sensor_data

	@staticmethod
	def generate_crc_from_array(data_array):
		POLYBYTE 	= 0x31  # SHT31 Polynomial
		CRC_INITIAL = 0xFF

		crc = CRC_INITIAL
		for byte in data_array:
			#print ("%X" % byte)
			crc = crc ^ byte
			for i in range(8):
				if ((crc & 0x80) != 0):
					crc = ((crc << 1) & 0x00FF) ^ POLYBYTE
				else:
					crc = ((crc << 1) & 0x00FF);
				#print ("i=%d crc = %x" % (i, crc))
		return crc

# Pin definitions
repl_button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)

print ("SHT31 I2C Example")

sht31 = SHT31_Sensor(freq = 100000,sdapin = 21, sclpin = 22)
measure_data = sht31.read_temp_humd()
print (measure_data)
measure_data = sht31.read_temp_humd(fahreheit = False)
print (measure_data)

# Wait for button 0 to be pressed, and then exit
while True:
    # If button 0 is pressed, drop to REPL
    if repl_button.value() == 0:
        print("Dropping to REPL now")
        sys.exit()


    # Do nothing
    utime.sleep_ms(10)
