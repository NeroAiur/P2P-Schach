class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def chessEncoder(x, y):
    return "ABCDEFGH"[x] + str(y+1)

def chessDecoder(string):
    return [ord(string[0].upper()) - 65, int(string[1]) - 1]

class Figure:
    def __init__(self, pos_x, pos_y, owner, color, game):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.owner = owner
        self.color = color
        self.game = game

    def updatePos(self, x, y):
        self.pos_x = x
        self.pos_y = y

class Pawn(Figure):
    def __init__(self, pos_x, pos_y, owner, color, game):
        super().__init__(pos_x, pos_y, owner, color, game)
        self.name = 'P'

    def move(self, new_x, new_y):
        # standard 1 nach vorne
        target = self.game.board[new_y*8 + new_x]
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
                if new_y == self.pos_y + 1 and new_x == self.pos_x + 1 or new_x == self.pos_x - 1:
                    return True
            else:
                if new_y == self.pos_y - 1 and new_x == self.pos_x + 1 or new_x == self.pos_x - 1:
                    return True
        
        return False

class Knight(Figure):
    def __init__(self, pos_x, pos_y, owner, color, game):
        super().__init__(pos_x, pos_y, owner, color, game)
        self.name = 'N'

    def move(self, new_x, new_y):
        if abs(self.pos_x - new_x) == 2 and abs(self.pos_y - new_y) == 1:
            return True
        if abs(self.pos_x - new_x) == 1 and abs(self.pos_y - new_y) == 2:
            return True
        
        return False
    
class Bishop(Figure): 
    def __init__(self, pos_x, pos_y, owner, color, game):
        super().__init__(pos_x, pos_y, owner, color, game)
        self.name = 'B'

    def move(self, new_x, new_y):
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
                    if self.game.board[(self.pos_y + i*y_move_dir)*8 + (self.pos_x + i*x_move_dir)] != 0:
                        return False

            if self.game.board[new_y*8 + new_x] != 0:
                if self.game.board[new_y*8 + new_x].color == self.color:
                    return False
            
            return True
        return False
    

class Rook(Figure): 
    def __init__(self, pos_x, pos_y, owner, color, game):
        super().__init__(pos_x, pos_y, owner, color, game)
        self.name = 'R'

    def move(self, new_x, new_y):
        if (new_x != 0 and new_y != 0):
            return False
        
        # horizontal movement
        if (new_x != 0):
            if self.pos_x < new_x:
                x_move_dir = 1
            else:            
                x_move_dir = -1

            # check if there is shit in the way
            if abs(self.pos_x - new_x) > 1:
                for i in range(1,abs(self.pos_x - new_x)):
                    if self.game.board[(self.pos_x + i*x_move_dir)] != 0:
                        return False
                    
            return True

        # vertical movement
        if (new_y != 0):
            if self.pos_y < new_y:
                y_move_dir = 1
            else:            
                y_move_dir = -1

            if abs(self.pos_y - new_y) > 1:
                for i in range(1,abs(self.pos_y - new_y)):
                    if self.game.board[(self.pos_y* 8 + self.pos_x + i*y_move_dir)  ] != 0:
                        return False
            
            return True
        return False

class Game:
    def __init__(self, player1, player2):
        self.player1 = player1 # player 1 is white 
        self.player2 = player2
        self.board = self.initBoard()
        self.turn = player1 # 1 means player1s turn, 2 means its player2s turn

    def printBoard(self):
        for i in range(8):
            print (str(i+1) + " |", end=' ')
            for j in range(8):
                if self.board[i*8+j] == 0:
                    print(self.board[i*8+j], end=' ')
                else:
                    if self.board[i*8+j].color == "white":
                        print(bcolors.OKGREEN + self.board[i*8+j].name + bcolors.ENDC, end=' ')
                    else:
                        print(bcolors.FAIL + self.board[i*8+j].name + bcolors.ENDC, end=' ')
                    
            print()
        print("    ---------------")
        print("    A B C D E F G H")

    def initBoard(self):
        board = [0]*64
        # spawn in the pawns
        # for i in range(8):
        #     board[8 + i] = Pawn(i, 1, self.player1, "white", self)
        #     board[6*8 + i] = Pawn(i, 6, self.player2, "black", self)

        # spawn in the knights
        board[1] = Knight(1, 0, self.player1, "white", self)
        board[6] = Knight(6, 0, self.player1, "white", self)

        board[7*8 + 1] = Knight(1, 7, self.player2, "black", self)
        board[7*8 +6] = Knight(6, 7, self.player2, "black", self)

        # spawn in the bishops
        board[2] = Bishop(2, 0, self.player1, "white", self)
        board[5] = Bishop(5, 0, self.player1, "white", self)

        board[7*8 + 2] = Bishop(2, 7, self.player2, "black", self)
        board[7*8 + 5] = Bishop(5, 7, self.player2, "black", self)

        # spawn in the rooks
        board[0] = Rook(0, 0, self.player1, "white", self)
        board[7] = Rook(7, 0, self.player1, "white", self)

        board[7*8 + 0] = Rook(0, 7, self.player2, "black", self)
        board[7*8 + 7] = Rook(7, 7, self.player2, "black", self)

        
        return board

    def move(self, prev_x, prev_y, new_x, new_y):

        if prev_x < 0 or prev_x > 7 or prev_y < 0 or prev_y > 7:
            print("Position is out of bounds")
            return False
        if new_x < 0 or new_x > 7 or new_y < 0 or new_y > 7:
            print("Move is out of bounds")
            return False

        if self.board[prev_y*8 + prev_x] == 0:
            print("There is no figure on the Position " + chessEncoder(prev_x, prev_y))
            return False
        
        if prev_x == new_x and prev_y == new_y:
            print("You can't stay in the same position")
            return False

        else:
            if self.board[prev_y*8 + prev_x].owner != self.turn:
                print(bcolors.FAIL + "It is not your turn" + bcolors.ENDC)
                return False
            # Validate move through pieces move method
            if self.board[prev_y*8 + prev_x].move(new_x, new_y):
                # Valid Move
                # KILL THE PIECE
                if self.board[new_y*8 + new_x] != 0:
                    self.board[new_y*8 + new_x] = 0

                self.board[prev_y*8 + prev_x].updatePos(new_x, new_y)
                self.board[new_y*8 + new_x] = self.board[prev_y*8 + prev_x]
                self.board[prev_y*8 + prev_x] = 0

                if self.turn == self.player1:
                    self.turn = self.player2
                else:
                    self.turn = self.player1
                return True

            else:
                print(bcolors.FAIL + "Move is illegal just like YOU" + bcolors.ENDC) # Debug Statements Sollten vor Abgabe raus
                return False
                
        
g = Game("Green","Red")
running = True
g.printBoard()
while running:
    if g.turn == g.player1:
        print("It's " + bcolors.OKGREEN + str(g.turn) + bcolors.ENDC +"'s turn")
    else:
        print("It's " + bcolors.FAIL + str(g.turn) + bcolors.ENDC +"'s turn")
    print("Enter a move like \"A2 to A3\": ")
    move = input()
    if move == "exit" or move == "quit" or move == "q":
        break
    if move == "s":
        if g.turn == g.player1:
            g.turn = g.player2
        else:
            g.turn = g.player1
        continue
    pos = move[0:2]
    to = move[-2:]
    print(str(pos) + " to " + str(to))
    from_x = chessDecoder(pos)[0]
    from_y = chessDecoder(pos)[1]
    to_x = chessDecoder(to)[0]
    to_y = chessDecoder(to)[1]
    g.move(from_x, from_y, to_x, to_y)
    g.printBoard()