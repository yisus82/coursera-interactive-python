# Rock-paper-scissors-lizard-Spock template


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

import random


# helper functions

def number_to_name(number):
    # fill in your code below

    # convert number to a name using if/elif/else
    # don't forget to return the result!
    if number == 0:
        return "rock"
    elif number == 1:
        return "Spock"
    elif number == 2:
        return "paper"
    elif number == 3:
        return "lizard"
    elif number == 4:
        return "scissors"
    else:
        return "Invalid number!"


def name_to_number(name):
    # fill in your code below

    # convert name to number using if/elif/else
    # don't forget to return the result!
    if name == "rock":
        return 0
    elif name == "Spock":
        return 1
    elif name == "paper":
        return 2
    elif name == "lizard":
        return 3
    elif name == "scissors":
        return 4
    else:
        return "Invalid name!"


def rpsls(name):
    # fill in your code below

    # print the player's guess
    print("Player chooses", name)
    # convert name to player_number using name_to_number
    player_number = name_to_number(name)
    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0, 5)
    # convert comp_number to comp_name using number_to_name
    comp_name = number_to_name(comp_number)
    # print the computer's guess
    print("Computer chooses", comp_name)
    # compute difference of player_number and comp_number modulo five
    difference = (player_number - comp_number) % 5
    # use if/elif/else to determine winner
    if difference == 0:
        print("Player and computer tie!")
    elif difference == 1 or difference == 2:
        print("Player wins!")
    elif difference == 3 or difference == 4:
        print("Computer wins!")
    else:
        print("Error!")
    print("")


# test your code
option = input("Choose your move (rock, Spock, paper, lizard, scissors: ")
while option != "":
    rpsls(option)
    option = input("Choose your move (rock, Spock, paper, lizard, scissors: ")
