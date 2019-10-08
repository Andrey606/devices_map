import paho.mqtt.client as mqtt #import the client1
import time

broker_address = '192.168.50.18'
port = 8883
USERNAME = "omo-dev-embedded"
PASS = "omo"
topic_TX = "hubCommands/omo-dev-embedded"
topic_RX = "hubEvents/omo-dev-embedded"


getpermit = '{ "hostCommand": { "getpermit": 1 } }'
discovery = '{ "hostCommand": { "discovery": 1 } }'
discovery_answer = '{ discovery finished }'

STATUS = False

TIMEOUT = 1

########################################
def on_message(client, userdata, message):
    global STATUS
    answer = str(message.payload.decode("utf-8"))
    #print("message received " ,str(message.payload.decode("utf-8")))
    #print("message topic=",message.topic)
    #print("message qos=",message.qos)
    #print("message retain flag=",message.retain)
    
    if discovery_answer == answer:
        STATUS = True
    else:
        print("Error")
########################################


def send_responce():
    global STATUS
    STATUS = False

    #print("creating new instance")
    client = mqtt.Client("P1") #create new instance
    client.on_message=on_message #attach function to callback
    #print("connecting to broker")
    client.username_pw_set(USERNAME, PASS)
    client.connect(broker_address, port, 60) #connect to broker

    client.loop_start() #start the loop
    #print("Subscribing to topic",topic_RX)
    client.subscribe(topic_RX)
    #print("Publishing message to topic",topic_TX)
    client.publish(topic_TX, discovery)
    
    t = time.time()

    while 1:
        if (time.time() - t) >= TIMEOUT:
            print("TIMEOUT")
            break
        elif STATUS == True:
            print("message received via", (time.time() - t))
            break

    client.loop_stop() #stop the loop

    return STATUS