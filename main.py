import machine
import sys
import utime
import ubinascii

from machine import Pin, I2C
from sht31 import SHT31_Sensor
from umqtt.simple import MQTTClient


msg_rec_flag = False

# default MQTT setting
#SERVER =  "iot.eclipse.org"
SERVER =  "mosquitto.org"
CLIENTID = ubinascii.hexlify(machine.unique_id());
TOPIC = b"xyzabc/fahrenheit"

def sub_cb(topic, msg):	
	global msg_rec_flag
	print ((topic,msg))
	msg_rec_flag = True
	print (msg_rec_flag)


def main(clientID = CLIENTID, server = SERVER, temp=0, topic = TOPIC):
	print ("Client ID: %s" % clientID)
	print ("MQTT broker server: %s" % server)
	print ("Topic: %s" % topic)
	print ("Temperature F: %d" % temp)
	c = MQTTClient(clientID, server)
	c.set_callback(sub_cb)
	if c.connect() == 0:
		print('cCient connect status : Success')	
	else:
		print ('Client connect status : Failure')
	print('Publish data to the broker.')
	c.publish(topic, str(temp))
	print('subscribe topic (%s)' % topic)
	c.subscribe(topic)
	while not msg_rec_flag:
		if True:
			print ('Waiting for subscribe message')
			print (msg_rec_flag)
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
