import machine
import sys
import utime
from machine import Pin, I2C
from sht31 import SHT31_Sensor

# Pin definitions
repl_button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)

print ("SHT31 I2C Example")

sht31 = SHT31_Sensor(freq = 100000,sdapin = 21, sclpin = 22)
measure_data = sht31.read_temp_humd()
print (measure_data)
measure_data = sht31.read_temp_humd(fahreheit = False)
print (measure_data)

from umqtt.simple import MQTTClient

print ('connecting to an online broker')
client = MQTTClient('<Unique ID','<Broker Address>')

print ('client connect status :')
print(client.connect())
print ("publish : 'xyzabc/fahrenheit', '72'")
client.publish('xyzabc/fahrenheit', '72')

# Wait for button 0 to be pressed, and then exit
while True:
    # If button 0 is pressed, drop to REPL
    if repl_button.value() == 0:
        print("Dropping to REPL now")
        sys.exit()


    # Do nothing
    utime.sleep_ms(10)
