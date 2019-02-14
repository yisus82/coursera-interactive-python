# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import random
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math

# initialize global variables used in your code

# The secret number the player has to guess
secret = 0

# The low end of the range
low = 0

# The high end of the range
high = 100

# The guesses the player has left
remaining_guesses = 7


# define helper functions

def max_guesses():
    """ Calculates the maximum guesses given to the player. """
    # The number of allowed guesses has to be the smallest
    # integer n such that 2 ** n >= high - low + 1
    # So we calculate the log in base 2 and round it up
    return math.ceil(math.log((high - low + 1), 2))


def gen_secret():
    """ Generates a secret number within the current range."""
    return random.randrange(low, high)


def init():
    """ Finish the current game and starts a new one. """
    global secret, remaining_guesses

    # Generate a new secret number
    secret = gen_secret()

    print("")
    print("New game. Range is from", low, "to", high)

    # Reset remaining guesses
    remaining_guesses = max_guesses()

    print("Number of remaining guesses is", remaining_guesses)


# define event handlers for control panel

def range100():
    # button that changes range to range [0,100) and restarts
    global low, high
    low = 0
    high = 100
    init()


def range1000():
    # button that changes range to range [0,1000) and restarts
    global low, high
    low = 0
    high = 1000
    init()


def get_input(guess):
    # main game logic goes here	

    # Translate text into number
    guess_number = int(guess)

    print("")
    print("Guess was", guess_number)

    # Substracts a guess from the remaining guesses
    global remaining_guesses
    remaining_guesses -= 1

    print("Number of remaining guesses is", remaining_guesses)

    # The player guesses right
    if guess_number == secret:
        print("Correct!")
        init()

    # The player has no guesses left
    elif remaining_guesses == 0:
        print("You ran out of guesses. The number was", secret)
        init()

    # The player guess is too high
    elif guess_number > secret:
        print("Lower!")

    # The player guess is too low
    elif guess_number < secret:
        print("Higher!")


# create frame
f = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements
f.add_button("Range is [0, 100)", range100, 200)
f.add_button("Range is [0, 1000)", range1000, 200)
f.add_input("Enter a guess", get_input, 200)

# start frame
f.start()

# Initiate game
init()
