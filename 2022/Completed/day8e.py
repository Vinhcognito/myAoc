my_file = open("day8input.txt", "r")
content = my_file.read().strip()
grid = content.split("\n")

hPointer = 1
vPointer = 1
rowLength = len(grid[0])
listLength = len(grid)
treeCounter = 2 * rowLength
visibleTreeMap = [[True]]

#allgood, initializing treemap with trues and falses
for x in range(listLength):
    if x > 0:
        visibleTreeMap.append([True])
    for y in range(rowLength - 1):
        if x == 0 or x == (listLength - 1) or y == (rowLength - 2):
            visibleTreeMap[x].append(True)
        else:
            visibleTreeMap[x].append(False)



while vPointer < (listLength - 1):
    treeCounter += 2
    miniTreeCounter = 2
    hPointer = 1
    while hPointer < (rowLength - 1):
        flag = False
        for x in range(hPointer):
            if grid[vPointer][hPointer] > grid[vPointer][x]:
                flag = True
                print(vPointer,hPointer, "loop 1")
            else:
                flag = False
                print(flag, "loop 1")
                break
        if flag:
            if visibleTreeMap[vPointer][hPointer] == False:
                visibleTreeMap[vPointer][hPointer] = True
                treeCounter += 1
                miniTreeCounter += 1
            hPointer += 1
        else:
            hPointer = rowLength - 2
            break
    while hPointer > 0:
        flag = False
        for x in range(1, (rowLength - hPointer)):
            if grid[vPointer][hPointer] > grid[vPointer][hPointer + x]:
                flag = True
                print(vPointer,hPointer, "loop 2")
            else:
                flag = False
                print(flag, "loop 2")
                break
        if flag:
            if visibleTreeMap[vPointer][hPointer] == False:
                visibleTreeMap[vPointer][hPointer] = True
                treeCounter += 1
                miniTreeCounter += 1
            hPointer -= 1
        else:
            hPointer = 1
            break
    vPointer += 1
    print("Trees visible in row", vPointer, ":", miniTreeCounter)
""" 
while hPointer < (rowLength - 1):
    miniTreeCounter = 2
    vPointer = 1
    while vPointer < (listLength - 1):
        flag = False
        for x in range(vPointer):
            if grid[vPointer][hPointer] > grid[x][hPointer]:
                flag = True
                print(vPointer,hPointer, "loop 3")
            else:
                flag = False
                print(flag, "loop 3")
                break
        if flag:
            if visibleTreeMap[vPointer][hPointer] == False:
                visibleTreeMap[vPointer][hPointer] = True
                treeCounter += 1
                miniTreeCounter += 1
            vPointer += 1
        else:
            vPointer = listLength - 2
            break
    while vPointer > 0:
        flag = False
        print(vPointer)
        for x in range(1, (vPointer - listLength)):
            if grid[vPointer][hPointer] > grid[vPointer + x][hPointer]:
                flag = True
                print(vPointer,hPointer, "loop 4")
            else:
                flag = False
                print(flag, "loop 4")
                break
        if flag:
            if visibleTreeMap[vPointer][hPointer] == False:
                visibleTreeMap[vPointer][hPointer] = True
                treeCounter += 1
                miniTreeCounter += 1
            vPointer -= 1
        else:
            vPointer = 1
            break
    hPointer += 1
    print("Trees visible in column", hPointer, ":", miniTreeCounter)

print("Total visible trees (including border trees):",treeCounter) """