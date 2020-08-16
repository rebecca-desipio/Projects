
#!/usr/bin/python3
import RPi.GPIO as GPIO
gameover = False

def single_player():
    import tictactoe_task1

def multi_player():
    import tictactoe_task2


play_tictactoe = input('Do you want to play tic-tac-toe? (y or n) ')
play_again = False
while gameover==False:
    try:
        if (play_tictactoe == 'y') | (play_again==True):
            num_of_players = input('How many players? (1 or 2): ')

            if num_of_players == '2':
                single_player()
            else:
                multi_player()

            play_again = input('Do you want to play again? (y or n) ')
            if play_again == 'y':
                gameover=False
            else:
                gameover=True
                print('See you next time!')
                GPIO.cleanup()

        else:
            print('See you next time!')


    except KeyboardInterrupt:
        GPIO.cleanup()