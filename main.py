# to load onto ESP8266

from machine import Pin, I2C
import json
import network
import time

import machine
from umqtt.simple import MQTTClient

def doConnect():
	network_name = 'EEERover'
	network_pw = 'exhibition'

	ap_if = network.WLAN(network.AP_IF)
	ap_if.active(False)

	sta_if = network.WLAN(network.STA_IF)
	if not sta_if.isconnected():
	    print('connecting to network...')
	    sta_if.active(True)
	    sta_if.connect(network_name, network_pw)
	    while not sta_if.isconnected():
	        pass
	# print('network config:', sta_if.ifconfig())

# read data and return it in JSON format
def doReadings():
	i2c.writeto_mem(0x13, 0x80, bytearray([0x08]))
	data = i2c.readfrom_mem(0x13, 0x87, 2)
	dataInInt = int.from_bytes(data, 'big')
	print('data in int:', dataInInt)
	
	read1json = {"proximity": dataInInt}
	return json.dumps(read1json)

def sendData():
	payload = doReadings()
	client.publish('esys/<anonymous>' ,bytes(payload,'utf-8'))


# initialising ESP 
i2c = I2C(sda=Pin(4), scl=Pin(5), freq=100000)

# connect to internet
doConnect()

# connect to broker
broker_id = '192.168.0.10'
client = MQTTClient(machine.unique_id(), broker_id)
#time.sleep_ms(1000)
client.connect()