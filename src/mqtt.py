import network
import time
from machine import Pin, PWM
from umqtt.simple import MQTTClient

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("POCO X3 Pro","123456789")
time.sleep(5)
print(wlan.isconnected())

LED = Pin(5, Pin.OUT, value = 0)
pwmLED = PWM(LED)
motor1a = Pin(19, Pin.OUT)
motor1b = Pin(20, Pin.OUT)
pwm1a = PWM(motor1a)
pwm1b = PWM(motor1b)

mqtt_server = 'broker.mqttdashboard.com'
client_id = 'bigles'
topic_sub = b'eternals'

start = 0
rot = 0
duty = 0
freq = 100

def sub_cb(topic, msg):
    global start
    global rot
    global duty
    global freq
    print("New message on topic {}".format(topic.decode('utf-8')))
    msg = msg.decode('utf-8')
    print(msg)
    print(type(msg))
    func = int(msg[0])
    msg = msg[1:]
    print(msg)
    print(func)
    if func == 1:
        start = int(msg)
    if func == 2:
        rot = int(msg)
    if func == 3:
        duty = int(msg)
    if func == 4:
        freq = int(msg)
    print("start = " , start)
    print("rotation = ", rot)
    print("duty =" , duty)
    print("freq = " , freq)
    if freq != 0:
        if start == 1:
            if rot == 1:
                pwm1a.duty_u16(duty)
                pwm1a.freq(freq)
                pwm1b.duty_u16(0)
            if rot == 0:
                pwm1b.duty_u16(duty)
                pwm1b.freq(freq)
                pwm1a.duty_u16(0)
        elif start == 0:
            pwm1b.duty_u16(0)
            pwm1a.duty_u16(0)

    
    
    

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