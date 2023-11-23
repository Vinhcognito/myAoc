from liz import *
wipeTerminal()
import timing

my_file = open("inputs\day19sampleinput.txt", "r")
#sample : 9*1,12*2 = 33 total
#my_file = open("inputs\day19input.txt", "r")
content = my_file.read().strip()
cl=content.split("\n")

blueprint=[]
#ore cost for ore robot
#ore cost for clay robot
#ore and clay cost for obsi robot
#ore and obsi cost for geode robot

for line in cl:
    blueprint.append(ints(line)[1:])

""" maximize the number of opened geodes after 24 minutes  """
""" Determine the quality level of each blueprint by multiplying that 
blueprint's ID number with the largest number of geodes 
that can be opened in 24 minutes using that blueprint. 
 """
