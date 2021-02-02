# @file actors.py
# @brief  all actors
# @Author WuLung Hsu, wuulong@gmail.com, 2021/2/1
import math

import cocos.sprite
import cocos.audio
import cocos.actions as ac
import cocos.euclid as eu
import cocos.collision_model as cm

from collections import defaultdict
from pyglet.window import key
import pyglet.image
from pyglet.image import Animation

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
        """
        space_pressed = pressed[key.SPACE] == 1
        if PlayerShoot.INSTANCE is None and space_pressed:
            self.parent.add(PlayerShoot(self.x, self.y + 50))
        """


        w = self.width * 0.5
        movement_h = pressed[key.RIGHT] - pressed[key.LEFT]
        if movement_h != 0 and w <= self.x <= self.parent.width - w:
            self.move(self.speed_h * movement_h * elapsed)

        movement_v = pressed[key.UP] - pressed[key.DOWN]
        h = self.height * 0.5
        if movement_v != 0 and h <= self.y <= self.parent.height - h:
            self.move(self.speed_v * movement_v * elapsed)
            #print("y=%i, yi=%i" %(self.y, self.y//44))
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

    def collide(self, other):
        other.kill()
        self.kill()
