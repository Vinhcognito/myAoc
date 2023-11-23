import re
my_file = open("day4input.txt", "r")
content = my_file.read().strip()
content_list=content.split("\n")

countContain=0
countOverlap=0

for n in content_list:
    ranges = [int(x) for x in re.split("-|,", n)]
    if (ranges[0]>=ranges[2] and ranges[1]<=ranges[3]) or (ranges[0]<=ranges[2] and ranges[1]>=ranges[3]):
        countContain+=1
    if ranges[2]<=ranges[1] and ranges[3]>=ranges[0]:
        countOverlap+=1

print("No. of pairs: ",len(content_list))
print("Answer 1: ",countContain)
print("Answer 2: ",countOverlap)