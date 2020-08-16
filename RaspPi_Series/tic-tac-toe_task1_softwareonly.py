#!/usr/bin/python3

# task 1: create a tic-tac-toe game with two users
# task 2: create a game playing against the computer

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

    playing = True
    
else:
    print('Alright... see you next time!')

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
                else:
                    b[3] = ' O |'

        elif move=='2':
            if move in stored_moves:
                error = True
                print('You cannot move there!')
            else:
                stored_moves.append(move)
                print(stored_moves)
                if player == 'X':
                    b[4] = ' X |'
                else:
                    b[4] = ' O |'
        elif move=='3':
            if move in stored_moves:
                error = True
                print('You cannot move there!')
            else:
                stored_moves.append(move)
                print(stored_moves)
                if player == 'X':
                    b[5] = ' X  \n'
                else:
                    b[5] = ' O  \n'
        elif move=='4':
            if move in stored_moves:
                error = True
                print('You cannot move there!')
            else:
                stored_moves.append(move)
                print(stored_moves)
                if player == 'X':
                    b[12] = ' X |'
                else:
                    b[12] = ' O |'
        elif move=='5':
            if move in stored_moves:
                error = True
                print('You cannot move there!')
            else:
                stored_moves.append(move)
                print(stored_moves)
                if player == 'X':
                    b[13] = ' X |'
                else:
                    b[13] = ' O |'
        elif move=='6':
            if move in stored_moves:
                error = True
                print('You cannot move there!')
            else:
                stored_moves.append(move)
                print(stored_moves)
                if player == 'X':
                    b[14] = ' X  \n'
                else:
                    b[14] = ' O  \n'
        elif move=='7':
            if move in stored_moves:
                error = True
                print('You cannot move there!')
            else:
                stored_moves.append(move)
                print(stored_moves)
                if player == 'X':
                    b[21] = ' X |'
                else:
                    b[21] = ' O |'
        elif move=='8':
            if move in stored_moves:
                error = True
                print('You cannot move there!')
            else:
                stored_moves.append(move)
                print(stored_moves)
                if player == 'X':
                    b[22] = ' X |'
                else:
                    b[22] = ' O |'
        elif move=='9':
            if move in stored_moves:
                error = True
                print('You cannot move there!')
            else:
                stored_moves.append(move)
                print(stored_moves)
                if player == 'X':
                    b[23] = ' X  '
                else:
                    b[23] = ' O  '

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
            break

        # middle row
        if ((b[12] == ' X |') & (b[13]==' X |') & (b[14]==' X  \n')) | ((b[12] == ' O |') & (b[13]==' O |') & (b[14]==' O  \n')):
            if player==player1:
                print('Player 1 is the winner!')
            else:
                print('Player 2 is the winner!')
            break

        # last row
        if ((b[21] == ' X |') & (b[22]==' X |') & (b[23]==' X  ')) | ((b[21] == ' O |') & (b[22]==' O |') & (b[23]==' O  ')):
            if player==player1:
                print('Player 1 is the winner!')
            else:
                print('Player 2 is the winner!')
            break

        # then check verticals
        # first column
        if ((b[3] == ' X |') & (b[12]==' X |') & (b[21]==' X |')) | ((b[3] == ' O |') & (b[12]==' O |') & (b[21]==' O |')):
            if player==player1:
                print('Player 1 is the winner!')
            else:
                print('Player 2 is the winner!')
            break

        # second column
        if ((b[4] == ' X |') & (b[13]==' X |') & (b[22]==' X |')) | ((b[4] == ' O |') & (b[13]==' O |') & (b[22]==' O |')):
            if player==player1:
                print('Player 1 is the winner!')
            else:
                print('Player 2 is the winner!')
            break

        # third column
        if ((b[5] == ' X  \n') & (b[14]==' X  \n') & (b[23]==' X  ')) | ((b[5] == ' O  \n') & (b[14]==' O  \n') & (b[23]==' O  ')):
            if player==player1:
                print('Player 1 is the winner!')
            else:
                print('Player 2 is the winner!')
            break

        # and lastly... diagonals
        # diagonal from top left to bottom right
        if ((b[3] == ' X |') & (b[13]==' X |') & (b[23]==' X  ')) | ((b[3] == ' O |') & (b[13]==' O |') & (b[23]==' O  ')):
            if player==player1:
                print('Player 1 is the winner!')
            else:
                print('Player 2 is the winner!')
            break

        # diagonal from top right to bottom left
        if ((b[5] == ' X  \n') & (b[13]==' X |') & (b[21]==' X |')) | ((b[5] == ' O |') & (b[13]==' O |') & (b[21]==' O |')):
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
                print('Player 1 turn')

        if len(stored_moves) == 9:
            print('Tie! There is no winner.')
            break

        error = False
        


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

