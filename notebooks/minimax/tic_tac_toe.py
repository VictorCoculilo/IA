class TicTacToe:
    """
    Classe que implementa o jogo da velha (Tic-Tac-Toe) para dois jogadores ('X' e 'O').

    Atributos:
        board (list): Lista de 9 elementos representando o tabuleiro 3x3.
                      Cada posição pode ser ' ', 'X' ou 'O'.
        current (str): Jogador atual, sendo 'X' ou 'O'.

    Métodos:
        available_moves():
            Retorna uma lista de índices das posições vazias no tabuleiro.

        make_move(idx):
            Realiza uma jogada na posição `idx` se ela estiver vazia.
            Alterna o jogador atual. Retorna True se a jogada for válida, False caso contrário.

        winner():
            Verifica se algum jogador venceu. Retorna 'X', 'O' ou None.

        full():
            Verifica se o tabuleiro está completo (sem espaços vazios).

        game_over():
            Retorna True se o jogo terminou (vitória ou empate), False caso contrário.

        copy():
            Retorna uma cópia profunda do estado atual do jogo (usado em algoritmos de busca).
    """

    def __init__(self):
        self.board = [' '] * 9
        self.current = 'X'

    def available_moves(self):
        return [i for i, v in enumerate(self.board) if v == ' ']

    def make_move(self, idx):
        if self.board[idx] == ' ':
            self.board[idx] = self.current
            self.current = 'O' if self.current == 'X' else 'X'
            return True
        return False

    def winner(self):
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),
                (1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for a,b,c in wins:
            if self.board[a] == self.board[b] == self.board[c] != ' ':
                return self.board[a]
        return None

    def full(self):
        return ' ' not in self.board

    def game_over(self):
        return self.winner() or self.full()

    def copy(self):
        new = TicTacToe()
        new.board = self.board[:]
        new.current = self.current
        return new