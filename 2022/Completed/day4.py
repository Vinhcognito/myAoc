import math
import time
import fileinput

def calc(s1,s2,s3,s4):
    #check exclusiveness? for part 1
    n1=int(s1)
    n2=int(s2)
    n3=int(s3)
    n4=int(s4)

    if n1 <= n3 and n2 >= n4:
        return 1
    if n3 <= n1 and n4 >= n2:
        return 1

    return 0

def calcOver(s1,s2,s3,s4):
    #check overlap? for part 2
    n1=int(s1)
    n2=int(s2)
    n3=int(s3)
    n4=int(s4)

    #if (n4> n1 < n3) and ( n4 > n2 < n3):
    if n3<n2:
        return 0
    #if (n2> n3 < n1) and ( n2 > n4 < n1):
    if n4>n1:
        return 0

    return 1

#read and split
my_file = open("day4input.txt", "r")
content = my_file.read().strip()
content_list=content.split("\n")

count1=0
count2=0

for n in content_list:
    count1+=calc(*(n.split(",")[0]).split("-"),*(n.split(",")[1]).split("-"))
    count2+=calcOver(*(n.split(",")[0]).split("-"),*(n.split(",")[1]).split("-"))
    

print(count1)
print(count2)