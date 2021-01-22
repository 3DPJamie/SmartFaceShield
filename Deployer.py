import jetson.inference
import jetson.utils
import sys
import time
import Adafruit_PCA9685
import numpy as np 

servo = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)
servo.set_pwm_freq(50)

# Config Servo input
ServoL = 0
ServoR = 1

#Servo Min-Max values
servoL_min = 150
servoL_max = 500

servoR_min = 100
servoR_max = 420

#Angle functions for servos
def _map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min)*(out_max-out_min) / (in_max - in_min) + out_min)

def _angle_servoL(x):
    return int(_map(x, 0, 180, servoL_min, servoL_max))

def _angle_servoR(x):
    return int(_map(x, 180, 0, servoR_min, servoR_max))

#initiate servo positions to open face-shield
servoL_pwm = _angle_servoL(0)
servo.set_pwm(ServoL, 0, servoL_pwm)
servoR_pwm = _angle_servoR(0)
servo.set_pwm(ServoR, 0, servoR_pwm)

#detectNet
net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.8)

#create a camera stream
camera=jetson.utils.videoSource("csi://0", argv=sys.argv)

#display window
display = jetson.utils.videoOutput()

while True:
    img = camera.Capture()
    detections = net.Detect(img)
    display.Render(img)

	#overlay the performance
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS())) 

    for detect in detections:

        ID=detect.ClassID
        item=net.GetClassDesc(ID)
            
        if item=="person" and detect.Area >= 250000:
            servoL_pwm = _angle_servoL(90)
            servo.set_pwm(ServoL, 0, servoL_pwm)
            servoR_pwm = _angle_servoR(90)
            servo.set_pwm(ServoR, 0, servoR_pwm)
        elif item!="person":
            servoL_pwm = _angle_servoL(0)
            servo.set_pwm(ServoL, 0, servoL_pwm)
            servoR_pwm = _angle_servoR(0)
            servo.set_pwm(ServoR, 0, servoR_pwm)
        else:
            servoL_pwm = _angle_servoL(0)
            servo.set_pwm(ServoL, 0, servoL_pwm)
            servoR_pwm = _angle_servoR(0)
            servo.set_pwm(ServoR, 0, servoR_pwm)                        
		
 #flip CSI camera with following code python3 Deployer.py --input-flip=rotate-180 csi://0
