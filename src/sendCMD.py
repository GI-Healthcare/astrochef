#!/usr/bin/env python3

import rospy
import os
import json
import xml.etree.ElementTree as ET
from std_msgs.msg import String, Float32
import getpass
import serial
import time

BASE_PATH = f"/home/{getpass.getuser()}/catkin_ws/src/astrochef"
DB_PATH = os.path.join(BASE_PATH, "UserInterface/database/AstroChefDB.db")
RECIPE_PATH = os.path.join(BASE_PATH, "UserInterface/database/Recipes/")
WASHING_PATH = os.path.join(BASE_PATH, "config/washingProcess.xml")
SHUTDOWN_PATH = os.path.join(BASE_PATH, "config/shutdownProcess.xml")

stepperPicoDevices = ["gantryStepper", "potStepper", "spiceDelivery", "bigDelivery", "extractionFan", 
                      "oilPump", "waterPump", "washWaterPump", "induction", "deviceLED", "waitTime", "stirring", "door"]
relayDevices = []

# Serial configurations
SERIAL_PORT = "/dev/ttyACM0"  # Modify this to your actual port
BAUDRATE = 9600

ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=3000)
ser.flush()

def wait_for_time(duration):
    """Waits for the specified duration in seconds."""
    try:
        delay = float(duration)
        time.sleep(delay)
    except ValueError:
        rospy.logerr(f"Invalid wait time: {duration}")

def sendDataOverSerial(device, data):
    message = str(device)+":"+str(data)+"\n"
    # message = f"{device}::{data}\n"
    rospy.loginfo(message)
    ser.write(message.encode('utf-8'))
    line = ser.readline().decode('utf-8').rstrip()
    rospy.loginfo(f"Received: {line}")
    return line

def cancelCooking():
    pass

def callback(msg):
    state = msg.data

    if state == "start":
        executionState = False
        rospy.loginfo("Starting cooking process")

    elif state == "abort":
        executionState = True
        rospy.loginfo("Cancelling cooking process. Resetting")
        cancelCooking()

    elif state[0].isdigit():
        handle_digit_state(state)

    else:
        rospy.logerr("Unable to start cooking process")

def handle_digit_state(state):
    rospy.loginfo("Retrieving cooking details")
    foodID = state.split("_")[0]
    fn = [filename for filename in os.listdir(RECIPE_PATH) if filename.startswith(foodID)]
    filePath = os.path.join(RECIPE_PATH, fn[0])

    try:
        tree = ET.parse(filePath)
        root = tree.getroot()
        rospy.loginfo("Starting to execute recipe steps")
        for r in root.findall("recipe"):
            noOfSteps = len(r)
            progressSteps = 1 / noOfSteps
            progressVar = 0
            for steps in r:
                device_id = steps.attrib["id"]
                if device_id == "waitTime":
                    wait_for_time(steps.attrib["value"])
                if device_id in relayDevices:
                    error_msg = "Unable to send command to Relay Device"
                elif device_id in stepperPicoDevices:
                    # rospy.logwarn("Sending by adip: "+str(device_id))
                    error_msg = "Unable to send command to Stepper Pico Device"
                else:
                    continue

                response = sendDataOverSerial(device_id, steps.attrib["value"])
                rospy.logwarn(response)
                progressVar += progressSteps
                progressPub.publish(progressVar)
                if response != "success":  # You can modify this based on your expected response
                    rospy.logerr(error_msg)
                    break

                if state == "abort":
                    rospy.loginfo("Cancelling cooking process. Resetting")
                    cancelCooking()
                    break

    except ET.ParseError:
        rospy.logerr(f"Recipe xml incorrect formatting or value: {filePath}")
    except FileNotFoundError:
        rospy.logerr(f"Unable to open recipe file {filePath}")

if __name__ == '__main__':
    try:
        rospy.init_node('SendCommand')
        rospy.Subscriber('ui_cmd', String, callback)
        pub = rospy.Publisher('sendPico', String, queue_size=1)
        progressPub = rospy.Publisher('progress', Float32, queue_size=1)
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
    finally:
        ser.close()