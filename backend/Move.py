from ChessTranscode import *

class Move:
    def __init__(self, piece, from_x, from_y, to_x, to_y, kills, is_special=False, linked_to=None):
        self.piece = piece
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y
        self.kills = kills
        self.is_special = is_special
        self.linked_to = linked_to

    def printMove(self):
        print(self.piece.name + " from " + chessEncoder(self.from_x, self.from_y) + " to " + chessEncoder(self.to_x, self.to_y))