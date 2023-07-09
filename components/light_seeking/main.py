import paho.mqtt.client as mqtt
import json


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    client.subscribe("algo/light", qos=2)


def on_message(client, userdata, msg):
    light_sensors = json.loads(msg.payload)
    client.publish("res/light", str(follow_light(light_sensors)))


# Returns the max light detected and the index of the corresponding sensor.
def get_light_infos(light_sensors):
    max_light = 0
    max_index = 0
    for i in range(len(light_sensors)):
        value = light_sensors[i]
        if value > max_light:
            max_light = value
            max_index = i
    return (max_light, max_index)


# Light following detection algorithm
def follow_light(light_sensors):
    max_light, max_index = get_light_infos(light_sensors)

    if max_light < LIGHT_DETECTION_THRESHOLD:
        return [0, 0]

    return MATRIX[max_index]


def initMQTT():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1880, 60)

    client.loop_forever()

    return client


if __name__ == "__main__":
    LIGHT_DETECTION_THRESHOLD = 700
    MAX_SPEED = 10

    MATRIX = [
        [-MAX_SPEED, MAX_SPEED],
        [-MAX_SPEED / 2, MAX_SPEED / 2],
        [MAX_SPEED, MAX_SPEED],
        [MAX_SPEED, MAX_SPEED],
        [MAX_SPEED / 2, -MAX_SPEED / 2],
        [MAX_SPEED, -MAX_SPEED],
        [-MAX_SPEED, MAX_SPEED],
        [MAX_SPEED, -MAX_SPEED],
    ]

    client = initMQTT()
