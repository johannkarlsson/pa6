#from spellchecker   import SpellChecker
from termcolor      import colored
from datetime       import datetime
import os
import random
import math
#spell = SpellChecker()

class Wordle:
    def __init__(self, profile, max_guesses = 5, letter_count = 5):
        self.profile = profile
        self.max_guesses = max_guesses # How many guesses are allowed
        self.letter_count = letter_count # How many letters we are playing
        self.guess_counter = self.max_guesses
        self.green_guessed_letters = [] # Keeps track of letters that should be printed green, when available letters are printed.
        self.yellow_guessed_letters = [] # Keeps track of letters that should be printed yellow, when available letters are printed.
        self.letters = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],[' ', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],[' ',' ', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']]
        self.correct_word = None
        self.guess_word = None
        self.duplicate_letters_in_correct_word = []
        self.win_count = 0
        self.loss_count = 0
        self.word_list = self.get_word_list()
        self.player_dir = 'player_profiles/'


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
        """ Generate a X letter wordle from text file """
        word_list = self.word_list
        word = (random.choice(word_list)).upper()
        return word


    """ ----------- MAIN GAME -----------"""
    def play_wordle(self):
        print('Logged in as: ' + self.profile)
        self.correct_word = self.generate_word()
        self.duplicate_letters_in_correct_word = self.duplicate_letter_check() # We must know if there are duplicate letters in the word. Those letters should not be added to the "already printed" list, since we want them to be yellow if guessed.
        self.guess_counter = self.max_guesses
        while self.guess_counter != 0:                      # Until all guesses are used up
            self.print_guess_count()                        # Print the amount of guesses left
            self.print_letters()                            # Print the letters that are available to the player
            self.guess_word = self.get_input()              # Get the guess from player
            if self.guess():                                # If the guess was legitimate:
                self.letters = self.eliminate_letters()     # remove the guessed letters from our pool of letters to show the player, since he has already used them
                self.guess_counter -= 1
                if self.win_check():                        # Check if win condition is met
                    self.resolve_win()                      # The win condition was met, we resolve the win and ask the player if he wants to play again
                    self.play_again()
                    return
            else:
                pass
        else:                                               # All guesses are used up
            if self.win_check():                            # The last guess could be correct, so we check
                self.resolve_win()
                self.play_again()
                return
            else:
                self.resolve_loss()                         #The last guess was not correct, resolve the loss
                self.play_again()
                return

    """ ----------- CHECKS ------------- """
    def input_check(self):
        """ Check if word meets requirements """
        if self.length_check(): # Check if the length requirement is met
            if self.dictionary_check(): # Check if the word is a real english word
                return True
            else:
                print()
                print(colored("Word not in word list!", 'red'))
                print()
                return False
        else:
            print()
            print(colored(f"Word must be exactly {self.letter_count} letters!", 'red'))
            print()
            return False

    def length_check(self):
        """ Check if word is length of letter_count """
        try:
            if len(self.guess_word) == self.letter_count:
                return True
            return False
        except TypeError:
            print()

    def dictionary_check(self):
        """ Check if word is in the english dictionary """
        if self.guess_word.lower() in self.word_list:
            return True
        return False

    """ ----------- LOGIC -------------"""
    def get_input(self):
        """ Get user input """
        try:
            guess_word = input(f"Enter your guess ({self.letter_count} letters): ").upper()
            return guess_word
        except KeyboardInterrupt: # Prófa vera fyndinn haha
            print()
            print("Ctrl+c huh? You won't get away this easily!")

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
        already_printed = []                # Keep track of letters that have already been printed, to avoid double counting that letter as a yellow letter later in the process
        green_letters_in_current_guess = [] # Safeguard to avoid printing a yellow letter if the letter is supposed to be green later in the word
        box = (4 * self.letter_count) + 1
        print("_" * box)
        print("|", end="")
        correct_word = self.correct_word
        guess_word = self.guess_word
        duplicates_printed = []
        
        for index, letter in enumerate(guess_word):                          # Begin by asserting which letter should be green. This is done to avoid letters being printed as yellow, when they should be green later in the word.
                if guess_word[index] == correct_word[index]:
                    green_letters_in_current_guess.append(letter)

        for index, letter in enumerate(guess_word):

            # THE LETTER IS A GREEN LETTER
            if guess_word[index] == correct_word[index]:    
                print(colored(f" {letter} ", 'grey', 'on_green'), end = "|")
                self.green_guessed_letters.append(letter)
                if guess_word[index] not in self.duplicate_letters_in_correct_word: # Add the letter to the already_printed list to avoid it being printed yellow later
                    already_printed.append(letter)
                else:                                                         # unless it is a duplicate letter.
                    duplicates_printed[letter] += 1                           # update how many instances of the duplicate letter have been printed
                    if duplicates_printed[letter] == self.duplicate_letters_in_correct_word[letter]:    # If the duplicate letter has been printed the correct number of times as yellow/green, add it to already printed, so it will be grey
                        already_printed.append(letter)

            # THE LETTER IS A YELLOW LETTER
            elif letter in correct_word and letter not in already_printed and letter not in green_letters_in_current_guess:
                print(colored(f" {letter} ", 'grey', 'on_yellow'), end = "|")
                if guess_word[index] not in self.duplicate_letters_in_correct_word: # Add the letter to the already_printed list to avoid it being printed yellow later, unless it is a duplicate letter.         # 
                    already_printed.append(letter)
                else:
                    duplicates_printed[letter] += 1                           # update how many instances of the duplicate letter have been printed
                    if duplicates_printed[letter] == self.duplicate_letters_in_correct_word[letter]:  # If the duplicate letter has been printed the correct number of times as yellow/green, add it to already printed, so it will be grey
                        already_printed.append(letter)
                self.yellow_guessed_letters.append(letter)

            # THE LETTER IS A YELLOW LETTER THAT IS ALSO A DUPLICATE
            elif letter in correct_word and letter not in already_printed and letter in self.duplicate_letters_in_correct_word:
                print(colored(f" {letter} ", 'grey', 'on_yellow'), end = "|")
                duplicates_printed[letter] += 1                               # update how many instances of the duplicate letter have been printed
                if duplicates_printed[letter] == self.duplicate_letters_in_correct_word[letter]:  # If the duplicate letter has been printed the correct number of times as yellow/green, add it to already printed, so it will be grey
                    already_printed.append(letter)
                self.yellow_guessed_letters.append(letter)
            
            # THE LETTER IS A GREY LETTER
            else:
                print(colored(f" {letter} ", 'white',), end='|')
        print()
        print("‾" * box)


    def duplicate_letter_check(self):
        """ Return a dictionary containing the correct word's duplicate letters and their count """
        string = self.correct_word
        count = 0
        duplicates = {}
        for char in string:             #  Get the duplicate letters
            if string.count(char) > 1:
                if char not in duplicates:
                    duplicates[char] = 0
        for char in string:
            if char in duplicates:      #  Get their count
                duplicates[char] += 1
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
        """ Print the available letters for guessing; green if they are correct, yellow if correct but not in correct place """
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
        file_name_path = self.player_dir+self.profile+'.txt' # Full path to file
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
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S") # To get the correct format: DD/MM/YYYY HH:MM:SS
        return dt_string

    def get_score(self):
        ''' Just something to score the game '''
        score = math.floor((((self.guess_counter + 1) * (1 / self.max_guesses)) * 1200) * len(self.correct_word)) # If you get it on the last guess of a 5 guess, 5 letter game --> ((1 * (1/5) * 1200) * 5) = 1200
        return score

    def reset_letters(self):
        '''Resets the letters to the original lists when you play again'''
        self.green_guessed_letters = []
        self.yellow_guessed_letters = []
        self.letters = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],[' ', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],[' ',' ', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']]

    def clear_console(self): # This is also in fancy_stuff.py but circular imports problems
        '''HELPER FUNCTION TO CLEAR SCREEN'''
        command = 'clear'
        if os.name in ('nt', 'dos'):
            command = 'cls'
        os.system(command)