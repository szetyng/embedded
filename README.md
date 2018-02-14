# Embedded Systems - ACE Caddie
Code for Embedded Systems Design. Load main.py onto ESP8266.  

Main.py is the code that runs on the ESP8266 connected to the Proximity Sensor.   
  
The ESP8266 is the main publisher, publishing messages to the topic 'esys/<anonymous>.  
  How main works:  
  Creates a Client instance  
  Connects to broker  
    Detects if game has started (Indicated by Button press)  
    Counts number of swings until the ball goes in hole (swings are indicated by button press)  
    Publishes score once a game has ended 
  
  Subscribe.py is the code run by the client subscribed to 'esys/<anonymous>', e.g an app on your smartphone  
    How subscribe.py works:   
    Subcribes to topic 'esys/<anonymous>'
