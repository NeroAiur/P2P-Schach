from __future__ import annotations
from copy import deepcopy

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

class Move:
    def __init__(self, piece: Figure, from_x, from_y, to_x, to_y, pawn_condition=None):
        self.piece = piece
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y
        self.is_pawn = self.piece.name == 'P'
        self.pawn_condition = pawn_condition # 0 = has to be empty, 1 there has to be an enemy

    def printMove(self):
        print(self.piece.name + " from " + chessEncoder(self.from_x, self.from_y) + " to " + chessEncoder(self.to_x, self.to_y))

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.moves = []
        self.figures = []
        self.king = None
        self.inCheck = False

class Figure:
    def __init__(self, pos_x, pos_y, owner, color, game: Game):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.owner = owner
        self.color = color
        self.game = game

    def updatePos(self, x, y):
        self.pos_x = x
        self.pos_y = y

    def returnAllMoves(self):
        pass

    def bruteForceGenerateAllMoves(self):
        moves = []

        #if self.name != 'P':
        for x in range(8):
            for y in range(8):
                if self.validateMove(x, y):
                    moves.append(Move(self, self.pos_x, self.pos_y, x, y))
        return moves
        
        #else:
        #    return self.returnAllMoves()
    

class Pawn(Figure):
    def __init__(self, pos_x, pos_y, owner, color, game: Game):
        super().__init__(pos_x, pos_y, owner, color, game)
        self.name = 'P'

    def returnAllMoves(self):
        allMoves = []

        # standard 1 nach vorne
        if self.color == "white":
            if self.pos_y < 7:
                allMoves.append(Move(self, self.pos_x, self.pos_y, self.pos_x, self.pos_y + 1, 0))
        else:
            if self.pos_y > 0:
                allMoves.append(Move(self, self.pos_x, self.pos_y, self.pos_x, self.pos_y - 1, 0))

        # 2 nach vorne von der Startposition
        if self.color == "white" and self.pos_y == 1:
            allMoves.append(Move(self, self.pos_x, self.pos_y, self.pos_x, self.pos_y + 2, 0))
        elif self.pos_y == 6:
            allMoves.append(Move(self, self.pos_x, self.pos_y, self.pos_x, self.pos_y - 2, 0))

        # diagionaler Angriff
        if self.color == "white":
            if self.pos_y < 7 and self.pos_x < 7:
                allMoves.append(Move(self, self.pos_x, self.pos_y, self.pos_x + 1, self.pos_y + 1, 1))
            if self.pos_y < 7 and self.pos_x > 0:
                allMoves.append(Move(self, self.pos_x, self.pos_y, self.pos_x - 1, self.pos_y + 1, 1))
        else:            
            if self.pos_y > 0 and self.pos_x < 7:
                allMoves.append(Move(self, self.pos_x, self.pos_y, self.pos_x + 1, self.pos_y - 1, 1))
            if self.pos_y > 0 and self.pos_x > 0:
                allMoves.append(Move(self, self.pos_x, self.pos_y, self.pos_x - 1, self.pos_y - 1, 1))

        return allMoves

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

class Knight(Figure):
    def __init__(self, pos_x, pos_y, owner, color, game: Game):
        super().__init__(pos_x, pos_y, owner, color, game)
        self.name = 'N'

    def validateMove(self, new_x, new_y):
        if self.game.getBoard(new_x, new_y) == 0 or self.game.getBoard(new_x, new_y).color != self.color: # checken das keine Mate auf dem Feld steht
            if abs(self.pos_x - new_x) == 2 and abs(self.pos_y - new_y) == 1:
                return True
            if abs(self.pos_x - new_x) == 1 and abs(self.pos_y - new_y) == 2:
                return True
        
        return False
    
class Bishop(Figure): 
    def __init__(self, pos_x, pos_y, owner, color, game: Game):
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
    
class Rook(Figure): 
    def __init__(self, pos_x, pos_y, owner, color, game: Game):
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
    
class Queen(Figure): 
    def __init__(self, pos_x, pos_y, owner, color, game: Game):
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

class King(Figure):
    def __init__(self, pos_x, pos_y, owner, color, game: Game):
        super().__init__(pos_x, pos_y, owner, color, game)
        self.name = 'K'
    
    def validateMove(self, new_x, new_y):
        if abs(self.pos_x - new_x) <= 1 and abs(self.pos_y - new_y) <= 1:
            if self.game.getBoard(new_x, new_y) == 0 or self.game.getBoard(new_x, new_y).color != self.color: # friendly fire check
                return True

class Game:
    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1 # player 1 is white 
        self.player2 = player2
        self.board = self.initBoard()
        self.initPlayerFigures()
        self.turn = player1

    def printBoard(self):
        for i in range(8):
            print (str(i+1) + " |", end=' ')
            for j in range(8):
                if self.getBoard(j, i) == 0:
                    print("0", end=' ')
                else:
                    if self.getBoard(j, i).color == "white":
                        print(bcolors.OKGREEN + self.board[i*8+j].name + bcolors.ENDC, end=' ')
                    else:
                        print(bcolors.FAIL + self.board[i*8+j].name + bcolors.ENDC, end=' ')
                    
            print()
        print("    ---------------")
        print("    A B C D E F G H")

    def setBoard(self, x, y, content):
        self.board[y*8 + x] = content

    def getBoard(self, x, y):
        return self.board[y*8 + x]

    def initBoard(self):
        board = [0]*64
        # spawn in the pawns
        for i in range(8):
            board[8 + i] = Pawn(i, 1, self.player1, "white", self)
            board[6*8 + i] = Pawn(i, 6, self.player2, "black", self)

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

        # spawn in the queens
        board[4] = Queen(4, 0, self.player1, "white", self)

        board[7*8 + 4] = Queen(4, 7, self.player2, "black", self)

        # spawn in the kings
        board[3] = King(3, 0, self.player1, "white", self)

        board[7*8 + 3] = King(3, 7, self.player2, "black", self)

        return board
    
    def initPlayerFigures(self):
        for x in range(8):
            for y in range(8):
                if self.getBoard(x, y) != 0:
                    if y < 2:
                        self.player1.figures.append(self.getBoard(x, y))
                    if y > 5:
                        self.player2.figures.append(self.getBoard(x, y))

        self.player1.king = self.getBoard(3, 0)
        self.player2.king = self.getBoard(3, 7)

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
            if self.getBoard(prev_x, prev_y).owner != self.turn:
                print(bcolors.FAIL + "It is not your turn" + bcolors.ENDC)
                return False
            # Validate move
            for move in self.turn.moves:
                if move.from_x == prev_x and move.from_y == prev_y and move.to_x == new_x and move.to_y == new_y:
                    # Valid Move
                    # KILL THE PIECE
                    if self.getBoard(new_x, new_y) != 0:
                        if self.turn == self.player1:
                            self.player2.figures.remove(self.getBoard(new_x, new_y))
                        else:
                            self.player1.figures.remove(self.getBoard(new_x, new_y))
                        self.setBoard(new_x, new_y, 0)

                    self.getBoard(prev_x, prev_y).updatePos(new_x, new_y)
                    self.setBoard(new_x, new_y, self.getBoard(prev_x, prev_y))
                    self.setBoard(prev_x, prev_y, 0)

                    return True

        # kein passender generierter move gefunden
        print(bcolors.FAIL + "Move is illegal just like YOU" + bcolors.ENDC) # Debug Statements Sollten vor Abgabe raus
        return False
            
    def generateAllMoves(self, player: Player): # Definitiv die effizienteste Methode jaja bruteforce ist sehr TOLL mir gehts gut
        player.moves = []

        # Generiere all theoretisch möglichen Züge vom Spieler (inklusive konditioneller Bauernzüge)
        for figure in player.figures:
            new_moves = figure.bruteForceGenerateAllMoves()
            if new_moves != None:
                player.moves.extend(new_moves)


        enemy_player = self.player2 if player == self.player1 else self.player1
        to_remove = []

        # # Gehe durch alle gegnerischen Moves, filtere die Heraus die die aktuelle Figur angreifen
        # # und nach deren Bewegung den König gefährden könnten (Dame, Läufer, Turm)
        # for enemy_move in enemy_player.moves:
        #     for move in player.moves:
        #         if enemy_move.to_x == move.from_x and enemy_move.to_y == move.from_y:
        #             if move.to_x != enemy_move.from_x or move.to_y != enemy_move.from_y: # wenn die Figur dusch diesen Move erledigt wird muss nichts überprüft werden
        #                     if self.move_causes_check(move, player, enemy_move.piece):       # Sollte wahrscheinlich auch nur auf Dame, Läufer, Turm beschränkt werden, gugge erstma
        #                         to_remove.append(move)

        # Wenn der König bewegt wird oder derzeit im Schach steht muss eine genereller Check prüfung erfolgen
        for move in player.moves:
            if self.simulate_move(move, player):
                to_remove.append(move)

        # move move move
        for move in to_remove:
            if move in player.moves:
                player.moves.remove(move)

        player.moves = list(set(player.moves))
                

    def simulate_move(self, move: Move, player: Player):
        if move.piece.name == 'K' and move.to_x == 4 and move.to_y == 1:
            1+1
        test_board = list(self.board)       
        test_board[move.from_y*8 + move.from_x] = 0
        test_board[move.to_y*8 + move.to_x] = move.piece

        # Falls der König sich bewegt
        prev_king_pos_x = player.king.pos_x
        prev_king_pos_y = player.king.pos_y
        if move.piece.name == 'K':
            player.king.updatePos(move.to_x, move.to_y)
        
        copy_of_game = deepcopy(self)
        copy_of_game.board = test_board

        enemy_player = self.player2
        if player2.color == player.color:
            enemy_player = self.player1

        for figure in enemy_player.figures:
            figure.game = copy_of_game
            if figure.validateMove(player.king.pos_x, player.king.pos_y):
                player.king.updatePos(prev_king_pos_x, prev_king_pos_y)
                figure.game = self
                return True
            figure.game = self

        player.king.updatePos(prev_king_pos_x, prev_king_pos_y)
        return False


    def move_causes_check(self, move: Move, player: Player, enemy_figure: Figure):
        test_board = list(self.board)
        test_board[move.from_y*8 + move.from_x] = 0
        test_board[move.to_y*8 + move.to_x] = move.piece

        actual_game = enemy_figure.game         
        copy_of_game = deepcopy(actual_game)
        copy_of_game.board = test_board

        enemy_figure.game = copy_of_game
        newMoveset = enemy_figure.bruteForceGenerateAllMoves()
        enemy_figure.game = actual_game

        for newMove in newMoveset:
            if enemy_figure.name != 'P':
                if newMove.to_x == player.king.pos_x and newMove.to_y == player.king.pos_y:
                    if newMove.pawn_condition == None or newMove.pawn_condition == 1:
                        return True
        
        return False


                
player1 = Player("Player 1", "white")
player2 = Player("Player 2", "black")

g = Game(player1, player2)
running = True
g.printBoard()
player1.moves = g.generateAllMoves(player1)
player2.moves = g.generateAllMoves(player2)
while running:
    if g.turn == g.player1:
        print("It's " + bcolors.OKGREEN + str(g.turn.name) + bcolors.ENDC +"'s turn")
    else:
        print("It's " + bcolors.FAIL + str(g.turn.name) + bcolors.ENDC +"'s turn")
    print("Enter a move like \"A2 to A3\" or \"c7 c6\" or quit with 'q': ")

    #check for check kek
    enemy_player = g.player2 if g.turn == g.player1 else g.player1
    g.turn.inCheck = False
    for figure in enemy_player.figures:
        if figure.validateMove(g.turn.king.pos_x, g.turn.king.pos_y):
            g.turn.inCheck = True

    # print("Your King is at " +chessEncoder(g.turn.king.pos_x, g.turn.king.pos_y))

    g.generateAllMoves(g.turn)

    #print all moves
    # print("Possible moves: ")
    # print("Pawns:  ", end=' ')
    # for move in g.turn.moves:
    #     if move.piece.name == 'P':
    #         print(chessEncoder(move.from_x, move.from_y) + " to " + chessEncoder(move.to_x, move.to_y) + ",", end=' ')
    # print()

    # print("Knights:", end=' ')
    # for move in g.turn.moves:
    #     if move.piece.name == 'N':
    #         print(chessEncoder(move.from_x, move.from_y) + " to " + chessEncoder(move.to_x, move.to_y) + ",", end=' ')
    # print()

    # print("Bishops:", end=' ')
    # for move in g.turn.moves:
    #     if move.piece.name == 'B':
    #         print(chessEncoder(move.from_x, move.from_y) + " to " + chessEncoder(move.to_x, move.to_y) + ",", end=' ')
    # print()

    # print("Rooks:  ", end=' ')
    # for move in g.turn.moves:
    #     if move.piece.name == 'R':
    #         print(chessEncoder(move.from_x, move.from_y) + " to " + chessEncoder(move.to_x, move.to_y) + ",", end=' ')
    # print()

    # print("Queen:  ", end=' ')
    # for move in g.turn.moves:
    #     if move.piece.name == 'Q':
    #         print(chessEncoder(move.from_x, move.from_y) + " to " + chessEncoder(move.to_x, move.to_y) + ",", end=' ')
    # print()

    # print("King:   ", end=' ')
    # for move in g.turn.moves:
    #     if move.piece.name == 'K':
    #         print(chessEncoder(move.from_x, move.from_y) + " to " + chessEncoder(move.to_x, move.to_y) + ",", end=' ')
    # print()

    # GameOver Check
    if len(g.turn.moves) == 0:
        if g.turn.inCheck:
            print(bcolors.FAIL + "CHECKMATE" + bcolors.ENDC)
            if g.turn == g.player1:
                print(bcolors.FAIL + player2.name + " wins" + bcolors.ENDC)
            else:
                print(bcolors.OKGREEN + player1.name + " wins" + bcolors.ENDC)
        else:
            print(bcolors.OKGREEN + "STALEMATE" + bcolors.ENDC)
        running = False
        break
    
    if g.turn.inCheck:
        print(bcolors.FAIL + "You are CZECH" + bcolors.ENDC)

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
    if g.move(from_x, from_y, to_x, to_y):

        g.generateAllMoves(g.turn) # update moveset
        if  g.turn == g.player1:
            g.turn = g.player2
        else:
            g.turn = g.player1



    g.printBoard()

    # check for Check