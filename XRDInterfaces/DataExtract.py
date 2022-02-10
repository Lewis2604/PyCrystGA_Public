import numpy as np
import re

file = r"C:/PhD/Year_4/Algorithm/Test/Exponent/IMDC/5/(5)/Statistics/FitnessHistory.txt"
fileOpen = open(file)

lines = fileOpen.readlines()

genString = '[1-9][0-9]*'
eltString = 'Elite'
mutString = 'Mutant'
fitString = '\(.*?\)'
listString = '\[.*?\]'

gen = re.compile(genString)
elt = re.compile(eltString)
mut = re.compile(mutString)
fit = re.compile(fitString)
lst = re.compile(listString)

for line in lines:
    lstMatch = lst.search(line)
    if lstMatch:
        print(line)
"""
todo extract data from txt file, 
format data appropriately, 
plot relevant dat for individual parameter tracking
"""






