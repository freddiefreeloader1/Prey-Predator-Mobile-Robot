from machine import Pin, PWM
import time
import network
from umqtt.simple import MQTTClient

mqtt_server = '192.168.1.104'
client_id = 'bigles'
topic_sub = b'eternals'

motor1a = Pin(1, Pin.OUT)
motor1b = Pin(2, Pin.OUT)
motor2a = Pin(6, Pin.OUT)
motor2b = Pin(5, Pin.OUT)

pwm1a = PWM(motor1a)
pwm1b = PWM(motor1b)    
pwm2a = PWM(motor2a)
pwm2b = PWM(motor2b)      

def forward():
    pwm1a.duty_u16(45000)
    pwm1a.freq(50)
    pwm1b.duty_u16(0)

    pwm2a.duty_u16(36500)
    pwm2a.freq(50)
    pwm2b.duty_u16(0)
        
    time.sleep(0.29)

    pwm1a.duty_u16(0)
    pwm1a.freq(50)
    pwm1b.duty_u16(0)

    pwm2a.duty_u16(0)
    pwm2a.freq(50)
    pwm2b.duty_u16(0)
def halfforward():
    pwm1a.duty_u16(45000)
    pwm1a.freq(50)
    pwm1b.duty_u16(0)

    pwm2a.duty_u16(36500)
    pwm2a.freq(50)
    pwm2b.duty_u16(0)
        
    time.sleep(0.14)

    pwm1a.duty_u16(0)
    pwm1a.freq(50)
    pwm1b.duty_u16(0)

    pwm2a.duty_u16(0)
    pwm2a.freq(50)
    pwm2b.duty_u16(0)

def backwards():
    pwm1a.duty_u16(0)
    pwm1a.freq(50)
    pwm1b.duty_u16(50000)

    pwm2a.duty_u16(0)
    pwm2a.freq(50)
    pwm2b.duty_u16(45000)
        
    time.sleep(0.5)

    pwm1a.duty_u16(0)
    pwm1a.freq(50)
    pwm1b.duty_u16(0)

    pwm2a.duty_u16(0)
    pwm2a.freq(50)
    pwm2b.duty_u16(0)
    
def halfbackwards():
    pwm1a.duty_u16(0)
    pwm1a.freq(50)
    pwm1b.duty_u16(50000)

    pwm2a.duty_u16(0)
    pwm2a.freq(50)
    pwm2b.duty_u16(45000)
        
    time.sleep(0.25)

    pwm1a.duty_u16(0)
    pwm1a.freq(50)
    pwm1b.duty_u16(0)

    pwm2a.duty_u16(0)
    pwm2a.freq(50)
    pwm2b.duty_u16(0)
def rightforward():
    pwm1a.duty_u16(20000)
    pwm1a.freq(50)
    pwm1b.duty_u16(0)

    time.sleep(0.63)

    pwm1a.duty_u16(0)
    pwm1a.freq(50)
    pwm1b.duty_u16(0)

    pwm2a.duty_u16(0)
    pwm2a.freq(50)
    pwm2b.duty_u16(0)

def leftforward():
    
    pwm2a.duty_u16(20000)
    pwm2a.freq(50)
    pwm2b.duty_u16(0)

    time.sleep(0.55)

    pwm2a.duty_u16(0)
    pwm2a.freq(50)
    pwm2b.duty_u16(0)

    pwm1a.duty_u16(0)
    pwm1a.freq(50)
    pwm1b.duty_u16(0)
    
def leftbackward():
    
    pwm2a.duty_u16(0)
    pwm2a.freq(50)
    pwm2b.duty_u16(40000)

    time.sleep(0.70)

    pwm2a.duty_u16(0)
    pwm2a.freq(50)
    pwm2b.duty_u16(0)

    pwm1a.duty_u16(0)
    pwm1a.freq(50)
    pwm1b.duty_u16(0)

def rightbackward():
    
    pwm1a.duty_u16(0)
    pwm1a.freq(50)
    pwm1b.duty_u16(40000)

    time.sleep(0.70)

    pwm1a.duty_u16(0)
    pwm1a.freq(50)
    pwm1b.duty_u16(0)

    pwm1a.duty_u16(0)
    pwm1a.freq(50)
    pwm1b.duty_u16(0)


def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("mechalab_intra", "mechastudent")
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip
try:
    ip = connect()
except KeyboardInterrupt:
    machine.reset()

def drivemotors(motorcommands):
    for command in motorcommands:
        if command == "F":
            print("forward")
            forward()
        if command == "B":
            print("backward")
            backwards()
        if command == "HF":
            print("hf")
            halfforward()
        if command == "HB":
            print("hb")
            halfbackwards()
        if command == "RF":
            print("rf")
            rightforward()
        if command == "LF":
            print("lf")
            leftforward()
        if command == "RB":
            rightbackward()
        if command == "LB":
            leftbackward()
            
def sub_cb(topic, msg):
    print("New message on topic {}".format(topic.decode('utf-8')))
    msg = msg.decode('utf-8')
    print(type(msg))
    command = msg
    if type(command) is str:
        if command == "F":
            print("forward")
            forward()
        if command == "B":
            print("backward")
            backwards()
        if command == "HF":
            print("hf")
            halfforward()
        if command == "HB":
            print("hb")
            halfbackwards()
        if command == "RF":
            print("rf")
            rightforward()
        if command == "LF":
            print("lf")
            leftforward()
        if command == "RB":
            rightbackward()
        if command == "LB":
            leftbackward()
            
    '''else:
        motorcommands = eval(msg)
        drivemotors(motorcommands)'''
    
    

def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, keepalive=60)
    client.set_callback(sub_cb)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
    print('Failed to connect to MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()
    
try:
    client = mqtt_connect()
except OSError as e:
    reconnect()
while True:
    client.subscribe(topic_sub)
    time.sleep(1)

        


path = [(6, 0), (5, 0), (4, 0), (3, 0), (3, 1), (3, 2), (2, 2), (2, 3), (2, 4), (2, 5)]



            
