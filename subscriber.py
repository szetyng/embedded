
import paho.mqtt.client as mqtt
import json
import operator
from operator import itemgetter#, attrgetter


def setupgame():
	incorrect_par = True
	while(incorrect_par):
		username = input("Enter your name: ")
		par_str = input("Enter par (3,4 or 5): ")
		par = int(par_str)
		if par > 5 or par < 3:
			print ("Incorrect par")
		else:
			incorrect_par = False
			return (par,username)
		pass

def getscore(par,swing):
	if swing == 1: # swing = 1 will give us ace regardless of par value
		return ("ace", -4)

	relation = swing-par
	if relation == -1:
		return ("birdie",relation)
	elif relation == -2:
		return ("eagle", relation)
	elif relation == -3:
		return ("albatross", relation)
	elif relation == 0:
		return ("par", relation)
	elif relation == 1:
		return ("bogey", relation)
	elif relation == 2:
		return ("double bogey", relation)
	elif relation == 3:
		return ("triple bogey", relation)
	elif relation >= 4:
		return ("you suck at golf. try finishing instead", relation)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

	# Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("esys/anonymous")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	 # get the user input

	jdata = msg.payload.decode('utf-8') # json
	print(msg.topic+" "+jdata)
	golfdata = json.loads(jdata) # python dictionary
	finalswing = golfdata["swing"]
	score = getscore(par, finalswing)
	rank = get_ranking(score)

# initialising the array of score
def get_ranking(score):

	initRanking=[
		("Dharshana", -1, 'birdie'),
		("Mohika", 0, 'par'),
		("Chelle", 3, 'triple bogey')
	]
	# add new record to ranking
	initRanking.append([username,score[1], score[0]])

	sortedrank = sorted(initRanking, key = itemgetter(1))

	for i in range(len(sortedrank)):
		print(str(i+1) + ". " + sortedrank[i][0] + "\t" + sortedrank[i][2])



#client = mqtt.Client(clientID="")
client = mqtt.Client("")
client.on_connect = on_connect

initGame = setupgame()
par = initGame[0]
username = initGame[1]

client.on_message = on_message

client.connect('192.168.0.10')
client.loop_forever()