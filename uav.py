import paho.mqtt.client as mqttClient
import time
import random
import math
import sys
import json
#importing all the libraries
all_data=[]   #to store preferences of individual UAV in list
ls=[]  #to know how many vehicle are left to get picked in case of ties
all_clients = []  #all UAV list
uav_location=[]
total_input=0
r=int(sys.argv[2])   #to know how many UAV are there in system
for i in range(1, r):
    all_clients.append('uav' + str(i))
    ls.append(i)
vehicle_location = []
ans=[]
v={}



def distance(curr, to):#to calculate distance between UAV location and vehicle location
    return math.sqrt((to[1] - curr[1]) ** 2 + (to[2] - curr[2]) ** 2)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected  # Use global variable
        Connected = True  # Signal connection
    else:
        print("Connection failed Return Code : ", rc)


def on_message(client, userdata, message):  #to receive msg from HQ and other UAV's via broker
    # Task-5 Write code here
    if(message.topic=='location/hq'):  #if msg came from HQ based on msg topic
        a= str(message.payload.decode("utf-8", "ignore"))
        #a=str(message.payload)
        #print(a)
        #print("ashish")
        a=a.split()
        #print(a)
        #print("as")
        for i in range(0,12,2):
            vehicle_location.append(dict({1:int(a[i]),2:int(a[i+1])}))
            #print(vehicle_location)
    else:    #if msg came from other UAV
        a=str(message.payload.decode("utf-8","ignore"))
        #print("ashish")
        #print(message.topic)
        all_data.append(dict({1:message.topic[len(message.topic)-1],2:int(a)}))
        #print(all_data)
        #print("ashish")


    #d = json.loads(message.payload)
    #if (distance(d, curr) < 20):
        #contact.append(str(message.topic))


# Task-1 Write code here

client_name = sys.argv[1]  #getting the UAV name
client_name="uav"+client_name
print(client_name)
broker_address = "127.0.0.1"  # Broker address
port = 1883
with open(str(client_name)+".txt","r") as fp:  #reading UAV location from txt file
    lines=fp.readlines()
    for line in lines:
        a=line.split()
        uav_location.append(dict({1:int(a[0]),2:int(a[1])}))
# Task-2 Write code here
# create new instance MQTT client
# client
#print(uav_location)
client = mqttClient.Client(client_name)
client.on_connect = on_connect  # attach function to callback
client.on_message = on_message  # attach function to callback

client.connect(broker_address, port=port)  # connect to broker

client.loop_start()  # start the loop
client.subscribe("location/hq")   #to connect to HQ

for item in all_clients:    #to connect to other UAV
   if (item != client_name):
       client.subscribe("location/" + item)
#print(len(uav_location))
#print(vehicle_location)
#print(len(vehicle_location))
#end_time = time.time() + 15
#while time.time() < end_time:
    # Task-4 Write code here
    #curr = location_generator()
time.sleep(6)  #wait to read all data from text file
end_time=time.time()+len(uav_location)*10
while time.time() < end_time:
    print(len(uav_location))
    print(len(vehicle_location))
    #print(vehicle_location)
    #print(uav_location[total_input])
    for i in range(0, len(vehicle_location)):
        #print(distance(vehicle_location[i], uav_location[0]))
        v = dict({1: i + 1, 2: distance(vehicle_location[i], uav_location[total_input%len(uav_location)])})
        ans.append(v)
    ans=sorted(ans, key=lambda i: i[2])
    print(ans)
    preferred_list=[]  #preference of a UAV in sorted order
    for i in ans:
        preferred_list.append(i[1])
    print(preferred_list)
    print("ashish")
    #all_data.append(dict({1:client_name[len(client_name)-1],2:preferred_list}))
    ans = []
    vehicle_location = []
    time.sleep(2)
    #listToStr = ' '.join([str(elem) for elem in preferred_list])
    t0=time.time()
    client.publish("location/" + client_name,str(preferred_list[0]))  #senidng UAV preference to broker
    total_input+=1
    time.sleep(5)
    value=""
    all_data=sorted(all_data,key=lambda i:i[1])
    print(all_data)

    for i in all_data:
        if(int(i[1])<int(client_name[len(client_name)-1])):
            preferred_list.remove(i[2])
    value+=str(int(client_name[len(client_name)-1])) +"#"+str(preferred_list[0]) #based on ID preference

    """
    for i in range(len(all_clients)):
        flag=0
        #print(i+1)
        for j in all_data[i][2]:
            #print(j)
            if(j in ls):
                value.append(dict({1:i+1, 2: j}))
                ls.remove(j)
                flag=1
            if(flag==1):
                break
    """
    ls=[]
    client.publish("preference/" + client_name, str(value)) #sending the assigned vehicle back to HQ
    t1 = time.time()
    #print(t1-t0)
    preferred_list = []
    value=""
    all_data=[]
    for i in range(0,7):
        ls.append(i)
    time.sleep(3)

    # for item in all_clients:
    # if(item!=client_name):
client.loop_stop()
print("exiting")

#print(contact)
#time.sleep(200)
