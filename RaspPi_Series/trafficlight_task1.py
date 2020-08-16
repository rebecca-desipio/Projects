#!/usr/bin/python

# import libraries
from gpiozero import *
from time import *
import RPi.GPIO as GPIO

GPIO.cleanup()

# define inputs/outputs
red = LED(14)
yellow = LED(15)
green = LED(18)

A = Button(23)

# turn the green light on if the
# button is pressed
while True:
  if A.is_pressed == 1:
    green.on()
    sleep(3)
    break

# with the green light on, if the button 
# is pressed again, transition to yellow,
# and then red. Once the button is pressed 
# a second time, switch back to green. Repeat.

while True:
  if A.is_pressed == 1:
    if green.is_active == True:
      green.off()
      sleep(.25)
      yellow.on()
      sleep(4)
      yellow.off()
      sleep(.25)
      red.on()
    elif red.is_active == True:
      red.off()
      sleep(.25)
      green.on()



GPIO.cleanup()
