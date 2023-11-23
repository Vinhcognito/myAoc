import os
os.system("cls" if os.name == "nt" else "clear")
import math
import time


def calcPoints(m,n):
    #for part 1
    if m == "A":
        if n == "X":
            points = 4
        if n == "Y":
            points = 8
        if n == "Z":
            points = 3
    if m == "B":
        if n == "X":
            points = 1
        if n == "Y":
            points = 5
        if n == "Z":
            points = 9
    if m == "C":
        if n == "X":
            points = 7
        if n == "Y":
            points = 2
        if n == "Z":
            points = 6


    return points

def calcResponse(m,n):
    #determine proper response
    if m == "A":
        if n == "X":
            response = "Z"
        if n == "Y":
            response = "X"
        if n == "Z":
            response = "Y"
    if m == "B":
        if n == "X":
            response = "X"
        if n == "Y":
            response = "Y"
        if n == "Z":
            response = "Z"
    if m == "C": 
        if n == "X":
            response = "Y"
        if n == "Y":
            response = "Z"
        if n == "Z":
            response = "X"
    return (m,response)

#read and split
my_file = open("day2input.txt", "r")
content = my_file.read().strip()
content_list=content.split("\n")

sum=0

#part 1 answer
""" for n in content_list:
    pair = n.split(" ")
    sum+=calcPoints(*pair) 
    or
    sum+=calcPoints(n.split(" "))"""

#part 2 answer
for n in content_list:
    pair = n.split(" ")
    sum+= calcPoints(*calcResponse(*pair))
    

print(sum)