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