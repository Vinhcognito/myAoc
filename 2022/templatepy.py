from liz import *
from collections import namedtuple
wipeTerminal()


my_file = open("inputs\day23sampleinput.txt", "r")
#my_file = open("inputs\day23input.txt", "r")

content = my_file.read().strip()
cl=content.split("\n")

grid=[]

