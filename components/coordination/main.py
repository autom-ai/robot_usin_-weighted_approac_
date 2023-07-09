import paho.mqtt.client as mqtt
import json

# Determine the correct speed for each motor based on the results of the other algorithms
def coordination(dist, light):
    if dist == [MAX_SPEED, MAX_SPEED]:
        weights = [0.5, 0.5]
    else:
        weights = [1, 0]

    return [x * weights[0] + y * weights[1] for x, y in zip(dist, light)]


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    client.subscribe("sensors", qos=0)
    for i in SERVICES:
        client.subscribe(f"res/{i}", qos=0)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global speed, speeds
    if b"nan" in msg.payload:
        return
    arr_msg = json.loads(msg.payload)
    if msg.topic == "sensors":
        client.publish("algo/light", str(arr_msg[0]))
        client.publish("algo/dist", str(arr_msg[1]))
        client.publish("move", str(speed))
    elif "res/" in msg.topic:
        speeds[msg.topic] = json.loads(msg.payload)
        speed = coordination(speeds["res/dist"], speeds["res/light"])


def initMQTT():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("localhost", 1880, 60)

    client.loop_forever()


if __name__ == "__main__":
    MAX_SPEED = 10
    SERVICES = ["light", "dist"]

    speed = [0, 0]
    speeds = {"res/light": [0, 0], "res/dist": [0, 0]}

    client = initMQTT()
