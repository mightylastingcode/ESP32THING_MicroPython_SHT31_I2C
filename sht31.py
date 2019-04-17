import machine
import sys
import utime
from machine import Pin, I2C


POLYBYTE 	= 0x31  # SHT31 Polynomial
CRC_INITIAL = 0xFF

def generate_crc_from_array(data_array):
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
i2c = I2C(freq=100000, sda=Pin(21), scl=Pin(22))  

print ("SHT31 I2C Example")

print (i2c.scan())

status = i2c.writeto(0x44,b'\x24\x00')
print (status)

utime.sleep (1) ## delay (20 slow)
databytes = i2c.readfrom(0x44, 6)

len(databytes)  # 6
print (databytes) # b'^0\xce\x9b~1'
for x in databytes: print ("%x" % x)    
print ()

# Temperature CRC
dataset = [databytes[0],databytes[1]]
for x in dataset: print ("%x" % x)    
print ()

cal_crc = generate_crc_from_array(dataset)
print ("Calculated CRC = %x" % cal_crc)
if (databytes[2] == cal_crc):
	print ("CRC is good.")
else:
	print ("CRC is bad.")

#Humidity CRC
dataset = [databytes[3],databytes[4]]
for x in dataset: print ("%x" % x)    
print ()

cal_crc = generate_crc_from_array(dataset)
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

# Wait for button 0 to be pressed, and then exit
while True:
    # If button 0 is pressed, drop to REPL
    if repl_button.value() == 0:
        print("Dropping to REPL now")
        sys.exit()


    # Do nothing
    utime.sleep_ms(10)
