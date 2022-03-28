# from colorama import init
from glob import glob
from threading      import get_ident
from spellchecker   import SpellChecker
from os.path        import exists
from termcolor      import colored
from datetime       import datetime
import sys
import os
import time
import random
spell = SpellChecker()

#TODO
# Búa til menu, play eða edit CHECK
# Leyfa logins, profiles CHECK
# Finna hvernig við score-um leikinn
# Geyma scores með profile name í txt skjali CHECK
# Leyfa breytingum á leik, til dæmis 4 stafa orð og bara 3 gisk MAYBE CHECK???
# Giska rett í síðasta en fæ you lose

# CONSTANTS
# MAX_GUESSES = 5 # PLACEHOLDER fyrir variable frá input úr edit game fallinu úr main menu

# GLOBALS
glob_guesses = 5
glob_letters = 5


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

def print_main_menu():
    main_menu ="""
----------------------------------------------------------

                        MAIN MENU

1. Play      2. Add Words      3. Edit Game       4. Quit

----------------------------------------------------------
"""
    print(main_menu)

def main_menu():
    print_main_menu()
    menu_input = input("Please select an option: ")
    if menu_input == "1":
        play_option()
    elif menu_input == "2":
        add_option()
    elif menu_input == "3":
        edit_option()
        main_menu()
    elif menu_input == "4":
        return
    else:
        print("Please enter a valid input")
        main_menu()

""" ----------- FUN STUFF ------------- """
def load_wordle(profile):
    '''ANIMATION FUNCTION'''
    print('Logging in as ' + profile)
    animation = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]
    for i in range(len(animation)):
        time.sleep(0.2)
        sys.stdout.write("\r" + animation[i % len(animation)])
        sys.stdout.flush()
    print("\n")
    play_wordle(profile)

def clear_console():
    '''HELPER FUNCTION TO CLEAR SCREEN'''
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

""" ----------- LOGIN OPTION ------------- """
def play_option():
    print('User chose 1 -- PLACEHOLDER DÓT')
    print('Þarf ekkert þetta fall held ég, þetta er bara milliliður')
    login_profile()

def login_profile(): # Spyr notanda um nafn hans til að búa til skrá
    profile = input("Please enter your profile name: ").upper()
    create_player_file(profile)

def create_player_file(profile):
    '''Creates text files to store player scores'''
    filename = profile + '.txt'         # Create full file name
    directory = "player_profiles/"      # Create full file path
    if not os.path.exists(directory):
       os.makedirs(directory)
    file_name_path = directory+filename
    if exists(file_name_path):
        f = open(file_name_path, 'a')   # Opens file in write mode
        clear_console()
        load_wordle(profile) 
    else:
        f = open(file_name_path, 'a')
        clear_console()
        print('Profile created!')
        load_wordle(profile)

""" ----------- ADD WORDS ------------- """
def add_option():
    print('What word would you like to append to the word bank?')
    word_bank_input = input('Input word: ')
    file = open('test_words.txt', 'a')
    if duplicate_word_check(word_bank_input):
        file.write(word_bank_input + '\n')
        print(f'"{word_bank_input}" added to word bank')
        file.close() # Uppfærist með hverju instance-i. Annars var það bara þegar forritið hættir keyrslu
        add_more_words()
    else:
        print('Word already in word bank')
        add_more_words()

def add_more_words():
    prompt = input('Would you like to add another word? (y/n): ').lower()
    if prompt == 'y':
        add_option()
    elif prompt == 'n':
        main_menu()
    else:
        print('Please enter a valid input')
        add_more_words()

def duplicate_word_check(word):
    with open('test_words.txt', 'r') as file:
        words = file.read()
    if word not in words:
        return True
    else:
        return False

""" ----------- EDIT OPTION ------------- """
def edit_option():
    '''Edit game calls on two other functions'''
    global glob_guesses
    global glob_letters
    glob_guesses = edit_guesses()
    glob_letters = edit_letters()

def edit_guesses():
    '''Edit how many guesses'''
    max_guesses = input('How many guesses would you like to have? (1-6): ')
    if max_guesses_check(max_guesses):
        return max_guesses
    else:
        print('Please enter a valid input')
        edit_guesses()

def edit_letters():
    '''Edit length of word'''
    word_letters = input('How many letters would you like to guess? (1-6): ')
    if word_letters_check(word_letters):
        return word_letters
    else:
        print('Please enter a valid input')
        edit_letters()

def max_guesses_check(max_guesses):
    '''HELPER'''
    '''Checks if max_guesses is a digit between 1 and 6'''
    if max_guesses.isdigit():
        if int(max_guesses) > 0 and int(max_guesses) < 7:
            return True
        else:
            return False
    else:
        return False

def word_letters_check(word_letters):
    '''HELPER'''
    '''Checks if word_letters is a digit between 1 and 6'''
    if word_letters.isdigit():
        if int(word_letters) > 0 and int(word_letters) < 7:
            return True
        else:
            return False
    else:
        return False

""" ----------- VEIT EKKI HVAÐ ÞÚ KALLAR ÞETTA ------------- """
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
    guess_word = input("Enter your guess (5 letters): ").upper() # Er hægt að gera bara upper() hér því þá er breytan alltaf í hástöfum og þarf ekki að declare-a það oftar?
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
    global glob_guesses
    if (0.66 * glob_guesses) <= guess_counter <= glob_guesses:
        print(colored(f"GUESSES LEFT = {guess_counter}/{glob_guesses}",'green'))

    elif (0.33 * glob_guesses) <= guess_counter <= (0.66 * glob_guesses):
        print(colored(f"GUESSES LEFT = {guess_counter}/{glob_guesses}",'yellow'))

    if (0.00 * glob_guesses) <= guess_counter <= (0.33 * glob_guesses):
        print(colored(f"GUESSES LEFT = {guess_counter}/{glob_guesses}",'red'))

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
    if guess_word == correct_word.upper():
        return True
    return False

def play_again():
    """ Ask user if he wants to play again """
    play_again = input("Would you like to play again? (y/n): ")
    if play_again == "y":
        return True
    if play_again == "n":
        return False

def play_wordle(profile):
    global glob_guesses
    print_header()
    print('Logged in as: ' + profile)
    correct_word = generate_word()
    # correct_word = "shyly"
    guess_counter = glob_guesses # Max number of guesses
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
                write_score_to_file(profile, guess_counter, correct_word)
                if play_again():
                    return True
                else:
                    return False
        else:
            pass
    else:
        if win_check(guess_word, correct_word):
            print(colored("YOU WON! GOOD JOB!", 'green'))
            write_score_to_file(profile, guess_counter, correct_word)
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

def write_score_to_file(profile, guess_counter, correct_word):
    '''Creates text files to store player scores'''
    filename = profile + '.txt'         # Create full file name
    directory = "player_profiles/"      # Create full file path
    file_name_path = directory+filename
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    f = open(file_name_path, 'a')   # Opens file in append mode
    f.write(f"{dt_string}\nGuesses left: {guess_counter} Answer: {correct_word.upper()}\n")



""" ---------- MAIN PROGRAM ----------"""
def main():
    main_menu()

""" MAIN LOOP """
while True:
    if main():
        pass
    else:
        break
