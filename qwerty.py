import numpy as np

def getMaxListIndex(list):
    maxVal = max(list)
    maxIndex = list.index(maxVal)
    return maxIndex

qwerty = [[10,20,40,30], [40,30,10,20], [20,10,30,40]]

maxQwertyIndex = []

for i in qwerty:
    maxQwertyIndex.append(getMaxListIndex(i))

print(maxQwertyIndex)

bestVal = []

count= 0
for list in qwerty:
    bestVal.append(list[maxQwertyIndex[count]])
    count+=1

print(bestVal)