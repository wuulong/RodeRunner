# @file scenario.py
# @brief  basic setting and value
# @Author WuLung Hsu, wuulong@gmail.com, 2021/2/1

import cocos.tiles
import cocos.actions as ac

class Scenario(object):
    cell_size = 40,44
    map_size = 28,16
    VERSION = "0.1"

    def get_level_def(level_id):
        level_sample = \
            "                  S         " + \
            "    $             S         " + \
            "#######H#######   S         " + \
            "       H----------S    $    " + \
            "       H    ##H   #######H##" + \
            "       H    ##H          H  " + \
            "     0 H    ##H       $0 H  " + \
            "##H#####    ########H#######" + \
            "  H                 H       " + \
            "  H           0     H       " + \
            "#########H##########H       " + \
            "         H          H       " + \
            "       $ H----------H   $   " + \
            "    H######         #######H" + \
            "    H         &  $         H" + \
            "############################"

        return level_sample

    def __init__(self):
        pass