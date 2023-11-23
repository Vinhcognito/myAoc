from liz import *
import copy
wipeTerminal()
import timing

my_file = open("day16sampleinput.txt", "r")
#my_file = open("day16input.txt", "r")
content = my_file.read().strip()
cl=content.split("\n")

valve=['']
RATE=0
PATH=1

valveID={}

#parase valves
for i,line in enumerate(cl):
    _, valveName, _, _, valveRate, _, _, _, _, *paths = line.split()
    valve.append([0,[]])
    valveID[valveName]=i+1
    valve[i+1][RATE]=int(valveRate.split('=')[1].split(';')[0])
    valve[i+1][PATH]=paths
    for j in range(len(valve[i+1][PATH])):
        valve[i+1][PATH][j]=valve[i+1][PATH][j].split(',')[0]

#replace path strs with path #'s corresponding to index
for i in range(len(valve)-1):
    for j,str in enumerate(valve[i+1][PATH]):
        valve[i+1][PATH][j]=valveID[valve[i+1][PATH][j]]

pass
route=[0]

totalRoutes=0
bestRoute=[]
bestValveScore=0



def timeStep(route:list,timeleft:int,action:int):
    '''timeleft is time after performing action
        action = -1 is activate valve
        any other # is walk to that valveindex'''
    global totalRoutes
    global bestValveScore
    global bestRoute

    #log valve activation and action taken
    newRoute=copy.deepcopy(route)
    newTimeleft=copy.deepcopy(timeleft)
    newTimeleft-=1

    if newTimeleft!=0:
        newRoute.append(action)

        #send out timesteps for each possible action
        if (valve[action][RATE]!=0 and  
            action != -1):
            timeStep(newRoute,newTimeleft,-1)
        for valveIndex in valve[newRoute[-1]][PATH]:
            timeStep(newRoute,newTimeleft,valveIndex)
    else:
        #check final valvescore and record if best
        totalRoutes+=1
        print('routes checked: ',totalRoutes,'best score: ',bestValveScore)
        if calcValveScore(newActiveValves) > bestValveScore:
            bestValveScore=calcValveScore(newActiveValves)
            bestRoute=route
            return
        return
    return

def calcValveScore(route:list):
    score=0
    for index,action in enumerate(route):
        if action == -1:
            score+=valve[route[index-1]][RATE]*(30-index)
    return score


#firststep
#timeStep(route,activeValves,30,0)
solution =[1,4,-1,3,2,-1,1,9,10,-1,9,1,4,5,6,7,8,-1,7,6,5,-1,4,3,-1]
#print(bestRoute)
#print('bestvalve score= ',bestValveScore)

pass
