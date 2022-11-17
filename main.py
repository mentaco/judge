import pyxel
import character
from constant import *


class Wait:
    def __init__(self):
        self.arrow_1 = character.Arrow(WINDOW_X/2-8, 5)
        self.arrow_2 = character.Arrow(WINDOW_X/2-8, 9)
        self.arrow_3 = character.Arrow(WINDOW_X/2-8, 13)

    def update(self, count, flag):
        self.count = count
        self.flag = flag

    def draw(self):
        if self.flag:
            self.arrow_1.draw()
            if 60 < self.count:
                self.arrow_2.draw()
            if 90 < self.count:
                self.arrow_3.draw()


class App:
    def __init__(self):
        self.wait_flag = False
        self.frame_count = 0
        self.wait_count = 0
        pyxel.init(WINDOW_X, WINDOW_Y, title="JUDGE", capture_scale=3, fps=30)
        pyxel.load('resource.pyxres')
        self.player = character.Player(15, 20)
        self.enemy = character.Enemy(WINDOW_X-MAN_SIZE-15, 20, -MAN_SIZE)
        self.player_board = character.Board(self.player.x+8, 5)
        self.enemy_board = character.Board(self.enemy.x+8, 5)
        self.player_number = character.Number(self.player_board.x, self.player_board.y)
        self.enemy_number = character.Number(self.enemy_board.x, self.enemy_board.y)
        self.wait = Wait()

        pyxel.run(self.update, self.draw)

    def update(self):
        self.frame_count += 1
        self.wait_count = self.frame_count % INTERVAL
        self.player.movement()
        self.enemy.movement()
        self.player_board.update()
        self.enemy_board.update()
        
        if 30 <= self.wait_count <= 120:
            self.wait_flag = True
            self.player_number.update(1, False)
            self.enemy_number.update(1, False)
        else:
            self.wait_flag = False
        self.wait.update(self.wait_count, self.wait_flag)

        if self.wait_count == 121:
            self.player_number.update(pyxel.rndi(1, 9), True)
            self.enemy_number.update(pyxel.rndi(1, 9), True)

    def draw(self):
        pyxel.bltm(0, 0, 0, 0, 0, WINDOW_X, WINDOW_Y)
        self.player.draw()
        self.enemy.draw()
        self.player_board.draw()
        self.enemy_board.draw()
        self.player_number.draw()
        self.enemy_number.draw()
        self.wait.draw()


App()
