#!/usr/bin/python3

# task 1: create a tic-tac-toe game with two users
# task 2: create a game playing against the computer

# import libraries
import RPi.GPIO as GPIO
from time import *

# ---------------------------------
# make this a function to be able to call:
def board_setup():
    # first need to set the setup: (either BCM or BOARD)
    GPIO.setmode(GPIO.BCM)

    # then set output pins... this will make sure that all LED's start off
    # make sure to account for all pins being used for LED outputs
    # -- Positions 1-3 (X then O)
    GPIO.setup(25, GPIO.OUT); GPIO.setup(24, GPIO.OUT);
    GPIO.setup(23, GPIO.OUT); GPIO.setup(18, GPIO.OUT);
    GPIO.setup(15, GPIO.OUT); GPIO.setup(14, GPIO.OUT);
    # -- Positions 4-6 (X then O)
    GPIO.setup(6, GPIO.OUT); GPIO.setup(5, GPIO.OUT);
    GPIO.setup(0, GPIO.OUT); GPIO.setup(11, GPIO.OUT);
    GPIO.setup(9, GPIO.OUT); GPIO.setup(10, GPIO.OUT);
    # -- Positions 7-9 (X then O)
    GPIO.setup(22, GPIO.OUT); GPIO.setup(27, GPIO.OUT);
    GPIO.setup(17, GPIO.OUT); GPIO.setup(4, GPIO.OUT);
    GPIO.setup(3, GPIO.OUT); GPIO.setup(2, GPIO.OUT);

    # set all defaults to be off in case it wasn't cleared from previous run
    GPIO.output(25, GPIO.LOW);GPIO.output(24, GPIO.LOW);
    GPIO.output(23, GPIO.LOW);GPIO.output(18, GPIO.LOW);
    GPIO.output(15, GPIO.LOW);GPIO.output(14, GPIO.LOW);

    GPIO.output(6, GPIO.LOW);GPIO.output(5, GPIO.LOW);
    GPIO.output(0, GPIO.LOW);GPIO.output(11, GPIO.LOW);
    GPIO.output(9, GPIO.LOW);GPIO.output(10, GPIO.LOW);

    GPIO.output(22, GPIO.LOW);GPIO.output(27, GPIO.LOW);
    GPIO.output(17, GPIO.LOW);GPIO.output(4, GPIO.LOW);
    GPIO.output(3, GPIO.LOW);GPIO.output(2, GPIO.LOW);

    # set the 7 segment display to be offGPIO.setup(16, GPIO.OUT) # line a
    GPIO.setup(16, GPIO.OUT) # line a
    GPIO.setup(12, GPIO.OUT) # line b
    GPIO.setup(13, GPIO.OUT) # line c
    GPIO.setup(19, GPIO.OUT) # line d
    GPIO.setup(26, GPIO.OUT) # line e
    GPIO.setup(20, GPIO.OUT) # line f
    GPIO.setup(21, GPIO.OUT) # line g

    GPIO.output(16, GPIO.LOW); GPIO.output(12, GPIO.LOW);
    GPIO.output(13, GPIO.LOW); GPIO.output(19, GPIO.LOW);
    GPIO.output(26, GPIO.LOW); GPIO.output(20, GPIO.LOW);
    GPIO.output(21, GPIO.LOW)

    # after running this, all LED's should be off
    print('...SETTING BOARD...')
    sleep(2)

# set a breakpoint here that if the GPIO are sending warning or errors
# run GPIO.cleanup() in the command line
# then execute and rerun.
#--------------------------------------------------------
# set the 7 segment display

def seg_display_player1():

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(16, GPIO.OUT) # line a
    GPIO.setup(12, GPIO.OUT) # line b
    GPIO.setup(13, GPIO.OUT) # line c
    GPIO.setup(19, GPIO.OUT) # line d
    GPIO.setup(26, GPIO.OUT) # line e
    GPIO.setup(20, GPIO.OUT) # line f
    GPIO.setup(21, GPIO.OUT) # line g

    # display player 1
    GPIO.output(12, GPIO.HIGH)
    GPIO.output(13, GPIO.HIGH)

    GPIO.output(16, GPIO.LOW)
    GPIO.output(20, GPIO.LOW)
    GPIO.output(21, GPIO.LOW)
    GPIO.output(26, GPIO.LOW)
    GPIO.output(19, GPIO.LOW)

def seg_display_player2():
    GPIO.setup(16, GPIO.OUT) # line a
    GPIO.setup(12, GPIO.OUT) # line b
    GPIO.setup(13, GPIO.OUT) # line c
    GPIO.setup(19, GPIO.OUT) # line d
    GPIO.setup(26, GPIO.OUT) # line e
    GPIO.setup(20, GPIO.OUT) # line f
    GPIO.setup(21, GPIO.OUT) # line g

    # display player 2
    GPIO.output(16, GPIO.HIGH)
    GPIO.output(12, GPIO.HIGH)
    GPIO.output(21, GPIO.HIGH)
    GPIO.output(26, GPIO.HIGH)
    GPIO.output(19, GPIO.HIGH)

    GPIO.output(13, GPIO.LOW)
    GPIO.output(20, GPIO.LOW)

#--------------------------------------------------------
#------------ START OF MAIN SCRIPT-----------------------
#--------------------------------------------------------

try:
    playing = True
    board_setup()

    print('Let''s get started!')
    print('Here is the layout: \n')
    print('   |   |   ')
    print(' 1 | 2 | 3 ')
    print('---+---+---')
    print('   |   |   ')
    print(' 4 | 5 | 6 ')
    print('---+---+---')
    print('   |   |   ')
    print(' 7 | 8 | 9 \n')

    xoro = input('Do you want to be X or O? ')
    if (xoro != 'X') & (xoro != 'O'):
        print('\nYou did not enter a valid input...\nPlayer 1: X\nPlayer 2: O \n')
        player1 = 'X'
        player2 = 'O'
    elif xoro == 'X':
        print('\nPlayer 1: X \nPlayer 2: O \n')
        player1 = 'X'
        player2 = 'O'
    else:
        print('\nPlayer 1: O \nPlayer 2: X \n')
        player1 = 'O'
        player2 = 'X'

    print('Player 1 goes first: ')
    # define variables
    allowable_moves = ['1','2','3','4','5','6','7','8','9']
    stored_moves = []
    vline = '   |'
    cross = '---+'
    hline = '---\n'
    end = '   \n'
    b = [vline,vline,end,vline,vline,end,cross,cross,hline,vline,vline,end,vline,vline,end,cross,cross,hline,vline,vline,end,vline,vline,end]
    board = b[0]+b[1]+b[2]+b[3]+b[4]+b[5]+b[6]+b[7]+b[8]+b[9]+b[10]+b[11]+b[12]+b[13]+b[14]+b[15]+b[16]+b[17]+b[18]+b[19]+b[20]+b[21]+b[22]+b[23]
    error = False

    # references:
    # pos 1 = b[3]
    # pos 2 = b[4]
    # pos 3 = b[5]
    # pos 4 = b[12]
    # pos 5 = b[13]
    # pos 6 = b[14]
    # pos 7 = b[21]
    # pos 8 = b[22]
    # pos 9 = b[23]

    player = player1

    while playing:
            if playing == False:
                break
            # set 7 segment display based on player
            if player == player1:
                seg_display_player1()
            else:
                seg_display_player2()

            move = input('What is your move? ')
            if move not in allowable_moves:
                print('You did not enter a valid input... try again!')
            else:
                if move=='1':
                    if move in stored_moves:
                        error = True
                        print('You cannot move there!')
                    else:
                        stored_moves.append(move)
                        print(stored_moves)
                        if player == 'X':
                            b[3] = ' X |'
                            GPIO.output(25,GPIO.HIGH)
                        else:
                            b[3] = ' O |'
                            GPIO.output(24, GPIO.HIGH)

                elif move=='2':
                    if move in stored_moves:
                        error = True
                        print('You cannot move there!')
                    else:
                        stored_moves.append(move)
                        print(stored_moves)
                        if player == 'X':
                            b[4] = ' X |'
                            GPIO.output(23, GPIO.HIGH)
                        else:
                            b[4] = ' O |'
                            GPIO.output(18, GPIO.HIGH)
                elif move=='3':
                    if move in stored_moves:
                        error = True
                        print('You cannot move there!')
                    else:
                        stored_moves.append(move)
                        print(stored_moves)
                        if player == 'X':
                            b[5] = ' X  \n'
                            GPIO.output(15, GPIO.HIGH)
                        else:
                            b[5] = ' O  \n'
                            GPIO.output(14, GPIO.HIGH)
                elif move=='4':
                    if move in stored_moves:
                        error = True
                        print('You cannot move there!')
                    else:
                        stored_moves.append(move)
                        print(stored_moves)
                        if player == 'X':
                            b[12] = ' X |'
                            GPIO.output(6, GPIO.HIGH)
                        else:
                            b[12] = ' O |'
                            GPIO.output(5, GPIO.HIGH)
                elif move=='5':
                    if move in stored_moves:
                        error = True
                        print('You cannot move there!')
                    else:
                        stored_moves.append(move)
                        print(stored_moves)
                        if player == 'X':
                            b[13] = ' X |'
                            GPIO.output(0, GPIO.HIGH)
                        else:
                            b[13] = ' O |'
                            GPIO.output(11, GPIO.HIGH)
                elif move=='6':
                    if move in stored_moves:
                        error = True
                        print('You cannot move there!')
                    else:
                        stored_moves.append(move)
                        print(stored_moves)
                        if player == 'X':
                            b[14] = ' X  \n'
                            GPIO.output(9, GPIO.HIGH)
                        else:
                            b[14] = ' O  \n'
                            GPIO.output(10, GPIO.HIGH)
                elif move=='7':
                    if move in stored_moves:
                        error = True
                        print('You cannot move there!')
                    else:
                        stored_moves.append(move)
                        print(stored_moves)
                        if player == 'X':
                            b[21] = ' X |'
                            GPIO.output(22, GPIO.HIGH)
                        else:
                            b[21] = ' O |'
                            GPIO.output(27, GPIO.HIGH)
                elif move=='8':
                    if move in stored_moves:
                        error = True
                        print('You cannot move there!')
                    else:
                        stored_moves.append(move)
                        print(stored_moves)
                        if player == 'X':
                            b[22] = ' X |'
                            GPIO.output(17, GPIO.HIGH)
                        else:
                            b[22] = ' O |'
                            GPIO.output(4, GPIO.HIGH)
                elif move=='9':
                    if move in stored_moves:
                        error = True
                        print('You cannot move there!')
                    else:
                        stored_moves.append(move)
                        print(stored_moves)
                        if player == 'X':
                            b[23] = ' X  '
                            GPIO.output(3, GPIO.HIGH)
                        else:
                            b[23] = ' O  '
                            GPIO.output(2, GPIO.HIGH)

                board = b[0]+b[1]+b[2]+b[3]+b[4]+b[5]+b[6]+b[7]+b[8]+b[9]+b[10]+b[11]+b[12]+b[13]+b[14]+b[15]+b[16]+b[17]+b[18]+b[19]+b[20]+b[21]+b[22]+b[23]
                print(board)

                # Check if a winning combo has occured
                # first checking horizontals:
                # top row
                if ((b[3] == ' X |') & (b[4]==' X |') & (b[5]==' X  \n')) | ((b[3] == ' O |') & (b[4]==' O |') & (b[5]==' O  \n')):
                    if player==player1:
                        print('Player 1 is the winner!')
                    else:
                        print('Player 2 is the winner!')
                    playing=False

                # middle row
                if ((b[12] == ' X |') & (b[13]==' X |') & (b[14]==' X  \n')) | ((b[12] == ' O |') & (b[13]==' O |') & (b[14]==' O  \n')):
                    if player==player1:
                        print('Player 1 is the winner!')
                    else:
                        print('Player 2 is the winner!')
                    playing=False

                # last row
                if ((b[21] == ' X |') & (b[22]==' X |') & (b[23]==' X  ')) | ((b[21] == ' O |') & (b[22]==' O |') & (b[23]==' O  ')):
                    if player==player1:
                        print('Player 1 is the winner!')
                    else:
                        print('Player 2 is the winner!')
                    playing=False

                # then check verticals
                # first column
                if ((b[3] == ' X |') & (b[12]==' X |') & (b[21]==' X |')) | ((b[3] == ' O |') & (b[12]==' O |') & (b[21]==' O |')):
                    if player==player1:
                        print('Player 1 is the winner!')
                    else:
                        print('Player 2 is the winner!')
                    playing=False

                # second column
                if ((b[4] == ' X |') & (b[13]==' X |') & (b[22]==' X |')) | ((b[4] == ' O |') & (b[13]==' O |') & (b[22]==' O |')):
                    if player==player1:
                        print('Player 1 is the winner!')
                    else:
                        print('Player 2 is the winner!')
                    playing=False

                # third column
                if ((b[5] == ' X  \n') & (b[14]==' X  \n') & (b[23]==' X  ')) | ((b[5] == ' O  \n') & (b[14]==' O  \n') & (b[23]==' O  ')):
                    if player==player1:
                        print('Player 1 is the winner!')
                    else:
                        print('Player 2 is the winner!')
                    playing=False

                # and lastly... diagonals
                # diagonal from top left to bottom right
                if ((b[3] == ' X |') & (b[13]==' X |') & (b[23]==' X  ')) | ((b[3] == ' O |') & (b[13]==' O |') & (b[23]==' O  ')):
                    if player==player1:
                        print('Player 1 is the winner!')
                    else:
                        print('Player 2 is the winner!')
                    playing=False

                # diagonal from top right to bottom left
                if ((b[5] == ' X  \n') & (b[13]==' X |') & (b[21]==' X |')) | ((b[5] == ' O  \n') & (b[13]==' O |') & (b[21]==' O |')):
                    if player==player1:
                        print('Player 1 is the winner!')
                    else:
                        print('Player 2 is the winner!')
                    playing=False

                if len(stored_moves) == 9:
                    print('Tie! There is no winner.')
                    playing=False

                # change player status
                if error == False:
                    if player == player1:
                        player = player2
                        print('Player 2 turn')
                    else:
                        player = player1
                        print('Player 1 turn')

                error = False

except KeyboardInterrupt:
    GPIO.cleanup()
    #----------------------- NOTES ------------------#
    # Combinations to win
    #   Horizontal: 123, 456, 789
    #   Vertical: 147, 258, 369
    #   Diagonal: 159, 357

    # pos 1 = b[3]
    # pos 2 = b[4]
    # pos 3 = b[5]
    # pos 4 = b[12]
    # pos 5 = b[13]
    # pos 6 = b[14]
    # pos 7 = b[21]
    # pos 8 = b[22]
    # pos 9 = b[23]