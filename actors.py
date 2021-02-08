# @file actors.py
# @brief  all actors
# @Author WuLung Hsu, wuulong@gmail.com, 2021/2/1
import math

import cocos.sprite
import cocos.audio
import cocos.actions as ac
import cocos.euclid as eu
import cocos.collision_model as cm
from cocos.director import director
from cocos.scenes.transitions import SplitColsTransition, FadeTransition


from collections import defaultdict
from pyglet.window import key
import pyglet.image
from pyglet.image import Animation

from scenario import Scenario,CellVector
import gamelayer

class Actor(cocos.sprite.Sprite):
    def __init__(self, image, x, y):
        super(Actor, self).__init__(image)
        self.position = eu.Vector2(x, y)
        self.cshape = cm.AARectShape(self.position,
                                     self.width * 0.5,
                                     self.height * 0.5)

    def move(self, offset):
        self.position += offset
        self.cshape.center += offset

    def update(self, elapsed):
        pass

    def collide(self, other):
        pass

    def xy_align_bound(self):
        pos_x = self.x // Scenario.cell_size[0]
        pos_y = (self.y - 44) // Scenario.cell_size[1]
        pos_x,pos_y = Scenario.pos_in_bound(pos_x,pos_y)
        self.x = (pos_x) * Scenario.cell_size[0] + Scenario.cell_size[0]/2
        self.y = ((pos_y+1) * Scenario.cell_size[1]) + (Scenario.cell_size[1]/2)
        #print("y=%i"  %(self.y))

    def get_xy(self):
        return eu.Vector2(self.x,self.y)

class Gold(Actor):
    def __init__(self, x, y):
        super(Gold, self).__init__('assets/gold.png', x, y)

class Enermy(Actor):
    def __init__(self, x, y):
        super(Enermy, self).__init__('assets/guard1.png', x, y)
        self.speed_h = eu.Vector2(200, 0)
        self.speed_v = eu.Vector2(0, 200)

class Player(Actor):
    KEYS_PRESSED = defaultdict(int)

    def __init__(self, x, y):
        super(Player, self).__init__('assets/runner1.png', x, y)
        self.speed_h = eu.Vector2(200, 0)
        self.speed_v = eu.Vector2(0, 200)


        assets = "assets/"
        runner = pyglet.image.load(assets + 'runner.png')
        self.runner_stand = pyglet.image.load(assets + 'runner1.png')
        runner_seq = pyglet.image.ImageGrid(runner, 3, 9)
        anis = {}
        dur = 0.01
        anis['W'] = Animation.from_image_sequence(runner_seq[9*2:9*2+3], dur)
        anis['w'] = Animation.from_image_sequence(runner_seq[9*2+3:9*2+6], dur)
        anis['U'] = Animation.from_image_sequence(runner_seq[9*2+6:9*2+8], dur)
        anis['D'] = runner_seq[9*2+8]
        anis['d'] = runner_seq[8]
        anis['R'] = Animation.from_image_sequence(runner_seq[9*0:9*0+3], dur)
        anis['r'] = Animation.from_image_sequence(runner_seq[9*0+3:9*0+6], dur)
        anis['H'] = runner_seq[9*0+6]
        anis['h'] = runner_seq[9*0+7]
        self.anis = anis

        self.last_move = ""
        self.move_act = {'d': self.anis['W'], 'a': self.anis['w'],'w': self.anis['U'], 's':self.runner_stand}
    def update(self, elapsed):
        pressed = Player.KEYS_PRESSED


        #w = self.width * 0.5
        movement_h = pressed[key.RIGHT] - pressed[key.LEFT]
        movement_v = pressed[key.UP] - pressed[key.DOWN]
        env = self.parent.get_player_env()

        if env[1][1]==' ' and (env[0][1]==' ' or env[0][1]=='-'):
            self.move(self.speed_v * -1 * elapsed)

        else:
            if movement_h != 0: # and w <= self.x <= self.parent.width - w:
                if (movement_h>0 and env[1][2] not in ('#','B') ) or (movement_h<0 and env[1][0] not in ('#','B')):
                    self.move(self.speed_h * movement_h * elapsed)
                    #print("move_h")

            #h = self.height * 0.5
            if movement_v != 0: # and h <= self.y <= self.parent.height - h:
                if (movement_v>0 and (env[1][1]=='H' and env[2][1]!='#')) or (movement_v<0 and (env[0][1]!='#')):
                    self.move(self.speed_v * movement_v * elapsed)
                    #print("move_v")
            last_move=""
            if movement_h!=0:
                if movement_h>0:
                    last_move = 'd'
                else:
                    last_move = 'a'

            if movement_v!=0:
                last_move = 'w'

            if last_move=="":
                last_move='s'

            if last_move != self.last_move:
                self.image = self.move_act[last_move]
                self.last_move = last_move
                self.xy_align_bound()


    def collide(self, other):

        if isinstance(other, Gold):
            self.parent.gold_cnt-=1
            Scenario.INSTANCE.score+=250
            print("score=%i,gold_cnt=%i" %(Scenario.INSTANCE.score,self.parent.gold_cnt))
            if self.parent.gold_cnt==0:
                self.parent.hladder_active()
            other.kill()
        if isinstance(other, Enermy):
            Scenario.INSTANCE.men-=1
            #print("men=%i" %(Scenario.INSTANCE.men))
            if Scenario.INSTANCE.men <0:
                director.replace(SplitColsTransition(gamelayer.game_over(True)))
            else:
                self.parent.unschedule(self.parent.game_loop)
                #self.parent.end()
                gamelayer.next_level(True)

        #self.kill()
