#PURPOSE: 測試畫整關地圖
from __future__ import division, print_function, unicode_literals

# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

import cocos
from cocos.director import director
from cocos.sprite import Sprite
import pyglet


class TestLayer(cocos.layer.Layer):
    def __init__(self):
        super( TestLayer, self ).__init__()
        self.level = "                  S         " + \
                "    $             S         " +\
                "#######H#######   S         " +\
                "       H----------S    $    " +\
                "       H    ##H   #######H##" +\
                "       H    ##H          H  " +\
                "     0 H    ##H       $0 H  " +\
                "##H#####    ########H#######" +\
                "  H                 H       " +\
                "  H           0     H       " +\
                "#########H##########H       " +\
                "         H          H       " +\
                "       $ H----------H   $   " +\
                "    H######         #######H" +\
                "    H         &  $         H" +\
                "############################"


        #self.x,self.y = director.get_window_size()
        assets = "../assets/"
        self.tiles = {'#': pyglet.image.load(assets + "brick.png"),
                      'H': pyglet.image.load(assets + "ladder.png"),
                      '&': pyglet.image.load(assets + "runner1.png"),
                      '$': pyglet.image.load(assets + "gold.png"),
                      '0': pyglet.image.load(assets + "guard1.png"),
                      'S': pyglet.image.load(assets + "hladder.png"),
                      '-': pyglet.image.load(assets + "rope.png"),
                      ' ': pyglet.image.load(assets + "empty.png")
                      }

    def draw( self ):
        for y in range(16):
            for x in range(28):
                type = self.level[x+(15-y)*28]
                self.tiles[type].blit(x*40,y*44)

def main():
    pyglet.resource.path.append("../assets")
    pyglet.resource.reindex()
    director.init(width=1120,height=704)
    test_layer = TestLayer ()
    main_scene = cocos.scene.Scene (test_layer)
    director.run (main_scene)

if __name__ == '__main__':
    main()
