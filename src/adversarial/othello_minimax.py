def minimax_othello(game, depth, maximizing_player, player):
    """
    Minimax para Othello com profundidade limitada.

    :param game: instância do jogo Othello
    :param depth: profundidade máxima da busca
    :param maximizing_player: bool, True se for vez do jogador maximizador
    :param player: o jogador para quem estamos calculando a melhor jogada ('X' ou 'O')
    :return: score numérico da posição
    """
    winner = game.winner()
    if winner == player:
        return 10000  # Vitória do jogador
    elif winner and winner != player and winner != 'Empate':
        return -10000  # Derrota do jogador
    elif game.full() or depth == 0 or not game.available_moves():
        # Avaliação heurística simples: diferença de peças
        x_count = sum(row.count('X') for row in game.board)
        o_count = sum(row.count('O') for row in game.board)
        if player == 'X':
            return x_count - o_count
        else:
            return o_count - x_count

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

def best_move_othello(game, depth=3):
    """
    Retorna a melhor jogada para o jogador atual no Othello usando minimax.

    :param game: instância do jogo Othello
    :param depth: profundidade da busca
    :return: tupla (row, col) da melhor jogada
    """
    player = game.current
    best_score = float('-inf')
    best_move = None

    for move in game.available_moves():
        new_game = game.copy()
        new_game.make_move(*move)
        score = minimax_othello(new_game, depth - 1, False, player)
        if score > best_score:
            best_score = score
            best_move = move

    return best_move
