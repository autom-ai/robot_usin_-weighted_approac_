from controller import Robot

# create the Robot instance.
robot = Robot()

TIME_STEP = int(robot.getBasicTimeStep())
MAX_SPEED = 10
SPEED_UNIT = 0.00053429
NUM_SENSORS = 8
DISTANCE_RANGE = 2000
LIGHT_DETECTION_THRESHOLD = 700

DIST_MATRIX = [
    [-5000, -5000],
    [-20000, 40000],
    [-30000, 50000],
    [-70000, 70000],
    [70000, -60000],
    [50000, -40000],
    [40000, -20000],
    [-5000, -5000],
    [-10000, -10000],
]

LIGHT_MATRIX = [
    [-1, 1],
    [-0.5, 0.5],
    [1, 1],
    [1, 1],
    [0.5, -0.5],
    [1, -1],
    [-1, 1],
    [1, -1],
]


def bound(x, a, b):
    return a if x < a else (b if x > b else x)


# Init wheel motors
def initMotor():
    leftMotor = robot.getDevice("left wheel motor")
    rightMotor = robot.getDevice("right wheel motor")

    leftMotor.setPosition(float("inf"))
    rightMotor.setPosition(float("inf"))
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)

    return leftMotor, rightMotor


# Init distance sensors
def initDistance():
    sensors = []
    for i in range(NUM_SENSORS):
        sensor = robot.getDevice(f"ds{i}")
        sensor.enable(TIME_STEP)
        sensors.append(sensor)

    return sensors


# Init light sensors
def initLight():
    sensors = []
    for i in range(NUM_SENSORS):
        sensor = robot.getDevice(f"ls{i}")
        sensor.enable(TIME_STEP)
        sensors.append(sensor)
    return sensors


leftMotor, rightMotor = initMotor()
light_sensors = initLight()
distance_sensors = initDistance()


# Wall avoidance algorithm
def braitengerg():
    speed = [0, 0]
    sensors_values = [x.getValue() for x in distance_sensors]

    for i in range(2):
        for j in range(NUM_SENSORS):
            speed[i] += SPEED_UNIT * DIST_MATRIX[j][i] * (1.0 - (sensors_values[j] / DISTANCE_RANGE))
        speed[i] = bound(speed[i], -MAX_SPEED, MAX_SPEED)

    return speed


# Returns the max light detected and the index of the corresponding sensor.
def get_light_infos():
    max_light = 0
    max_index = 0
    for i in range(len(light_sensors)):
        value = light_sensors[i].getValue()
        if value > max_light:
            max_light = value
            max_index = i
    return (max_light, max_index)


# Light following detection algorithm
def follow_light():
    max_light, max_index = get_light_infos()

    if max_light < LIGHT_DETECTION_THRESHOLD:
        return [0, 0]

    return [x * MAX_SPEED for x in LIGHT_MATRIX[max_index]]


while robot.step(TIME_STEP) != -1:
    dist = braitengerg()
    light = follow_light()
    if dist == [MAX_SPEED, MAX_SPEED]:
        weights = [0.5, 0.5]
    else:
        weights = [1, 0]

    speed = [x * weights[0] + y * weights[1] for x, y in zip(dist, light)]

    leftMotor.setVelocity(speed[0])
    rightMotor.setVelocity(speed[1])
