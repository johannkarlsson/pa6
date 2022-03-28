from email import header
import sys
import os
import time
from os.path import exists
from wordle_class_test import Wordle
from fancy_stuff import FancyStuff
fancy_stuff = FancyStuff()
from checks import Check
check = Check()

# GLOBALS


class MainMenu:
    def __init__(self):
        self.max_guesses = 6
        self.word_letters = 5

    def print_header(self):
        print(fancy_stuff.header)

    def print_main_menu(self):
        print(fancy_stuff.menu_header)

    def main_menu(self):
        self.print_main_menu()
        menu_input = input("Please select an option: ")
        if menu_input == "1":
            return self.play_option()
        elif menu_input == "2":
            self.add_option()
        elif menu_input == "3":
            self.edit_option()
            self.main_menu()
        elif menu_input == "4":
            quit()
        else:
            print("Please enter a valid input!")
            self.main_menu()

    """ ----------- LOGIN OPTION ------------- """
    def play_option(self): # Spyr notanda um nafn hans til að búa til skrá
        profile = input("Please enter your profile name: ").upper()
        return self.create_player_file(profile)

    def create_player_file(self, profile):
        '''Creates text files to store player scores'''
        #wordle = Wordle(self.max_guesses, self.word_letters)
        filename = profile + '.txt'         # Create full file name
        directory = "player_profiles/"      # Create full file path
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_name_path = directory+filename
        if exists(file_name_path):
            f = open(file_name_path, 'a')   # Opens file in append mode
            fancy_stuff.clear_console()
            fancy_stuff.load_wordle(profile)
            return self.launch_wordle(profile)
        else:
            f = open(file_name_path, 'a')
            fancy_stuff.clear_console()
            print('Profile created!')
            fancy_stuff.load_wordle(profile)
            return self.launch_wordle(profile)

    def launch_wordle(self, profile):
        wordle = Wordle(self.max_guesses, self.word_letters)
        return wordle.play_wordle(profile)

    """ ----------- ADD WORDS ------------- """
    def add_option(self):
        print('What word would you like to append to the word bank?')
        word_bank_input = input('Input word: ')
        file = open('test_words.txt', 'a')
        if check.duplicate_word_check(word_bank_input):
            file.write(word_bank_input + '\n')
            print(f'"{word_bank_input}" added to word bank')
            file.close() # Uppfærist með hverju instance-i. Annars var það bara þegar forritið hættir keyrslu
            self.add_more_words()
        else:
            print('Word already in word bank')
            self.add_more_words()

    def add_more_words(self):
        prompt = input('Would you like to add another word? (y/n): ').lower()
        if prompt == 'y':
            self.add_option()
        elif prompt == 'n':
            fancy_stuff.clear_console()
            self.main_menu()
        else:
            print('Please enter a valid input')
            self.add_more_words()

    """ ----------- EDIT OPTION ------------- """
    def edit_option(self):
        '''Edit game calls on two other functions'''
        self.max_guesses = self.edit_guesses()
        self.word_letters = self.edit_letters()

    def edit_guesses(self):
        '''Edit how many guesses'''
        max_guesses_input = input('How many guesses would you like to have? (1-10): ')
        if check.max_guesses_check(max_guesses_input):
            return int(max_guesses_input)
        else:
            print('Please enter a valid input')
            self.edit_guesses()

    def edit_letters(self):
        '''Edit length of word'''
        word_letters_input = input('How many letters would you like to guess? (4-6): ')
        if check.word_letters_check(word_letters_input):
            return int(word_letters_input)
        else:
            print('Please enter a valid input')
            self.edit_letters()

""" ---------- MAIN PROGRAM ----------"""
def main():
    while True:
        fancy_stuff.clear_console()
        main_menu = MainMenu()
        main_menu.main_menu()
    else:
        quit()
        

""" MAIN LOOP """
while True:
    if main():
        pass
    else:
        break