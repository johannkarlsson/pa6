class Check:
    def __init__(self):
        pass

    def duplicate_word_check(word):
        with open('test_words.txt', 'r') as file:
            words = file.read()
        if word not in words:
            return True
        else:
            return False