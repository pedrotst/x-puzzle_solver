from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.properties import StringProperty, DictProperty, ListProperty
from random import shuffle

Builder.load_string('''
<GameGrid>
    cols: 4
    rows: 4
    Button:
        text: root.numbers_list[0]
        on_press: root.update_num(0)
    Button:
        text: root.numbers_list[1]
        on_press: root.update_num(1)
    Button:
        text: root.numbers_list[2]
        on_press: root.update_num(2)
    Button:
        text: root.numbers_list[3]
        on_press: root.update_num(3)
    Button:
        text: root.numbers_list[4]
        on_press: root.update_num(4)
    Button:
        text: root.numbers_list[5]
        on_press: root.update_num(5)
    Button:
        text: root.numbers_list[6]
        on_press: root.update_num(6)
    Button:
        text: root.numbers_list[7]
        on_press: root.update_num(7)
    Button:
        text: root.numbers_list[8]
        on_press: root.update_num(8)

''')

class Tree(object):
    def __init__(self, state = None):
        # self.left = 
        # self.right = 
        # self.down = 
        # self.up = 
        self.data = data

class Solver(object):
    def __init__(self):
        pass

class Board(object):
    def __init__(self, numbers_list):
        self.numbers_list = numbers_list
        self.numbers_list[0] = ''
        # shuffle(self.numbers_list)
        self.blank_pos = self.numbers_list.index('')

        # for i in range(len(self.numbers_list)):
        #     if self.numbers_list[i] == '':
        #         self.blank_pos = i
        #         break

    def move(self, move_to):
        if (((not self.blank_pos == 3) and (not self.blank_pos == 6) and self.blank_pos == move_to + 1)
            or ((not self.blank_pos == 2) and (not self.blank_pos == 5) and self.blank_pos == move_to - 1)
            or self.blank_pos == move_to - 3
            or self.blank_pos == move_to + 3):
            self.numbers_list[self.blank_pos], self.numbers_list[move_to] = self.numbers_list[move_to], self.numbers_list[self.blank_pos]
            self.blank_pos = move_to
            return True
        return False

class GameGrid(GridLayout):
    numbers_list = ListProperty(str(i) for i in range(9))
    def __init__(self, **kwargs):
        super(GameGrid, self).__init__(**kwargs)
        self.board = Board(self.numbers_list)

    def update_num(self, key):
        self.board.move(key)


if __name__ == '__main__':
    runTouchApp(GameGrid())
