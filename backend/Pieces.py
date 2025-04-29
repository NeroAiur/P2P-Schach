from Move import Move

class Piece:
    def __init__(self, pos_x, pos_y, owner, color, game):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.owner = owner
        self.color = color
        self.game = game
        self.has_been_moved = False

    def updatePos(self, x, y):
        self.pos_x = x
        self.pos_y = y

    def returnAllMoves(self):
        pass

    def bruteForceGenerateAllMoves(self):
        moves = []

        # if self.name != 'P':
        for x in range(8):
            for y in range(8):
                if self.validateMove(x, y):
                    kills = self.game.getBoard(x, y)
                    if kills == 0:
                        kills = None
                    moves.append(Move(self, self.pos_x, self.pos_y, x, y, kills))
        return moves
        
        # else:
        #    return self.returnAllMoves()
    

class Pawn(Piece):
    def __init__(self, pos_x, pos_y, owner, color, game):
        super().__init__(pos_x, pos_y, owner, color, game)
        self.name = 'P'
        self.moved_two_fields_last_turn = False

    def validateMove(self, new_x, new_y):
        # standard 1 nach vorne
        target = self.game.getBoard(new_x, new_y)
        if self.color == "white":
            if new_y == self.pos_y + 1 and new_x == self.pos_x and target == 0:
                return True
        else:
            if new_y == self.pos_y - 1 and new_x == self.pos_x and target == 0:
                return True
            
        # 2 nach vorne von der Startposition
        if self.color == "white" and self.pos_y == 1:
            if new_y == self.pos_y + 2 and new_x == self.pos_x and target == 0:
                return True
            
        elif self.pos_y == 6:
            if new_y == self.pos_y - 2 and new_x == self.pos_x and target == 0:
                return True
        
        # diagionaler Angriff
        if target != 0 and target.color != self.color:
            if self.color == "white":
                if new_y == self.pos_y + 1 and (new_x == self.pos_x + 1 or new_x == self.pos_x - 1):
                    return True
            else:
                if new_y == self.pos_y - 1 and (new_x == self.pos_x + 1 or new_x == self.pos_x - 1):
                    return True
        
        return False

class Knight(Piece):
    def __init__(self, pos_x, pos_y, owner, color, game):
        super().__init__(pos_x, pos_y, owner, color, game)
        self.name = 'N'

    def validateMove(self, new_x, new_y):
        # check for same colored pieces on field
        if self.game.getBoard(new_x, new_y) == 0 or self.game.getBoard(new_x, new_y).color != self.color:
            if abs(self.pos_x - new_x) == 2 and abs(self.pos_y - new_y) == 1:
                return True
            if abs(self.pos_x - new_x) == 1 and abs(self.pos_y - new_y) == 2:
                return True
        
        return False
    
class Bishop(Piece): 
    def __init__(self, pos_x, pos_y, owner, color, game):
        super().__init__(pos_x, pos_y, owner, color, game)
        self.name = 'B'

    def validateMove(self, new_x, new_y):
        if abs(self.pos_x - new_x) == abs(self.pos_y - new_y):
            if self.pos_x < new_x:
                x_move_dir = 1
            else:            
                x_move_dir = -1
            if self.pos_y < new_y:
                y_move_dir = 1
            else:
                y_move_dir = -1

            # check if there is shit in the way
            if abs(self.pos_x - new_x) > 1:
                for i in range(1,abs(self.pos_x - new_x)):
                    if self.game.getBoard((self.pos_x + i*x_move_dir), (self.pos_y + i*y_move_dir)) != 0:
                        return False

            # check for friendly fire
            if self.game.getBoard(new_x, new_y) != 0:
                if self.game.getBoard(new_x, new_y).color == self.color:
                    return False
            
            return True
        return False
    
class Rook(Piece): 
    def __init__(self, pos_x, pos_y, owner, color, game):
        super().__init__(pos_x, pos_y, owner, color, game)
        self.name = 'R'

    def validateMove(self, new_x, new_y):
        if (abs(new_x - self.pos_x) != 0 and abs(new_y - self.pos_y) != 0):
            return False
        
        # horizontal movement
        if (abs(self.pos_x - new_x) != 0):
            if self.pos_x < new_x:
                x_move_dir = 1
            else:            
                x_move_dir = -1

            # check if there is shit in the way
            for i in range(1,abs(self.pos_x - new_x)):
                if self.game.getBoard((self.pos_x + i*x_move_dir), self.pos_y) != 0:
                    return False

        # vertical movement
        else:
            if self.pos_y < new_y:
                y_move_dir = 1
            else:            
                y_move_dir = -1

            for i in range(1,abs(self.pos_y - new_y)):
                if self.game.getBoard(self.pos_x, (self.pos_y + i*y_move_dir)) != 0:
                    return False
            
        # friendly fire check
        if self.game.getBoard(new_x, new_y) != 0:
            if self.game.getBoard(new_x, new_y).color == self.color:
                return False
            
        return True
    
class Queen(Piece): 
    def __init__(self, pos_x, pos_y, owner, color, game):
        super().__init__(pos_x, pos_y, owner, color, game)
        self.name = 'Q'

    def validateMove(self, new_x, new_y):
        return self.rookMovement(new_x, new_y) or self.bishopMovement(new_x, new_y)
    
    def rookMovement(self, new_x, new_y):
        if new_x == 4 and new_y == 1: 
            1+1

        if (abs(new_x - self.pos_x) != 0 and abs(new_y - self.pos_y) != 0):
            return False
        
        # horizontal movement
        if (abs(self.pos_x - new_x) != 0):
            if self.pos_x < new_x:
                x_move_dir = 1
            else:            
                x_move_dir = -1

            # check if there is shit in the way
            for i in range(1,abs(self.pos_x - new_x)):
                if self.game.getBoard((self.pos_x + i*x_move_dir), self.pos_y) != 0:
                    return False

        # vertical movement
        else:
            if self.pos_y < new_y:
                y_move_dir = 1
            else:            
                y_move_dir = -1

            for i in range(1,abs(self.pos_y - new_y)):
                if self.game.getBoard(self.pos_x, (self.pos_y + i*y_move_dir)) != 0:
                    return False
            
        # friendly fire check
        if self.game.getBoard(new_x, new_y) != 0:
            if self.game.getBoard(new_x, new_y).color == self.color:
                return False
            
        return True
    
    def bishopMovement(self, new_x, new_y):
        if abs(self.pos_x - new_x) == abs(self.pos_y - new_y):
            if self.pos_x < new_x:
                x_move_dir = 1
            else:            
                x_move_dir = -1
            if self.pos_y < new_y:
                y_move_dir = 1
            else:
                y_move_dir = -1

            # check if there is shit in the way
            if abs(self.pos_x - new_x) > 1:
                for i in range(1,abs(self.pos_x - new_x)):
                    if self.game.getBoard((self.pos_x + i*x_move_dir), (self.pos_y + i*y_move_dir)) != 0:
                        return False

            # check for friendly fire
            if self.game.getBoard(new_x, new_y) != 0:
                if self.game.getBoard(new_x, new_y).color == self.color:
                    return False
            
            return True
        return False

class King(Piece):
    def __init__(self, pos_x, pos_y, owner, color, game):
        super().__init__(pos_x, pos_y, owner, color, game)
        self.name = 'K'
        self.has_castled = False
    
    def validateMove(self, new_x, new_y):
        if abs(self.pos_x - new_x) <= 1 and abs(self.pos_y - new_y) <= 1:
            # friendly fire check
            if self.game.getBoard(new_x, new_y) == 0 or self.game.getBoard(new_x, new_y).color != self.color:
                return True
