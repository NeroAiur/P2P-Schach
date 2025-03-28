two_d_array = [[0 for x in range(8)] for y in range(8)]

two_d_array[5][5] = 25

for i in range(8):
    two_d_array[4][i] = i

for i in range(8):
    print(two_d_array[i])

class Letter:
    def __init__(self, letter, pos_x, pos_y):
        self.letter = letter
        self.pos_x = pos_x
        self.pos_y = pos_y

    def write_into_array(self, array):
        array[self.pos_x][self.pos_y] = self.letter

A = Letter("A", 3, 4)
A.write_into_array(two_d_array)

print("--------------------------------------------------------------------")
for i in range(8):
    print(two_d_array[i])
