class Check:
    def duplicate_word_check(self, word_bank, word):
        ''' When adding. Checks if word already exists in wordbank '''
        with open(word_bank, 'r') as file:
            words = file.read()
        if word not in words:
            return True
        else:
            return False

    def add_word_length_check(self, word_length):
        ''' When adding. Checks if word_length is a digit between 4 and 6 '''
        if int(word_length) > 3 and int(word_length) < 7:
            return True
        else:
            return False

    def max_guesses_check(self, max_guesses):
        ''' When editing. Checks if max_guesses is a digit between 1 and 10 '''
        if max_guesses.isdigit():
            if int(max_guesses) > 0 and int(max_guesses) < 11:
                return True
            else:
                return False
        else:
            return False
    
    def word_letters_check(self, word_letters):
        ''' When editing. Checks if word_letters is a digit between 4 and 6 '''
        if word_letters.isdigit():
            if int(word_letters) > 3 and int(word_letters) < 7:
                return True
            else:
                return False
        else:
            return False