#PURPOSE: 測試畫玩家動作的動畫
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
from pyglet.image import Animation

## the following is in case we want to get the images
## from other directories:
# pyglet.resource.path.append("/data/other/directory")
# pyglet.resource.reindex()


class TestLayer(cocos.layer.Layer):
    is_event_handler = True
    def __init__(self):
        super( TestLayer, self ).__init__()

        x,y = director.get_window_size()
        assets = "../assets/"
        runner = pyglet.image.load(assets + 'runner.png')
        runner_seq = pyglet.image.ImageGrid(runner, 3, 9)
        anis = {}
        anis['W'] = Animation.from_image_sequence(runner_seq[9*2:9*2+3], 0.5)
        anis['w'] = Animation.from_image_sequence(runner_seq[9*2+3:9*2+6], 0.5)
        anis['U'] = Animation.from_image_sequence(runner_seq[9*2+6:9*2+8], 0.5)
        anis['D'] = runner_seq[9*2+8]
        anis['d'] = runner_seq[8]
        anis['R'] = Animation.from_image_sequence(runner_seq[9*0:9*0+3], 0.5)
        anis['r'] = Animation.from_image_sequence(runner_seq[9*0+3:9*0+6], 0.5)
        anis['H'] = runner_seq[9*0+6]
        anis['h'] = runner_seq[9*0+7]
        self.anis = anis

        self.ani_keys=['W','w','U','D','d','R','r','H','h']
        self.ani_idx = 0
        self.sprite = Sprite(anis[self.ani_keys[self.ani_idx]])
        #self.sprite = Sprite(runner_seq[8])
        self.sprite.position = x//3, y//3
        self.add( self.sprite  )

    def on_mouse_press(self, x, y, buttons, mod):
        self.ani_idx+=1
        if self.ani_idx == len(self.ani_keys):
            self.ani_idx = 0
        self.sprite.image = self.anis[self.ani_keys[self.ani_idx]]

        pass

def main():
    pyglet.resource.path.append("../assets")
    pyglet.resource.reindex()
    director.init()
    test_layer = TestLayer ()
    main_scene = cocos.scene.Scene (test_layer)
    director.run (main_scene)

if __name__ == '__main__':
    main()
