from machine import Pin, I2C
import json
import network
import time

import machine
import ubinascii
from umqtt.simple import MQTTClient
#clientID = ubinascii.hexlify(machine.unique_id())


# initialising ESP 
i2c = I2C(sda=Pin(4), scl=Pin(5), freq=100000)
# i2c.writeto_mem(0x13, 0x80, bytearray([0x08]))
# data = i2c.readfrom_mem(0x13, 0x87, 2)
# dataInInt = int.from_bytes(data, 'big')
# print(dataInInt)

# connect to broker
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)
time.sleep_ms(1000)
sta_if = network.WLAN(network.STA_IF)
time.sleep_ms(1000)
sta_if.active(True)
time.sleep_ms(1000)
sta_if.connect('EEERover', 'exhibition')
time.sleep_ms(2000)
if sta_if.isconnected(): 
	print('connecteddd :D')
	print('config set:', sta_if.ifconfig())
else:
	print('nope :(')

# connect to broker
client = MQTTClient('14140928', '192.168.0.10')
time.sleep_ms(1000)
client.connect()

# def doConnect():
# 	ap_if = network.WLAN(network.AP_IF)
# 	ap_if.active(False)
# 	#time.sleep_ms(1000)
# 	sta_if = network.WLAN(network.STA_IF)
# 	#time.sleep_ms(1000)
# 	sta_if.active(True)
# 	time.sleep_ms(1000)
# 	sta_if.connect('EEERover', 'exhibition')
# 	#time.sleep_ms(2000)
# 	if sta_if.isconnected(): 
# 		print('connecteddd :D')
# 		print('config set:', sta_if.ifconfig())
# 	else:
# 		print('nope :(')

# read data and return it in JSON format
def doReadings():
	i2c.writeto_mem(0x13, 0x80, bytearray([0x08]))
	data = i2c.readfrom_mem(0x13, 0x87, 2)
	dataInInt = int.from_bytes(data, 'big')
	print(dataInInt)
	read1json = {"proximity": dataInInt}
	return json.dumps(read1json)

def sendData():
	# import machine
	# import ubinascii
	# from umqtt.simple import MQTTClient
	#clientID = ubinascii.hexlify(machine.unique_id())

	payload = doReadings()

	# client = MQTTClient('14140928', '192.168.0.10')
	# time.sleep_ms(1000)
	# client.connect()
	#time.sleep_ms(1000)
	client.publish('esys/<anonymous>' ,bytes(payload,'utf-8'))
	