def main_menu_print():
    main_menu ="""
----------------------------------

            WELCOME
1. Play     2. Add Words     3. Quit

----------------------------------
"""
    print(main_menu)

def main_menu_input():
    main_menu_input = input("Please select an option: ")
    if main_menu_input == "1":
        play_game()
    elif main_menu_input == "2":
        add_words()
    else:
        return


def play_game():
    print('playing game')

def add_words():
    print('What words would you like to append to the word bank?')
    word_bank_input = input('Input word: ')
    file = open('test_words.txt', 'w')
    file.write(word_bank_input)


    
main_menu_print()
main_menu_input()