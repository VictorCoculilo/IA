import time
from colorama import Fore, init
init(autoreset=True)

from othello import Othello
from othello_board import print_board
from othello_mcts import mcts
from othello_minimax import best_move_othello

# Substituir print_board
Othello.print_board = lambda self: print_board(self.board, self.cols)

def play():
    game = Othello()
    minimax_player = 'X'
    mcts_player = 'O'

    while not game.game_over():
        game.print_board()
        print(f"\nVez de {game.current}")
        time.sleep(1)

        if game.available_moves():
            if game.current == minimax_player:
                move = best_move_othello(game, depth=3)
                print(f"Minimax ({minimax_player}) joga em {move}")
                game.make_move(*move)
            else:
                move = mcts(game, iterations=200)
                print(f"MCTS ({mcts_player}) joga em {move}")
                game.make_move(*move)
        else:
            print(f"{game.current} não tem movimentos válidos. Passando a vez.")
            game.current = minimax_player if game.current == mcts_player else mcts_player

        time.sleep(1)

    game.print_board()
    winner = game.winner()
    if winner == minimax_player:
        print(Fore.GREEN + "Minimax venceu!")
    elif winner == mcts_player:
        print(Fore.RED + "MCTS venceu!")
    elif winner == 'Empate':
        print(Fore.YELLOW + "Empate!")
    else:
        print(Fore.CYAN + "Jogo finalizado.")

if __name__ == "__main__":
    play()
