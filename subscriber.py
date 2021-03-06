import paho.mqtt.client as mqtt
import json
import operator
from operator import itemgetter


# Asks for username and Par from user
def setup_game():
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

# Takes user input Par and the number of swings to determine final score
def get_score(par,swing):
	# swing = 1 returns ace regardless of par value
	if swing == 1: 
		return ("ace", -4)

	relation = swing - par
	
	if relation >= 4:
		return ("you suck at golf, try fishing instead", relation)
	else:
		return (golf_terms[relation], relation)

# Appends player's game details into the array init_ranking and then ranks all users, lower score = higher ranking
def get_ranking(score):
	# current scores from friends
	init_ranking=[
		("Dharshana", -1, 'birdie'),
		("Mohika", 0, 'par'),
		("Chelle", 3, 'triple bogey')
	]
	# add new record to ranking
	init_ranking.append([username,score[1], score[0]])

	sorted_rank = sorted(init_ranking, key = itemgetter(1))
	#Print rank, name, score
	for i in range(len(sorted_rank)):
		print(str(i+1) + ". " + sorted_rank[i][0] + "\t" + sorted_rank[i][2])

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("esys/anonymous")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	jdata = msg.payload.decode('utf-8') # json
	print(msg.topic+" "+jdata)
	golfdata = json.loads(jdata) # python dictionary

	finalswing = golfdata["swing"] 

	score = get_score(par, finalswing)
	get_ranking(score)



# Client = mqtt.Client(clientID="")
client = mqtt.Client("")
client.on_connect = on_connect

# Gets user details: par and username
game_details = setup_game()
par = game_details[0]
username = game_details[1]

# Mapping from relation to score 
golf_terms={
	-1 : "birdie" ,
	-2 : "eagle" ,
	-3 : "albatross" ,
	0 : "par" ,
	1 : "bogey" ,
	2 : "double bogey" ,
	3 : "triple bogey" 
}

client.on_message = on_message

client.connect('192.168.0.10')
client.loop_forever()
