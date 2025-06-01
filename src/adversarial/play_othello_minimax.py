import time
from colorama import Fore, init, Style
init(autoreset=True)

from othello import Othello  # Sua classe Othello
from othello_board import print_board

# Função heurística para Othello
def evaluate_othello(board, player):
    opponent = 'O' if player == 'X' else 'X'
    player_count = sum(row.count(player) for row in board)
    opponent_count = sum(row.count(opponent) for row in board)
    return player_count - opponent_count  # Simples: mais peças = melhor

# Minimax adaptado para Othello
def minimax_othello(game, depth, maximizing_player, player):
    winner = game.winner()
    if winner == player:
        return 10000
    elif winner and winner != player and winner != 'Empate':
        return -10000
    elif game.full() or depth == 0 or not game.available_moves():
        return evaluate_othello(game.board, player)

    if maximizing_player:
        max_eval = float('-inf')
        for move in game.available_moves():
            new_game = game.copy()
            new_game.make_move(*move)
            eval = minimax_othello(new_game, depth - 1, False, player)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in game.available_moves():
            new_game = game.copy()
            new_game.make_move(*move)
            eval = minimax_othello(new_game, depth - 1, True, player)
            min_eval = min(min_eval, eval)
        return min_eval

# IA: escolher melhor jogada usando minimax_othello
def best_move(game, depth=4):
    player = game.current
    best_score = float('-inf')
    move_choice = None

    for move in game.available_moves():
        new_game = game.copy()
        new_game.make_move(*move)
        score = minimax_othello(new_game, depth - 1, False, player)
        if score > best_score:
            best_score = score
            move_choice = move
    return move_choice

# Substitui print_board na classe Othello
Othello.print_board = lambda self: print_board(self.board, self.cols)

# Função principal do jogo
def play():
    game = Othello()
    human = input("Escolha seu lado (X ou O): ").strip().upper()
    assert human in ['X', 'O']
    ai = 'O' if human == 'X' else 'X'

    while not game.game_over():
        game.print_board()
        print(f"\nVez de {game.current}")
        if game.available_moves():
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
                move = best_move(game, depth=4)
                print(f"IA joga em {move}")
                game.make_move(*move)
                time.sleep(1)
        else:
            print(f"{game.current} não tem movimentos válidos. Passando a vez.")
            game.current = ai if game.current == human else human
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
    play()
