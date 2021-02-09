f=open("./level_def.txt","r")
lines = f.readlines()
idx=0
level_id=1
for line in lines:
    if idx % 16 == 0:
        fo = open("level/level-%i.txt" % level_id, "w")
    fo.write("%s" %(line))
    if idx % 16 == 15:
        fo.close()
        level_id+=1
    idx+=1
