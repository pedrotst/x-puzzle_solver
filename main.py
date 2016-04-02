from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty, DictProperty, ListProperty
from random import shuffle
from board import Board
import time
import random 
from functools import partial
from solver import *
import pdb

Builder.load_string('''
<GameGrid>
    cols: 1
    rows: 2
    BoxLayout:
        size_hint: .1, .1
        orientation: 'horizontal'
        Button:
            text: 'randomize'
            on_press: root.randomize()
        Button:
            text: 'solve'
            on_press: root.solve()
    GridLayout:
        cols: 3
        rows: 3
        Button:
            id: b1
            text: root.numbers_list[0]
            on_press: root.update_num(0)
        Button:
            id:b2
            text: root.numbers_list[1]
            on_press: root.update_num(1)
        Button:
            id: b3
            text: root.numbers_list[2]
            on_press: root.update_num(2)
        Button:
            id: b4
            text: root.numbers_list[3]
            on_press: root.update_num(3)
        Button:
            id: b5
            text: root.numbers_list[4]
            on_press: root.update_num(4)
        Button:
            id: b6
            text: root.numbers_list[5]
            on_press: root.update_num(5)
        Button:
            id:b7
            text: root.numbers_list[6]
            on_press: root.update_num(6)
        Button:
            id:b8
            text: root.numbers_list[7]
            on_press: root.update_num(7)
        Button:
            id:b9
            text: root.numbers_list[8]
            on_press: root.update_num(8)

''')

class GameGrid(GridLayout):
    numbers_list = ListProperty(str(i) for i in range(9))

    def __init__(self, **kwargs):
        super(GameGrid, self).__init__(**kwargs)
        self.numbers_list[0] = ''
        self.board = Board(self.numbers_list)

    def update_num(self, key):
        self.board.move(key)

    def button_update(self):
        but_list = ['b'+str(i) for i in range(9)]
        for child in self.children:
            if child.id in but_list:
                child.texture_update()
                child.do_layout()

    def auto_move(self, move_list, *args):
        try:
            i = move_list.__next__()
            if i == 0:
                self.board.move_up()
            elif i == 1:
                self.board.move_down()
            elif i == 2:
                self.board.move_left()
            elif i == 3:
                self.board.move_right()
        except StopIteration:
            Clock.unschedule(self.auto_move)

    def solve(self):
        visited_states = []
        move_list = []
        solve_method = SolveBFS(self.board, visited_states)
        solver = Solver(solve_method)
        move_list = iter(solver.solve())
        Clock.schedule_interval(partial(self.auto_move, move_list), .5)

    def randomize(self):
        # 0 = up
        # 1 = down
        # 2 = left
        # 3 = right
        move_list = iter([random.randint(0,4) for i in range(random.randint(0,300))])
        Clock.schedule_interval(partial(self.auto_move, move_list), .009)
        # print (random_moves)
        # for b in random_moves:
        #     x = ListProperty(b)
        #     self.board = Board(x)
        #     time.sleep(.5)

if __name__ == '__main__':
    runTouchApp(GameGrid())
