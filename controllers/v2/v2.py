# Import necessary libraries
from controller import Robot
import paho.mqtt.client as paho
import json

# Create the Robot instance.
robot = Robot()

# Set the time step and the number of sensors.
TIME_STEP = int(robot.getBasicTimeStep())
NUM_SENSORS = 8

# Define the broker and port for the MQTT client.
BROKER = "localhost"
PORT = 1880

# Initialize the left and right motors of the robot.
def initMotor():
    leftMotor = robot.getDevice("left wheel motor")
    rightMotor = robot.getDevice("right wheel motor")

    leftMotor.setPosition(float("inf"))
    rightMotor.setPosition(float("inf"))
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)

    return leftMotor, rightMotor

# Initialize the distance sensors using the Braitenberg algorithm.
def initBraitengerg():
    sensors = []
    for i in range(NUM_SENSORS):
        sensor = robot.getDevice(f"ds{i}")
        sensor.enable(TIME_STEP)
        sensors.append(sensor)

    return sensors

# Initialize the light sensors.
def initLight():
    sensors = []
    for i in range(NUM_SENSORS):
        sensor = robot.getDevice(f"ls{i}")
        sensor.enable(TIME_STEP)
        sensors.append(sensor)
    return sensors

# Initialize the MQTT client.
def initMQTT():
    client = paho.Client()  # create client object
    client.connect(BROKER, PORT)  # establish connection
    client.subscribe("move", qos=0)
    client.on_message = on_message
    return client

# Move the robot based on the values in the "speed" list.
def move():
    leftMotor.setVelocity(speed[0])
    rightMotor.setVelocity(speed[1])

# Publish the current values of the robot's sensors.
def publish_sensors():
    dist = [x.getValue() for x in dist_sensors]
    light = [x.getValue() for
