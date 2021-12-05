import numpy as np
import matplotlib.pyplot as plt
from abc import ABC

import game_of_life_interface


class GameOfLife(game_of_life_interface.GameOfLife, ABC):
    # This is the way you construct a class that inherits properties
    def __init__(self, size_of_board, board_start_mode, rules, rle, pattern_position):
        self.size_of_board = size_of_board
        self.board_start_mode = board_start_mode
        self.rules = rules
        self.rle = rle
        self.pattern_position = pattern_position  # method to use pairs in python
        self.board = self.create_board()

    def create_board(self):
        """ function that build the board
        :return:
        """
        if not self.rle.strip():
            board = self.mode()
        else:
            board = self.run_encoding()
        return board

    def run_encoding(self):
        """ function that take the rle string and build the pattern on the board"""
        string = self.rle  # example rle = "7bo6b$6bobo5b$7bo6b2$5b5o4b$4bo5bob2o$3bob2o3bob2o$3bobo2bobo3b$2obo3b"
        k = self.size_of_board
        self.pattern_position_row, self.pattern_position_col = self.pattern_position
        matrix = np.zeros(([k, k])).tolist()
        v = self.pattern_position_row
        t = 0
        u = 0
        q1 = 0
        while q1 != 1:
            while True:
                for i in range(0, len(string)):
                    q = string[i + u]
                    if string[i + u] != '$' and string[i + u] != '!':
                        if string[i + u] == 'b':
                            matrix[v][i + t + self.pattern_position_col] = 0
                        elif string[i + u] == 'o':
                            matrix[v][i + t + self.pattern_position_col] = 255
                        elif string[i + u].isdigit:
                            number = self.check_full_number(i + u, string)
                            if number < 10:
                                f1 = number * string[i + 1 + u]
                                if f1 == "{}".format('$' * number):
                                    v += number - 1
                                if f1 == "{}".format('b' * number):
                                    for var in range(0, number):
                                        matrix[v][i + var + t + self.pattern_position_col] = 0
                                    t += number - 2
                                elif f1 == "{}".format('o' * number):
                                    for var in range(0, number):
                                        matrix[v][i + var + t + self.pattern_position_col] = 255
                                    t += number - 2
                            elif number >= 10:

                                f1 = number * string[i + 2 + u]
                                if f1 == "{}".format('$' * number):
                                    v += len(f1) - 1
                                if f1 == "{}".format('b' * number):
                                    for var in range(0, number):
                                        matrix[v][i + var + t + self.pattern_position_col] = 0
                                    t += number - 2
                                elif f1 == "{}".format('o' * number):
                                    for var in range(0, number):
                                        matrix[v][i + var + t + self.pattern_position_col] = 255
                                    t += number - 2
                                u += 1

                    elif string[i + u] == '$':
                        v += 1
                        string = string[i + 1 + u:]
                        t = 0
                        u = 0
                        break
                    if string[i + u] == '!':
                        q1 = 1
                        break
                if q1 == 1:
                    break
        return matrix

    def check_full_number(self, index, string):
        l = string[index + 1]
        if str(l).isdigit():
            return int(string[index] + l)
        elif not string[index + 1].isdigit():
            return int(string[index])

    def mode(self):
        """ function that set to board mode"""
        a = self.board_start_mode
        c = self.size_of_board
        # pick_from4 = stay the same ( all zeros) but add a Gosper Glider Gun (GGG)
        if a == 1:
            b = np.random.choice((0, 255), size=(c, c), p=(0.5, 0.5))
        elif a == 2:
            b = np.random.choice((0, 255), size=(c, c), p=(0.2, 0.8))
        elif a == 3:
            b = np.random.choice((0, 255), size=(c, c), p=(0.8, 0.2))
        elif a == 4:
            self.pattern_position = (10, 10)
            y, x = self.pattern_position  # must be bigger them (something like) size 50
            matrix = np.zeros(([c, c])).tolist()
            matrix[0 + y][24 + x] = 255
            for i in [22 + x, 24 + x]:
                matrix[1 + y][i] = 255
            for i in [12 + x, 13 + x, 20 + x, 21 + x, 34 + x, 35 + x]:
                matrix[2 + y][i] = 255
            for i in [11 + x, 15 + x, 20 + x, 21 + x, 34 + x, 35 + x]:
                matrix[3 + y][i] = 255
            for i in [0 + x, 1 + x, 10 + x, 16 + x, 20 + x, 21 + x]:
                matrix[4 + y][i] = 255
            for i in [0 + x, 1 + x, 10 + x, 14 + x, 16 + x, 17 + x, 22 + x, 24 + x]:
                matrix[5 + y][i] = 255
            for i in [10 + x, 16 + x, 24 + x]:
                matrix[6 + y][i] = 255
            for i in [11 + x, 15 + x]:
                matrix[7 + y][i] = 255
            for i in [12 + x, 13 + x]:
                matrix[8 + y][i] = 255
                b = matrix

        return b

    def update(self):
        """ This method updates the board game by the rules of the game. Do a single iteration.
        Input None.
        :return: Output None. """
        self.rules_interface()
        matrix = self.board
        next_board = np.zeros(([self.size_of_board, self.size_of_board])).tolist()
        for r in range(self.size_of_board):
            for c in range(self.size_of_board):
                if self.cell_neighbors_status(r, c, matrix) == 1:
                    next_board[r][c] = 255
                elif self.cell_neighbors_status(r, c, matrix) == 0:
                    next_board[r][c] = 0
        self.board = next_board

    def cell_neighbors_status(self, row, col, board):
        matrix1 = board
        numbers_alive = self.count_cells_neighbors(row, col, matrix1)
        f1 = 0
        f2 = 0
        if matrix1[row][col] == 0:
            for i in range(len(self.born)):
                if numbers_alive == self.born[i]:
                    f1 = 1  # if a cell is going to be alive next turn
                    break
        elif matrix1[row][col] == 255:
            for i in range(len(self.surv)):
                if numbers_alive == self.surv[i]:
                    f2 = 1
                    break
        if f1 == 1:
            return 1
        elif f2 == 1:
            return 1
        else:
            return 0

    def count_cells_neighbors(self, row, col, board):
        number = 0
        f1 = 0
        matrix = board
        if row == 0 and col != 0 and col != self.size_of_board - 1:
            if matrix[self.size_of_board - 1][col - 1] == 255:
                number += 1
            if matrix[self.size_of_board - 1][col] == 255:
                number += 1
            if matrix[self.size_of_board - 1][col + 1] == 255:
                number += 1

            if matrix[row][col - 1] == 255:
                number += 1
            if matrix[row][col + 1] == 255:
                number += 1

            if matrix[row + 1][col - 1] == 255:
                number += 1
            if matrix[row + 1][col] == 255:
                number += 1
            if matrix[row + 1][col + 1] == 255:
                number += 1
            f1 = 1
        elif col == 0 and row != 0 and (row != self.size_of_board - 1):
            if matrix[row - 1][self.size_of_board - 1] == 255:
                number += 1
            if matrix[row][self.size_of_board - 1] == 255:
                number += 1
            if matrix[row + 1][self.size_of_board - 1] == 255:
                number += 1

            if matrix[row - 1][col] == 255:
                number += 1
            if matrix[row - 1][col + 1] == 255:
                number += 1

            if matrix[row][col + 1] == 255:
                number += 1

            if matrix[row + 1][col] == 255:
                number += 1
            if matrix[row + 1][col + 1] == 255:
                number += 1
            f1 = 1
        elif col == 0 and row == 0:
            if matrix[self.size_of_board - 1][self.size_of_board - 1] == 255:
                number += 1
            if matrix[row][self.size_of_board - 1] == 255:
                number += 1
            if matrix[self.size_of_board - 1][col] == 255:
                number += 1

            if matrix[row][col + 1] == 255:
                number += 1

            if matrix[row + 1][col] == 255:
                number += 1
            if matrix[row + 1][col + 1] == 255:
                number += 1
            f1 = 1
        if row == self.size_of_board - 1 and col != self.size_of_board - 1 and col != 0:
            if matrix[0][col] == 255:
                number += 1
            if matrix[0][col - 1] == 255:
                number += 1
            if matrix[0][col + 1] == 255:
                number += 1

            if matrix[row][col - 1] == 255:
                number += 1
            if matrix[row][col + 1] == 255:
                number += 1

            if matrix[row - 1][col - 1] == 255:
                number += 1
            if matrix[row - 1][col] == 255:
                number += 1
            if matrix[row - 1][col + 1] == 255:
                number += 1
            f1 = 1
        elif col == (self.size_of_board - 1) and (row != self.size_of_board - 1) and row != 0:
            if matrix[row - 1][0] == 255:
                number += 1
            if matrix[row][0] == 255:
                number += 1
            if matrix[row + 1][0] == 255:
                number += 1

            if matrix[row - 1][col] == 255:
                number += 1
            if matrix[row - 1][col - 1] == 255:
                number += 1

            if matrix[row][col - 1] == 255:
                number += 1

            if matrix[row + 1][col] == 255:
                number += 1
            if matrix[row + 1][col - 1] == 255:
                number += 1
            f1 = 1
        elif col == self.size_of_board - 1 and row == self.size_of_board - 1:
            if matrix[0][0] == 255:
                number += 1

            if matrix[row][0] == 255:
                number += 1
            if matrix[0][self.size_of_board - 1] == 255:
                number += 1

            if matrix[row][col - 1] == 255:
                number += 1

            if matrix[row - 1][col] == 255:
                number += 1
            if matrix[row - 1][col - 1] == 255:
                number += 1
            f1 = 1
        elif col == self.size_of_board - 1 and row == 0:
            if matrix[row][col - 1] == 255:
                number += 1

            if matrix[row + 1][col] == 255:
                number += 1
            if matrix[row + 1][col - 1] == 255:
                number += 1
            f1 = 1
        elif col == 0 and row == self.size_of_board - 1:
            if matrix[row - 1][col] == 255:
                number += 1

            if matrix[row - 1][col + 1] == 255:
                number += 1
            if matrix[row][col + 1] == 255:
                number += 1
            f1 = 1
        if f1 == 0:
            if matrix[row - 1][col - 1] == 255:
                number += 1
            if matrix[row - 1][col] == 255:
                number += 1
            if matrix[row - 1][col + 1] == 255:
                number += 1

            if matrix[row][col + 1] == 255:
                number += 1
            if matrix[row][col - 1] == 255:
                number += 1

            if matrix[row + 1][col - 1] == 255:
                number += 1
            if matrix[row + 1][col] == 255:
                number += 1
            if matrix[row + 1][col + 1] == 255:
                number += 1
        return number

    def rules_interface(self):
        rules = self.rules
        born = []
        surv = []
        for i in range(len(rules)):
            if rules[i] == 'B':
                for k in range(1, len(rules[i:])):
                    if rules[i + k] == '/':
                        break
                    if rules[i + k].isdigit:
                        born.append(int(rules[i + k]))
                    elif rules[i + k] == 'S':
                        break
            elif rules[i] == 'S':
                for k in range(1, len(rules[i:])):
                    if rules[i + k].isdigit:
                        surv.append(int(rules[i + k]))
                    elif rules[i + k] == 'B':
                        break
        born.sort()
        surv.sort()
        self.born = born
        self.surv = surv

    def display_board(self):
        plt.imshow(self.board)
        plt.show()
        return

    def return_board(self):
        return self.board

    def transform_rle_to_matrix(self, rle):

        string = rle
        k = 1
        n = self.number_of_col(rle)
        for i in range(len(string)):
            if string[i] == '$':
                k += 1
        matrix = np.zeros(([k, n])).tolist()
        v = 0
        t = 0
        u = 0
        q1 = 0
        while q1 != 1:
            while True:
                for i in range(0, len(string)):
                    q = string[i + u]
                    if string[i + u] != '$' and string[i + u] != '!':
                        if string[i + u] == 'b':
                            matrix[v][i + t] = 0
                        elif string[i + u] == 'o':
                            matrix[v][i + t] = 255
                        elif string[i + u].isdigit:
                            number = self.check_full_number(i + u, string)
                            if number < 10:
                                f1 = number * string[i + 1 + u]
                                if f1 == "{}".format('$' * number):
                                    v += number - 1
                                if f1 == "{}".format('b' * number):
                                    for var in range(0, number):
                                        matrix[v][i + var + t] = 0
                                    t += number - 2
                                elif f1 == "{}".format('o' * number):
                                    for var in range(0, number):
                                        matrix[v][i + var + t] = 255
                                    t += number - 2
                            elif number >= 10:
                                f1 = number * string[i + 2 + u]
                                if f1 == "{}".format('$' * number):
                                    v += len(f1) - 1
                                if f1 == "{}".format('b' * number):
                                    for var in range(0, number):
                                        matrix[v][i + var + t] = 0
                                    t += number - 2
                                elif f1 == "{}".format('o' * number):
                                    for var in range(0, number):
                                        matrix[v][i + var + t] = 255
                                    t += number - 2
                                u += 1

                    elif string[i + u] == '$':
                        v += 1
                        string = string[i + 1 + u:]
                        t = 0
                        u = 0
                        break
                    if string[i + u] == '!':
                        q1 = 1
                        break
                if q1 == 1:
                    break
        return matrix

    def number_of_col(self, rle):
        string = rle
        u = 0
        count = 0
        for i in range(0, len(string)):
            l = string[i + u]
            if string[i + u] != '$':
                if string[i + u] == 'o' or string[i + u] == 'b':
                    count += 1
                elif string[i + u].isdigit:
                    number = self.check_full_number(i + u, string)
                    if number < 10:
                        count += number
                        u += 1
                    elif number >= 10:
                        count += number
                        u += 2
            elif string[i + u] == '$':
                return count
                    

    def save_board_to_file(self, file_name):
        plt.imsave(file_name, self.board)


if __name__ == '__main__':  # You should keep this line for our auto-grading code.
    print('write your tests here')  # don't forget to indent your code here!
    dor = GameOfLife(50, 1, 'B3/S23', "",pattern_position=(10, 10))
    dor.rules_interface()
    # print(dor.return_board())
    print(dor.surv, dor.born)
    dor.display_board()
    #dor.update()
    #dor.display_board()
    # print(dor.return_board())
    r = 0
    print(type(dor.board))
    print(dor.transform_rle_to_matrix('11b5ob$b12b4b$8o8oo$o10b6o$o7o9b!'))
    while r != 180:
        dor.update()
        plt.imshow(dor.board)
        plt.pause(0.0005)
        r += 1

    # if a == 1:
    #   for i in range(0, len(b)):
    #      for k in range(0, len(b[i])):
    #         b[i][k] = np.random.choice((0, 255), p=(0.5, 0.5))
