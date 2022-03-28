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
class Wordle:

    def __init__(self):
        self.glob_guesses = 6
        self.glob_letters = 5
        self.green_guessed_letters = []
        self.yellow_guessed_letters = []

    """ ----------- VEIT EKKI HVAÐ ÞÚ KALLAR ÞETTA ------------- """
    def get_word_list():
        with open("wordlist.txt", "r") as file:
            allText = file.read()
            words = list(map(str, allText.split()))
            return words

    def generate_word(self):
        """ Generate a 5 letter wordle from text file """
        word_list = self.get_word_list()
        word = (random.choice(word_list))
        return word.upper()

    def get_input(self):
        """ Get user input """
        guess_word = input("Enter your guess (5 letters): ") # Er hægt að gera bara upper() hér því þá er breytan alltaf í hástöfum og þarf ekki að declare-a það oftar?
        return guess_word.upper()

    """ ----------- CHECKS ------------- """
    def input_check(self, guess_word):
        """ Check if word meets requirements """
        if self.length_check(guess_word):
            if self.dictionary_check(guess_word):
                return True
            else:
                print("Word not in word list!")
                print()
                return False
        else:
            print("Word must be exactly 5 letters!")
            print()
            return False

    def length_check(self, guess_word):
        """ Check if word is 5 letters """
        if len(self, guess_word) == 5:
            return True
        return False

    def dictionary_check(self, guess_word):
        """ Check if word is in the english dictionary """
        if guess_word == spell.correction(guess_word):
            return True
        return False

    """ ----------- LOGIC -------------"""

    def print_guess_count(self, guess_counter):
        """ Print the current guess number in the appropriate color """
        global glob_guesses
        if (0.66 * glob_guesses) <= guess_counter <= glob_guesses:
            print(colored(f"GUESSES LEFT = {guess_counter}/{glob_guesses}",'green'))

        elif (0.33 * glob_guesses) <= guess_counter <= (0.66 * glob_guesses):
            print(colored(f"GUESSES LEFT = {guess_counter}/{glob_guesses}",'yellow'))

        if (0.00 * glob_guesses) <= guess_counter <= (0.33 * glob_guesses):
            print(colored(f"GUESSES LEFT = {guess_counter}/{glob_guesses}",'red'))

    def guess(self, guess_word, correct_word):
        if self.input_check(guess_word):
            self.print_result(guess_word, correct_word)
            return True
        else:
            return False

    def print_result(self, guess_word, correct_word):
        """ Main logic for checking letters and printing the Wordle """
        already_printed = [] # Safeguard to avoid printing a yellow letter 
        correct_letters_in_current_guess = [] # Safeguard to avoid printing a yellow letter if the letter is supposed to be green later in the word
        print("_" * 21)
        print("|", end="")
        duplicates = self.duplicate_letter_check(correct_word)

        for index, letter in enumerate(self, guess_word):
                if self.guess_word[index] == self.correct_word[index]:
                    correct_letters_in_current_guess.append(letter)

        for index, letter in enumerate(guess_word):
            
            if guess_word[index] == correct_word[index]:
                print(colored(f" {letter} ", 'white', 'on_green'), end = "|")
                self.green_guessed_letters.append(guess_word[index])
                if self.guess_word[index] not in duplicates:
                    already_printed.append(letter)

            elif letter in correct_word and letter not in already_printed and letter not in duplicates and letter not in correct_letters_in_current_guess:
                print(colored(f" {letter} ", 'white', 'on_yellow'), end = "|")
                already_printed.append(letter)
                self.yellow_guessed_letters.append(guess_word[index])

            else:
                print(colored(f" {letter} ", 'white',), end='|')
        print()
        print("‾" * 21)


    def duplicate_letter_check(self, correct_word):
        """ Return a list of the duplicate letters of correct word"""
        string = correct_word
        duplicates = []
        for char in string:
            if string.count(char) > 1:
                if char not in duplicates:
                    duplicates.append(char)
        return duplicates

    def eliminate_letters(self, guess_word, letters, correct_word):
        """ Remove already used letters from the letter list """
        for letter in guess_word:
            if letter in letters and letter not in correct_word:
                letters.remove(letter)
        return letters

    def print_letters(self, letters):
        """ Print the available letters; green if they are correct, yellow if correct but not in correct place """
        print("Available letters: ", end='')
        for letter in letters:
            if letter in self.green_guessed_letters:
                print(colored(letter, 'green'), end= ' ')
            elif letter in self.yellow_guessed_letters:
                print(colored(letter, 'yellow'), end= ' ')
            else:
                print(letter, end=' ')
        print()

    def win_check(self, guess_word, correct_word):
        """ Check if word matches and thus game is won """
        if guess_word == correct_word:
            return True
        return False

    def play_again(self, profile):
        """ Ask user if he wants to play again """
        play_again = input("Would you like to play again? (y/n): ")
        if play_again == "y":
            self.play_wordle(profile)
        if play_again == "n":
            return

    def play_wordle(self, profile):
        global glob_guesses
        #print_header()
        print('Logged in as: ' + profile)
        correct_word = self.generate_word()
        # correct_word = "shyly"
        guess_counter = glob_guesses # Max number of guesses
        guess_word = None
        letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        while guess_counter != 0:
            self.print_guess_count(guess_counter)
            guess_word = self.get_input()
            if self.guess(guess_word, correct_word):
                letters = self.eliminate_letters(guess_word, letters, correct_word)
                guess_counter -= 1
                self.print_letters(letters)
                if self.win_check(guess_word, correct_word):
                    print(colored("YOU WON! GOOD JOB!", 'green'))
                    self.write_score_to_file(profile, guess_counter, correct_word)
                    self.play_again(profile)
                    # if play_again():
                    #     return True
                    # else:
                    #     return False
            else:
                pass
        else:
            if self.win_check(guess_word, correct_word):
                print(colored("YOU WON! GOOD JOB!", 'green'))
                self.write_score_to_file(profile, guess_counter, correct_word)
                self.play_again(profile)
                # if play_again():
                #     return True
                # else:
                #     return False
            else:
                print(colored("YOU LOSE! SORRY", 'red'))
                print(f"The correct word was '{correct_word}'")
                self.play_again(profile)
                # if play_again():
                #     return True
                # else:
                #     return False

    def write_score_to_file(profile, guess_counter, correct_word):
        '''Creates text files to store player scores'''
        filename = profile + '.txt'         # Create full file name
        directory = "player_profiles/"      # Create full file path
        file_name_path = directory+filename
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        f = open(file_name_path, 'a')   # Opens file in append mode
        f.write(f"{dt_string}\nGuesses left: {guess_counter} Answer: {correct_word}\n")