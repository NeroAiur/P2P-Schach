def chessEncoder(x, y):
    return "ABCDEFGH"[x] + str(y+1)

def chessDecoder(string):
    return [ord(string[0].upper()) - 65, int(string[1]) - 1]