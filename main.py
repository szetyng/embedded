# to load onto ESP8266
# --------------- import the necessary modules --------------------------------
from machine import Pin, I2C
import json
import network	# to configure the WiFi connection
import time
import machine
from umqtt.simple import MQTTClient

import utime
from machine import RTC


#------------- Read data, do comparison, publish accordingly -------------------
# return true when golf ball hits seensor
def check_goal(counter):
		#Opens write comm with slave at 0x13, send 0x87,
		#switch to read mode, read 2 bytes, return byte_array of 2 bytes
	data = i2c.readfrom_mem(0x13, 0x87, 2)
		# convert the 2 bytes to an int
	dataInInt = int.from_bytes(data, 'big')
		# comparing data with threshold (5000). Being greater than 5000 -> GOALLl -> send msg
	if dataInInt > 5000:
		tag = {"status": "game over", "swing": counter}
			# serialise to json format
		print (json.dumps(tag))
			# publish a msg to subscricers
		client.publish('esys/anonymous', bytes(json.dumps(tag),'utf-8'))
		return True
	return False

# ------------------------- define the rules here: -----------------------------
def golf_game():
	counter = 0
	while(True):
			# Get the digital logic level of the pin
		button = p_12.value()

		if button == 1:
			counter += 1
			print("counter = ", counter)
		
		# only starts checking after the game has started
		if counter >= 1:
			goal = check_goal(counter)
			if goal == True:
				counter = 0
				#return

		time.sleep_ms(200)
		pass

# ------------------- Connect to a specific  Wifi network ----------------------
	# specify the name and password of a network
network_name = 'EEERover'
network_pw = 'exhibition'
	# create station interface
sta_if = network.WLAN(network.STA_IF)
	# Check if the connection is established use: sta_if.isconnected()
if not sta_if.isconnected():
    print('Connecting to network...')
		# activate the station interface
    sta_if.active(True)
		# then connect to (an AP) your WiFi network:
    sta_if.connect(network_name, network_pw)
    while not sta_if.isconnected():
        pass
print ('Connected!')
	# create access-point interface
ap_if = network.WLAN(network.AP_IF)
	#disable the access-point interface when no longer needed (reduce overheads)
ap_if.active(False)

#------------------ connect to broker ------------------------------------------
broker_id = '192.168.0.10'
client = MQTTClient(machine.unique_id(), broker_id)
client.connect()
#============================================================================
	# initialize P12 in gpio mode and make it an input
p_12 = Pin(12,Pin.IN, None)
	# Create an instance of i2c class + Specify pins in initialiser arguments
i2c = I2C(sda=Pin(4), scl=Pin(5), freq=100000)
	# Opens write comm with slave at bus_addr, send reg_addr, send each byte in data
i2c.writeto_mem(0x13, 0x80, bytearray([0x03]))

print("May the odds be in your favour!")

golf_game()