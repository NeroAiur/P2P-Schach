from ChessTranscode import *

class Move:
    def __init__(self, piece, from_x, from_y, to_x, to_y, kills, linked_to=None):
        self.piece = piece
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y
        self.kills = kills
        self.linked_to = linked_to

    def printMove(self):
        print(chessEncoder(self.from_x, self.from_y) + chessEncoder(self.to_x, self.to_y))