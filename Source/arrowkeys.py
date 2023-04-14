import curses
import paho.mqtt.client as mqtt

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

broker_adress = "192.168.1.104"

client = mqtt.Client("P1")

client.connect(broker_adress)



try:
    while True:
        char = screen.getch()
        if char == ord('x'): 
            break
        elif char == ord("q"):
            client.publish("eternals", "S", qos=0)
            screen.addstr(0, 0, 'stop')
        elif char == ord("d"):
            client.publish("eternals", "CW",qos=0)
            screen.addstr(0, 0, 'clockwise ')        
        elif char == ord("w"):
            client.publish("eternals", "F", qos=0) 
            screen.addstr(0, 0, 'up   ')
        elif char == ord("s"):
            client.publish("eternals", "B",qos=0)
            screen.addstr(0, 0, 'down')
        elif char == ord("a"):
            client.publish("eternals", "CCW",qos=0)
            screen.addstr(0, 0, 'counterclockwise ')  
        
finally:
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()