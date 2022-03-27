import os
from os.path import exists
import sys
import time

def main_menu_print():
    main_menu ="""
----------------------------------------------------------

                        MAIN MENU

1. Play     2. Add Words     3. Edit Game         4. Quit

----------------------------------------------------------
"""
    print(main_menu)

def main_menu_input():
    main_menu_print()
    menu_input = input("Please select an option: ")
    if menu_input == "1":
        play_game()
    elif menu_input == "2":
        add_words()
    elif menu_input == "3":
        edit_game()
    elif menu_input == "4":
        return
    else:
        print("Please enter a valid input")
        main_menu_input()

def edit_game():
    max_guesses = input('How many guesses would you like to have? (1-6): ')
    word_letters = input('How many letters would you like to guess? (1-6): ')


def change_max_guesses():
    pass

def play_game():
    print('User chose 1')
    login_profile()

def login_profile(): # Spyr notanda um nafn hans til að búa til skrá
    profile = input("Please enter your profile name: ").upper()
    create_player_file(profile)

def create_player_file(profile): # Býr til skjal með profile name, hægt að setja scores þangað
    filename = profile + '.txt'
    directory = "player_profiles/"
    if not os.path.exists(directory):
       os.makedirs(directory)

    file_name_path = directory+filename
    if exists(file_name_path):
        clear_console()
        print('Logging in as ' + profile)
        load_wordle() 
    else:
        f = open(file_name_path, 'w')
        clear_console()
        print('Profile created!')
        print('Logging in as ' + profile)
        load_wordle()


def load_wordle():
    animation = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]

    for i in range(len(animation)):
        time.sleep(0.2)
        sys.stdout.write("\r" + animation[i % len(animation)])
        sys.stdout.flush()

    print("\n")
    play_wordle()

def clear_console():
    '''HELPER FUNCTION TO CLEAR SCREEN'''
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


def play_wordle():
    clear_console()
    print('playing wordle hans jóa sæta')




def add_more_words():
    prompt = input('Would you like to add another word? (y/n): ').lower()
    if prompt == 'y':
        add_words()
    elif prompt == 'n':
        main_menu_input()
    else:
        print('Please enter a valid input')
        add_more_words()

def add_words():
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

def duplicate_word_check(word):
    with open('test_words.txt', 'r') as file:
        words = file.read()
    if word not in words:
        return True
    else:
        return False









main_menu_input()