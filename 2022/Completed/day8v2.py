import re
import os
os.system("cls" if os.name == "nt" else "clear")

my_file = open("day8input.txt", "r")
#my_file = open("day8sampleinput.txt", "r")
content = my_file.read().strip()
cl=content.split("\n")

treeGrid=[] 
#0,0 = top left

#generate array of tree heights
for x,s in enumerate(cl):
    treeGrid.append([])
    for y,h in enumerate(s):
        treeGrid[x].append(int(h))

#count visible trees, part 1

count=0
xMax=len(treeGrid)
yMax=len(treeGrid[1])
counts = 0

#for part1
def checkTree(x,y,h):
    flag=0
    xCheck=0
    yCheck=0

    if (y == 0) or (y == yMax-1) or (x == 0) or (x == xMax-1):
        return 1
    else:
        while xCheck < xMax:
            while xCheck < x:
                if  h <= treeGrid[xCheck][y]:
                    flag+=1
                    xCheck = x + 1
                    #print("l")
                    break
                else:
                    xCheck+=1
                    if xCheck == x:
                        xCheck+=1
            while xCheck > x and xCheck < xMax:
                if h <= treeGrid[xCheck][y]:
                    flag+=1
                    #print("r")
                    xCheck = xMax
                    break
                else:
                    xCheck+=1
        while yCheck < yMax:
            while yCheck < y:
                if  h <= treeGrid[x][yCheck]:
                    flag+=1
                    #print("t")
                    yCheck = y + 1
                    break
                else:
                    yCheck+=1
                    if yCheck == y:
                        yCheck+=1
            while yCheck > y and yCheck < yMax:
                if h <= treeGrid[x][yCheck]:
                    flag+=1
                    #print("b")
                    yCheck = yMax
                    break
                else:
                    yCheck+=1
        if flag == 4:
            return 0
        else: 
            return 1

#part2
def checkTreeScenic(x,y,h):
    xCheck=0
    yCheck=0
    score=[0,0,0,0]

    if (y == 0) or (y == yMax-1) or (x == 0) or (x == xMax-1):
        return 0
    else:
        #top
        xCheck=x-1
        while xCheck >= 0:
            if h >= treeGrid[xCheck][y]:
                score[0]+=1
                if h==treeGrid[xCheck][y]:
                    break
            else:
                score[0]+=1
                break
            xCheck-=1
        #bottom
        xCheck=x+1
        while xCheck < xMax:
            if h >= treeGrid[xCheck][y]:
                score[1]+=1
                if h==treeGrid[xCheck][y]:
                    break
            else:
                score[1]+=1
                break
            xCheck+=1
        #left
        yCheck=y-1
        while yCheck >= 0:
            if h >= treeGrid[x][yCheck]:
                score[2]+=1
                if h == treeGrid[x][yCheck]:
                    break
            else:
                score[2]+=1
                break
            yCheck-=1
        #right
        yCheck=y+1
        while yCheck < yMax:
            if h >= treeGrid[x][yCheck]:
                score[3]+=1
                if h == treeGrid[x][yCheck]:
                    break
            else:
                score[3]+=1
                break
            yCheck+=1
    print(x,y,h,"   ",score,"=",(score[0] * score[1] * score[2] * score[3]))
    return (score[0] * score[1] * score[2] * score[3])

maxScenic=0
tempScenic=0

for x in range(xMax):
    for y in range(yMax):
        count+=checkTree(x,y,treeGrid[x][y])
        tempScenic=checkTreeScenic(x,y,treeGrid[x][y])
        if maxScenic < tempScenic:
            #print(x,y,tempScenic,maxScenic)
            maxScenic = tempScenic
            


edgeTrees= (2 * (len(treeGrid) + len(treeGrid[0])))-4 
print('part1 answer',count)
print('part2 answer',maxScenic)

""" #test treegrid
tempstr=''
for x in range(len(treeGrid)):
    print(tempstr)
    tempstr=''
    for y in range(len(treeGrid[x])):
        tempstr +=str(treeGrid[x][y])
        
 """
