#PURPOSE: 顯示文數字的邏輯
from __future__ import division, print_function, unicode_literals

# This code is so you can run the samples without installing the package
import sys
import os

import cocos
from cocos.director import director
from cocos.sprite import Sprite
import pyglet


class TestLayer(cocos.layer.Layer):
    def __init__(self):
        super( TestLayer, self ).__init__()

        self.x,self.y = director.get_window_size()

        assets = "../assets/"
        self.txt_image = pyglet.image.load(assets + 'text.png')
        self.txt_seq = pyglet.image.ImageGrid(self.txt_image, 6, 10)
        self.txt_image1 = self.txt_seq.__getitem__(self.txt_to_seq('X'))

    def txt_to_seq(self,char):
        v = ord(char)
        if v>=ord('0') and v<=ord('9'): #number
            ret = 5*10 + v-ord('0')
        elif v>=ord('A') and v<=ord('J'):
            ret = 4*10 + v-ord('A')
        elif v>=ord('K') and v<=ord('T'):
            ret = 3*10 + v-ord('K')
        elif v>=ord('U') and v<=ord('Z'):
            ret = 2*10 + v-ord('U')
        else:
            return 19 # space
        return ret

    def draw_hud(self,score,men,level,pos_x,pos_y):
        draw_txt = "SCORE%07i MEN%03i LEVEL%03i" %(score,men,level)
        for i in range(len(draw_txt)):
            seq = self.txt_to_seq(draw_txt[i])
            pos_x_cur = pos_x+ i*40
            txt_image1 = self.txt_seq.__getitem__(seq)
            txt_image1.blit(pos_x_cur,pos_y)

    def draw( self ):
        self.draw_hud(1000,5,1,0,self.y//2)
        #self.txt_image1.blit(self.x//2, self.y//2)

def main():
    pyglet.resource.path.append("../assets")
    pyglet.resource.reindex()
    director.init(width=1120)
    test_layer = TestLayer ()
    main_scene = cocos.scene.Scene (test_layer)
    director.run (main_scene)

if __name__ == '__main__':
    main()
