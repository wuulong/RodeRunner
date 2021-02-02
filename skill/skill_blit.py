#PURPOSE: 測試在某個地方貼圖
from __future__ import division, print_function, unicode_literals

# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "t 0.1, s, q"
tags = "Sprite"

import cocos
from cocos.director import director
from cocos.sprite import Sprite
import pyglet

## the following is in case we want to get the images
## from other directories:
# pyglet.resource.path.append("/data/other/directory")
# pyglet.resource.reindex()


class TestLayer(cocos.layer.Layer):
    def __init__(self):
        super( TestLayer, self ).__init__()

        self.x,self.y = director.get_window_size()

        self.sprite = Sprite('runner1.png')
        self.sprite.position = self.x//3, self.y//3
        self.add( self.sprite  )
        self.brick = pyglet.image.load("../assets/brick.png")
    def draw( self ):

        self.brick.blit(self.x//2, self.y//2)
        self.sprite.draw()

def main():
    pyglet.resource.path.append("../assets")
    pyglet.resource.reindex()
    director.init()
    test_layer = TestLayer ()
    main_scene = cocos.scene.Scene (test_layer)
    director.run (main_scene)

if __name__ == '__main__':
    main()
