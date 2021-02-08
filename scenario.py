# @file scenario.py
# @brief  basic setting and value
# @Author WuLung Hsu, wuulong@gmail.com, 2021/2/1

import os
import cocos.tiles
import cocos.actions as ac
import cocos.euclid as eu

class CellVector(eu.Vector2):
    def __init__(self,x,y):
        super(CellVector,self).__init__(x,y)
    def __init__(self,v2):
        super(CellVector,self).__init__(v2[0],v2[1])
    def exp(self,v2):
        return eu.Vector2(self.x * v2[0], self.y * v2[1])
    def rexp(self,v2):
        return eu.Vector2(self.x // v2[0], self.y // v2[1])
    def pos_to_xy(self):
        return self.exp(Scenario.cell_size)+Scenario.cell_size/2
    def xy_to_pos(self):
        v= self
        return eu.Vector2(int(v[0] // Scenario.cell_size[0]), int((v[1]-44) // Scenario.cell_size[1]))
class Scenario(object):
    cell_size = eu.Vector2(40,44)
    map_size = eu.Vector2(28,16)
    VERSION = "0.3"
    INSTANCE = None

    def pos_in_bound(pos_x,pos_y):
        if pos_x <0:
            pos_x=0
        if pos_x >= Scenario.map_size[0]:
            pos_x = Scenario.map_size[0]-1
        if pos_y <0:
            pos_y=0
        if pos_y >= Scenario.map_size[1]:
            pos_y = Scenario.map_size[1]-1
        return eu.Vector2( int(pos_x),int(pos_y))
    def xy_in_bound(x,y):
        pass
    def get_level_def(level_id):
        filename = "level/level-%i.txt" %(level_id)
        if os.path.isfile(filename):
            f= open(filename,"r")
            lines = ""
            for line in f:
                line1 = line.replace("\"\n","")
                line2 = line1.replace("\"","")
                lines += line2
            f.close()
            level_sample = "".join(lines)
        else:
            level_sample = None
        return level_sample

    def __init__(self):
        self.level_id = 0
        self.men = self._men = 1
        self.score = self._score = 0

    @property
    def men(self):
        return self._men

    @men.setter
    def men(self, val):
        self._men = val

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, val):
        self._score = val