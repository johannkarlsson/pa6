class Check:
    def __init__(self):
        pass

    def duplicate_word_check(word):
        '''Checks if word already exists in wordbank'''
        with open('test_words.txt', 'r') as file:
            words = file.read()
        if word not in words:
            return True
        else:
            return False

    def max_guesses_check(max_guesses):
        '''Checks if max_guesses is a digit between 1 and 10'''
        if max_guesses.isdigit():
            if int(max_guesses) > 0 and int(max_guesses) < 11:
                return True
            else:
                return False
        else:
            return False
    
    def word_letters_check(word_letters):
        '''Checks if word_letters is a digit between 4 and 6'''
        if word_letters.isdigit():
            if int(word_letters) > 3 and int(word_letters) < 7:
                return True
            else:
                return False
        else:
            return False