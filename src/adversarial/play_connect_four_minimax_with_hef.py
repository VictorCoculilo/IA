import time
from colorama import Fore, Style, init

# Reinitialize colorama after reset
init(autoreset=True)

from minimax import minimax_with_hef
from connect_four import ConnectFour, ROWS, COLS

from helper_functions import print_board

# Heuristic Evaluation Function
def evaluate_connect_four(board, player):
    opponent = 'O' if player == 'X' else 'X'
    score = 0

    def evaluate_window(window):
        if window.count(player) == 4:
            return 1000
        elif window.count(player) == 3 and window.count(' ') == 1:
            return 50
        elif window.count(player) == 2 and window.count(' ') == 2:
            return 10
        elif window.count(opponent) == 3 and window.count(' ') == 1:
            return -80
        return 0

    rows = len(board)
    cols = len(board[0])

    # Avaliar janelas horizontais
    for r in range(rows):
        for c in range(cols - 3):
            window = board[r][c:c+4]
            score += evaluate_window(window)

    # Avaliar janelas verticais
    for r in range(rows - 3):
        for c in range(cols):
            window = [board[r+i][c] for i in range(4)]
            score += evaluate_window(window)

    # Avaliar janelas diagonais \
    for r in range(rows - 3):
        for c in range(cols - 3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window)

    # Avaliar janelas diagonais /
    for r in range(3, rows):
        for c in range(cols - 3):
            window = [board[r-i][c+i] for i in range(4)]
            score += evaluate_window(window)

    return score



# AI Move Selector
def best_move(game, depth=4):
    '''
    Essa função determina a melhor jogada para a IA em um jogo de Connect Four,
    utilizando o algoritmo Minimax com uma função de avaliação heurística.
    Ela avalia todas as jogadas disponíveis e escolhe a que maximiza a pontuação
    heurística para o jogador atual, considerando a profundidade especificada.
    :param game: Instância do jogo Connect Four
    :param depth: Profundidade da busca Minimax
    :return: A melhor coluna para jogar
    '''
    player = game.current
    best_score = float('-inf')
    move_choice = None
    for move in game.available_moves():
        new_game = game.copy()
        new_game.make_move(move)
        # score = minimax_with_dls(new_game, depth - 1, False, player)
        score = minimax_with_hef(
            game=new_game,
            depth=depth - 1,
            maximizing=False,
            player=player,
            evaluate_fn=evaluate_connect_four
        )
        if score > best_score:
            best_score = score
            move_choice = move
    return move_choice

# Replace ConnectFour.print_board with updated function
ConnectFour.print_board = lambda self: print_board(self.board, COLS)

def play():
    game = ConnectFour()
    human = input("Escolha seu lado (X ou O): ").strip().upper()
    assert human in ['X', 'O']
    ai = 'O' if human == 'X' else 'X'

    while not game.game_over():
        game.print_board()
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
            move = best_move(game, depth=4)
            print(f"IA joga na coluna {move}")
            game.make_move(move)
            time.sleep(0.8)

    game.print_board()
    winner = game.winner()
    if winner == human:
        print(Fore.GREEN + "Você venceu!")
    elif winner == ai:
        print(Fore.RED + "A IA venceu.")
    else:
        print(Fore.CYAN + "Empate.")

if __name__ == "__main__":
    play()