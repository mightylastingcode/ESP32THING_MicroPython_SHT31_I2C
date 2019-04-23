'''

Author: Michael Li
Date: 4/25/2019

Example: MQTT Publish & Subscribe 
		1. Publish temperature in F from SHT31 sensor
		2. Scuscribe LED switch command (0,1,2) from the server.
		     0 - off, 1 - on, 2 - toggle

'''


import machine
import sys
import utime
import ubinascii

from machine import Pin, I2C
from sht31 import SHT31_Sensor
from umqtt.simple import MQTTClient


msg_rec_count = 0
blueledstate = 0

# default MQTT setting
#SERVER =  "iot.eclipse.org"
#SERVER =  "mqtt.mediumone.com"

SERVER 		= "mosquitto.org"
CLIENTID 	= ubinascii.hexlify(machine.unique_id());
PUB_TOPIC 	= b"xyzabc/fahrenheit"
SUB_TOPIC 	= b"xyzabc/led"
PORT 		= 1883
MQTT_USERNAME = None
MQTT_password = None




SUB_TOPIC = b"xyzabc/led"
def sub_cb(topic, msg):	
	global msg_rec_count
	global blueledstate
	print ((topic,msg))
	msg_rec_count = msg_rec_count + 1
	print ("Message counter value: %d" % msg_rec_count)
	if topic == SUB_TOPIC:
		if msg == b"1":
			print ("turn on led")
			blueledstate = 1
			blueled.value(1)
		elif msg == b"0":
			print ("turn off led")
			blueledstate = 0
			blueled.value(0)
		elif msg == b"2":	
			print ("toggle led")		
			if blueledstate == 0:
				blueledstate = 1
				blueled.value(1)
			else:				
				blueledstate = 0
				blueled.value(0)

def main(clientID = CLIENTID, server = SERVER, temp=0, topic = PUB_TOPIC):
	print ("Client ID: %s" % clientID)
	print ("MQTT broker server: %s" % server)
	print ("Topic: %s" % topic)
	print ("Temperature F: %d" % temp)
	c = MQTTClient(clientID, server, PORT, MQTT_USERNAME, MQTT_password)
	c.set_callback(sub_cb)
	if c.connect() == 0:
		print('cCient connect status : Success')	
	else:
		print ('Client connect status : Failure')
	print('Publish data to the broker.')
	c.publish(topic, str(temp))
	print('subscribe topic (%s)' % SUB_TOPIC)
	c.subscribe(SUB_TOPIC)
	while msg_rec_count < 4:
		if True:
			print ('Waiting for subscribe message')			
			# blocking wait for message
			c.wait_msg()
		else:
			# non blocking wait for message
			print ('Waiting for subscribe message')
			c_check_msg()
			time.sleep(1)			
	print ('Client disconnect')			
	c.disconnect()

# Module name
print ("Python name : %s." % __name__)

# Pin definitions
repl_button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
blueled = machine.Pin(5, machine.Pin.OUT)

if __name__ == "__main__":
	print ("SHT31 I2C Example")
	sht31 = SHT31_Sensor(freq = 100000,sdapin = 21, sclpin = 22)
	measure_data = sht31.read_temp_humd(fahreheit = False)
	print (measure_data)
	measure_data = sht31.read_temp_humd()
	print (measure_data)
	##main(clientID = '52dc166c-2de7-43c1-88ff-f80211c7a8f6',temp=measure_data[0])
	main(temp=measure_data[0])

# Wait for button 0 to be pressed, and then exit
while True:
    # If button 0 is pressed, drop to REPL
    if repl_button.value() == 0:
        print("Dropping to REPL now")
        sys.exit()


    # Do nothing
    utime.sleep_ms(10)
