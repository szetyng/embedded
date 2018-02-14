# Embedded Systems - Ace CADDIE
Code for Embedded Systems Design. Load main.py onto ESP8266.  

How To:  
    1. Connect the subscriber client to the broker `'EERover'`  
    2. Run sunscriber.py  
    2. Reset the ESP  
    3. Press button to start game (this is your 1st swing)  
    4. Play the game! (Press the button everytime you take a shot)  
  
Background:  
  
  Main.py is the code that runs on the ESP8266 connected to the Proximity Sensor.   
  The ESP8266 is the main publisher, publishing messages to the topic `'esys/<anonymous>`
    How main works:  
    Creates a Client instance  
    Connects to broker  
    Detects if game has started (Indicated by Button press)  
    Counts number of swings until the ball goes in hole (swings are indicated by button press)  
    Publishes score once a game has ended 
  
Subscribe.py is the code run by the client subscribed to `'esys/<anonymous>'`, e.g an app on your smartphone
    How subscribe.py works:   
    Subcribes to topic `'esys/<anonymous>'`  
    Takes in user entered data (Username and Par for the golf course)  
    Decodes message published by ESP when a game has finished  
    Calculates and returns score  
    Returns player's postiion in ranking  
  
  
   See our website https://dharshana1407.wixsite.com/acecaddie for more info! 
