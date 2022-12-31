import pyxel
from constant import *


class Man:
    def __init__(self, x, y, w=MAN_SIZE, h=MAN_SIZE):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.mv = 0

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
    def movement(self, scene):  # mv_lock を返す
        if scene == 0:
            self.x = PLAYER_X
            self.mv = 0
            return 1
        elif scene == 1:
            self.x = PLAYER_X
            self.mv = 1
            return 0
        else:
            if pyxel.btn(pyxel.KEY_K):
                self.x = PLAYER_ATACK_X
                self.mv = 2
                return 1
            elif pyxel.btn(pyxel.KEY_J):
                self.x = PLAYER_DODGE_X
                self.mv = 3
                return 0


class Enemy(Man):
    def movement(self, scene):
        if scene == 0:
            self.x = ENEMY_X
            self.mv = 0
            return 1
        elif scene == 1:
            self.x = ENEMY_X
            self.mv = 1
            return 0
        else:
            if pyxel.rndi(1, 30) % 7 == 0:
                if scene == 2:
                    self.x = ENEMY_ATACK_X
                    self.mv = 2
                    return 1
                else:
                    self.x = ENEMY_DODGE_X
                    self.mv = 3
                    return 0

class Board:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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


class Score:
    def __init__(self, x, y):
        self.score = 0
        self.x = x
        self.y = y
        self.str = str(self.score)

<<<<<<< HEAD
    def add_point(self, point):
        self.score += point
        self.str = str(self.score)
=======
    def update(self, flag):
        if flag == 1:   # 加点
            self.score += 1
        elif self.score > 0 and self.score == 2:   # 減点
            self.score -= 2

    def scoreCheck(self):
        if self.score == 10:
            return 1
        else:
            return 0
>>>>>>> dc9e3e2 (シーンの追加)

    def draw(self):
        pyxel.text(self.x, self.y, self.str, 0)


if __name__ == '__main__':
    class App:
        def __init__(self):
            pyxel.init(WINDOW_X, WINDOW_Y, title="JUDGE", capture_scale=3, fps=30)
            pyxel.load('resource.pyxres')
            self.player_score = Score(PLAYER_SCORE_X, PLAYER_SCORE_Y)
            self.enemy_score = Score(ENEMY_SCORE_X, ENEMY_SCORE_Y)
            pyxel.run(self.update, self.draw)
	
        def update(self):
            pass
	
        def draw(self):
            pyxel.bltm(0, 0, 0, 0, 0, WINDOW_X, WINDOW_Y)
            self.player_score.draw()
            self.enemy_score.draw()

    App()
