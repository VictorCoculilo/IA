import os
from colorama import Fore, Style, init
init(autoreset=True)

# Limpa a tela
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Colore as células do tabuleiro
def colorize(cell):
    if cell == 'X':
        return Fore.RED + 'X' + Style.RESET_ALL
    elif cell == 'O':
        return Fore.YELLOW + 'O' + Style.RESET_ALL
    else:
        return ' '

# Imprime o tabuleiro com contador
def print_board(board, cols):
    # Contagem de peças
    x_count = sum(row.count('X') for row in board)
    o_count = sum(row.count('O') for row in board)

    # Cabeçalho com contador
    print(f"\n{Fore.RED}X: {x_count}  {Fore.YELLOW}O: {o_count}{Style.RESET_ALL}\n")

    # Impressão das linhas com numeração
    for i, row in enumerate(board):
        print(f"{i} |" + "|".join(colorize(cell) for cell in row) + "|")
    print("   " + " ".join(map(str, range(cols))))
