#!/usr/bin/python3

# task 1: create a tic-tac-toe game with two users
# task 2: create a game playing against the computer

# import libraries
import random
from time import *

play = input('Do you want to play Tic-Tac-Toe? ')

if play == 'yes':
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


    play_computer = True
    xoro = input('Do you want to be X or O? ')
    if (xoro != 'X') & (xoro != 'O'):
        print('\nYou did not enter a valid input...\nPlayer 1: X\nPlayer 2: O \n')
        player1 = 'X'
        player2 = 'O'
        
    elif xoro == 'X':
        player1 = 'X'
        player2 = 'O'
        print('You will be Player 1: X \nThe computer will be Player 2: O')
        
    else:
        player1 = 'O'
        player2 = 'X'
        print('You will be Player 1: O \n The computer will be Player 2: X')

    player = player1
    playing = True

    print('Player 1 goes first: ')
    
else:
    print('Alright... see you next time!')
    playing = False


# define variables
allowable_moves = [1,2,3,4,5,6,7,8,9]
stored_moves = []
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
b = [vline,vline,end,vline,vline,end,cross,cross,hline,vline,vline,end,vline,vline,end,cross,cross,hline,vline,vline,end,vline,vline,end]
board = b[0]+b[1]+b[2]+b[3]+b[4]+b[5]+b[6]+b[7]+b[8]+b[9]+b[10]+b[11]+b[12]+b[13]+b[14]+b[15]+b[16]+b[17]+b[18]+b[19]+b[20]+b[21]+b[22]+b[23]
error = False
previous_moves = []
computer_moves = []

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

    #  for single player, want to enter this loop so the computer can be "smart"
    if (player == player2):
        
        print('Computer is thinking...')
        # the computer first wants to see if there is move to win.
        # check if there are any "smart" moves the computer can make
        print('TRYING TO WIN')
        # checking rows first
        if ((1 in computer_moves) & (2 in computer_moves) & (3 not in previous_moves)):
            move = 3
            computer_moves.append(move)
        elif ((1 in computer_moves) & (3 in computer_moves) & (2 not in previous_moves)):
            move = 2
            computer_moves.append(move)
        elif ((2 in computer_moves) & (3 in computer_moves) & (1 not in previous_moves)):
            move = 3
            computer_moves.append(move)
            
        elif ((4 in computer_moves) & (5 in computer_moves) & (6 not in previous_moves)):
            move = 6
            computer_moves.append(move)
        elif ((4 in computer_moves) & (6 in computer_moves) & (5 not in previous_moves)):
            move = 5
            computer_moves.append(move)
        elif ((5 in computer_moves) & (6 in computer_moves) & (4 not in previous_moves)):
            move = 4
            computer_moves.append(move)
            
        elif ((7 in computer_moves) & (8 in computer_moves) & (9 not in previous_moves)):
            move = 9
            computer_moves.append(move)
        elif ((8 in computer_moves) & (9 in computer_moves) & (7 not in previous_moves)):
            move = 7
            computer_moves.append(move)
        elif ((9 in computer_moves) & (7 in computer_moves) & (8 not in previous_moves)):
            move = 8
            computer_moves.append(move)
            
        # check columns next
        elif ((1 in computer_moves) & (4 in computer_moves) & (7 not in previous_moves)):
            move = 7
            computer_moves.append(move)
        elif ((1 in computer_moves) & (7 in computer_moves) & (4 not in previous_moves)):
            move = 4
            computer_moves.append(move)
        elif ((4 in computer_moves) & (7 in computer_moves) & (1 not in previous_moves)):
            move = 1
            computer_moves.append(move)
            
        elif ((2 in computer_moves) & (5 in computer_moves) & (8 not in previous_moves)):
            move = 8
            computer_moves.append(move)
        elif ((8 in computer_moves) & (2 in computer_moves) & (5 not in previous_moves)):
            move = 5
            computer_moves.append(move)
        elif ((5 in computer_moves) & (8 in computer_moves) & (2 not in previous_moves)):
            move = 2
            computer_moves.append(move)
            
        elif ((3 in computer_moves) & (6 in computer_moves) & (9 not in previous_moves)):
            move = 9
            computer_moves.append(move)
        elif ((6 in computer_moves) & (9 in computer_moves) & (3 not in previous_moves)):
            move = 3
            computer_moves.append(move)
        elif ((9 in computer_moves) & (3 in computer_moves) & (6 not in previous_moves)):
            move = 6
            computer_moves.append(move)

        # lastly, check diagonals
        elif ((1 in computer_moves) & (5 in computer_moves) & (9 not in previous_moves)):
            move = 9
            computer_moves.append(move)
        elif ((1 in computer_moves) & (9 in computer_moves) & (5 not in previous_moves)):
            move = 5
            computer_moves.append(move)
        elif ((5 in computer_moves) & (9 in computer_moves) & (1 not in previous_moves)):
            move = 1
            computer_moves.append(move)

        elif ((3 in computer_moves) & (5 in computer_moves) & (7 not in previous_moves)):
            move = 7
            computer_moves.append(move)
        elif ((3 in computer_moves) & (7 in computer_moves) & (5 not in previous_moves)):
            move = 5
            computer_moves.append(move)
        elif ((5 in computer_moves) & (7 in computer_moves) & (3 not in previous_moves)):
            move = 3
            computer_moves.append(move)

        # if there are no smart moves to make
        else:
            print('ENTERED HERE')
#------------------------ No moves were able to be made to win ---------------------------------#
    
            # the computer is checking if there are any moves that should be stopped that a human would recognize
            if len(previous_moves) == 1:
                print('SHOULD BE PRINTING A RANDOM NUMBER')
                move = (random.randint(1,9))
            # account for horizontal attemps          
            elif (1 in previous_moves) & (2 in previous_moves) & (3 not in computer_moves):
                if 3 not in computer_moves:
                    move = 3
                    computer_moves.append(move)
            elif (1 in previous_moves) & (3 in previous_moves) & (2 not in computer_moves):
                if 2 not in computer_moves:
                    move = 2
                    computer_moves.append(move)
            elif (2 in previous_moves) & (3 in previous_moves) & (1 not in computer_moves):
                if 1 not in computer_moves:
                    move = 1
                    computer_moves.append(move)
            elif (4 in previous_moves) & (5 in previous_moves) & (6 not in computer_moves):
                if 6 not in computer_moves:
                    move = 6
                    computer_moves.append(move)
            elif (4 in previous_moves) & (6 in previous_moves) & (5 not in computer_moves):
                if 5 not in computer_moves:
                    move = 5
                    computer_moves.append(move)
            elif (5 in previous_moves) & (6 in previous_moves) & (4 not in computer_moves):
                if 4 not in computer_moves:
                    move = 4
                    computer_moves.append(move)
            elif (7 in previous_moves) & (8 in previous_moves) & (9 not in computer_moves):
                if 9 not in computer_moves:
                    move = 9
                    computer_moves.append(move)
            elif (7 in previous_moves) & (9 in previous_moves) & (8 not in computer_moves):
                if 8 not in computer_moves:
                    move = 8
                    computer_moves.append(move)
            elif (8 in previous_moves) & (9 in previous_moves) & (7 not in computer_moves):
                if 7 not in computer_moves:
                    move = 7
                    computer_moves.append(move)
                    
            # account for vertical attemps
            elif (1 in previous_moves) & (4 in previous_moves) & (7 not in computer_moves):
                if 7 not in computer_moves:
                    move = 7
                    computer_moves.append(move)
            elif (1 in previous_moves) & (7 in previous_moves) & (4 not in computer_moves):
                if 4 not in computer_moves:
                    move = 4
                    computer_moves.append(move)
            elif (4 in previous_moves) & (7 in previous_moves) & (1 not in computer_moves):
                if 1 not in computer_moves:
                    move = 1
                    computer_moves.append(move)
            elif (2 in previous_moves) & (5 in previous_moves) & (8 not in computer_moves):
                if 8 not in computer_moves:
                    move = 8
                    computer_moves.append(move)
            elif (5 in previous_moves) & (8 in previous_moves) & (2 not in computer_moves):
                if 2 not in computer_moves:
                    move = 2
                    computer_moves.append(move)
            elif (8 in previous_moves) & (2 in previous_moves) & (5 not in computer_moves):
                if 5 not in computer_moves:
                    move = 5
                    computer_moves.append(move)
            elif (3 in previous_moves) & (6 in previous_moves) & (9 not in computer_moves):
                if 9 not in computer_moves:
                    move = 9
                    computer_moves.append(move)
            elif (6 in previous_moves) & (9 in previous_moves) & (3 not in computer_moves):
                if 3 not in computer_moves:
                    move = 3
                    computer_moves.append(move)
            elif (9 in previous_moves) & (3 in previous_moves) & (6 not in computer_moves):
                if 6 not in computer_moves:
                    move = 6
                    computer_moves.append(move)
                    
            #account for diagonal attempts
            elif (1 in previous_moves) & (5 in previous_moves) & (9 not in computer_moves):
                if 9 not in computer_moves:
                    move = 9
                    computer_moves.append(move)
            elif (1 in previous_moves) & (9 in previous_moves) & (5 not in computer_moves):
                if 5 not in computer_moves:
                    move = 5
                    computer_moves.append(move)
            elif (5 in previous_moves) & (9 in previous_moves) & (1 not in computer_moves):
                if 1 not in computer_moves:
                    move = 1
                    computer_moves.append(move)
                
            elif (3 in previous_moves) & (5 in previous_moves) & (7 not in computer_moves):
                if 7 not in computer_moves:
                    move = 7
                    computer_moves.append(move)
            elif (3 in previous_moves) & (7 in previous_moves) & (5 not in computer_moves):
                if 5 not in computer_moves:
                    move = 5
                    computer_moves.append(move)
            elif (5 in previous_moves) & (7 in previous_moves) & (3 not in computer_moves):
                if 3 not in computer_moves:
                    move = 3
                    computer_moves.append(move)
            else:
                move = int(str(random.randint(1,9)))
                print('REACHED THIS POINT')
            

        sleep(2)
        worked = True

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
    # if there was a valid input, now set the move on the board
    if worked == True:
        if move==1:
            if move in stored_moves:
                error = True
                print('You cannot move there!')
            else:        
                stored_moves.append(move)
                print(stored_moves)
                if player == 'X':
                    b[3] = X_space
                else:
                    b[3] = O_space

        elif move==2:
            if move in stored_moves:
                error = True
                print('You cannot move there!')
            else:
                stored_moves.append(move)
                print(stored_moves)
                if player == 'X':
                    b[4] = X_space
                else:
                    b[4] = O_space
        elif move==3:
            if move in stored_moves:
                error = True
                print('You cannot move there!')
            else:
                stored_moves.append(move)
                print(stored_moves)
                if player == 'X':
                    b[5] = X_end
                else:
                    b[5] = O_end
        elif move==4:
            if move in stored_moves:
                error = True
                print('You cannot move there!')
            else:
                stored_moves.append(move)
                print(stored_moves)
                if player == 'X':
                    b[12] = X_space
                else:
                    b[12] = O_space
        elif move==5:
            if move in stored_moves:
                error = True
                print('You cannot move there!')
            else:
                stored_moves.append(move)
                print(stored_moves)
                if player == 'X':
                    b[13] = X_space
                else:
                    b[13] = O_space
        elif move==6:
            if move in stored_moves:
                error = True
                print('You cannot move there!')
            else:
                stored_moves.append(move)
                print(stored_moves)
                if player == 'X':
                    b[14] = X_end
                else:
                    b[14] = O_end
        elif move==7:
            if move in stored_moves:
                error = True
                print('You cannot move there!')
            else:
                stored_moves.append(move)
                print(stored_moves)
                if player == 'X':
                    b[21] = X_space
                else:
                    b[21] = O_space
        elif move==8:
            if move in stored_moves:
                error = True
                print('You cannot move there!')
            else:
                stored_moves.append(move)
                print(stored_moves)
                if player == 'X':
                    b[22] = X_space
                else:
                    b[22] = O_space
        elif move==9:
            if move in stored_moves:
                error = True
                print('You cannot move there!')
            else:
                stored_moves.append(move)
                print(stored_moves)
                if player == 'X':
                    b[23] = X_only
                else:
                    b[23] = O_only

        board = b[0]+b[1]+b[2]+b[3]+b[4]+b[5]+b[6]+b[7]+b[8]+b[9]+b[10]+b[11]+b[12]+b[13]+b[14]+b[15]+b[16]+b[17]+b[18]+b[19]+b[20]+b[21]+b[22]+b[23]
        print(board)

        # Check if a winning combo has occured
        # first checking horizontals:
        # top row
        if ((b[3] == X_space) & (b[4]==X_space) & (b[5]==X_end)) | ((b[3] == O_space) & (b[4]==O_space) & (b[5]==O_end)):
            if player==player1:
                print('Player 1 is the winner!')
            else:
                print('Player 2 is the winner!')
            break

        # middle row
        if ((b[12] == X_space) & (b[13]==X_space) & (b[14]==X_end)) | ((b[12] == O_space) & (b[13]==O_space) & (b[14]==O_end)):
            if player==player1:
                print('Player 1 is the winner!')
            else:
                print('Player 2 is the winner!')
            break

        # last row
        if ((b[21] == X_space) & (b[22]==X_space) & (b[23]==X_only)) | ((b[21] == O_space) & (b[22]==O_space) & (b[23]==O_only)):
            if player==player1:
                print('Player 1 is the winner!')
            else:
                print('Player 2 is the winner!')
            break

        # then check verticals
        # first column
        if ((b[3] == X_space) & (b[12]==X_space) & (b[21]==X_space)) | ((b[3] == O_space) & (b[12]==O_space) & (b[21]==O_space)):
            if player==player1:
                print('Player 1 is the winner!')
            else:
                print('Player 2 is the winner!')
            break

        # second column
        if ((b[4] == X_space) & (b[13]==X_space) & (b[22]==X_space)) | ((b[4] == O_space) & (b[13]==O_space) & (b[22]==O_space)):
            if player==player1:
                print('Player 1 is the winner!')
            else:
                print('Player 2 is the winner!')
            break

        # third column
        if ((b[5] == X_end) & (b[14]==X_end) & (b[23]==X_only)) | ((b[5] == O_end) & (b[14]==O_end) & (b[23]==O_only)):
            if player==player1:
                print('Player 1 is the winner!')
            else:
                print('Player 2 is the winner!')
            break

        # and lastly... diagonals
        # diagonal from top left to bottom right
        if ((b[3] == X_space) & (b[13]==X_space) & (b[23]==X_only)) | ((b[3] == O_space) & (b[13]==O_space) & (b[23]==O_only)):
            if player==player1:
                print('Player 1 is the winner!')
            else:
                print('Player 2 is the winner!')
            break

        # diagonal from top right to bottom left
        if ((b[5] == X_end) & (b[13]==X_space) & (b[21]==X_space)) | ((b[5] == O_space) & (b[13]==O_space) & (b[21]==O_space)):
            if player==player1:
                print('Player 1 is the winner!')
            else:
                print('Player 2 is the winner!')
            break
        
        # change player status
        if error == False:
            if player == player1:
                player = player2
                print('Player 2 turn')
            else:
                player = player1
                computer_moves.append(move)
                print('Player 1 turn')

        if len(stored_moves) == 9:
            print('Tie! There is no winner.')
            break

        error = False


    print('LAST MOVE = ',move)
                


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

