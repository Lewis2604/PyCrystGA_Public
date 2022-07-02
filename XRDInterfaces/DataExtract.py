import numpy as np
import re
from pprint import pprint

# file = r"D:\PhD\Year_4\AlgorithmNew\DBTFB\Static\(1)\Statistics\Pop_stats.txt"
# fileOpen = open(file)
#
# lines = fileOpen.readlines()
#
# pprint(lines)
#
# # genString = '[1-9][0-9]*'
# eltString = 'Elite'
# # mutString = 'Mutant'
# # fitString = '\(.*?\)'
# # listString = '\[.*?\]'
# #
# # gen = re.compile(genString)
# elt = re.compile(eltString)
# # mut = re.compile(mutString)
# # fit = re.compile(fitString)
# # lst = re.compile(listString)
# #
#
#
# lineNum = []
#
# for line_number, line in enumerate(lines):
#     for match in re.findall(elt, line):
#         lineNum.append(line_number+2)
#
# print(lineNum)
#
# linesOfInterest = []
#
# for num in lineNum:
#     line = lines[num]
#     linesOfInterest.append(line[4:])
#
# print(linesOfInterest)
#
# stdDev = []
#
# for i in linesOfInterest:
#     # print(i)
#     strip = i.strip("\n")
#     # print(strip)
#     split = i.split("\t")
#     stdDev.append(float(split[0]))
#
# print(len(stdDev))


def stdDevExtraction(file):
    fileOpen = open(file)
    lines = fileOpen.readlines()
    eltString = 'Elite'
    elt = re.compile(eltString)
    lineNum = []

    for line_number, line in enumerate(lines):
        for match in re.findall(elt, line):
            lineNum.append(line_number+2)

    linesOfInterest = []

    for num in lineNum:
        line = lines[num]
        linesOfInterest.append(line[4:])

    stdDev = []

    for i in linesOfInterest:
        strip = i.strip("\n")
        split = strip.split("\t")
        stdDev.append(float(split[0]))
    return stdDev

def listAvg(lst):
    return sum(lst) / len(lst)

newList = []
for i in stdDevExtraction(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\Static\(1)\Statistics\Pop_stats.txt"):
    newList.append(i**2)

print(listAvg(stdDevExtraction(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\Static\(1)\Statistics\Pop_stats.txt")))
print(np.sqrt((listAvg(newList))))


"""
todo extract data from txt file, 
format data appropriately, 
plot relevant dat for individual parameter tracking
"""






