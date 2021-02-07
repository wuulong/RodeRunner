# @file mainmenu.py
# @brief  menu scence
# @Author WuLung Hsu, wuulong@gmail.com, 2021/2/1

import cocos.menu
import cocos.scene
import cocos.layer
import cocos.actions as ac
from cocos.director import director
from cocos.scenes.transitions import FadeTRTransition

import pyglet.app

from gamelayer import new_game
from scenario import Scenario

class MainMenu(cocos.menu.Menu):
    def __init__(self):
        super(MainMenu, self).__init__('Rode Runner V' + Scenario.VERSION)

        self.menu_anchor_y = 'center'
        self.menu_anchor_x = 'center'
        self.level_start = 0

        items = list()
        items.append(cocos.menu.MenuItem('New Game', self.on_new_game))
        items.append(cocos.menu.EntryMenuItem('Level Start:', self.on_level_start, str(self.level_start)) )
        items.append(cocos.menu.MenuItem('Quit', pyglet.app.exit))

        self.create_menu(items, ac.ScaleTo(1.0, duration=3), ac.ScaleTo(1.0, duration=0.25))
    def on_level_start(self,value):
        if value.isnumeric():
            self.level_start = int(value)

    def on_new_game(self):
        director.push(FadeTRTransition(new_game(self.level_start), duration=2))


def new_menu():
    scene = cocos.scene.Scene()
    color_layer = cocos.layer.ColorLayer(205, 133, 63, 255)
    scene.add(MainMenu(), z=1)
    scene.add(color_layer, z=0)
    return scene
