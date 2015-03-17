from random import shuffle
from copy import deepcopy, copy
import threading
from math import sqrt
from gmpy import is_square

class Tree(object):
    def __init__(self, action = 'root', parent = None, state = None):
        """
        :param action: up left down or right
        :param state: current board
        """
        self.action = action
        self.parent = parent
        self.closed_list = [state]
        self.state = state
        self.heuristic = self.get_heuristic()

    def get_heuristic(self):
        board = deepcopy(self.state.get_board_list())
        heuristic = 0
        x = board.index('')
        board[x] = 0
        board_matrix = [(x,y) for x in range(self.state.block_size) for y in range(self.state.block_size)]
        # board_abs = [i for i in range(9)]
        # map_mat = zip(board_abs, board_comparator)
        # print(board)
        for pos, ele in zip(board_matrix, board):
            pos_x, pos_y = pos
            ele_pos_x, ele_pos_y = board_matrix[ele]
            dist_x = abs(pos_x - ele_pos_x)
            dist_y = abs(pos_y - ele_pos_y)
            # print("ele: {} x_dis: {} y_dis: {}, pos_x: {}, pos_y: {} ele_pos_x: {}, ele_pos_y: {}, dist: {}".format(ele, dist_x,dist_y, pos_x, pos_y, ele_pos_x, ele_pos_y, dist_y+dist_x))
            heuristic += dist_x + dist_y
        return heuristic

    # def set_left(self, tree):
    #     self.left = tree
    
    # def set_right(self, tree):
    #     self.right = tree
    
    # def set_up(self, tree):
    #     self.up = tree
    
    # def set_down(self, tree):
    #     self.down = tree

class SolveMethod():
    def __init__(self, initial_state, visited_states):
        self.fringe = [Tree(state = initial_state)]
        # print(self.fringe[0].state)
        self.visited_states = visited_states
        if not self.is_visited(initial_state):
            self.add_visited(initial_state)

        self.final_state = [i for i in range(initial_state.block_size ** 2)]
        self.final_state[0] = ''

    def expand_nodes(self, node):
        """
        :param node: is a board
        :return: sucessors
        """
        c1, c2 = Board(list(node.state.get_board_list())), Board(list(node.state.get_board_list()))
        c3, c4 = Board(list(node.state.get_board_list())), Board(list(node.state.get_board_list()))
        sucessors = []
        up = c1.move_up()
        if not self.is_visited(up):
            sucessors.append(Tree('up', node, up))
            self.add_visited(up)

        down = c2.move_down()
        if(not self.is_visited(down)):
            sucessors.append(Tree('down', node, down))
            self.add_visited(down)
        # sucessors += [Tree('down', node, down)] if not self.is_visited(down) else []

        left = c3.move_left()
        if not self.is_visited(left):
            sucessors.append(Tree('left', node, left))
            self.add_visited(left)

        right = c4.move_right()
        if not self.is_visited(right):
            sucessors.append(Tree('right', node, right))
            self.add_visited(right)
        return sucessors

    def goal_test(self, state):
        # print(final_state)
        # print(final_state, list(state))
        if state == self.final_state:
            return True
        return False

    def is_visited(self, board):
        if board.get_board_list() in self.visited_states:
            return True
        return False

    def add_visited(self,board):
        self.visited_states.append(board.get_board_list())
        # print(self.visited_states)
        # self.i += 1
        # print(self.i)
        # print(self.visited_states)
        # print(self.visited_states)

class SolveBFS(SolveMethod):
    def __init__(self, initial_state, visited_states):
        super(SolveBFS, self).__init__(initial_state, visited_states)

    def tree_search(self):
        self.i = 0
        while not self.i == 380000:
            if self.fringe == []:
                return False
            node = self.fringe.pop(0)
            # print(node.state)
            if self.goal_test(node.state.get_board_list()):
                return node
            self.fringe += self.expand_nodes(node)
            self.fringe.sort(key = lambda x: x.heuristic)


class Solver(threading.Thread):
    def __init__(self, initial_state, solve_method):
        super(Solver, self).__init__()
        self.solver = solve_method

    def run(self):
        x = self.solver.tree_search()
        if x:
            print(x.state)
            y = x.parent
            while y is not None:
                print(y.state)
                y = y.parent
        else:
            print("No solution Found!")

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

if __name__ == '__main__':
    # board = Board(list(i for i in range(9)))
    visited_states = []
    # board = Board([1,5,2,3,9,6,7,15,4,10,11,14,8,'',12,13])
    board = Board([1,2,7,10,13,6,15,23,8,14,16,9,20,12,5,17,18,'',19,4,21,22,11,24,3])
    # board = Board([1,2,5,3,4,'',6,7,8])
    # board = Board([1,'',2,3,4,5,6,7,8])
    # board = Board([1,5,2,'',6,8,10,3,4,13,9,7,12,14,15,11])
    # print(board)
    # board = Board([1,4,2,3,'',5,6,7,8])
    solve_method= SolveBFS(board, visited_states)
    solver = Solver(board,solve_method)
    # solver.run()
    solver.run()
    # t = Tree(state = board)
    # print("Heuristic: {}".format(t.heuristic))