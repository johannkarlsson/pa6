from spellchecker   import SpellChecker
from termcolor      import colored
from datetime       import datetime
import os
import random
import math
spell = SpellChecker()

class Wordle:
    def __init__(self, profile, max_guesses = 5, letter_count = 5):
        self.profile = profile
        self.max_guesses = max_guesses
        self.letter_count = letter_count
        self.guess_counter = self.max_guesses
        self.green_guessed_letters = []
        self.yellow_guessed_letters = []
        self.letters = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],[' ', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],[' ',' ', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']]
        self.correct_word = None
        self.guess_word = None
        self.win_count = 0
        self.loss_count = 0
        self.word_list = self.get_word_list()


    """ ----------- STARTUP ------------- """
    def get_word_list(self):
        word_bank = f'wordlist_{self.letter_count}.txt'
        directory = "wordlists/"
        file_name_path = directory+word_bank
        with open(file_name_path, "r") as file:
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
        guess_word = input(f"Enter your guess ({self.letter_count} letters): ").upper()
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
            print(f"Word must be exactly {self.letter_count} letters!")
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
        box = (4 * self.letter_count) + 1
        print("_" * box)
        print("|", end="")
        correct_word = self.correct_word
        guess_word = self.guess_word
        duplicates = self.duplicate_letter_check()

        for index, letter in enumerate(guess_word):
                if guess_word[index] == correct_word[index]:
                    correct_letters_in_current_guess.append(letter)

        for index, letter in enumerate(guess_word):
            
            if guess_word[index] == correct_word[index]:
                print(colored(f" {letter} ", 'grey', 'on_green'), end = "|")
                self.green_guessed_letters.append(guess_word[index])
                if guess_word[index] not in duplicates:
                    already_printed.append(letter)

            elif letter in correct_word and letter not in already_printed and letter not in duplicates and letter not in correct_letters_in_current_guess:
                print(colored(f" {letter} ", 'grey', 'on_yellow'), end = "|")
                already_printed.append(letter)
                self.yellow_guessed_letters.append(guess_word[index])

            else:
                print(colored(f" {letter} ", 'white',), end='|')
        print()
        print("‾" * box)


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
        ''' Replaces guessed letters with spaces to keep the keyboard layout intact '''
        for letter in self.guess_word:
            for lst in self.letters:
                if letter in lst and letter not in self.correct_word:
                    index = lst.index(letter)
                    lst[index] = ' '
        return self.letters

    def print_letters(self):
        """ Print the available letters; green if they are correct, yellow if correct but not in correct place """
        print("Available letters: ")
        for row in self.letters: # For each row in the keyboard
            for letter in row: # For each letter in the row
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
            self.reset_letters()
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
        '''Keeps count of wins during current session'''
        self.win_count += 1
        print(colored("YOU WON! GOOD JOB!", 'green'))
        print(f"Current session record: W: {self.win_count} L: {self.loss_count}")
        self.write_score_to_file('W')
    
    def resolve_loss(self):
        '''Keeps count of losses during current session'''
        self.loss_count += 1
        print(colored("YOU LOSE! SORRY", 'red'))
        print(f"The correct word was '{self.correct_word}'")
        print(f"Current session record: W: {self.win_count} L: {self.loss_count}")
        self.write_score_to_file('L')

    def write_score_to_file(self, w_or_l):
        '''Creates text files to store player scores'''
        file_name_path = self.get_player_file_name_path()
        dt_string = self.get_current_date_time()
        score = self.get_score()
        f = open(file_name_path, 'a')   # Opens file in append mode
        if w_or_l == 'W':
            f.write(f"\n*WIN*\n{dt_string}\nGuesses used: {self.max_guesses - self.guess_counter}/{self.max_guesses} Answer: {self.correct_word}\nScore: {score}\n-----------------------------------------------\n")
        else:
            f.write(f"\n*LOSS*\n{dt_string}\nGuesses used: {self.max_guesses - self.guess_counter}/{self.max_guesses} Answer: {self.correct_word}\nScore: 0\n-----------------------------------------------\n")

    def get_current_date_time(self):
        '''Returns current date and time'''
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        return dt_string

    def get_player_file_name_path(self):
        '''Returns the full file path of the player profile'''
        filename = self.profile + '.txt'         # Create full file name
        directory = "player_profiles/"      # Create full file path
        file_name_path = directory+filename
        return file_name_path

    def get_score(self):
        score = math.floor((((self.guess_counter + 1) * (1 / self.max_guesses)) * 1200) * len(self.correct_word))
        return score

    def reset_letters(self):
        '''Resets the letters to the original lists when you play again'''
        self.green_guessed_letters = []
        self.yellow_guessed_letters = []
        self.letters = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],[' ', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],[' ',' ', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']]


    def clear_console(self):
        '''HELPER FUNCTION TO CLEAR SCREEN'''
        command = 'clear'
        if os.name in ('nt', 'dos'):
            command = 'cls'
        os.system(command)