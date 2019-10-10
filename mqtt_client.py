import paho.mqtt.client as mqtt
import time


class MQTT():

    client = mqtt.Client("P1")

    timeout = 5
    answer = ""
    status = False
    t = 0
    
    def __init__(self, ip='192.168.50.168', port=8883, username="raspberrypi", password="omo", tx_topic="hubCommands/raspberrypi", rx_topic="map_builder/raspberrypi"):
        self.IP = ip
        self.port = port
        self.USERNAME = username
        self.PASS = password
        self.topic_TX = tx_topic
        self.topic_RX = rx_topic
        

    def create_connection(self):
        self.client.on_message=self.on_message #attach function to callback
        self.client.username_pw_set(self.USERNAME, self.PASS)
        self.client.connect(self.IP, self.port, 60) #connect to broker
        self.client.loop_start() #start the loop
        self.client.subscribe(self.topic_RX, 2)

    def close_connection(self):
        self.client.loop_stop()

    def send_discovery_request(self):
        self.client.publish(self.topic_TX, '{ "hostCommand": { "discovery": 1 } }')
        self.t = time.time()
        self.status = False
        self.answer = "{ discovery finished success }"

        while 1:
            if(time.time() - self.t > self.timeout):
                print("MQTT ERROR: timeout")
                return False
            if(self.status == True):
                return True

    def send_setpermit_request(self):
        self.client.publish(self.topic_TX, '{ "hostCommand": { "setpermit": 60 } }')

    def send_closepermit_request(self):
        self.client.publish(self.topic_TX, '{ "hostCommand": { "setpermit": 0 } }')
    
    def send_getpermit_request(self):
        self.client.publish(self.topic_TX, '{ "hostCommand": { "getpermit": 1 } }')

    def on_message(self, client, userdata, message):
        answer = str(message.payload.decode("utf-8"))
        #print("message received " ,str(message.payload.decode("utf-8")))
        #print("message topic=",message.topic)
        #print("message qos=",message.qos)
        #print("message retain flag=",message.retain)
        print(answer)
        if(self.answer == answer):
            self.status = True
        