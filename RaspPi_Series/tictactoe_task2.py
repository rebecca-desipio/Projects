#!/usr/bin/python3

# task 1: create a tic-tac-toe game with two users
# task 2: create a game playing against the computer

# import libraries
import random
import RPi.GPIO as GPIO
from time import *

#---------FUNCTION for Setting up the GPIO -----------
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
#----------END of FUNCTION---------------

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
# try exce[pt is used in case there is a keyboard interrupt
try:
    playing = True # used when asking the user if they want to play again

    board_setup()

    # simply providing instructions here
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

    # having the player pick which symbol they want to be
    xoro = input('Do you want to be X or O? ')
    if (xoro != 'X') & (xoro != 'O'):
        print('\nYou did not enter a valid input...\nPlayer 1: X\nPlayer 2: O \n')
        player1 = 'X'
        player2 = 'O'

    elif xoro == 'X':
        player1 = 'X'
        player2 = 'O'
        print('You will be Player 1: X \nThe computer will be Player 2: O')

    else: # if an X or O is not entered, automatically set to the following
        player1 = 'O'
        player2 = 'X'
        print('You will be Player 1: O \n The computer will be Player 2: X')

    # by default, player 1 will always go first and will
    # always be the human player
    # Challenge: could add a question for who goes first by random
    print('Player 1 goes first: ')
    player = player1 # set the variable for the player to always start as player1

    #-------------- DEFINE VARIABLES ---------------------
    allowable_moves = [1,2,3,4,5,6,7,8,9]  # used for comparison in anaylsis
    stored_moves = [] # store all the moves of each player to use in analysis
    previous_moves = [] # stores all moves up until the one being played
    computer_moves = [] # stores the computers moves only.
    # define variables to create the visual representation of the board
    # Created variables to be used for each individual position (1-9)... but
    # there are 24 total positions due to using two lines to represent one box
    vline = '   |'
    cross = '---+'
    hline = '---\n'
    end = '   \n'
    O_space = ' O |'
    X_space = ' X |'
    O_end = ' O  \n'
    X_end = ' X  \n'
    O_only = ' O  '
    X_only = ' X  '
    # set up the board by appending
    b = [vline,vline,end,vline,vline,end,cross,cross,hline,vline,vline,end,vline,vline,end,cross,cross,hline,vline,vline,end,vline,vline,end]
    board = b[0]+b[1]+b[2]+b[3]+b[4]+b[5]+b[6]+b[7]+b[8]+b[9]+b[10]+b[11]+b[12]+b[13]+b[14]+b[15]+b[16]+b[17]+b[18]+b[19]+b[20]+b[21]+b[22]+b[23]
    # set needed boolean values
    play_computer = True
    playing = True
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

    #   Horizontal: 123, 456, 789
    #   Vertical: 147, 258, 369
    #   Diagonal: 159, 357
    while playing:
        # if they don't want to play again, exit to the main menu
        if playing == False:
            break

        # set 7 segment display based on player
        if player == player1:
            seg_display_player1()
        else:
            seg_display_player2()

        #  for single player, want to enter this loop so the computer can be "smart"
        if (player == player2):
            # if it is the computers first move, it just needs to generate a random number
            if len(previous_moves) == 1:
                #print('SHOULD BE PRINTING A RANDOM NUMBER')
                move = (random.randint(1,9))

            print('Computer is thinking...')
            # the computer first wants to see if there is move to win.
            # check if there are any "smart" moves the computer can make
            #print('TRYING TO WIN')

            # checking rows first
            # MOVE POS 3
            if ((1 in computer_moves) & (2 in computer_moves) & (3 not in previous_moves)):
                move = 3
                computer_moves.append(move) # append each move to the stored previous computer moves array

            # MOVE POS 2
            elif ((1 in computer_moves) & (3 in computer_moves) & (2 not in previous_moves)):
                move = 2
                computer_moves.append(move)

            # MOVE POS 3
            elif ((2 in computer_moves) & (3 in computer_moves) & (1 not in previous_moves)):
                move = 3
                computer_moves.append(move)

            # MOVE POS 6
            elif ((4 in computer_moves) & (5 in computer_moves) & (6 not in previous_moves)):
                move = 6
                computer_moves.append(move)

            # MOVE POS 5
            elif ((4 in computer_moves) & (6 in computer_moves) & (5 not in previous_moves)):
                move = 5
                computer_moves.append(move)

            # MOVE POS 4
            elif ((5 in computer_moves) & (6 in computer_moves) & (4 not in previous_moves)):
                move = 4
                computer_moves.append(move)

            # MOVE POS 9
            elif ((7 in computer_moves) & (8 in computer_moves) & (9 not in previous_moves)):
                move = 9
                computer_moves.append(move)

            # MOVE POS 7
            elif ((8 in computer_moves) & (9 in computer_moves) & (7 not in previous_moves)):
                move = 7
                computer_moves.append(move)

            # MOVE POS 8
            elif ((9 in computer_moves) & (7 in computer_moves) & (8 not in previous_moves)):
                move = 8
                computer_moves.append(move)

            # check columns next
            # MOVE POS 7
            elif ((1 in computer_moves) & (4 in computer_moves) & (7 not in previous_moves)):
                move = 7
                computer_moves.append(move)

            # MOVE POS 4
            elif ((1 in computer_moves) & (7 in computer_moves) & (4 not in previous_moves)):
                move = 4
                computer_moves.append(move)

            # MOVE POS 1
            elif ((4 in computer_moves) & (7 in computer_moves) & (1 not in previous_moves)):
                move = 1
                computer_moves.append(move)

            # MOVE POS 8
            elif ((2 in computer_moves) & (5 in computer_moves) & (8 not in previous_moves)):
                move = 8
                computer_moves.append(move)

            # MOVE POS 5
            elif ((8 in computer_moves) & (2 in computer_moves) & (5 not in previous_moves)):
                move = 5
                computer_moves.append(move)

            # MOVE POS 2
            elif ((5 in computer_moves) & (8 in computer_moves) & (2 not in previous_moves)):
                move = 2
                computer_moves.append(move)

            # MOVE POS 9
            elif ((3 in computer_moves) & (6 in computer_moves) & (9 not in previous_moves)):
                move = 9
                computer_moves.append(move)

            # MOVE POS 3
            elif ((6 in computer_moves) & (9 in computer_moves) & (3 not in previous_moves)):
                move = 3
                computer_moves.append(move)

            # MOVE POS 6
            elif ((9 in computer_moves) & (3 in computer_moves) & (6 not in previous_moves)):
                move = 6
                computer_moves.append(move)

            # lastly, check diagonals
            # MOVE POS 9
            elif ((1 in computer_moves) & (5 in computer_moves) & (9 not in previous_moves)):
                move = 9
                computer_moves.append(move)

            # MOVE POS 5
            elif ((1 in computer_moves) & (9 in computer_moves) & (5 not in previous_moves)):
                move = 5
                computer_moves.append(move)

            # MOVE POS 1
            elif ((5 in computer_moves) & (9 in computer_moves) & (1 not in previous_moves)):
                move = 1
                computer_moves.append(move)

            # MOVE POS 7
            elif ((3 in computer_moves) & (5 in computer_moves) & (7 not in previous_moves)):
                move = 7
                computer_moves.append(move)

            # MOVE POS 5
            elif ((3 in computer_moves) & (7 in computer_moves) & (5 not in previous_moves)):
                move = 5
                computer_moves.append(move)

            # MOVE POS 3
            elif ((5 in computer_moves) & (7 in computer_moves) & (3 not in previous_moves)):
                move = 3
                computer_moves.append(move)

            # if there are no smart moves to make
            else:
                #print('ENTERED HERE')
    #------------------------ No moves were able to be made to win ---------------------------------#

                # the computer is checking if there are any moves that should be stopped that a human would recognize
                # account for horizontal attemps
                # MOVE POS 3
                if (1 in previous_moves) & (2 in previous_moves) & (3 not in computer_moves):
                    if 3 not in computer_moves: # want to make sure the computer hasn't alreayd moved here
                        move = 3
                        computer_moves.append(move)

                # MOVE POS 2
                elif (1 in previous_moves) & (3 in previous_moves) & (2 not in computer_moves):
                    if 2 not in computer_moves:
                        move = 2
                        computer_moves.append(move)

                # MOVE POS 1
                elif (2 in previous_moves) & (3 in previous_moves) & (1 not in computer_moves):
                    if 1 not in computer_moves:
                        move = 1
                        computer_moves.append(move)

                # MOVE POS 6
                elif (4 in previous_moves) & (5 in previous_moves) & (6 not in computer_moves):
                    if 6 not in computer_moves:
                        move = 6
                        computer_moves.append(move)

                # MOVE POS 5
                elif (4 in previous_moves) & (6 in previous_moves) & (5 not in computer_moves):
                    if 5 not in computer_moves:
                        move = 5
                        computer_moves.append(move)

                # MOVE POS 4
                elif (5 in previous_moves) & (6 in previous_moves) & (4 not in computer_moves):
                    if 4 not in computer_moves:
                        move = 4
                        computer_moves.append(move)

                # MOVE POS 9
                elif (7 in previous_moves) & (8 in previous_moves) & (9 not in computer_moves):
                    if 9 not in computer_moves:
                        move = 9
                        computer_moves.append(move)

                # MOVE POS 8
                elif (7 in previous_moves) & (9 in previous_moves) & (8 not in computer_moves):
                    if 8 not in computer_moves:
                        move = 8
                        computer_moves.append(move)

                # MOVE POS 7
                elif (8 in previous_moves) & (9 in previous_moves) & (7 not in computer_moves):
                    if 7 not in computer_moves:
                        move = 7
                        computer_moves.append(move)

                # account for vertical attemps
                # MOVE POS 7
                elif (1 in previous_moves) & (4 in previous_moves) & (7 not in computer_moves):
                    if 7 not in computer_moves:
                        move = 7
                        computer_moves.append(move)

                # MOVE POS 4
                elif (1 in previous_moves) & (7 in previous_moves) & (4 not in computer_moves):
                    if 4 not in computer_moves:
                        move = 4
                        computer_moves.append(move)

                # MOVE POS 1
                elif (4 in previous_moves) & (7 in previous_moves) & (1 not in computer_moves):
                    if 1 not in computer_moves:
                        move = 1
                        computer_moves.append(move)

                # MOVE POS 8
                elif (2 in previous_moves) & (5 in previous_moves) & (8 not in computer_moves):
                    if 8 not in computer_moves:
                        move = 8
                        computer_moves.append(move)

                # MOVE POS 2
                elif (5 in previous_moves) & (8 in previous_moves) & (2 not in computer_moves):
                    if 2 not in computer_moves:
                        move = 2
                        computer_moves.append(move)

                # MOVE POS 5
                elif (8 in previous_moves) & (2 in previous_moves) & (5 not in computer_moves):
                    if 5 not in computer_moves:
                        move = 5
                        computer_moves.append(move)

                # MOVE POS 9
                elif (3 in previous_moves) & (6 in previous_moves) & (9 not in computer_moves):
                    if 9 not in computer_moves:
                        move = 9
                        computer_moves.append(move)

                # MOVE POS 3
                elif (6 in previous_moves) & (9 in previous_moves) & (3 not in computer_moves):
                    if 3 not in computer_moves:
                        move = 3
                        computer_moves.append(move)

                # MOVE POS 6
                elif (9 in previous_moves) & (3 in previous_moves) & (6 not in computer_moves):
                    if 6 not in computer_moves:
                        move = 6
                        computer_moves.append(move)

                #account for diagonal attempts
                # MOVE POS 9
                elif (1 in previous_moves) & (5 in previous_moves) & (9 not in computer_moves):
                    if 9 not in computer_moves:
                        move = 9
                        computer_moves.append(move)

                # MOVE POS 5
                elif (1 in previous_moves) & (9 in previous_moves) & (5 not in computer_moves):
                    if 5 not in computer_moves:
                        move = 5
                        computer_moves.append(move)

                # MOVE POS 1
                elif (5 in previous_moves) & (9 in previous_moves) & (1 not in computer_moves):
                    if 1 not in computer_moves:
                        move = 1
                        computer_moves.append(move)

                # MOVE POS 7
                elif (3 in previous_moves) & (5 in previous_moves) & (7 not in computer_moves):
                    if 7 not in computer_moves:
                        move = 7
                        computer_moves.append(move)

                # MOVE POS 5
                elif (3 in previous_moves) & (7 in previous_moves) & (5 not in computer_moves):
                    if 5 not in computer_moves:
                        move = 5
                        computer_moves.append(move)

                # MOVE POS 3
                elif (5 in previous_moves) & (7 in previous_moves) & (3 not in computer_moves):
                    if 3 not in computer_moves:
                        move = 3
                        computer_moves.append(move)

                else:
                    move = int(str(random.randint(1,9)))
                    #print('REACHED THIS POINT')



            # if we've made it to this point in the code, then the computer was able to successfully make a move.
            worked = True
            sleep(2)

        # after it has gone through the above process...
        # now we want to switch to player 1's turn
        else:
            # now it is player one's turn
            # check for a valid input, and if not, ask the user to input again.
            try:
                move = int(input('What is your move? '))
                previous_moves.append(move)
                print('player 1 has moved: ',previous_moves)
                worked = True
            except ValueError:
                print('You did not enter a valid input... try again!')
                worked = False

        # now... no matter which players turn it was... we want to update the board.
        # this will happen every iteration as long as a valid input was set.
        # if there was a valid input, now set the move on the board and update the player
        if worked == True:
            if move==1:
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

            elif move==2:
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
            elif move==3:
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
            elif move==4:
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
            elif move==5:
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
            elif move==6:
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
            elif move==7:
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
            elif move==8:
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
            elif move==9:
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

            # update the board
            board = b[0]+b[1]+b[2]+b[3]+b[4]+b[5]+b[6]+b[7]+b[8]+b[9]+b[10]+b[11]+b[12]+b[13]+b[14]+b[15]+b[16]+b[17]+b[18]+b[19]+b[20]+b[21]+b[22]+b[23]
            print(board) # display the board

            # Check if a winning combo has occured
            # first checking horizontals:
            # top row
            if ((b[3] == X_space) & (b[4]==X_space) & (b[5]==X_end)) | ((b[3] == O_space) & (b[4]==O_space) & (b[5]==O_end)):
                if player==player1:
                    print('Player 1 is the winner!')
                else:
                    print('Player 2 is the winner!')
                playing = False

            # middle row
            if ((b[12] == X_space) & (b[13]==X_space) & (b[14]==X_end)) | ((b[12] == O_space) & (b[13]==O_space) & (b[14]==O_end)):
                if player==player1:
                    print('Player 1 is the winner!')
                else:
                    print('Player 2 is the winner!')
                playing = False

            # last row
            if ((b[21] == X_space) & (b[22]==X_space) & (b[23]==X_only)) | ((b[21] == O_space) & (b[22]==O_space) & (b[23]==O_only)):
                if player==player1:
                    print('Player 1 is the winner!')
                else:
                    print('Player 2 is the winner!')
                playing = False

            # then check verticals
            # first column
            if ((b[3] == X_space) & (b[12]==X_space) & (b[21]==X_space)) | ((b[3] == O_space) & (b[12]==O_space) & (b[21]==O_space)):
                if player==player1:
                    print('Player 1 is the winner!')
                else:
                    print('Player 2 is the winner!')
                playing = False

            # second column
            if ((b[4] == X_space) & (b[13]==X_space) & (b[22]==X_space)) | ((b[4] == O_space) & (b[13]==O_space) & (b[22]==O_space)):
                if player==player1:
                    print('Player 1 is the winner!')
                else:
                    print('Player 2 is the winner!')
                playing = False

            # third column
            if ((b[5] == X_end) & (b[14]==X_end) & (b[23]==X_only)) | ((b[5] == O_end) & (b[14]==O_end) & (b[23]==O_only)):
                if player==player1:
                    print('Player 1 is the winner!')
                else:
                    print('Player 2 is the winner!')
                playing = False

            # and lastly... diagonals
            # diagonal from top left to bottom right
            if ((b[3] == X_space) & (b[13]==X_space) & (b[23]==X_only)) | ((b[3] == O_space) & (b[13]==O_space) & (b[23]==O_only)):
                if player==player1:
                    print('Player 1 is the winner!')
                else:
                    print('Player 2 is the winner!')
                playing = False

            # diagonal from top right to bottom left
            if ((b[5] == X_end) & (b[13]==X_space) & (b[21]==X_space)) | ((b[5] == O_end) & (b[13]==O_space) & (b[21]==O_space)):
                if player==player1:
                    print('Player 1 is the winner!')
                else:
                    print('Player 2 is the winner!')
                playing = False

            # change player status
            if error == False:
                if player == player1:
                    player = player2
                    print('Player 2 turn')
                else:
                    player = player1
                    computer_moves.append(move)
                    print('Player 1 turn')

            # if all moves are exhausted and there are no moves left... it's a tie
            if len(stored_moves) == 9:
                print('Tie! There is no winner.')
                playing = False

            error = False

            #print('LAST MOVE = ',move)

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
