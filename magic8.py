#!/usr/bin/python3

# Write a Magic 8 Ball Program
# Tasks:
#	- Ask the user to input their question and display it
#	- Create random responses that will output (at least 8)
# 	- Allow the user to either continue or quit

import random
import time

def find_an_answer(val):
	response = answers[val]
	print('Magic 8 ball says...'+response)

while True:
	question = input('Ask a question: ')
	print('Generating response...')
	time.sleep(3)

	answers = ['it is certain','yes - definitiely','most likely','outlook good',\
	'ask again later','cannot predict now','don''t count on it','my sources say no',\
	'outlook not so good']

	val = random.randint(0,8)

	find_an_answer(val)

	ask_another_q = input('Do you want to ask another question? [Y]/[N]: ')
	if ask_another_q == 'Y':
		continue
	elif ask_another_q == 'N':
		print('Thanks for Playing! Good-Bye.')
		break
	else:
		print('Invalid Response... Exiting Script')
		break
