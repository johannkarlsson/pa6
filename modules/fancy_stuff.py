import time
import sys
import os


class FancyStuff:
    def __init__(self):
        self.header = """
------------------------------------------------------------

            WELCOME TO WORDLE - PYTHON EDITION
                Authors - Jóhann & Bjössi
                
------------------------------------------------------------"""
        self.menu_header = """
------------------------------------------------------------

                        MAIN MENU

1. Play      2. Add Words       3. Edit Game     4. History

                        Q. Quit

------------------------------------------------------------
"""
    def load_wordle(self, profile):
        '''ANIMATION FUNCTION'''
        print('Logging in as ' + profile)
        animation = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]
        for i in range(len(animation)):
            time.sleep(0.10)
            sys.stdout.write("\r" + animation[i % len(animation)])
            sys.stdout.flush()
        print("\n")
        self.clear_console()

    def clear_console(self):
        '''HELPER FUNCTION TO CLEAR SCREEN'''
        command = 'clear'
        if os.name in ('nt', 'dos'):
            command = 'cls'
        os.system(command)

    def print_header(self):
        print(self.header)
        time.sleep(3)
        return