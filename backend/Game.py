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
    return [ord(string[0]) - 65, int(string[1]) - 1]

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

class Pawn(Figure): #chess
    def __init__(self, pos_x, pos_y, owner, color, game):
        super().__init__(pos_x, pos_y, owner, color, game)
        self.name = 'P'

    def move(self, new_x, new_y):
        # standard 1 nach vorne
        if self.color == "white":
            if new_y == self.pos_y + 1 and new_x == self.pos_x and self.game.board[new_y*8 + new_x] == 0:
                return True
        else:
            if new_y == self.pos_y - 1 and new_x == self.pos_x and self.game.board[new_y*8 + new_x] == 0:
                return True
            
        # 2 nach vorne beim Start
        if self.color == "white" and self.pos_y == 1:
            if new_y == self.pos_y + 2 and new_x == self.pos_x and self.game.board[new_y*8 + new_x] == 0:
                return True
            
        

class Knight(Figure): #chess
    def __init__(self, pos_x, pos_y, owner, color):
        super().__init__(pos_x, pos_y, owner, color)

class Game: #chess
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.board = self.initBoard()

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
        for i in range(8):
            board[8 + i] = Pawn(i, 1, self.player1, "white", self)
            board[6*8 + i] = Pawn(i, 6, self.player2, "black", self)
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
        else:
            # Validate move through peace method
            self.board[prev_y*8 + prev_x].move(new_x, new_y)
        
g = Game(1,2)
running = True
while running:
    g.printBoard()
    print("Enter a move like \"A2 to A3\": ")
    move = input()
    if move == "exit" or move == "quit" or move == "q":
        break
    pos = move[0:2]
    to = move[-2:]
    print(str(pos) + " to " + str(to))
    g.move(chessDecoder(pos)[0], chessDecoder(pos)[1], chessDecoder(to)[0], chessDecoder(to)[1])