import paho.mqtt.client as mqtt
import time


def on_message(client, userdata, message):
    global STATUS
    answer = str(message.payload.decode("utf-8"))
    #print("message received " ,str(message.payload.decode("utf-8")))
    #print("message topic=",message.topic)
    #print("message qos=",message.qos)
    #print("message retain flag=",message.retain)

class MQTT():

    client = mqtt.Client("P1")
    
    def __init__(self, ip='192.168.50.18', port=8883, username="omo-dev-embedded", password="omo", tx_topic="hubCommands/omo-dev-embedded", rx_topic="map_builder/omo-dev-embedded"):
        self.IP = ip
        self.port = port
        self.USERNAME = username
        self.PASS = password
        self.topic_TX = tx_topic
        self.topic_RX = rx_topic
        

    def create_connection(self):
        self.client.on_message=on_message #attach function to callback
        self.client.username_pw_set(self.USERNAME, self.PASS)
        self.client.connect(self.IP, self.port, 60) #connect to broker
        self.client.loop_start() #start the loop

    def close_connection(self):
        self.client.loop_stop()

    def send_discovery_request(self):
        self.client.publish(self.topic_TX, '{ "hostCommand": { "discovery": 1 } }')
        return "{ discovery finished success }"

    def send_setpermit_request(self):
        self.client.publish(self.topic_TX, '{ "hostCommand": { "setpermit": 60 } }')

    def send_closepermit_request(self):
        self.client.publish(self.topic_TX, '{ "hostCommand": { "getpermit": 1 } }')
    
    def send_getpermit_request(self):
        self.client.publish(self.topic_TX, '{ "hostCommand": { "setpermit": 0 } }')