from pynput.keyboard import Key, Listener
import paho.mqtt.client as mqtt


broker_adress = "192.168.1.104"

client = mqtt.Client("P1")

client.connect(broker_adress)

prev = ''
def on_press(key):
    global prev
    var = key
    if var.char == 'w' and prev != 'w':
        client.publish("eternals","FC")
        print('F')
    if var.char == 's' and prev != 's':
        client.publish("eternals","BC")
        print('B')
    if var.char == 'd' and prev != 'd':
        client.publish("eternals","CWC")
        print('CW')
    if var.char == 'a' and prev != 'a':
        client.publish("eternals","CCWC")
        print('CCW')
    if var.char == 'q' and prev != 'q':
        print('S')
        client.publish("eternals","SC")
    prev = var.char
def on_release(key):
    global prev
    client.publish("eternals", "S", qos=0)
    prev = ''
    if key == Key.esc:
        return False

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
