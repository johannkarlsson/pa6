from email import header
import sys
import os
import time
from os.path import exists
from wordle_class_test import Wordle
from fancy_stuff import FancyStuff
from checks import Check

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
            self.print_player_history()
        elif menu_input == "5":
            quit()
        else:
            print("Please enter a valid input!")
            self.main_menu()

    def print_player_history(self):
        '''Prints all player profiles'''
        player_history = input("What player history would you like to see?: ").upper()
        filename = player_history + '.txt'
        directory = "player_profiles/"
        file_name_path = directory+filename
        if exists(file_name_path):
            with open(file_name_path, 'r') as f:
                print(f.read())
                anykey = input("Press enter to return to main menu: ")
        else:
            print('Player does not exist')
            self.print_player_history()


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
            FancyStuff().clear_console()
            FancyStuff().load_wordle(profile)
            return self.launch_wordle(profile)
        else:
            f = open(file_name_path, 'a')
            FancyStuff().clear_console()
            print('Profile created!')
            FancyStuff().load_wordle(profile)
            return self.launch_wordle(profile)

    def launch_wordle(self, profile):
        wordle = Wordle(self.max_guesses, self.word_letters)
        return wordle.play_wordle(profile)

    """ ----------- ADD WORDS ------------- """
    def add_option(self):
        print('What word would you like to append to the word bank?')
        word_bank_input = input('Input word: ')
        file = open('test_words.txt', 'a')
        if Check.duplicate_word_check(word_bank_input):
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

    """ ----------- EDIT OPTION ------------- """
    def edit_option(self):
        '''Edit game calls on two other functions'''
        self.max_guesses = self.edit_guesses()
        self.word_letters = self.edit_letters()

    def edit_guesses(self):
        '''Edit how many guesses'''
        max_guesses_input = input('How many guesses would you like to have? (1-10): ')
        if Check.max_guesses_check(max_guesses_input):
            return int(max_guesses_input)
        else:
            print('Please enter a valid input')
            self.edit_guesses()

    def edit_letters(self):
        '''Edit length of word'''
        word_letters_input = input('How many letters would you like to guess? (4-6): ')
        if Check.word_letters_check(word_letters_input):
            return int(word_letters_input)
        else:
            print('Please enter a valid input')
            self.edit_letters()

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