import cocos.euclid as eu
class CellVector(eu.Vector2):
    def __init__(self,x,y):
        super(CellVector,self).__init__(x,y)
    def exp(self,v2):
        self.x *= v2[0]
        self.y *= v2[1]
        return self
cell_size = eu.Vector2(40,44)
pos = CellVector(2, 3)
print(pos.exp(cell_size))
#print(pos+(10,20))