import pyxel
from constant import *

class Man:
    def __init__(self, x, y, w=MAN_SIZE, h=MAN_SIZE):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.mv = 0
    
    def movement(self, mv):
        self.mv = mv
    
    def draw(self):
        if self.mv == 0:    # ready
            pyxel.blt(self.x, self.y, 0, 0, 0, self.w, self.h, colkey=7)
        elif self.mv == 1:  # poise
            pyxel.blt(self.x, self.y, 0, 32, 32, self.w, self.h, colkey=7)
        elif self.mv == 2:  # attack
            pyxel.blt(self.x, self.y, 0, 32, 0, self.w, self.h, colkey=7)
        elif self.mv == 3:  # dodge
            pyxel.blt(self.x, self.y, 0, 0, 32, self.w, self.h, colkey=7)
        

class Player(Man):
    def movement(self, scene):
        if scene == 0:
            self.x = 15
            self.mv = 0
        elif scene == 1:
            self.x = 15
            self.mv = 1
        else:
            if pyxel.btn(pyxel.KEY_K):
                self.x = ATACK_X
                self.mv = 2
            elif pyxel.btn(pyxel.KEY_J):
                self.x = DODGE_X
                self.mv = 3


class Enemy(Man):
    def movement(self, scene):
        if scene == 0:
            self.mv = 0
        elif scene == 1:
            self.mv = 1
        # else:
        #     if pyxel.btn(pyxel.KEY_K):
        #         self.x = ATACK_X
        #         self.mv = 2
        #     elif pyxel.btn(pyxel.KEY_J):
        #         self.x = DODGE_X
        #         self.mv = 3
        


class Board:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        pass

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 80, 16, 16, colkey=7)


class Number:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.flag = False

    def update(self, flag, num=1):
        self.num = num
        self.flag = flag

    def draw(self):
        if self.flag:
            u = self.num * 16 - 16
            v = 64
            pyxel.blt(self.x, self.y, 0, u, v, 16, 16, colkey=7)


class Arrow:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        pass

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 16, 80, 16, 16, colkey=7)
