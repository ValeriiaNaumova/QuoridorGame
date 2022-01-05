from .board import Board
from .constants import RED, BLACK


class Game:
    def __init__(self):
        self.selected = None
        self.board = Board()
        self.turn = BLACK

    def update(self):
        self.board.draw()

    def change_turn(self):
        if self.turn == RED:
            self.turn = BLACK
        else:
            self.turn = RED

    def ai_move(self, board):
        self.board = board
        self.change_turn()

    def get_board(self):
        return self.board
