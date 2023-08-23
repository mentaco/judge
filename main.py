import pyxel
import character
from constant import *


class Wait:
    def __init__(self):
        self.arrow_1 = character.Arrow(WINDOW_X/2-8, 5)
        self.arrow_2 = character.Arrow(WINDOW_X/2-8, 9)
        self.arrow_3 = character.Arrow(WINDOW_X/2-8, 13)
        self.wait_interval = (WAIT_END_TIME - WAIT_START_TIME) / 3

    def arrow_draw(self, count):
        self.arrow_1.draw()
        if  WAIT_START_TIME + self.wait_interval < count:
            self.arrow_2.draw()
        if WAIT_START_TIME + self.wait_interval * 2 < count:
            self.arrow_3.draw()


class NumberGenerate:
    def __init__(self, p_board_x, p_board_y, e_board_x, e_board_y):
        self.player_number = character.Number(p_board_x, p_board_y)
        self.enemy_number = character.Number(e_board_x, e_board_y)
        self.player_number_flag = 0
        self.enemy_number_flag = 0
        self.generate_flag = 0
    
    def update(self):
        self.player_number.update(False)
        self.enemy_number.update(False)
    
    def generate(self, player_num, enemy_num):
        self.player_number.update(True, player_num)
        self.enemy_number.update(True, enemy_num)
    
    def number_draw(self):
        self.player_number.draw()
        self.enemy_number.draw()


class Judgment:
    def judging(self, p_num, e_num, p_mv, e_mv):    # player_score, enemy_score それぞれの flag を返す
        if p_num > e_num:
            if p_mv == 2:
                if  e_mv == 1:
                    return 1, 0
                elif e_mv == 3:
                    return 0, 1
            elif p_mv == 3:
                return -1, 0
        elif p_num < e_num:
            if p_mv == 1:
                if e_mv == 2:
                    return 0, 1
            elif p_mv == 2:
                return -1, 0
            elif p_mv == 3:
                if e_mv == 2:
                    return 1, 0
        else:
            if p_mv == 2:
                return 1, -1
        return 0, 0
    
    def scoreCheck(self, p_score, e_score):
        if p_score >= WIN_POINT:
            return SCENE_WIN
        elif e_score >= WIN_POINT:
            return SCENE_LOSE
        else:
            return SCENE_PLAY


class App:
    def __init__(self):
        pyxel.init(WINDOW_X, WINDOW_Y, title="JUDGE", capture_scale=3, fps=30)
        pyxel.load('resource.pyxres')
        self.scene = SCENE_TITLE
        self.text_color = 0
        self.wait_flag = 0
        self.frame_count = 0
        self.wait_count = 0
        self.mv_count = 0
        self.mv_flag = 0
        self.key_push = 0
        self.player_mv_lock_global = 1
        self.player_mv_lock_local = 1
        self.enemy_mv_lock_global = 1
        self.enemy_mv_lock_local = 1
        self.player_mv = 0
        self.enemy_mv = 0
        self.player_num = 0
        self.enemy_num = 0
        self.p_score_flag = 0
        self.e_score_flag = 0
        self.player = character.Player(PLAYER_X, PLAYER_Y)
        self.enemy = character.Enemy(ENEMY_X, PLAYER_Y, -MAN_SIZE)
        self.player_board = character.Board(self.player.x+8, 5)
        self.enemy_board = character.Board(self.enemy.x+8, 5)
        self.wait = Wait()
        self.num_generate = NumberGenerate(self.player_board.x, self.player_board.y,
                                                self.enemy_board.x, self.enemy_board.y)
        self.player_score = character.Score(7, WINDOW_Y - 7)
        self.enemy_score = character.Score(WINDOW_X - 10, WINDOW_Y - 7)
        self.judgment = Judgment()
	
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.scene == SCENE_TITLE:
            self.update_title()
        elif self.scene == SCENE_PLAY:
            self.update_play()
        elif self.scene == SCENE_WIN or self.scene == SCENE_LOSE:
            self.update_end()

    def update_title(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.scene = SCENE_PLAY

    def update_play(self):
        self.frame_count += 1
        self.wait_count = self.frame_count % INTERVAL

        # 待ち状態
        if WAIT_START_TIME <= self.wait_count < WAIT_END_TIME:
            self.num_generate.update()
            self.wait_flag = 1
        else:
            self.wait_flag = 0

        # 数字を生成
        if self.wait_count == WAIT_END_TIME:
            self.mv_count = 0
            self.player_num = pyxel.rndi(1, 9)
            self.enemy_num = pyxel.rndi(1, 9)
            self.num_generate.generate(self.player_num, self.enemy_num)
            self.mv_flag = 1
            self.player_mv_lock_global = 0
            self.player_mv_lock_local = 0
            self.enemy_mv_lock_global = 0
            self.enemy_mv_lock_local = 0

        # 入力を受け付け終了
        if self.wait_count == INTERVAL - 10:
            # スコアの更新
            self.p_score_flag, self.e_score_flag = self.judgment.judging(self.player_num, self.enemy_num,
                                                                            self.player_mv, self.enemy_mv)
            self.player_score.update(self.p_score_flag)
            self.enemy_score.update(self.e_score_flag)

            self.mv_flag = 0
            self.player_mv_lock_global = 1
            self.player_mv_lock_local = 1
            self.player.mv = 0
            self.enemy_mv = 0
            self.key_push = 0

            self.scene = self.judgment.scoreCheck(self.player_score.score, self.enemy_score.score)

        # プレイヤーからの入力
        if self.player_mv_lock_global or self.enemy_mv_lock_global:
            if not self.key_push:
                self.player_mv_lock_global, self.player_mv_lock_local, self.player_mv = self.player.movement(0)
                self.enemy_mv_lock_global, self.enemy_mv_lock_local, self.enemy_mv = self.enemy.movement(0)
        else:
            self.mv_count += 1
            if self.key_push:
                if not self.player_mv_lock_local:
                    self.player_mv_lock_global, self.player_mv_lock_local, self.player_mv = self.player.movement(2)
                if (not self.enemy_mv_lock_local) and self.mv_count > 20:
                    self.enemy_mv_lock_global, self.enemy_mv_lock_local, self.enemy_mv = self.enemy.movement(2,
                                                                                                            self.player_num,
                                                                                                            self.enemy_num)
            else: 
                self.player_mv_lock_global, self.player_mv_lock_local, self.player_mv = self.player.movement(1)
                self.enemy_mv_lock_global, self.enemy_mv_lock_local, self.enemy_mv = self.enemy.movement(1)
                self.key_push = 1
    
    def update_end(self):
        count = pyxel.frame_count % 40

        if count < 20:
            if self.scene == SCENE_WIN:
                self.text_color = 14
            else:
                self.text_color = 5
        else:
            self.text_color = 7

    def draw(self):
        pyxel.cls(7)

        if self.scene == SCENE_TITLE:
            self.draw_title()
        elif self.scene == SCENE_PLAY:
            self.draw_play()
        elif self.scene == SCENE_WIN or self.scene == SCENE_LOSE:
            self.draw_end()

    def draw_title(self):
        pyxel.text(WINDOW_X / 2 - 10, WINDOW_Y / 2 - 5, "JUDGE", 0)

    def draw_play(self):
        pyxel.bltm(0, 0, 0, 0, 0, WINDOW_X, WINDOW_Y)
        self.player.draw()
        self.enemy.draw()
        self.player_board.draw()
        self.enemy_board.draw()
        if self.wait_flag:
            self.wait.arrow_draw(self.wait_count)
        self.num_generate.number_draw()
        self.player_score.draw()
        self.enemy_score.draw()
    
    def draw_end(self):
        if self.scene == SCENE_WIN:
            pyxel.text(WINDOW_X / 2 - 14, WINDOW_Y / 2 - 5, "YOU WIN !", self.text_color)
        else:
            pyxel.text(WINDOW_X / 2 - 17, WINDOW_Y / 2 - 5, "YOU LOSE...", self.text_color)


App()
