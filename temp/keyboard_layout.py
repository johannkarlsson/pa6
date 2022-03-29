from re import M


# keyboard = """Q W E R T Y U I O P
#  A S D F G H J K L
#   Z X C V B N M"""


# print(keyboard)

keyboard = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],[' ', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],[' ',' ', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']]

print(keyboard[0])
print(f'  {keyboard[1]}')
print(f'    {keyboard[2]}')

for row in keyboard:
    for key in row:
        print(key, end=' ')
    print()