from threading import get_ident
from spellchecker import SpellChecker
import sys
# from colorama import init
from termcolor import colored
spell = SpellChecker()
import random

#TODO
# Búa til menu, play eða edit
# Leyfa logins, profiles
# Geyma scores með profile name í txt skjali
# Leyfa breytingum á leik, til dæmis 4 stafa orð og bara 3 gisk
# Giska rett í síðasta en fæ you lose

# CONSTANTS
MAX_GUESSES = 6 # PLACEHOLDER fyrir variable frá input úr edit game fallinu úr main menu


green_guessed_letters = []
yellow_guessed_letters = []

def print_header():
    header = """
----------------------------------

WELCOME TO WORDLE - PYTHON EDITION
    Author - Jóhann Karlsson

----------------------------------
"""
    print(header)

def get_word_list():
    with open("wordlist.txt", "r") as file:
        allText = file.read()
        words = list(map(str, allText.split()))
        return words

def generate_word():
    """ Generate a 5 letter wordle from text file """
    word_list = get_word_list()
    return (random.choice(word_list))

def get_input():
    """ Get user input """
    guess_word = input("Enter your guess (5 letters): ")
    return guess_word

""" ----------- CHECKS ------------- """
def input_check(guess_word):
    """ Check if word meets requirements """
    if length_check(guess_word):
        if dictionary_check(guess_word):
            return True
        else:
            print("Word not in word list!")
            print()
            return False
    else:
        print("Word must be exactly 5 letters!")
        print()
        return False

def length_check(guess_word):
    """ Check if word is 5 letters """
    if len(guess_word) == 5:
        return True
    return False

def dictionary_check(guess_word):
    """ Check if word is in the english dictionary """
    if guess_word == spell.correction(guess_word):
        return True
    return False

""" ----------- LOGIC -------------"""

def print_guess_count(guess_counter):
    """ Print the current guess number in the appropriate color """
    if (0.66 * MAX_GUESSES) <= guess_counter <= MAX_GUESSES: # Sama og 4/6, 5/6, 6/6
        print(colored(f"GUESSES LEFT = {guess_counter}/{MAX_GUESSES}",'green'))

    elif (0.33 * MAX_GUESSES) <= guess_counter <= (0.5 * MAX_GUESSES):
        print(colored(f"GUESSES LEFT = {guess_counter}/{MAX_GUESSES}",'yellow'))

    if guess_counter == 1:
        print(colored(f"GUESSES LEFT = {guess_counter}/{MAX_GUESSES}",'red'))

def guess(guess_word, correct_word):
    if input_check(guess_word):
        print_result(guess_word, correct_word)
        return True
    else:
        return False

def print_result(guess_word, correct_word):
    """ Main logic for checking letters and printing the Wordle """
    already_printed = []
    correct_letters_in_current_guess = []
    print("_" * 21)
    print("|", end="")
    duplicates = duplicate_letter_check(correct_word)

    for index, letter in enumerate(guess_word):
            if guess_word[index].upper() == correct_word[index].upper():
                correct_letters_in_current_guess.append(letter.upper())

    for index, letter in enumerate(guess_word):
        if guess_word[index].upper() == correct_word[index].upper():
            print(colored(f" {letter.upper()} ", 'white', 'on_green'), end = "|")
            green_guessed_letters.append(guess_word[index].upper())
            if guess_word[index].upper() not in duplicates:
                already_printed.append(letter.upper())

        elif letter.upper() in correct_word.upper() and letter.upper() not in already_printed and letter.upper() not in duplicates and letter.upper() not in correct_letters_in_current_guess:
            print(colored(f" {letter.upper()} ", 'white', 'on_yellow'), end = "|")
            already_printed.append(letter.upper())
            yellow_guessed_letters.append(guess_word[index].upper())
        # elif letter.upper() in correct_word.upper() and letter.upper() not in already_printed:
        #     print(colored(f" {letter.upper()} ", 'white', 'on_yellow'), end = "|")
        else:
            print(colored(f" {letter.upper()} ", 'white',), end='|')
    print()
    print("‾" * 21)


def duplicate_letter_check(correct_word):
    """ Return a list of the duplicate letters of correct word"""
    string = correct_word
    duplicates = []
    for char in string:
        if string.count(char) > 1:
            if char.upper() not in duplicates:
                duplicates.append(char.upper())
    return duplicates

def eliminate_letters(guess_word, letters, correct_word):
    """ Remove already used letters from the letter list """
    for letter in guess_word:
        if letter.upper() in letters and letter not in correct_word:
            letters.remove(letter.upper())
    return letters

def print_letters(letters):
    """ Print the available letters; green if they are correct, yellow if correct but not in correct place """
    print("Available letters: ", end='')
    for letter in letters:
        if letter in green_guessed_letters:
            print(colored(letter.upper(), 'green'), end= ' ')
        elif letter in yellow_guessed_letters:
            print(colored(letter.upper(), 'yellow'), end= ' ')
        else:
            print(letter.upper(), end=' ')
    print()

def win_check(guess_word, correct_word):
    """ Check if word matches and thus game is won """
    if guess_word == correct_word:
        return True
    return False

def play_again():
    """ Ask user if he wants to play again """
    play_again = input("Would you like to play again? (y/n): ")
    if play_again == "y":
        return True
    if play_again == "n":
        return False



""" ---------- MAIN PROGRAM ----------"""
def main():
    print_header()
    correct_word = generate_word()
    #correct_word = "shyly"
    guess_counter = MAX_GUESSES # Set the guess counter to max guesses
    guess_word = None
    letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    while guess_counter != 0:
        print_guess_count(guess_counter)
        guess_word = get_input()
        if guess(guess_word, correct_word):
            letters = eliminate_letters(guess_word, letters, correct_word)
            guess_counter -= 1
            print_letters(letters)
            if win_check(guess_word, correct_word):
                print(colored("YOU WON! GOOD JOB!", 'green'))
                if play_again():
                    return True
                else:
                    return False
        else:
            pass
    else:
        if win_check(guess_word, correct_word):
            print(colored("YOU WON! GOOD JOB!", 'green'))
            if play_again():
                return True
            else:
                return False
        else:
            print(colored("YOU LOSE! SORRY", 'red'))
            print(f"The correct word was '{correct_word}'")
            if play_again():
                return True
            else:
                return False



""" MAIN LOOP """
while True:
    if main():
        pass
    else:
        break
