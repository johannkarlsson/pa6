def main_menu_print():
    main_menu ="""
----------------------------------

            WELCOME
1. Play     2. Add Words     3. Quit

----------------------------------
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
        return
    else:
        print("Please enter a valid input")
        main_menu_input()


def play_game():
    print('playing game')

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
    if duplicate_check(word_bank_input):
        file.write(word_bank_input + '\n')
        print(f'"{word_bank_input}" added to word bank')
        file.close() # Uppfærist með hverju instance-i. Annars var það bara þegar forritið hættir keyrslu
        add_more_words()
    else:
        print('Word already in word bank')
        add_more_words()

def duplicate_check(word):
    with open('test_words.txt', 'r') as file:
        words = file.read()
    if word not in words:
        return True
    else:
        return False

main_menu_input()