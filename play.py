import time
import os
from os.path                import exists
from modules.wordle_game    import Wordle
from modules.fancy_stuff    import FancyStuff
from modules.checks         import Check
check = Check()
fancy_stuff = FancyStuff()

class MainMenu:
    def __init__(self):
        self.max_guesses = 5 # Alvöru wordle notar 6 en verkefnalýsing segir 5 boo
        self.word_letters = 5
        self.player_dir = 'player_profiles/'
        self.wordbank_dir = 'wordlists/'


    """ ------------- MAIN MENU -------------"""
    def print_header(self):
        fancy_stuff.print_header()

    def print_main_menu(self):
        print(fancy_stuff.menu_header)

    def main_menu(self):
        self.print_header()
        while True:
            fancy_stuff.clear_console()
            self.print_main_menu()
            self.main_menu_options()

    def main_menu_options(self):
        while True:
            menu_input = input("Please select an option: ")
            if menu_input == "1":
                return self.play_option()
            elif menu_input == "2":
                return self.add_option()
            elif menu_input == "3":
                return self.edit_option()
            elif menu_input == "4":
                return self.print_player_history()
            elif menu_input.lower() == "q":
                quit()
            else:
                print("Please enter a valid input!")


    """ ----------- 1. PLAY OPTION ------------- """

    def play_option(self): # Spyr notanda um nafn hans til að búa til skrá
        profile = input("Please enter your profile name: ").upper()
        return self.create_player_file(profile)

    def create_player_file(self, profile):
        '''Creates text files to store player scores'''
        if not os.path.exists(self.player_dir):
            os.makedirs(self.player_dir)
        file_name_path = self.get_player_file_name_path(profile)
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
        wordle = Wordle(profile, self.max_guesses, self.word_letters)
        return wordle.play_wordle()


    """ ----------- 2. ADD WORDS OPTION ------------- """
    def add_option(self):
        print('What word would you like to append to the word bank? (ENTER to exit)')
        while True:
            word_bank_input = input('Input word: ')
            if word_bank_input == '':
                return
            word_bank = f'wordlist_{len(word_bank_input)}.txt'
            file_name_path = self.wordbank_dir+word_bank
            try:
                if check.add_word_length_check(len(word_bank_input)):
                    file = open(file_name_path, 'a')
                if check.duplicate_word_check(file_name_path, word_bank_input):
                    file.write(word_bank_input + '\n')
                    print(f'"{word_bank_input}" added to word bank')
                    file.close() # Uppfærist með hverju instance-i. Annars var það bara þegar forritið hættir keyrslu
                    self.add_more_words()
                    return
                else:
                    print('Word already in word bank')
            except FileNotFoundError:
                print("Please enter word of length 4-6")

    def add_more_words(self):
        prompt = input('Would you like to add another word? (y/n): ').lower()
        if prompt == 'y':
            self.add_option()
        elif prompt == 'n':
            return
        else:
            print('Please enter a valid input')


    """ ----------- 3. EDIT OPTION ------------- """
    def edit_option(self):
        '''Edit game calls on two other functions'''
        self.max_guesses = self.edit_guesses()
        self.word_letters = self.edit_letters()

    def edit_guesses(self):
        '''Edit how many guesses'''
        while True:
            max_guesses_input = input('How many guesses would you like to have? (1-10): ')
            if check.max_guesses_check(max_guesses_input):
                return int(max_guesses_input)
            print('Please enter a valid input')

    def edit_letters(self):
        '''Edit length of word'''
        while True:
            word_letters_input = input('How many letters would you like to guess? (4-6): ')
            if check.word_letters_check(word_letters_input):
                return int(word_letters_input)
            print('Please enter a valid input')


    """ -------------- 4. HISTORY OPTION ----------------- """
    
    def print_player_history(self):
        while True:
            '''Prints player profiles'''
            player = input("What player history would you like to see? (ENTER to exit): ").upper()
            if player == '':
                return
            filename = player + '.txt'
            file_name_path = self.player_dir+filename
            if exists(file_name_path):
                with open(file_name_path, 'r') as f:
                    print(f.read())
                    input("Press ENTER to return to main menu: ")
                    return
            else:
                print('Player does not exist')

    def get_player_file_name_path(self, profile):
        '''Returns the full file path of the player profile'''
        filename = profile + '.txt'         # Create full file name
        file_name_path = self.player_dir+filename
        return file_name_path


""" -------------------- MAIN PROGRAM --------------------"""

def main():
    while True:
        fancy_stuff.clear_console()
        main_menu = MainMenu()
        main_menu.main_menu()
        
if __name__ == "__main__":
    main()