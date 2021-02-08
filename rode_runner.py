# @file rode_runner.py
# @brief  application init
# @Author WuLung Hsu, wuulong@gmail.com, 2021/2/1
# Version History:
# - V0.1: Initiation, Load map, New game, Quit game
from cocos.director import director
import pyglet.font
import pyglet.resource

from mainmenu import new_menu
from scenario import Scenario

if __name__ == '__main__':
    pyglet.resource.path.append('assets')
    pyglet.resource.reindex()
    w, h = (Scenario.map_size[0] * Scenario.cell_size[0]),((Scenario.map_size[1]+1) * Scenario.cell_size[1])
    director.init(caption='Rode Runner',width=w, height=h)
    director.run(new_menu())
