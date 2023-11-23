import math
import time
import fileinput

def calcPoints(string):
    if string.islower():
        return (ord(string)-96)
    if string.isupper():
        return (ord(string)-38)
    

'''def findCommon(string):
    #part 1
    li=list(string)
    mid = int(len(li)/2)
    bag1=set(li[0:mid])
    bag2=set(li[mid:])
    
    match = (set(bag1)& set(bag2)).pop()
    return(match)'''

def findCommon(s1,s2,s3):
    #part 2
    bag1=set(s1)
    bag2=set(s2)
    bag3=set(s3)

    match = (bag1&bag2&bag3).pop()

    return(match)



#read and split
my_file = open("day3input.txt", "r")
content = my_file.read().strip()
content_list=content.split("\n")

sum=0
count=0

#could have used 
#for n in range(0,len(content_list),3):
for n in content_list:
    count+=1
    if count%3 == 1:
        s1=n
    if count%3 == 2:
        s2=n
    if count%3 == 0:
        s3=n
        count=0
        sum+=calcPoints(findCommon(s1,s2,s3)) 

print(sum)
    
    

    
