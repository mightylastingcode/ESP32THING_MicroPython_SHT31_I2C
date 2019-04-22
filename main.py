import machine
import sys
import utime
import ubinascii

from machine import Pin, I2C
from sht31 import SHT31_Sensor
from umqtt.simple import MQTTClient


# default MQTT setting
#SERVER =  "iot.eclipse.org"
SERVER =  "mosquitto.org"
CLIENTID = ubinascii.hexlify(machine.unique_id());
TOPIC = b"xyzabc/fahrenheit"

def main(clientID = CLIENTID, server = SERVER, temp=0, topic = TOPIC):
	print ("Client ID: %s" % clientID)
	print ("MQTT broker server: %s" % server)
	print ("Topic: %s" % topic)
	print ("Temperature F: %d" % temp)
	c = MQTTClient(clientID, server)
	print ('client connect status :')
	print(c.connect())
	c.publish(b"xyzabc/fahrenheit", str(temp))
	c.disconnect()

# Module name
print ("Python name : %s." % __name__)

# Pin definitions
repl_button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)

if __name__ == "__main__":
	print ("SHT31 I2C Example")
	sht31 = SHT31_Sensor(freq = 100000,sdapin = 21, sclpin = 22)
	measure_data = sht31.read_temp_humd(fahreheit = False)
	print (measure_data)
	measure_data = sht31.read_temp_humd()
	print (measure_data)
	main(temp=measure_data[0])

# Wait for button 0 to be pressed, and then exit
while True:
    # If button 0 is pressed, drop to REPL
    if repl_button.value() == 0:
        print("Dropping to REPL now")
        sys.exit()


    # Do nothing
    utime.sleep_ms(10)
