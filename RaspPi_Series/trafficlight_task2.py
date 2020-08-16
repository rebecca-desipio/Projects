#!/usr/bin/python

# import libraries
from gpiozero import *
from time import *

# define inputs/outputs
red1 = LED(14); red2 = LED(16); 
yellow1 = LED(15); yellow2 = LED(20); 
green1 = LED(18); green2 = LED(21);

A = Button(23)
B = Button(24)

# turn the green light on if the
# button is pressed
while True:
  if A.is_pressed == 1 | B.is_pressed == 1:
    green1.on()
    red2.on()
    sleep(3)
    break

# with the green light on, if the button 
# is pressed again, transition to yellow,
# and then red. Once the button is pressed 
# a second time, switch back to green. Repeat.

while True:
  if B.is_pressed == 1:
      sleep(1.5)
      # set green light on 1 and red light on 2
      green1.off()
      sleep(.25)
      # change set 1 to change to yellow
      # keep set 2 set to red
      yellow1.on(); sleep(4)
      # change set 1 to red and set 2 will wait 1 sec until changing to green
      yellow1.off(); sleep(.25);
      red1.on();     sleep(2);
      red2.off() 
      green2.on()

  # now if the A buton is pressed for set one...
  # we want to have set 2 change yellow then red
  # and set 1 will then change to green.
  if A.is_pressed == 1:
      sleep(1.5)
      # set green light on 1 and red light on 2
      green2.off()
      sleep(.25)
      # change set 1 to change to yellow
      # keep set 2 set to red
      yellow2.on(); sleep(4)
      # change set 1 to red and set 2 will wait 1 sec until changing to green
      yellow2.off(); sleep(.25);
      red2.on();     sleep(2);
      red1.off()
      green1.on()

  # if both buttons are held down  at the same time
  # terminate the program... need to hold until terminates
  if (A.is_pressed == 1) & (B.is_pressed ==1):
    print('ending program....')
    break

