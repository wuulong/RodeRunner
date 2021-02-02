# @file gamelayer.py
# @brief  game main logic control
# @Author WuLung Hsu, wuulong@gmail.com, 2021/2/1
#import random

from cocos.director import director
from cocos.scenes.transitions import SplitColsTransition, FadeTransition
import cocos.layer
import cocos.scene
import cocos.text
import cocos.actions as ac

import pyglet
from collections import defaultdict

import actors
import mainmenu
from scenario import Scenario

class GameLayer(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self,sc):
        super(GameLayer, self).__init__()

        actors.Player.KEYS_PRESSED = defaultdict(int)
        self.sc = sc

        w, h = cocos.director.director.get_window_size()
        self.width = w
        self.height = h

        self.score = self._score = 0
        self.men = self._men = 3

        assets = "assets/"
        self.tiles = {'#': pyglet.image.load(assets + "brick.png"),
                      'H': pyglet.image.load(assets + "ladder.png"),
                      '&': pyglet.image.load(assets + "runner1.png"),
                      '$': pyglet.image.load(assets + "gold.png"),
                      '0': pyglet.image.load(assets + "guard1.png"),
                      'S': pyglet.image.load(assets + "hladder.png"),
                      '-': pyglet.image.load(assets + "rope.png"),
                      ' ': pyglet.image.load(assets + "empty.png")
                      }
        self.level = Scenario.get_level_def(1)
        runner_x, runner_y = self.get_syms_pos('&')
        self.player = actors.Player(runner_x * Scenario.cell_size[0], runner_y * Scenario.cell_size[1])
        self.add(self.player)
        self.schedule(self.game_loop)

    @property
    def points(self):
        return self._men

    @points.setter
    def points(self, val):
        self._men = val

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, val):
        self._score = val
    def get_syms_pos(self,sym): #ex: get player position from level definition
        idx = self.level.find(sym,1)
        return idx %28,15-idx//28
    def draw( self ):
        for y in range(16):
            for x in range(28):
                type = self.level[x+(15-y)*28]
                self.tiles[type].blit(x*40,y*44)

    def game_loop(self, dt):
        self.draw()
        self.player.draw()

        for _, node in self.children:
            node.update(dt)
        if self.player.y > (Scenario.map_size[1]-1)*Scenario.cell_size[1]:
            director.replace(SplitColsTransition(game_over()))
        #user input handle
        #move_h = pressed[key.RIGHT] - pressed[key.LEFT]
        #move_v = pressed[key.UP] - pressed[key.DOWN]
        #self.coll_man.clear()

    def on_key_press(self, k, _):
        actors.Player.KEYS_PRESSED[k] = 1

    def on_key_release(self, k, _):
        actors.Player.KEYS_PRESSED[k] = 0

    def on_mouse_press(self, x, y, buttons, mod):
        pass


def new_game():
    sc = Scenario()
    game_layer = GameLayer(sc)
    return cocos.scene.Scene(game_layer)


def game_over():
    print("game_over")
    w, h = director.get_window_size()
    layer = cocos.layer.Layer()
    text = cocos.text.Label('Game Over', position=(w*0.5, h*0.5),
                            font_name='Oswald', font_size=72,
                            anchor_x='center', anchor_y='center')
    layer.add(text)
    scene = cocos.scene.Scene(layer)
    new_scene = FadeTransition(mainmenu.new_menu())
    func = lambda: director.replace(new_scene)
    scene.do(ac.Delay(3) + ac.CallFunc(func))
    return scene
