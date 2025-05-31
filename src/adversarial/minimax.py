def minimax(game, maximizing):
    """
    Implementa o algoritmo Minimax para encontrar o valor de utilidade de um estado do jogo.

    Este algoritmo assume que o jogador 'X' está maximizando e o jogador 'O' está minimizando.
    Ele percorre recursivamente a árvore de possibilidades do jogo até encontrar um estado terminal,
    atribuindo pontuação de +1 para vitória de 'X', -1 para vitória de 'O' e 0 para empate.

    Parâmetros:
        game (TicTacToe): Instância do jogo com o estado atual do tabuleiro.
        maximizing (bool): Indica se o jogador atual está tentando maximizar (True) ou minimizar (False) o valor.

    Retorno:
        int: Valor de utilidade do estado atual:
             +1 se o jogador 'X' vence,
             -1 se o jogador 'O' vence,
              0 se for empate.
    """
    if game.winner() == 'X':
        return 1
    elif game.winner() == 'O':
        return -1
    elif game.full():
        return 0

    if maximizing:
        best = float('-inf')
        for move in game.available_moves():
            new_game = game.copy()
            new_game.make_move(move)
            score = minimax(new_game, False)
            best = max(best, score)
        return best
    else:
        best = float('inf')
        for move in game.available_moves():
            new_game = game.copy()
            new_game.make_move(move)
            score = minimax(new_game, True)
            best = min(best, score)
        return best

def best_move(game):
    player = game.current
    best_val = float('-inf') if player == 'X' else float('inf')
    best_action = None

    for move in game.available_moves():
        new_game = game.copy()
        new_game.make_move(move)
        val = minimax(new_game, maximizing=(player == 'O'))

        if (player == 'X' and val > best_val) or (player == 'O' and val < best_val):
            best_val = val
            best_action = move

    return best_action

# Minimax with Heuristic Evaluation Function
'''
Essa função implementa o algoritmo Minimax com uma função de avaliação heurística.
Ela avalia o estado atual do jogo e retorna um valor que representa a qualidade desse estado
para o jogador atual.

A função de avaliação heurística deve ser definida externamente e passada como argumento. Ela deve 
retornar um valor numérico que representa a qualidade do estado do jogo para o jogador atual. 
Quanto maior o valor, melhor o estado para o jogador atual.

:param game: Instância do jogo com o estado atual do tabuleiro.
:param depth: Profundidade da busca Minimax.
:param maximizing: Indica se o jogador atual está tentando maximizar (True) ou minimizar (False) o valor.
:param player: O jogador atual ('X' ou 'O').
:param evaluate_fn: Função de avaliação heurística que avalia o estado do jogo.
:return: Valor numérico representando a qualidade do estado do jogo. 
'''
def minimax_with_hef(game, depth, maximizing, player, evaluate_fn):
    winner = game.winner()
    if winner == player:
        return 10000
    elif winner and winner != player:
        return -10000
    elif game.full() or depth == 0:
        return evaluate_fn(game.board, player)

    if maximizing:
        best = float('-inf')
        for move in game.available_moves():
            new_game = game.copy()
            new_game.make_move(move)
            val = minimax_with_hef(new_game, depth - 1, False, player, evaluate_fn)
            best = max(best, val)
        return best
    else:
        best = float('inf')
        for move in game.available_moves():
            new_game = game.copy()
            new_game.make_move(move)
            val = minimax_with_hef(new_game, depth - 1, True, player, evaluate_fn)
            best = min(best, val)
        return best
