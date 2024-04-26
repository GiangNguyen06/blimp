from paho.mqtt import client as mqtt_client
import pygame
import random
import json

broker = 'localhost'
port = 1883
topic = "servo"
client_id = f'python-mqtt-{random.randint(0, 1000)}'



def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker")
        else:
            print("Failed to connect to return code %d\n", rc)
    client = mqtt_client.Client(client_id)
    
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def ensure_mqtt_client(client):
    if client is None or not client.is_connected():
        client = connect_mqtt()
        client.loop_start()
        print("MQTT client connected")
    return client


def publish(client, message):
    msg = json.dumps(message)
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print(f"Sent '{msg}' to '{topic}'")
def run():
    client = None
    
    pygame.init()
    pygame.joystick.init()
    joystick_count = pygame.joystick.get_count()
    
    new_angle = 0
    current_angle = 0
    
    if joystick_count == 0:
        print("No joysticks found.")
        return
    
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    client = ensure_mqtt_client(client)
    while True:
        for event in pygame.event.get():
            
            
                if event.type == pygame.JOYAXISMOTION:
                    
                    if event.axis == 5:
                        axis = joystick.get_axis(5)
                        throttle = (axis + 1) * 100
                        print(f"Throttle {5} value: {axis:> 6.3f}")
                        throttle = round(throttle)
                        message = {"motor_speed": throttle}
                        publish(client, message)
                     
                    elif event.axis == 4:
                         axis = joystick.get_axis(4)
                         reverse = (axis + 1) * (-100)
                         reverse = round(reverse)
                         print(f"Reverse {4} value: {axis:> 6.3f}")
                         message = {"motor_speed": reverse}
                         publish(client, message)   
                          
                             
                elif event.type == pygame.JOYBUTTONDOWN:
                    
                    if event.button == 10:  # Adjust button index as needed
                            message = {"message" :"You got scammed LOL!"}
                            publish(client, message)
                            if joystick.rumble(0, 1, 500):
                                print("Rum-rum")
                    
                    elif event.button == 3:
                            print("Going backward!")
                            message = {"direction" : 40}
                            publish(client, message)
                            
                    elif event.button == 0:
                            print("Going forward!")
                            message = {"direction" : 90}
                            publish(client, message)
                            
                    elif event.button == 1:
                            print("Going up!")
                            message = {"direction" : 70}
                            publish(client, message)
                            
                    elif event.button == 2:
                            print("Going down!")
                            message = {"direction" : 20}
                            publish(client, message)
                            
                    elif event.button == 11:
                            new_angle = current_angle + 10
                            if new_angle > 360:
                                    new_angle -= 20
                            print(f"Up {new_angle} value: {new_angle:>6.3f}")
                            message = {"absolute_angle": new_angle}
                            publish(client, message)
                            current_angle = new_angle
                            
                    elif event.button == 12:
                            new_angle = current_angle - 10
                            if new_angle < 0:
                                    new_angle += 20
                            print(f"Down {new_angle} value: {new_angle:>6.3f}")
                            message = {"absolute_angle": new_angle}
                            publish(client, message)  
                            current_angle = new_angle
                            
                            
                    elif event.button == 14:
                            print("Turning right!")
                            message = {"rear_motor" : 70}
                            publish(client, message)
                            
                    elif event.button == 13:
                            print("Turning left!")
                            message = {"rear_motor" : 110}
                            publish(client, message)
                            
                    
                    
                elif event.type == pygame.JOYBUTTONUP:
                    if event.button == 14 or event.button == 13:
                        message = {"rear_motor" : 90}
                        publish(client, message)
                     
                            
                            
                            
                            
    # Limit the loop to run at a reasonable rate
    pygame.time.wait(100)
if __name__ == '__main__':
    run()
