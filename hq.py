import time
import random
import math
import sys
import json
import paho.mqtt.client as mqttClient
from sys import getsizeof
all_clients = []
final=[]
r=int(sys.argv[2])   #for knowing how many uav are there
for i in range(1, r):
    all_clients.append('uav' + str(i))
def on_connect(client, userdata, flags, rc):    #on connect function
    if rc == 0:
        print("Connected to broker")
        global Connected  # Use global variable
        Connected = True  # Signal connection
    else:
        print("Connection failed Return Code : ",rc)

def on_message(client, userdata, message):    #to receieve messages from connected UAV's
    d= str(message.payload.decode("utf-8", "ignore"))
    #print(getsizeof(d))
    final.append(dict({1:int(d.split('#')[0]),2:int(d.split('#')[1])}))  #getting all preferences
    if(len(final)==(r-1)):
        print(final)
        t=sorted(final,key=lambda i: i[2])
        print(t)
        text=''
        for i in t:
            text+=str(i[1])+' '
        final.clear()

        with open('output.txt','a') as file2:   #writing preferences on text file
            file2.write(text)
            file2.write('\n')
    #file2.write("\n")



Connected = False  # global variable for the state of the connection
client_name=sys.argv[1]
broker_address = "127.0.0.1"  # Broker address
port = 1883  # Broker port

client = mqttClient.Client(client_name)
client.on_connect = on_connect  # attach function to callback
client.on_message = on_message  # attach function to callback


client.connect(broker_address, port=port)  # connect to broker

client.loop_start()  # start the loop
print(client_name)
for item in all_clients:
    print(item)
    client.subscribe("preference/" + item)    #getting connected to all UAV's

time.sleep(4)
with open("vehicle_location.txt","r") as f1:   #reading vechcile location and sending it the broker
    lines=f1.readlines()
    for line in lines:
        print(line)
        client.publish("location/"+client_name,str(line))
        time.sleep(10)


time.sleep(2)