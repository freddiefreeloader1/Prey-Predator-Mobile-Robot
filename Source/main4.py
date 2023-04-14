from time import sleep
import IMAGE
import paho.mqtt.client as mqttClient
import time
import matplotlib.pyplot as plt
import io
from PIL import Image
import cv2
import search

global grid
global orientation
global path
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
    binaryimage = message.payload
    var = io.BytesIO(binaryimage)
    var = Image.open(var)
    var.show()
    var = var.save("map6.jpg")
    var = cv2.imread(var)
    grid = IMAGE.img_processing("map6.jpg")




def on_message_stats(client, userdata, message):
    global nummsg
    global grid
    global orientation
    global path
    msg = message.payload
    msg = eval(msg)
    msg = msg[0]
    orientation = 0
    if type(msg) is dict:
        ID = msg["ID"]
        if ID == 13:
            pos = msg["POS"]
            ylines = [46.5, 122, 200, 277, 357, 429]
            xlines = [43, 119, 196, 272, 348, 422, 497, 576]
            centroidx = (pos[0][0] + pos[1][0]+pos[2][0]+pos[3][0])/4
            centroidy = (pos[0][1] + pos[1][1]+pos[2][1]+pos[3][1])/4
            erroryabs = [abs(item - centroidy) for item in ylines]
            errorxabs = [abs(item - centroidx) for item in xlines]
            idxx = errorxabs.index(min(errorxabs))
            idxy = erroryabs.index(min(erroryabs))
            errorx = [item - centroidx for item in xlines][idxx]
            errory = [item - centroidy for item in ylines][idxy]
            sx,sy = search.findcurrentpos(centroidx, centroidy)
            print(sx,sy)
            ex,ey = search.findstartend(grid,"G",sx,sy)
            orientationrob = search.findcontorientation4(pos[0][0],pos[1][0], pos[0][1],pos[1][1])
            desorientation = search.findcontorientation(errorx, errory)
            print(orientationrob)
            print(desorientation)
            if nummsg % 50 != 0:
                pass
                client1.publish("eternals", str([str(errorx),str(errory),orientationrob, desorientation]),qos=0)
            path = None
            if nummsg % 50 == 0 and type(path) is not None:
                print(nummsg)
                sx,sy = search.findcurrentpos(centroidx, centroidy)
                print(sx,sy,ex,ey)
                print(grid)
                path = search.UCS(sx,sy,grid,"G",ex,ey)
                print(path)
                orientation = search.findorientation(pos[0][0],pos[1][0], pos[0][1],pos[1][1])
                print(orientation)
                motorcommands = search.generatemotorcommands(path, orientation)
                #motorcommands.append(errorx)
                #motorcommands.append(errory)
                print(motorcommands)
                # client1.publish("eternals", str(motorcommands))
                grid = search.updategrid(grid, centroidx, centroidy)
                ex,ey = search.findstartend(grid,"G", sx,sy)
            nummsg += 1 


def on_message_start(client, userdata, message):
    msg = message.payload
    # print(msg)  
def on_message_config(client, userdata, message):
    msg = message.payload
    # print(msg)  
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


            

            


