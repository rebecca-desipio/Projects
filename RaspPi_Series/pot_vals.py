#!/usr/bin/python3

from gpiozero import MCP3008
from time import *
import RPi.GPIO as GPIO
import numpy as np

#try:
#    while True:
#        with MCP3008(channel=0) as pot:
#            print(pot.value)
#except KeyboardInterrupt:
#    print('ending script')

GPIO.setmode(GPIO.BCM)

servoPin=26
GPIO.setup(servoPin,GPIO.OUT)
pwm=GPIO.PWM(servoPin,50)
pwm.start(2.5)

# mapping pwm to pot input
def map(position,t):
    val = int(round(position,0))
    print('rounded val: ',val)
    if val == 1023:
        val = 1022
    servopos = t[val]
    print('servopos: ',servopos)
    pwm.ChangeDutyCycle(servopos)
#    sleep(.25)

try:
    while True:
        adcx=MCP3008(channel=0, device=0)
        position = (adcx.value*1023)
        print(position)
        t = np.arange(2.5,12,(9.5/1023))
#        print(len(t))
        map(position,t)
#        pwm.ChangeDutyCycle(servopos)
#    sleep(.25)

except KeyboardInterrupt:
    pass
pwm.stop()
GPIO.cleanup()
