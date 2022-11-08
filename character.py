import pyxel

class Man:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def update(self):
        pass

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, self.w, self.h, colkey=7)

class Board:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        pass

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 16, 96, 16, 16, colkey=7)

class Number:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.flag = False

    def update(self, num, flag):
        self.num = num
        self.flag = flag

    def draw(self):
        if self.flag:
            u = (self.num % 4 - 1) * 16
            if self.num < 5:
                v = 64
            elif self.num < 9:
                v = 80
            else:
                v = 96
            pyxel.blt(self.x, self.y, 0, u, v, 16, 16, colkey=7)


class Arrow:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        pass

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 32, 96, 16, 16, colkey=7)
