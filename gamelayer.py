# @file gamelayer.py
# @brief  game main logic control
# @Author WuLung Hsu, wuulong@gmail.com, 2021/2/1

import os

from cocos.director import director
from cocos.scenes.transitions import SplitColsTransition, FadeTransition
import cocos.layer
import cocos.scene
import cocos.text
import cocos.actions as ac
import cocos.euclid as eu
import cocos.collision_model as cm

import pyglet
from collections import defaultdict

import actors
import mainmenu
from scenario import Scenario,CellVector

class GameLayer(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self,sc):
        super(GameLayer, self).__init__()

        actors.Player.KEYS_PRESSED = defaultdict(int)
        self.sc = sc

        w, h = cocos.director.director.get_window_size()
        self.width = w
        self.height = h

        self.enermys = []
        #self.golds = []
        self.gold_cnt = 0

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

        self.txt_image = pyglet.image.load(assets + 'text.png')
        self.txt_seq = pyglet.image.ImageGrid(self.txt_image, 6, 10)



        self.set_level(self.sc.level_id)

        self.create_player()
        self.create_enermy()
        self.create_gold()

        self.collman = cm.CollisionManagerGrid(0, w, 0, h, Scenario.cell_size[0]//2, Scenario.cell_size[1]//2)

        self.schedule(self.game_loop)

    def set_level(self,level_id):
        actors.Player.KEYS_PRESSED = defaultdict(int)
        self.level = Scenario.get_level_def(level_id)
    def hladder_active(self):
        self.level = self.level.replace('S','H')
    def create_player(self):
        runner_pos = CellVector(self.get_syms_pos('&')[0])
        runner_xy = runner_pos.pos_to_xy()
        self.player = actors.Player(runner_xy[0],runner_xy[1]+44)
        self.add(self.player)
    def create_enermy(self):
        enermys_pos = self.get_syms_pos('0')

        for enermy_pos in enermys_pos:
            enermy_xy = CellVector(enermy_pos).pos_to_xy()
            enermy = actors.Enermy(enermy_xy[0],enermy_xy[1]+44)
            self.enermys.append(enermy)
            self.add(enermy)

    def create_gold(self):
        golds_pos = self.get_syms_pos('$')
        for gold_pos in golds_pos:
            gold_xy = CellVector(gold_pos).pos_to_xy()
            gold = actors.Gold(gold_xy[0],gold_xy[1]+44)
            #self.golds.append(gold)
            self.add(gold)
            self.gold_cnt+=1

    def get_player_env(self):
        pos = CellVector(self.player.get_xy()).xy_to_pos()
        env = self.get_env_bypos(pos)
        return env

    def pos_get_sym(self,pos_x,pos_y):
        #filter fix charactor
        sym = self.level[28*(15-pos_y)+pos_x]

        if sym=="#" or sym=="H" or sym=="-":
            return sym
        else:
            return " "
    def get_env_bypos(self,pos):
        # get position surrounding level charactor string, if out of boundry use 'B'
        #  logic seq: center, x=0, x=15, y=0,y=27
        # env definition: 3 row string, env[0] is bottom, env[0][0] is bottom,left
        env = []
        for i in range(3):
            env.append("BBB")

        pos = Scenario.pos_in_bound(pos[0],pos[1])
        sym=self.pos_get_sym(pos[0],pos[1])

        if (pos[0]>0 and pos[0]<27) and (pos[1]>0 and pos[1]<15):
            env[0] = self.pos_get_sym(pos[0]-1,pos[1]-1) + self.pos_get_sym(pos[0],pos[1]-1) + self.pos_get_sym(pos[0]+1,pos[1]-1)
            env[1] = self.pos_get_sym(pos[0]-1,pos[1]) + sym + self.pos_get_sym(pos[0]+1,pos[1])
            env[2] = self.pos_get_sym(pos[0]-1,pos[1]+1) + self.pos_get_sym(pos[0],pos[1]+1) + self.pos_get_sym(pos[0]+1,pos[1]+1)
        elif pos[1]==0:
            if (pos[0]>0 and pos[0]<27):
                env[1] = self.pos_get_sym(pos[0]-1,pos[1]) + sym + self.pos_get_sym(pos[0]+1,pos[1])
                env[2] = self.pos_get_sym(pos[0]-1,pos[1]+1) + self.pos_get_sym(pos[0],pos[1]+1) + self.pos_get_sym(pos[0]+1,pos[1]+1)
            elif pos[0]==0:
                env[1] = "B" + sym + self.pos_get_sym(pos[0]+1,pos[1])
                env[2] = "B" + self.pos_get_sym(pos[0],pos[1]+1) + self.pos_get_sym(pos[0]+1,pos[1]+1)
            else: #pos[0]==27
                env[1] = self.pos_get_sym(pos[0]-1,pos[1]) + sym + "B"
                env[2] = self.pos_get_sym(pos[0]-1,pos[1]+1) + self.pos_get_sym(pos[0],pos[1]+1) + "B"
        elif pos[1]==15:
            if (pos[0]>0 and pos[0]<27):
                env[0] = self.pos_get_sym(pos[0]-1,pos[1]-1) + self.pos_get_sym(pos[0],pos[1]-1) + self.pos_get_sym(pos[0]+1,pos[1]-1)
                env[1] = self.pos_get_sym(pos[0]-1,pos[1]) + sym + self.pos_get_sym(pos[0]+1,pos[1])
            elif pos[0]==0:
                env[0] = "B" + self.pos_get_sym(pos[0],pos[1]-1) + self.pos_get_sym(pos[0]+1,pos[1]-1)
                env[1] = "B" + sym + self.pos_get_sym(pos[0]+1,pos[1])
            else:
                env[0] = self.pos_get_sym(pos[0]-1,pos[1]-1) + self.pos_get_sym(pos[0],pos[1]-1) + "B"
                env[1] = self.pos_get_sym(pos[0]-1,pos[1]) + sym + "B"
        elif pos[0]==0:
            if (pos[1]>0 and pos[1]<15):
                env[0] = "B" + self.pos_get_sym(pos[0],pos[1]-1) + self.pos_get_sym(pos[0]+1,pos[1]-1)
                env[1] = "B" + sym + self.pos_get_sym(pos[0]+1,pos[1])
                env[2] = "B" + self.pos_get_sym(pos[0],pos[1]+1) + self.pos_get_sym(pos[0]+1,pos[1]+1)
        else: # pos[0]==27:
            env[0] = self.pos_get_sym(pos[0]-1,pos[1]-1) + self.pos_get_sym(pos[0],pos[1]-1) + "B"
            env[1] = self.pos_get_sym(pos[0]-1,pos[1]) + sym + "B"
            env[2] = self.pos_get_sym(pos[0]-1,pos[1]+1) + self.pos_get_sym(pos[0],pos[1]+1) + "B"

        return env


    def get_syms_pos(self,sym): #ex: get player position from level definition
        start = 1
        ret = []
        idx=1
        while idx>0:
            idx = self.level.find(sym,start)
            if idx>0:
                ret.append(eu.Vector2(idx %28,15-idx//28))
            start = idx+1

        return ret
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
        display_type = ['#','H','-',' ']
        for y in range(16):
            for x in range(28):
                type = self.level[x+(15-y)*28]
                if type in display_type:
                    try:
                        self.tiles[type].blit(x*40,(y+1)*44)
                    except:
                        pass
        self.draw_hud(self.sc.score,self.sc.men,self.sc.level_id,0,0)


    def collide(self, node):
        if node is not None:
            for other in self.collman.iter_colliding(node):
                node.collide(other)
                return True
        return False

    def game_loop(self, dt):
        #to next level
        if ((self.player.y-44) // Scenario.cell_size[1]) ==  Scenario.map_size[1]-1:
            self.unschedule(self.game_loop)
            #self.end()
            next_level(False)
            return

        self.collman.clear()
        for _, node in self.children:
            self.collman.add(node)
            if not self.collman.knows(node):
                self.remove(node)

        if self.collide(self.player):
            pass

        #self.draw()
        self.player.draw()

        for _, node in self.children:
            node.update(dt)

    def on_key_press(self, k, _):
        actors.Player.KEYS_PRESSED[k] = 1

    def on_key_release(self, k, _):
        actors.Player.KEYS_PRESSED[k] = 0

    def on_mouse_press(self, x, y, buttons, mod):
        #print(self.pos_get_sym(1,1))
        #env= self.get_player_env()
        #print(env)
        #self.player.xy_align_bound()
        #print(self.get_syms_pos('0'))
        pass

def new_game(level_id):
    Scenario.INSTANCE = Scenario()
    Scenario.INSTANCE.level_id = level_id
    game_layer = GameLayer(Scenario.INSTANCE)
    return cocos.scene.Scene(game_layer)

# stay == True: stay at same level
def next_level(stay=False):
    if stay==False:
        #new_level =  Scenario.INSTANCE.level_id+1
        Scenario.INSTANCE.level_id+=1
    else:
        #new_level =  Scenario.INSTANCE.level_id
        pass
    filename = "level/level-%i.txt" % (Scenario.INSTANCE.level_id)
    if os.path.isfile(filename):

        game_layer = GameLayer(Scenario.INSTANCE)
        director.push(FadeTransition(cocos.scene.Scene(game_layer), duration=2))
    else:
        director.replace(SplitColsTransition(game_over(False)))

def game_over(over=True):
    #print("game_over")
    w, h = director.get_window_size()
    layer = cocos.layer.Layer()
    if over:
        label_txt = "Game Over"
    else:
        label_txt = "Game Pass"
    text = cocos.text.Label(label_txt, position=(w*0.5, h*0.5),
                            font_name='Oswald', font_size=72,
                            anchor_x='center', anchor_y='center')
    layer.add(text)
    scene = cocos.scene.Scene(layer)
    new_scene = FadeTransition(mainmenu.new_menu())
    func = lambda: director.replace(new_scene)
    scene.do(ac.Delay(3) + ac.CallFunc(func))
    return scene




