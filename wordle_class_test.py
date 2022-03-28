# from colorama import init

#from glob import glob
from threading      import get_ident
from spellchecker   import SpellChecker
from os.path        import exists
from termcolor      import colored
from datetime       import datetime
import sys
import os
import time
import random
import math
spell = SpellChecker()
#TODO
# Búa til menu, play eða edit CHECK
# Leyfa logins, profiles CHECK
# Finna hvernig við score-um leikinn
# Geyma scores með profile name í txt skjali CHECK
# Leyfa breytingum á leik, til dæmis 4 stafa orð og bara 3 gisk MAYBE CHECK???
# Giska rett í síðasta en fæ you lose
class Wordle:
    def __init__(self, profile, max_guesses = 6, letter_count = 5):
        self.profile = profile
        self.max_guesses = max_guesses
        self.letter_count = letter_count
        self.guess_counter = self.max_guesses
        self.green_guessed_letters = []
        self.yellow_guessed_letters = []
        self.letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        self.correct_word = None
        self.guess_word = None
        self.win_count = 0
        self.loss_count = 0
        self.word_list = self.get_word_list()


    """ ----------- VEIT EKKI HVAÐ ÞÚ KALLAR ÞETTA ------------- """
    def get_word_list(self):
        word_bank = f'wordlist_{len(self.letter_count)}.txt'
        with open(word_bank, "r") as file:
            allText = file.read()
            words = list(map(str, allText.split()))
            return words

    def generate_word(self):
        """ Generate a 5 letter wordle from text file """
        word_list = self.word_list
        word = (random.choice(word_list)).upper()
        return word

    def get_input(self):
        """ Get user input """
        guess_word = input(f"Enter your guess ({self.letter_count} letters): ").upper() # Er hægt að gera bara upper() hér því þá er breytan alltaf í hástöfum og þarf ekki að declare-a það oftar?
        return guess_word

    """ ----------- CHECKS ------------- """
    def input_check(self):
        """ Check if word meets requirements """
        if self.length_check():
            if self.dictionary_check():
                return True
            else:
                print("Word not in word list!")
                print()
                return False
        else:
            print("Word must be exactly 5 letters!")
            print()
            return False

    def length_check(self):
        """ Check if word is length of letter_count """
        if len(self.guess_word) == self.letter_count:
            return True
        return False

    def dictionary_check(self):
        """ Check if word is in the english dictionary """
        if self.guess_word == spell.correction(self.guess_word):
            return True
        return False

    """ ----------- LOGIC -------------"""

    def print_guess_count(self):
        """ Print the current guess number in the appropriate color """
        #global max_guesses
        if (0.66 * self.max_guesses) <= self.guess_counter <= self.max_guesses:
            print(colored(f"GUESSES LEFT = {self.guess_counter}/{self.max_guesses}",'green'))

        elif (0.33 * self.max_guesses) <= self.guess_counter <= (0.66 * self.max_guesses):
            print(colored(f"GUESSES LEFT = {self.guess_counter}/{self.max_guesses}",'yellow'))

        if (0.00 * self.max_guesses) <= self.guess_counter <= (0.33 * self.max_guesses):
            print(colored(f"GUESSES LEFT = {self.guess_counter}/{self.max_guesses}",'red'))

    def guess(self):
        if self.input_check():
            self.print_result()
            return True
        else:
            return False

    def print_result(self):
        """ Main logic for checking letters and printing the Wordle """
        already_printed = [] # Safeguard to avoid printing a yellow letter 
        correct_letters_in_current_guess = [] # Safeguard to avoid printing a yellow letter if the letter is supposed to be green later in the word
        print("_" * 21)
        print("|", end="")
        correct_word = self.correct_word
        guess_word = self.guess_word
        duplicates = self.duplicate_letter_check()

        for index, letter in enumerate(guess_word):
                if guess_word[index] == correct_word[index]:
                    correct_letters_in_current_guess.append(letter)

        for index, letter in enumerate(guess_word):
            
            if guess_word[index] == correct_word[index]:
                print(colored(f" {letter} ", 'white', 'on_green'), end = "|")
                self.green_guessed_letters.append(guess_word[index])
                if guess_word[index] not in duplicates:
                    already_printed.append(letter)

            elif letter in correct_word and letter not in already_printed and letter not in duplicates and letter not in correct_letters_in_current_guess:
                print(colored(f" {letter} ", 'white', 'on_yellow'), end = "|")
                already_printed.append(letter)
                self.yellow_guessed_letters.append(guess_word[index])

            else:
                print(colored(f" {letter} ", 'white',), end='|')
        print()
        print("‾" * 21)


    def duplicate_letter_check(self):
        """ Return a list of the duplicate letters of correct word"""
        string = self.correct_word
        duplicates = []
        for char in string:
            if string.count(char) > 1:
                if char not in duplicates:
                    duplicates.append(char)
        return duplicates

    def eliminate_letters(self):
        """ Remove already used letters from the letter list """
        for letter in self.guess_word:
            if letter in self.letters and letter not in self.correct_word:
                self.letters.remove(letter)
        return self.letters

    def print_letters(self):
        """ Print the available letters; green if they are correct, yellow if correct but not in correct place """
        print("Available letters: ", end='')
        for letter in self.letters:
            if letter in self.green_guessed_letters:
                print(colored(letter, 'green'), end= ' ')
            elif letter in self.yellow_guessed_letters:
                print(colored(letter, 'yellow'), end= ' ')
            else:
                print(letter, end=' ')
        print()

    def win_check(self):
        """ Check if word matches and thus game is won """
        if self.guess_word == self.correct_word:
            return True
        return False

    def play_again(self):
        """ Ask user if he wants to play again """
        play_again_input = input("Would you like to play again? (y/n): ").lower()
        if play_again_input == "y":
            self.clear_console()
            self.play_wordle()
        if play_again_input == "n":
            return

    def play_wordle(self):
        print('Logged in as: ' + self.profile)
        self.correct_word = self.generate_word()
        # self.correct_word = "FLAME"
        self.guess_counter = self.max_guesses
        while self.guess_counter != 0:
            self.print_guess_count()
            self.guess_word = self.get_input()
            if self.guess():
                self.letters = self.eliminate_letters()
                self.guess_counter -= 1
                self.print_letters()
                if self.win_check():
                    self.resolve_win()
                    self.play_again()
                    return
            else:
                pass
        else:
            if self.win_check():
                self.resolve_win()
                self.play_again()
                return
            else:
                self.resolve_loss()
                self.play_again()
                return

    def resolve_win(self):
                self.win_count += 1
                print(colored("YOU WON! GOOD JOB!", 'green'))
                print(f"Current session record: W:{self.win_count} L: {self.loss_count}")
                self.write_score_to_file()
    
    def resolve_loss(self):
                print(colored("YOU LOSE! SORRY", 'red'))
                self.loss_count += 1
                print(f"The correct word was '{self.correct_word}'")
                print(f"Current session record: W:{self.win_count} L: {self.loss_count}")
                self.write_score_to_file()

    def write_score_to_file(self):
        '''Creates text files to store player scores'''
        filename = self.profile + '.txt'         # Create full file name
        directory = "player_profiles/"      # Create full file path
        file_name_path = directory+filename
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        # score = (self.guess_counter + 1) * 10 * len(self.correct_word)
        score = math.floor(((self.guess_counter + 1) / (self.max_guesses)) * 100 * len(self.correct_word))
        f = open(file_name_path, 'a')   # Opens file in append mode
        f.write(f"{dt_string}\nGuesses left: {self.guess_counter} Answer: {self.correct_word}\nScore: {score}\n-----------------------------------------------\n")

    def clear_console(self):
        '''HELPER FUNCTION TO CLEAR SCREEN'''
        command = 'clear'
        if os.name in ('nt', 'dos'):
            command = 'cls'
        os.system(command)