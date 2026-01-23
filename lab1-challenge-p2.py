#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain = Brain()

# Robot configuration code
left_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
right_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
top_motor = Motor(Ports.PORT7, GearSetting.RATIO_18_1, True)

controller_1 = Controller(PRIMARY)

bumper_g = Bumper(brain.three_wire_port.g)
range_finder_front = Sonar(brain.three_wire_port.e)
lightSensor = Line(brain.three_wire_port.b)

# wait for rotation sensor to fully initialize
wait(30, MSEC)

# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = (
        brain.battery.voltage(MV)
        + brain.battery.current(CurrentUnits.AMP) * 100
        + brain.timer.system_high_res()
    )
    urandom.seed(int(random))

# Set random seed
initializeRandomSeed()

def play_vexcode_sound(sound_name):
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# Clear console
wait(200, MSEC)
print("\033[2J")

#endregion VEXcode Generated Robot Configuration


# ------------------------------------------
# Project:      VEXcode Project
# Author:       VEX
# Description:  VEXcode V5 Python Project
# ------------------------------------------


# ======================
# State Definitions
# ======================
IDLE = 0
DRIVING_FWD = 1
DRIVING_BKWD = 2

current_state = IDLE


# ======================
# Constants
# ======================
PI = 3.142
wheelDiameterCM = 4.25 * 2.54
wheelRadiusCM = wheelDiameterCM / 2
wheelCircumferenceCM = PI * wheelDiameterCM

gearRatio = 5
wheelTrack = 11 * 2.54
degreesPerCM = 360 / wheelCircumferenceCM


# ======================
# Motion Functions
# ======================
def driveStraightCM(direction, distanceInCM, speed_CM_per_sec):
    rpm = speed_CM_per_sec / wheelRadiusCM * 60 * gearRatio / (2 * PI)
    degrees = distanceInCM * gearRatio * degreesPerCM

    left_motor.spin_for(direction, degrees, DEGREES, rpm, RPM, False)
    right_motor.spin_for(direction, degrees, DEGREES, rpm, RPM, False)


def drive_for(direction, turns, speed):
    left_motor.set_velocity(speed, RPM)
    left_motor.spin_for(direction, turns, TURNS, wait=False)

    right_motor.set_velocity(speed, RPM)
    right_motor.spin_for(direction, turns, TURNS, wait=False)



def driveStraightWait(direction, distanceInCM, speed_CM_per_sec):
    rpm = speed_CM_per_sec / wheelRadiusCM * 60 * gearRatio / (2 * PI)
    degrees = distanceInCM * gearRatio * degreesPerCM

    left_motor.spin_for(direction, degrees, DEGREES, rpm, RPM, False)
    right_motor.spin_for(direction, degrees, DEGREES, rpm, RPM, True)


# ======================
# Event Handlers
# ======================
def handleLeft1Button():
    global current_state
    print("Left 1 Button Pressed")

    if current_state == IDLE:
        print("IDLE -> FORWARD")
        current_state = DRIVING_FWD
        driveStraightCM(FORWARD, 100, 10)
    else:
        print("-> IDLE")
        current_state = IDLE
        left_motor.stop()
        right_motor.stop()


def handleBumperG():
    global current_state
    print("Bumper Pressed")

    if current_state == DRIVING_FWD:
        print("FORWARD -> BACKWARD")
        current_state = DRIVING_BKWD

        position = left_motor.position(TURNS)
        speed = 10 / wheelRadiusCM * 60 * gearRatio / (2 * PI)
        drive_for(REVERSE, position, speed)


# ======================
# Sensor Checkers
# ======================
def checkLight():
    return lightSensor.reflectivity(PERCENT) > 6


def handleLight():
    global current_state
    speed_CM_per_sec = 10;
    rpm = speed_CM_per_sec / wheelRadiusCM * 60 * gearRatio / (2 * PI)

    if current_state == DRIVING_FWD:
        print(
            "FORWARD -> BACKWARD, light sensor at %d"
            % lightSensor.reflectivity(PERCENT)
        )
        current_state = IDLE
        left_motor.stop()
        right_motor.stop()
        driveStraightWait(REVERSE, 15, 5)
        top_motor.spin_to_position(150, DEGREES, rpm/2, RPM)
        driveStraightWait(FORWARD, 15, 5)
        top_motor.spin_to_position(0, DEGREES, rpm/2, RPM)
        print("Torque: %.3f" % top_motor.torque())
        top_motor.torque()

wasMoving = False

def checkMotionComplete():
    global wasMoving

    isMoving = left_motor.is_spinning() or right_motor.is_spinning()
    finished = wasMoving and not isMoving
    wasMoving = isMoving

    return finished


def handleMotionComplete():
    global current_state

    if current_state == DRIVING_FWD:
        print("FORWARD -> BACKWARD")
        current_state = DRIVING_BKWD
        driveStraightCM(REVERSE, 100, 10)

    elif current_state == DRIVING_BKWD:
        print("BACKWARD -> IDLE")
        current_state = IDLE

    else:
        print("E-stop")


# ======================
# Event Registration
# ======================
controller_1.buttonL1.pressed(handleLeft1Button)
bumper_g.pressed(handleBumperG)


# ======================
# Main Loop
# ======================
top_motor.set_position(0, DEGREES)
while True:
    if checkMotionComplete():
        handleMotionComplete()

    if checkLight():
        handleLight()

    #print("Distance:", range_finder_front.distance(MM))
    wait(10)
