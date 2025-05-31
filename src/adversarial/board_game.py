class BoardGame:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [[' '] * cols for _ in range(rows)]
        self.current = 'X'

    def available_moves(self):
        raise NotImplementedError

    def make_move(self, move):
        raise NotImplementedError

    def winner(self):
        raise NotImplementedError

    def full(self):
        return all(all(cell != ' ' for cell in row) for row in self.board)

    def game_over(self):
        return self.winner() or self.full()

    def copy(self):
        new = self.__class__()
        new.board = [row.copy() for row in self.board]
        new.current = self.current
        return new

    def print_board(self):
        for row in self.board:
            print('|' + '|'.join(row) + '|')
        print(' ' + ' '.join(map(str, range(self.cols))))
