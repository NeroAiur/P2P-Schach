from __future__ import annotations
from copy import deepcopy
from Pieces import *
from ChessTranscode import *
from Move import Move
import os

clear = lambda: os.system('cls')

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

class Move:
    def __init__(self, piece: Piece, from_x, from_y, to_x, to_y, pawn_condition=None):
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
        self.time = None

    def addTime(self, add_time):
        self.time += add_time

class Game:
    def __init__(self, player1: Player, player2: Player, start_time=150, add_time=10):
        self.player1 = player1 # player 1 is white 
        self.player2 = player2
        self.board = self.initBoard()
        self.initPlayerPieces()
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
    
    def initPlayerPieces(self):
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

        for move in player.moves:
            if self.simulate_move(move, player):
                to_remove.append(move)

        # move move move
        for move in to_remove:
            if move in player.moves:
                player.moves.remove(move)

        player.moves = list(set(player.moves))
                

    def simulate_move(self, move: Move, player: Player):  
        # Falls der König sich bewegt
        prev_king_pos_x = player.king.pos_x
        prev_king_pos_y = player.king.pos_y
        if move.piece.name == 'K':
            player.king.updatePos(move.to_x, move.to_y)
        
        copy_of_game = deepcopy(self)

        enemy_player = copy_of_game.player2
        if copy_of_game.player2.color == player.color:
            enemy_player = copy_of_game.player1

        # wenn ein gegner dort ist, vernichte ihn
        if copy_of_game.getBoard(move.to_x, move.to_y) != 0:
            enemy_player.figures.remove(copy_of_game.getBoard(move.to_x, move.to_y))
            
        copy_of_game.setBoard(move.to_x, move.to_y, move.piece)
        copy_of_game.setBoard(move.from_x, move.from_y, 0)

        for figure in enemy_player.figures:
            figure.game = copy_of_game
            if figure.validateMove(player.king.pos_x, player.king.pos_y):
                player.king.updatePos(prev_king_pos_x, prev_king_pos_y)
                figure.game = self
                return True
            figure.game = self

        player.king.updatePos(prev_king_pos_x, prev_king_pos_y)
        return False
    
    def run(self):
        running = True
        player1.moves = self.generateAllMoves(player1)
        player2.moves = self.generateAllMoves(player2)
        while running:
            self.printBoard()
            if self.turn == self.player1:
                print("It's " + bcolors.OKGREEN + str(self.turn.name) + bcolors.ENDC +"'s turn")
            else:
                print("It's " + bcolors.FAIL + str(self.turn.name) + bcolors.ENDC +"'s turn")
            print("Enter a move like \"A2 to A3\" or \"c7 c6\" or quit with 'q': ")

            #check for check kek
            enemy_player = self.player2 if self.turn == self.player1 else self.player1
            self.turn.inCheck = False
            for figure in enemy_player.figures:
                if figure.validateMove(self.turn.king.pos_x, self.turn.king.pos_y):
                    self.turn.inCheck = True

            self.generateAllMoves(self.turn)

            #print all moves
            print("Possible moves: ")
            print("Pawns:  ", end=' ')
            for move in self.turn.moves:
                if move.piece.name == 'P':
                    print(chessEncoder(move.from_x, move.from_y) + " to " + chessEncoder(move.to_x, move.to_y) + ",", end=' ')
            print()

            print("Knights:", end=' ')
            for move in self.turn.moves:
                if move.piece.name == 'N':
                    print(chessEncoder(move.from_x, move.from_y) + " to " + chessEncoder(move.to_x, move.to_y) + ",", end=' ')
            print()

            print("Bishops:", end=' ')
            for move in self.turn.moves:
                if move.piece.name == 'B':
                    print(chessEncoder(move.from_x, move.from_y) + " to " + chessEncoder(move.to_x, move.to_y) + ",", end=' ')
            print()

            print("Rooks:  ", end=' ')
            for move in self.turn.moves:
                if move.piece.name == 'R':
                    print(chessEncoder(move.from_x, move.from_y) + " to " + chessEncoder(move.to_x, move.to_y) + ",", end=' ')
            print()

            print("Queen:  ", end=' ')
            for move in self.turn.moves:
                if move.piece.name == 'Q':
                    print(chessEncoder(move.from_x, move.from_y) + " to " + chessEncoder(move.to_x, move.to_y) + ",", end=' ')
            print()

            print("King:   ", end=' ')
            for move in self.turn.moves:
                if move.piece.name == 'K':
                    print(chessEncoder(move.from_x, move.from_y) + " to " + chessEncoder(move.to_x, move.to_y) + ",", end=' ')
            print()

            # GameOver Check
            if len(self.turn.moves) == 0:
                if self.turn.inCheck:
                    print(bcolors.FAIL + "CHECKMATE" + bcolors.ENDC)
                    if self.turn == self.player1:
                        print(bcolors.FAIL + player2.name + " wins" + bcolors.ENDC)
                    else:
                        print(bcolors.OKGREEN + player1.name + " wins" + bcolors.ENDC)
                else:
                    print(bcolors.OKGREEN + "STALEMATE" + bcolors.ENDC)
                running = False
                break

            if self.turn.inCheck:
                print(bcolors.FAIL + "You are CZECH" + bcolors.ENDC)

            move = input()
            if move == "exit" or move == "quit" or move == "q":
                break
            if move == "s":
                if self.turn == self.player1:
                    self.turn = self.player2
                else:
                    self.turn = self.player1
                continue
            pos = move[0:2]
            to = move[-2:]
            print(str(pos) + " to " + str(to))
            from_x = chessDecoder(pos)[0]
            from_y = chessDecoder(pos)[1]
            to_x = chessDecoder(to)[0]
            to_y = chessDecoder(to)[1]
            if self.move(from_x, from_y, to_x, to_y):

                self.generateAllMoves(self.turn) # update moveset
                if  self.turn == self.player1:
                    self.turn = self.player2
                else:
                    self.turn = self.player1

            clear()

player1 = Player("Player 1", "white")
player2 = Player("Player 2", "black")

g = Game(player1, player2)
g.run()