#!/usr/bin/python3

from gpiozero import *
from time import *
import RPi.GPIO as GPIO
import numpy as np

GPIO.setmode(GPIO.BCM)

servoPin1=26 # define servo GPIO pin
servoPin2=19
GPIO.setup(servoPin1,GPIO.OUT) # set servo as a output device
GPIO.setup(servoPin2,GPIO.OUT)
pwm1=GPIO.PWM(servoPin1,50) # set the frequency to 50Hz
pwm2=GPIO.PWM(servoPin2,50)
pwm1.start(2.5) # starting position is at 0 degrees
pwm2.start(2.5)
armControl = Button(14)
endScript = Button(21)

armdown = False


# mapping pwm to pot input
def map(position,t):
    val = int(round(position,0))
#    print('rounded val: ',val)
    if val == 1023:
        val = 1022
    servopos = t[val]
#    print('servopos: ',servopos)
    pwm1.ChangeDutyCycle(servopos)
#    sleep(.25)


while True:
    adc=MCP3008(channel=0, device=0)
    position = (adc.value*1023)
#     print(position)
    t = np.arange(2.5,12,(9.5/1023))
#        print(len(t))
    map(position,t)
#    sleep(.25)
    if armControl.is_pressed == 1:
        if armdown == False:
            print('Lower Arm')
            pwm2.ChangeDutyCycle(7.25)
            armdown = True
            sleep(0.25)
        else:
            print('Raise Arm')
            pwm2.ChangeDutyCycle(3.5)
            armdown=False
            sleep(0.25)

    if endScript.is_pressed == 1:
        break

pwm1.stop()
pwm2.stop()
GPIO.cleanup()
