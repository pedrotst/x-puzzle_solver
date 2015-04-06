from math import sqrt
from gmpy import is_square
import random
from copy import copy

class Board(object):
    def __init__(self, numbers_list):
        self.numbers_list = numbers_list
        # shuffle(self.numbers_list)
        self.blank_pos = numbers_list.index('')
        list_size = len(numbers_list)
        if is_square(list_size):
            self.block_size = int(sqrt(list_size))
        else:
            raise AttributeError("List passed is not a square. This cannot be a game!")

    def randomize(self):
        # 0 = up
        # 1 = down
        # 2 = left
        # 3 = right
        move_list = [random.randint(0,4) for i in range(random.randint(0,1000))]
        moves_list = [copy(self.numbers_list)]
        for i in move_list:
            if i == 0:
                self.move_up()
            elif i == 1:
                self.move_down()
            elif i == 2:
                self.move_left()
            elif i == 3:
                self.move_right()
            if not self.numbers_list in moves_list:
                moves_list.append(copy(self.numbers_list))
        return moves_list


    def move(self, move_to):
        if (((not self.blank_pos == 3) and (not self.blank_pos == 6) and self.blank_pos == move_to + 1)
            or ((not self.blank_pos == 2) and (not self.blank_pos == 5) and self.blank_pos == move_to - 1)
            or self.blank_pos == move_to - 3
            or self.blank_pos == move_to + 3):
            self.numbers_list[self.blank_pos], self.numbers_list[move_to] = self.numbers_list[move_to], self.numbers_list[self.blank_pos]
            self.blank_pos = move_to
        return self

    def move_up(self):
        blk = self.block_size
        if (blk <= self.blank_pos):
            self.numbers_list[self.blank_pos], self.numbers_list[self.blank_pos - blk] = \
            self.numbers_list[self.blank_pos - blk], self.numbers_list[self.blank_pos]
            self.blank_pos = self.blank_pos - blk
        return self

            
    def move_down(self):
        blk = self.block_size
        if (self.blank_pos < blk*blk-blk):
            self.numbers_list[self.blank_pos], self.numbers_list[self.blank_pos + blk] = \
            self.numbers_list[self.blank_pos + blk], self.numbers_list[self.blank_pos]
            self.blank_pos = self.blank_pos + blk
        return self

            
    def move_left(self):
        blk = self.block_size
        condition = False
        for i in range(blk):
            condition = condition or (self.blank_pos == blk*i)
        # if not (self.blank_pos == 0 or self.blank_pos == blk or self.blank_pos == blk * 2):
        if not condition:
            self.numbers_list[self.blank_pos], self.numbers_list[self.blank_pos - 1] = \
            self.numbers_list[self.blank_pos - 1], self.numbers_list[self.blank_pos]
            self.blank_pos = self.blank_pos - 1
        return self

            
    def move_right(self):
        blk = self.block_size
        condition = False
        for i in range(1,blk+1):
            condition = condition or (self.blank_pos == blk*i-1)
        # if not (self.blank_pos == blk-1 or self.blank_pos == blk*2 - 1 or self.blank_pos == blk*3 - 1):
        if not condition:
            self.numbers_list[self.blank_pos], self.numbers_list[self.blank_pos + 1] = \
            self.numbers_list[self.blank_pos + 1], self.numbers_list[self.blank_pos]
            self.blank_pos = self.blank_pos + 1
        return self

    def same_board(self, b2):
        if self.numbers_list is b2.numbers_list:
            return True
        return False

    def get_board_list(self):
        return self.numbers_list


    def __str__(self):
        blk = self.block_size
        string = ''
        for i in range(blk):
            string += str(self.numbers_list[blk*i:blk*(i+1)])
            string += '\n'
        return string

    def __repr__(self):
        return self.__str__()
