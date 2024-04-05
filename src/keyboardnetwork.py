import paho.mqtt.client as mqtt

broker_adress = "192.168.1.104"

client = mqtt.Client("P1")

client.connect(broker_adress)

client.publish("eternals","selamlar", qos=0)