#PURPOSE: 挖洞，填洞動畫測試
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
        hole_img = pyglet.image.load(assets + 'hole.png')
        hole_seq1 = pyglet.image.ImageGrid(hole_img, 2, 9)
        hole_seq2 = pyglet.image.ImageGrid(hole_img, 4, 9)
        anis = {}
        anis['T'] = Animation.from_image_sequence(hole_seq1[9*0:9*0+9], 0.1)
        anis['t'] = Animation.from_image_sequence(hole_seq1[9*1:9*1+9], 0.1)
        flats = []
        flats.append(hole_seq2[9*2+8])
        flats.append(hole_seq2[9*3+8])
        flats.append(hole_seq2[9*0+8])
        anis['F'] = Animation.from_image_sequence(flats, 1)

        self.anis = anis

        self.ani_keys=['T','t','F']
        self.ani_idx = 0
        self.sprite = Sprite(anis[self.ani_keys[self.ani_idx]])
        #self.sprite = Sprite(runner_seq[8])
        self.sprite.position = x//3, y//3
        self.add( self.sprite  )

    def on_mouse_press(self, x, y, buttons, mod):
        self.ani_idx+=1

        if self.ani_idx == len(self.ani_keys):
            self.ani_idx = 0
        print("idx=%i" %self.ani_idx)
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
