from board_game import BoardGame

DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),          (0, 1),
              (1, -1),  (1, 0), (1, 1)]

class Othello(BoardGame):
    def __init__(self):
        super().__init__(8, 8)
        # Início padrão do Othello
        self.board[3][3] = 'O'
        self.board[3][4] = 'X'
        self.board[4][3] = 'X'
        self.board[4][4] = 'O'
        self.current = 'X'

    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def available_moves(self):
        moves = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == ' ' and self._would_flip(r, c):
                    moves.append((r, c))
        return moves

    def game_over(self):
        return not self.available_moves() and not self._other_player_has_moves()

    def _other_player_has_moves(self):
        temp_current = self.current
        self.current = 'O' if self.current == 'X' else 'X'
        has_moves = bool(self.available_moves())
        self.current = temp_current
        return has_moves
    
    def _would_flip(self, row, col):
        for dr, dc in DIRECTIONS:
            if self._check_direction(row, col, dr, dc):
                return True
        return False

    def _check_direction(self, row, col, dr, dc):
        r, c = row + dr, col + dc
        pieces_to_flip = []

        while self.in_bounds(r, c) and self.board[r][c] not in (' ', self.current):
            pieces_to_flip.append((r, c))
            r += dr
            c += dc

        if self.in_bounds(r, c) and self.board[r][c] == self.current and pieces_to_flip:
            return True
        return False

    def make_move(self, row, col):
        if not self.in_bounds(row, col) or self.board[row][col] != ' ':
            return False

        flipped = []
        for dr, dc in DIRECTIONS:
            flipped += self._flip_direction(row, col, dr, dc)

        if not flipped:
            return False  # Jogada inválida (não vira peças)

        self.board[row][col] = self.current
        for r, c in flipped:
            self.board[r][c] = self.current

        self.current = 'O' if self.current == 'X' else 'X'
        return True

    def _flip_direction(self, row, col, dr, dc):
        r, c = row + dr, col + dc
        pieces = []

        while self.in_bounds(r, c) and self.board[r][c] not in (' ', self.current):
            pieces.append((r, c))
            r += dr
            c += dc

        if self.in_bounds(r, c) and self.board[r][c] == self.current:
            return pieces
        return []

    def winner(self):
        x_count = sum(row.count('X') for row in self.board)
        o_count = sum(row.count('O') for row in self.board)
        if self.available_moves():
            return None  # Jogo ainda não acabou
        if x_count > o_count:
            return 'X'
        elif o_count > x_count:
            return 'O'
        return 'Empate'
    
