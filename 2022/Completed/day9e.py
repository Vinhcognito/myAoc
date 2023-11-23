my_file = open("day9input.txt", "r")
content = my_file.read().strip()
lines = content.split("\n")
matrix = [[1]]
hCoords = [0,0]
tCoords = [0,0]

for x in lines:
    elements = x.split()
    if elements[0] == "L":
        counter = 0
        while counter < int(elements[1]):
            if hCoords[1] > 0:
                hCoords[1] -= 1
            else:
                for y in matrix:
                    y.insert(0, 0)
            if (tCoords[1] - hCoords[1]) == 2:
                tCoords[1] -= 1
                tCoords[0] = hCoords[0]
                matrix[tCoords[0], tCoords[1]] = 1         
            counter += 1
    elif elements[0] == "R":
        counter = 0
        while counter < int(elements[1]):
            if hCoords[1] < (len(matrix[0] - 1)):
                hCoords[1] += 1
            else:
                for y in matrix:
                    y.append(0)
            if (hCoords[1] - tCoords[1]) == 2:
                tCoords[1] += 1
                tCoords[0] = hCoords[0]
                matrix[tCoords[0], tCoords[1]] = 1
            counter += 1
    elif elements[0] == "U":
        counter = 0
        while counter < int(elements[1]):
            if hCoords[0] > 0:
                hCoords[0] -= 1
            else:
                matrix.insert(0, [0])
                for y in range(2, len(matrix[1])):
                    matrix[0].append(False)
            if (tCoords[0] - hCoords[0]) == 2:
                tCoords[0] -= 1
                tCoords[1] = hCoords[1]
                matrix[tCoords[0], tCoords[1]] = 1
            counter += 1
    elif elements[0] == "D":
        counter = 0
        while counter < int(elements[1]):
            if hCoords[0] < (len(matrix[0]) - 1):
                hCoords[0] += 1
            else:
                matrix[0].append(False)
                for y in range(2, len(matrix[1])):
                    matrix[-1].append(False)
            if (hCoords[0] - tCoords[0]) == 2:
                tCoords[0] -= 1
                tCoords[1] = hCoords[1]
                matrix[tCoords[0], tCoords[1]] = 1
            counter += 1
    else:
        print("Instruction not recognized")
print("Instructions read")
count = 0
for y in matrix:
    print(y, "\n")
    count += sum(y)
print("No. of squares visited by tail at least once", count)