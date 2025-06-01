import time
from colorama import Fore, Style, init
init(autoreset=True)

from othello import Othello
from othello_mcts import mcts
from othello_board import print_board

Othello.print_board = lambda self: print_board(self.board, self.cols)

def play_ai_vs_ai():
    game = Othello()

    while not game.game_over():
        game.print_board()
        print(f"\nVez de {game.current}")

        if game.available_moves():
            print("IA pensando...")
            move = mcts(game, iterations=200)
            print(f"{game.current} joga em {move}")
            game.make_move(*move)
            time.sleep(0.5)
        else:
            print(f"{game.current} não tem jogadas válidas. Passando a vez.")
            game.current = 'O' if game.current == 'X' else 'X'
            time.sleep(0.5)

    game.print_board()
    winner = game.winner()
    print("\nResultado Final:")
    if winner == 'Empate':
        print(Fore.CYAN + "Empate!")
    else:
        print(Fore.GREEN + f"Vencedor: {winner}")


def play():
    game = Othello()
    human = input("Escolha seu lado (X ou O): ").strip().upper()
    assert human in ['X', 'O']
    ai = 'O' if human == 'X' else 'X'

    while not game.game_over():
        game.print_board()
        if game.current == human:
            while True:
                try:
                    move = input(f"Sua jogada ({human}), digite linha,coluna (ex: 2,3): ")
                    row, col = map(int, move.strip().split(','))
                    if (row, col) in game.available_moves():
                        game.make_move(row, col)
                        break
                    else:
                        print("Movimento inválido.")
                except:
                    print("Entrada inválida. Use o formato linha,coluna")
        else:
            print("IA pensando...")
            move = mcts(game, iterations=200)
            print(f"IA joga em {move}")
            game.make_move(*move)
            time.sleep(1)

    game.print_board()
    winner = game.winner()
    if winner == human:
        print(Fore.GREEN + "Você venceu!")
    elif winner == ai:
        print(Fore.RED + "A IA venceu.")
    elif winner == 'Empate':
        print(Fore.CYAN + "Empate.")
    else:
        print(Fore.YELLOW + "Jogo finalizado.")

if __name__ == "__main__":
    play_ai_vs_ai()
