from random import shuffle
from copy import deepcopy, copy
import threading
from board import Board

class Tree(object):
    def __init__(self, action = 'root', parent = None, state = None):
        """
        :param action: up left down or right
        :param state: current board
        """
        self.action = action
        self.parent = parent
        self.state = state
        heur1 = self.get_heuristic1()
        # heur2 = self.get_heuristic2()
        # print(heur1, heur2)
        self.heuristic = heur1 + self.get_parentnum()

    def get_parentnum(self):
        count = 0
        parent = self.parent
        while parent is not None:
            count += 1
            parent = parent.parent
        return count

    def get_heuristic1(self):
        board = deepcopy(self.state.get_board_list())
        heuristic = 0
        x = board.index('')
        board[x] = 0
        board_matrix = [(x,y) for x in range(self.state.block_size) for y in range(self.state.block_size)]
        # board_abs = [i for i in range(9)]
        # map_mat = zip(board_abs, board_comparator)
        # print(board)
        for pos, ele in zip(board_matrix, board):
            if not ele == '':
                pos_x, pos_y = pos
                ele_pos_x, ele_pos_y = board_matrix[ele]
                dist_x = abs(pos_x - ele_pos_x)
                dist_y = abs(pos_y - ele_pos_y)
                # print("ele: {} x_dis: {} y_dis: {}, pos_x: {}, pos_y: {} ele_pos_x: {}, ele_pos_y: {}, dist: {}".format(ele, dist_x,dist_y, pos_x, pos_y, ele_pos_x, ele_pos_y, dist_y+dist_x))
                heuristic += dist_x + dist_y
        return heuristic

    def get_heuristic2(self):
        solved_list = [i for i in range(self.state.block_size ** 2)]
        list_copy = list(self.state.get_board_list())
        list_copy[list_copy.index('')] = 0
        counter = 0
        while not list_copy == solved_list:
            print(list_copy)
            space = list_copy.index(0)
            correct = list_copy.index(space)
            list_copy[space], list_copy[correct] = list_copy[correct], list_copy[space]
            counter += 1
        return counter


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
            # print(node)


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


if __name__ == '__main__':
    # board = Board(list(i for i in range(9)))
    visited_states = []
    # board = Board([2,8,5,15,9,4,12,3,7,1,11,14,13,'',6,10])
    # board = Board([1,2,7,10,13,6,15,23,8,14,16,9,20,12,5,17,18,'',19,4,21,22,11,24,3])
    board = Board([4,2,3,6,5,8,1,'',7])
    # board = Board([1,2,5,3,'',4,6,7,8])
    # board = Board([1,5,10,2,6,8,9,3,'',15,14,7,4,12,13,11])
    # print(board)
    # board = Board([1,4,2,3,'',5,6,7,8])
    solve_method= SolveBFS(board, visited_states)
    solver = Solver(board,solve_method)
    # solver.run()
    solver.run()
    # t = Tree(state = board)
    # print("Heuristic: {}".format(t.heuristic))