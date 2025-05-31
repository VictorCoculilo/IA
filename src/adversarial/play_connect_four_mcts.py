import time

from colorama import Fore, Style, init
init(autoreset=True)

from connect_four import ConnectFour, ROWS, COLS
from mcts import mcts
from helper_functions import print_board

def play():
    '''
    Main function to play the game
    '''
    game = ConnectFour()
    human = input("Escolha seu lado (X ou O): ").strip().upper()
    assert human in ['X', 'O']
    ai = 'O' if human == 'X' else 'X'

    while not game.game_over():
        print_board(game.board, COLS)
        if game.current == human:
            while True:
                try:
                    col = int(input(f"Sua jogada ({human}), escolha coluna (0-{COLS-1}): "))
                    if col in game.available_moves():
                        game.make_move(col)
                        time.sleep(0.5)
                        break
                    else:
                        print("Coluna inválida ou cheia.")
                except ValueError:
                    print("Entrada inválida.")
        else:
            print("IA pensando...")
            move = mcts(game, iterations=200)
            print(f"IA joga na coluna {move}")
            game.make_move(move)
            time.sleep(0.5)

    print_board(game.board)
    winner = game.winner()
    if winner == human:
        print("Você venceu!")
    elif winner == ai:
        print("Você perdeu!")
    else:
        print("Empate.")

if __name__ == "__main__":
    play()
