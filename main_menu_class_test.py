from email import header
import sys
import os
import time
from wordle_class_test import Wordle
from os.path import exists
from wordle_class_test import Wordle
from fancy_stuff import FancyStuff

# GLOBALS


class MainMenu:
    def __init__(self):
        self.max_guesses = 6
        self.word_letters = 5

    def print_header(self):
        print(FancyStuff().header)

    def print_main_menu(self):
        print(FancyStuff().menu_header)

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
        filename = profile + '.txt'         # Create full file name
        directory = "player_profiles/"      # Create full file path
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_name_path = directory+filename
        if exists(file_name_path):
            f = open(file_name_path, 'a')   # Opens file in write mode
            FancyStuff().clear_console()
            FancyStuff().load_wordle(profile) 
            return Wordle().play_wordle(profile)
        else:
            f = open(file_name_path, 'a')
            FancyStuff().clear_console()
            print('Profile created!')
            FancyStuff().load_wordle(profile)
            Wordle().play_wordle(profile)

    """ ----------- ADD WORDS ------------- """
    def add_option(self):
        print('What word would you like to append to the word bank?')
        word_bank_input = input('Input word: ')
        file = open('test_words.txt', 'a')
        if self.duplicate_word_check(word_bank_input):
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
            FancyStuff().clear_console()
            self.main_menu()
        else:
            print('Please enter a valid input')
            self.add_more_words()

    def duplicate_word_check(self, word):
        with open('test_words.txt', 'r') as file:
            words = file.read()
        if word not in words:
            return True
        else:
            return False

    """ ----------- EDIT OPTION ------------- """
    def edit_option(self):
        '''Edit game calls on two other functions'''
        global glob_guesses
        global glob_letters
        glob_guesses = self.edit_guesses()
        # glob_letters = edit_letters() # We don't wanna do this.

    def edit_guesses(self):
        '''Edit how many guesses'''
        self.max_guesses = input('How many guesses would you like to have? (1-6): ')
        if self.max_guesses_check(self.max_guesses):
            return int(self.max_guesses)
        else:
            print('Please enter a valid input')
            self.edit_guesses()

    def edit_letters(self):
        '''Edit length of word'''
        self.word_letters = input('How many letters would you like to guess? (1-6): ')
        if self.word_letters_check(self.word_letters):
            return int(self.word_letters)
        else:
            print('Please enter a valid input')
            self.edit_letters()

    def max_guesses_check(self):
        '''HELPER'''
        '''Checks if max_guesses is a digit between 1 and 6'''
        if self.max_guesses.isdigit():
            if int(self.max_guesses) > 0 and int(self.max_guesses) < 7:
                return True
            else:
                return False
        else:
            return False

    def word_letters_check(self):
        '''HELPER'''
        '''Checks if word_letters is a digit between 1 and 6'''
        if self.word_letters.isdigit():
            if int(self.word_letters) > 0 and int(self.word_letters) < 7:
                return True
            else:
                return False
        else:
            return False


""" ---------- MAIN PROGRAM ----------"""
def main():
    while True:
        FancyStuff().clear_console()
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