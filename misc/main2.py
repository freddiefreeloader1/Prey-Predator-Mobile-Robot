from time import sleep
import IMAGE
import paho.mqtt.client as mqttClient
import time
import matplotlib.pyplot as plt
import io
from PIL import Image
import cv2
import search
import random

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
global flag
global pos
global firstgrid
global motorcommands
SSG = "STOP"
global contorientation
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
    global firstgrid
    firstgrid = []
    binaryimage = message.payload
    var = io.BytesIO(binaryimage)
    var = Image.open(var)
    var.show()
    var = var.save("map6.jpg")
    var = cv2.imread(var)
    grid = IMAGE.img_processing("map6.jpg")
    for item in grid:
        firstgrid.append(item)
    blue, green, orange = search.generatelist(grid)


totalpoint = 0
lastx = 0
lasty = 0
contorientation = 0
flag = 1
role = "PREY"

def on_message_stats(client, userdata, message):
    global nummsg
    global grid
    global orientation
    global path
    global blue, green, orange
    global lastx, lasty
    global role
    global totalpoint
    global contorientation
    global flag
    global pos
    global firstgrid
    global motorcommands
    msg = message.payload
    msg = eval(msg)
    orientation = 0
    

    #print(SSG)
    if type(msg) is dict or type(msg) is list:
        ID = 13
        if SSG == "START" or SSG == "GO":
            for item in msg:
                if type(item) is not int:
                    if item["ID"] == 13:
                        pos = item["POS"]
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
                        if sx < 43.5 or sx > 576 or sy < 46.5 or sy > 429:
                            client1.publish("eternals", "S", qos=0)
                        blue, green, orange = search.generatelist(firstgrid)
                        ex,ey = search.findstartend(grid,"B",sx,sy,blue)
                        orientation = search.findorientation(pos[0][0],pos[1][0], pos[0][1],pos[1][1])
                        contorientation = search.findcontorientation4(pos[0][0],pos[1][0], pos[0][1],pos[1][1])
                        blue, green, orange = search.generatelist(firstgrid)
                        grid = search.updategrid(grid,centroidx,centroidy,blue)
                        blue, green, orange = search.generatelist(firstgrid)

                        if lastx != sx and lasty != sy:
                            if role == "PREDATOR":
                                if (sx,sy) in blue:
                                    totalpoint += predb
                                elif (sx,sy) in orange:
                                    totalpoint += predy
                                elif (sx,sy) in green:
                                    role = "PREY"
                            elif role == "PREY":
                                if (sx,sy) in blue:
                                    totalpoint += preyb
                                elif (sx,sy) in orange:
                                    totalpoint += preyy
                                elif (sx,sy) in green:
                                    role = "PREDATOR"
                        robotsay = [ID, role, totalpoint, (sx,sy)]
                        # print(robotsay)
                        client.publish("robotsay", str(robotsay),qos = 0)
                        lastx,lasty = sx,sy
                        path = search.UCS(sx,sy,grid,"B",ex,ey)
                        if type(path) == type(None):
                            grid = []
                            for item in firstgrid:
                                grid.append(item)
                            print(grid)
                            grid = search.updategrid(grid,centroidx,centroidy,blue)
                            path = search.UCS(sx,sy,grid,"B",ex,ey)
                        if nummsg % 50 == 0 and type(path) is not None and role == "PREDATOR":
                            print(nummsg)
                            sx,sy = search.findcurrentpos(centroidx, centroidy)
                            print(sx,sy,ex,ey)
                            print(grid)
                            ex = random.randint(1,7)
                            ey = random.randint(1,5)
                            path = search.UCS(sx,sy,grid,"B",ex,ey)
                            if type(path) == type(None):
                                grid = []
                                for item in firstgrid:
                                    grid.append(item)
                                print(grid)
                                grid = search.updategrid(grid,centroidx,centroidy,blue)
                                path = search.UCS(sx,sy,grid,"B",ex,ey)
                            print(path)
                            orientation = search.findorientation(pos[0][0],pos[1][0], pos[0][1],pos[1][1])
                            print(orientation)
                            motorcommands = search.generatemotorcommands(path, orientation)
                            #motorcommands.append(errorx)
                            #motorcommands.append(errory)
                            print(motorcommands)
                            client1.publish("eternals", str(motorcommands))
                            blue, green, orange = search.generatelist(firstgrid)
                            grid = search.updategrid(grid, centroidx, centroidy,blue)
                            blue, green, orange = search.generatelist(firstgrid)
                            print(grid)
                            ex = random.randint(1,7)
                            ey = random.randint(1,5)
                        if nummsg % 50 == 0 and type(path) is not None and role == "PREY":
                            print(nummsg)
                            sx,sy = search.findcurrentpos(centroidx, centroidy)
                            blue, green, orange = search.generatelist(firstgrid)
                            ex,ey = search.findstartend(grid,"B", sx,sy, blue)
                            blue, green, orange = search.generatelist(firstgrid)
                            print(sx,sy,ex,ey)
                            print(grid)
                            path = search.UCS(sx,sy,grid,"B",ex,ey)
                            if type(path) == type(None):
                                grid = []
                                for item in firstgrid:
                                    grid.append(item)
                                grid = search.updategrid(grid,centroidx,centroidy,blue)
                                path = search.UCS(sx,sy,grid,"B",ex,ey)
                            print(path)
                            orientation = search.findorientation(pos[0][0],pos[1][0], pos[0][1],pos[1][1])
                            print(orientation)
                            motorcommands = search.generatemotorcommands(path, orientation)
                            client1.publish("eternals", str(motorcommands))
                            #motorcommands.append(errorx)
                            #motorcommands.append(errory)
                            print(motorcommands)
                            blue, green, orange = search.generatelist(firstgrid)
                            grid = search.updategrid(grid, centroidx, centroidy, blue)
                            print(grid)
                            blue, green, orange = search.generatelist(firstgrid)
                            ex,ey = search.findstartend(grid,"B", sx,sy, blue)
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


            

            


