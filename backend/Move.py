from ChessTranscode import *

class Move:
    def __init__(self, piece, from_x, from_y, to_x, to_y, pawn_condition=None):
        self.piece = piece
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y
        self.is_pawn = self.piece.name == 'P'
        self.pawn_condition = pawn_condition # 0 = has to be empty, 1 there has to be an enemy

    def printMove(self):
        print(self.piece.name + " from " + chessEncoder(self.from_x, self.from_y) + " to " + chessEncoder(self.to_x, self.to_y))