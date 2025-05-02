from __future__ import annotations
from copy import deepcopy
import json
from .Pieces import *
from .ChessTranscode import *
from .Move import Move

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

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.moves = []
        self.pieces = []
        self.king = None
        self.inCheck = False
        self.time = None

    def addTime(self, add_time):
        self.time += add_time

class Game:
    def __init__(self, player1: Player, player2: Player, start_time=150, add_time=10):
        self.player1 = player1 # player 1 is white 
        self.player2 = player2 # player 2 is black
        self.board = self.initBoard()
        self.initPlayerPieces()
        self.turn = player1
        self.generateAllMoves(player1)
        self.generateAllMoves(player2)

    def printBoard(self):
        for i in range(8):
            print (str(8-i) + " |", end=' ')
            for j in range(8):
                if self.getBoard(j, 7-i) == 0:
                    print("0", end=' ')
                else:
                    if self.getBoard(j, 7-i).color == "white":
                        print(bcolors.OKGREEN + self.board[(7-i)*8+j].name + bcolors.ENDC, end=' ')
                    else:
                        print(bcolors.FAIL + self.board[(7-i)*8+j].name + bcolors.ENDC, end=' ')
                    
            print()
        print("    ---------------")
        print("    A B C D E F G H")

    def setBoard(self, x, y, content):
        self.board[y*8 + x] = content

    def getBoard(self, x, y):
        return self.board[y*8 + x]
    
    def getFENBoard(self):
        space = 0
        fenboard = ""
        for y in range(8):
            for x in range(8):
                if self.getBoard(x, y) == 0:
                    space += 1
                else:
                    if space > 0:
                        fenboard += str(space)
                        space = 0
                    letter = self.getBoard(x, y).name
                    if self.getBoard(x, y).color == "black":
                        fenboard += letter.lower()
                    else:
                        fenboard += letter.upper()
            if space > 0:
                fenboard += str(space)
                space = 0
            fenboard += "/"
        return fenboard

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
        board[3] = Queen(3, 0, self.player1, "white", self)
        board[7*8 + 3] = Queen(3, 7, self.player2, "black", self)

        # spawn in the kings
        board[4] = King(4, 0, self.player1, "white", self)
        board[7*8 + 4] = King(4, 7, self.player2, "black", self)

        return board
    
    def initPlayerPieces(self):
        for x in range(8):
            for y in range(8):
                if self.getBoard(x, y) != 0:
                    if y < 2:
                        self.player1.pieces.append(self.getBoard(x, y))
                    if y > 5:
                        self.player2.pieces.append(self.getBoard(x, y))

        self.player1.king = self.getBoard(4, 0)
        self.player2.king = self.getBoard(4, 7)

    def move(self, prev_x, prev_y, new_x, new_y):

        # Anpassung der Werte, weil das was ausm Frontend kommt um eins zu niedrig ist und ich zu dumm bin um das im Frontend anzupassen
        prev_y = prev_y + 1
        new_y = new_y + 1
        
        if prev_x < 0 or prev_x > 7 or prev_y < 0 or prev_y > 7:
            print("Position is out of bounds")
            return False
        
        if new_x < 0 or new_x > 7 or new_y < 0 or new_y > 7:
            print("Move is out of bounds")
            return False

        if self.board[prev_y*8 + prev_x] == 0:
            print("There is no piece on the Position " + chessEncoder(prev_x, prev_y))
            return False
        
        if prev_x == new_x and prev_y == new_y:
            print("You can't stay in the same position")
            return False

        else:
            if self.getBoard(prev_x, prev_y).owner != self.turn:
                print(bcolors.FAIL + "It is not your turn" + bcolors.ENDC)
                return False
            
            # validate move
            for move in self.turn.moves:
                if move.from_x == prev_x and move.from_y == prev_y and move.to_x == new_x and move.to_y == new_y:
                    # Valid Move
                    move.piece.has_been_moved = True
                    
                    # castling
                    if move.linked_to != None:
                        self.turn.king.has_castled = True

                        rook_move = move.linked_to
                        rook_move.piece.has_been_moved = True
                        rook_move.piece.updatePos(rook_move.to_x, rook_move.to_y)
                        self.setBoard(rook_move.to_x, rook_move.to_y, rook_move.piece)
                        self.setBoard(rook_move.from_x, rook_move.from_y, 0)
                        
                    # "moved two fields last turn"-upate for 'en passant' 
                    for piece in self.turn.pieces:
                        if piece.name == "P":
                            piece.moved_two_fields_last_turn = False

                    if move.piece.name == 'P' and abs(move.from_y - move.to_y) == 2:
                        move.piece.moved_two_fields_last_turn = True

                    # KILL THE PIECE -ANNIHILATION!!!
                    if move.kills != None:
                        if self.turn == self.player1:
                            self.player2.pieces.remove(move.kills)
                        else:
                            self.player1.pieces.remove(move.kills)
                        self.setBoard(move.kills.pos_x, move.kills.pos_y, 0)

                    move.piece.updatePos(new_x, new_y)
                    self.setBoard(new_x, new_y, move.piece)
                    self.setBoard(prev_x, prev_y, 0)
                    return True

        # no legal move found
        print(bcolors.FAIL + "Move is illegal just like YOU" + bcolors.ENDC) # Debug Statements Sollten vor Abgabe raus |BOOKMARK
        return False
            
    def generateAllMoves(self, player: Player): # Definitiv die effizienteste Methode jaja bruteforce ist sehr TOLL mir gehts gut
        player.moves = []
        enemy_player = self.player2 if player == self.player1 else self.player1
        to_remove = []

        # generate all theoretically possible moves
        # pieces
        for piece in player.pieces:
            new_moves = piece.bruteForceGenerateAllMoves()
            if new_moves != None:
                player.moves.extend(new_moves)

        # special moves
        # en passant
        for enemy_piece in enemy_player.pieces:
            if enemy_piece.name == 'P' and enemy_piece.moved_two_fields_last_turn:
                for own_piece in player.pieces:
                    if own_piece.name == 'P' and (own_piece.pos_x == enemy_piece.pos_x + 1 or own_piece.pos_x == enemy_piece.pos_x - 1):
                        if player.color == 'white' and own_piece.pos_y == 4:
                            player.moves.append(Move(own_piece, own_piece.pos_x, own_piece.pos_y, enemy_piece.pos_x, enemy_piece.pos_y + 1, enemy_piece))
                        if player.color == 'black' and own_piece.pos_y == 3:
                            player.moves.append(Move(own_piece, own_piece.pos_x, own_piece.pos_y, enemy_piece.pos_x, enemy_piece.pos_y - 1, enemy_piece))

        # castling
        if player.king.has_been_moved == False and player.king.has_castled == False and player.inCheck == False:
            y_pos = 0
            if player.color == 'black':
                y_pos = 7
            rook_pos = self.getBoard(0, y_pos)
            if rook_pos != 0 and rook_pos.name == "R" and rook_pos.has_been_moved == False:
                # long castling
                if self.getBoard(1, y_pos) == 0 and self.getBoard(2, y_pos) == 0 and self.getBoard(3, y_pos) == 0:
                    move_is_possible = True
                    for piece in enemy_player.pieces:
                        if piece.validateMove(1, y_pos) or piece.validateMove(2, y_pos) or piece.validateMove(3, y_pos):
                            move_is_possible = False
                            break
                    if move_is_possible:
                        player.moves.append(Move(player.king, player.king.pos_x, player.king.pos_y, 2, y_pos, None, Move(rook_pos, rook_pos.pos_x, rook_pos.pos_y, 3, y_pos, None)))
                # short castling
                if self.getBoard(5, y_pos) == 0 and self.getBoard(6, y_pos) == 0:
                    rook_pos = self.getBoard(7, y_pos)
                    move_is_possible = True
                    for piece in enemy_player.pieces:
                        if piece.validateMove(5, y_pos) or piece.validateMove(6, y_pos):
                            move_is_possible = False
                            break
                    if move_is_possible:
                        player.moves.append(Move(player.king, player.king.pos_x, player.king.pos_y, 6, y_pos, None, Move(rook_pos, rook_pos.pos_x, rook_pos.pos_y, 5, y_pos, None)))

        # saves move for removal bc it is illegal (e.g. inflicting checkmate on oneself)
        for move in player.moves:
            if self.simulate_move(move, player):
                to_remove.append(move)

        # removes illegal moves
        for move in to_remove:
            if move in player.moves:
                player.moves.remove(move)

        player.moves = list(set(player.moves))
                
    # returns true if the players king is in check after making this move   == move is illegal
    # returns false otherwise                                               == move is legal
    def simulate_move(self, move: Move, player: Player):  
        # if King moves
        prev_king_pos_x = player.king.pos_x
        prev_king_pos_y = player.king.pos_y
        if move.piece.name == 'K':
            player.king.updatePos(move.to_x, move.to_y)
        
        copy_of_game = deepcopy(self)

        enemy_player = copy_of_game.player2
        if copy_of_game.player2.color == player.color:
            enemy_player = copy_of_game.player1

        # if enemy there, ANNIHILATE IT
        if move.kills != None:
            enemy_player.pieces.remove(copy_of_game.getBoard(move.kills.pos_x, move.kills.pos_y))
            
        copy_of_game.setBoard(move.to_x, move.to_y, move.piece)
        copy_of_game.setBoard(move.from_x, move.from_y, 0)

        for piece in enemy_player.pieces:
            piece.game = copy_of_game
            if piece.validateMove(player.king.pos_x, player.king.pos_y):
                player.king.updatePos(prev_king_pos_x, prev_king_pos_y)
                piece.game = self
                return True
            piece.game = self

        player.king.updatePos(prev_king_pos_x, prev_king_pos_y)
        return False
    
    # --------------- turn during active game
    def run_turn(self, move):
        enemy_player = self.player2 if self.turn == self.player1 else self.player1
        self.turn.inCheck = False
        for piece in enemy_player.pieces:
            if piece.validateMove(self.turn.king.pos_x, self.turn.king.pos_y):
                self.turn.inCheck = True
        self.generateAllMoves(self.turn)

        # GameOver check
        if len(self.turn.moves) == 0:
            if self.turn.inCheck:
                print(bcolors.FAIL + "CHECKMATE" + bcolors.ENDC)
                if self.turn == self.player1:
                    # player2.name + " wins"
                    pass
                else:
                    # player1.name + " wins"
                    pass
            else:
                #"STALEMATE"
                pass

        if self.turn.inCheck:
            # "You are CZECH"
            pass

        pos = move[0:2]
        to = move[-2:]
        from_x = chessDecoder(pos)[0]
        from_y = chessDecoder(pos)[1]
        to_x = chessDecoder(to)[0]
        to_y = chessDecoder(to)[1]

        if self.move(from_x, from_y, to_x, to_y):
            # update moveset
            self.generateAllMoves(self.turn) 
            if  self.turn == self.player1:
                self.turn = self.player2
            else:
                self.turn = self.player1

        return json.dumps(self.getFENBoard())
    # ---------------

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

            # check for check kek
            enemy_player = self.player2 if self.turn == self.player1 else self.player1
            self.turn.inCheck = False
            for piece in enemy_player.pieces:
                if piece.validateMove(self.turn.king.pos_x, self.turn.king.pos_y):
                    self.turn.inCheck = True

            self.generateAllMoves(self.turn)

            # print all moves
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

            print(self.getFENBoard())

            # GameOver check
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

                # update moveset
                self.generateAllMoves(self.turn) 
                if  self.turn == self.player1:
                    self.turn = self.player2
                else:
                    self.turn = self.player1
