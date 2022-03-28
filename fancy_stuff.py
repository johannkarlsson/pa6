import time
import sys
import os
from wordle_class_test import Wordle


class FancyStuff:
    def __init__(self):
        self.header = """
----------------------------------

WELCOME TO WORDLE - PYTHON EDITION
    Author - Jóhann Karlsson
"""
        self.menu_header = """
------------------------------------------------------------

                        MAIN MENU

1. Play      2. Add Words       3. Edit Game     4. History

                        5. Quit

------------------------------------------------------------
"""
    def load_wordle(self, profile):
        '''ANIMATION FUNCTION'''
        print('Logging in as ' + profile)
        animation = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]
        for i in range(len(animation)):
            time.sleep(0.12)
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