import os
from colorama import Fore, Style, init
init(autoreset=True)

# Helper: clean screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Helper: color cell content
def colorize(cell):
    if cell == 'X':
        return Fore.RED + 'X' + Style.RESET_ALL
    elif cell == 'O':
        return Fore.YELLOW + 'O' + Style.RESET_ALL
    else:
        return ' '

def print_board(board, cols):
    clear_screen()
    for row in board:
        print('|' + '|'.join(colorize(cell) for cell in row) + '|')
    print(' ' + ' '.join(map(str, range(cols))))
