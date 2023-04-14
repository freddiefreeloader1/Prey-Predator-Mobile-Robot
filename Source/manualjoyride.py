from time import sleep
import IMAGE
import paho.mqtt.client as mqttClient
import time
import matplotlib.pyplot as plt
import io
from PIL import Image
import cv2
import search


global nummsg
global grid
global orientation
global path
global SSG
global predy 
global predb
global preyy
global preyb
global blue, green, orange
global role
global predys
global predbs
global preyys
global preybs
global speed
global destination
SSG = "STOP"

nummsg = 0

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected                #Use global variable
        Connected = True                #Signal connection 
    else:
        print("Connection failed")

def on_message_arena(client, userdata, message):
    global grid
    global blue, green, orange
    binaryimage = message.payload
    var = io.BytesIO(binaryimage)
    var = Image.open(var)
    var.show()
    var = var.save("map6.jpg")
    var = cv2.imread(var)
    grid = IMAGE.img_processing("map6.jpg")
    blue, green, orange = search.generatelist(grid)
    print(blue, green, orange)


totalpoint = 0
lastx = 0
lasty = 0
speed = "H"

def on_message_stats(client, userdata, message):
    global nummsg
    global grid
    global orientation
    global path
    global lastx,lasty
    global totalpoint
    global role
    global speed
    global destination

    msg = message.payload
    msg = eval(msg)

    orientation = 0
    if type(msg) is dict or type(msg) is list:
        ID = 13
        if SSG == "START" or SSG == "GO":
            for item in msg:
                if type(item) != type(int) or type(item) != type(str):
                    if item["ID"] == 13:
                        pos = item["POS"]
                        centroidx = (pos[0][0] + pos[1][0]+pos[2][0]+pos[3][0])/4
                        centroidy = (pos[0][1] + pos[1][1]+pos[2][1]+pos[3][1])/4
                        sx,sy = search.findcurrentpos(centroidx, centroidy)
                        orientation = search.findorientation(pos[0][0],pos[1][0], pos[0][1],pos[1][1])
                        if lastx != sx and lasty != sy:
                            if role == "PREDATOR":
                                if (sx,sy) in blue:
                                    totalpoint += predb
                                    speed = predbs
                                elif (sx,sy) in orange:
                                    totalpoint += predy
                                    speed = predys
                                elif (sx,sy) in green:
                                    role = "PREY"
                            elif role == "PREY":
                                if (sx,sy) in blue:
                                    totalpoint += preyb
                                    speed = preybs
                                elif (sx,sy) in orange:
                                    totalpoint += preyy
                                    speed = preyys
                                elif (sx,sy) in green:
                                    role = "PREDATOR"
                        if orientation == 0:
                            destination = (sx,sy+1)
                        elif orientation == 90:
                            destination = (sx-1, sy)
                        elif orientation == 180:
                            destination = (sx, sy -1)
                        elif orientation == 270:
                            destination = (sx+1,sy)
                        robotsay = [ID, role, speed, totalpoint, (sx,sy), destination]
                        print(robotsay)
                        client.publish("robotsay", str(robotsay),qos = 0)
                        lastx,lasty = sx,sy
                        break
            nummsg += 1



def on_message_start(client, userdata, message):
    global SSG
    msg = message.payload
    SSG = msg.decode("ASCII")
    # print(msg)  

def on_message_config(client, userdata, message):
    global predy 
    global predb
    global preyy
    global preyb
    global predys
    global predbs
    global preyys
    global preybs
    global role
    msg = message.payload
    msg = eval(msg)
    predy = msg["PREDATOR"][0]
    predb = msg["PREDATOR"][1]
    preyy = msg["PREY"][0]
    preyb = msg["PREY"][1]
    predys = msg["PREDATOR"][2]
    predbs= msg["PREDATOR"][3]
    preyys = msg["PREY"][2]
    preybs = msg["PREY"][3]
    if 13 in msg["PREDATOR"][4]:
        role = "PREDATOR"
    else:
        role = "PREY"


def on_message_tick(client, userdata, message):
    msg = message.payload
    # print(msg)
    
Connected = False   #global variable for the state of the connection
  
broker_address= "192.168.1.102"  #Broker address for mechalab_intra
broker_address_thispc = "192.168.1.104"  #this pc's adress
port = 1883                         #Broker port
  
client = mqttClient.Client("Python")             
client.on_connect= on_connect                      
client.message_callback_add("arena",on_message_arena)                    
client.message_callback_add("stats",on_message_stats)
client.message_callback_add("config",on_message_config)
client.message_callback_add("tick",on_message_tick)
client.message_callback_add("start",on_message_start)

broker_adress = "192.168.1.104"

client1 = mqttClient.Client("P1")
client1.connect(broker_address_thispc)


client.connect(broker_address, port=port)          #connect to broker
client.loop_start()        #start the loop
  
while Connected != True:    #Wait for connection
    time.sleep(0.1)
  
client.subscribe("arena")
client.subscribe("stats")
client.subscribe("config")
client.subscribe("tick")
client.subscribe("start")

try:
    while True:
        time.sleep(1)
  
except KeyboardInterrupt:
    print ("exiting")
    client.disconnect()
    client.loop_stop()


            

            


