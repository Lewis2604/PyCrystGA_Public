import re
import os
import subprocess
import string
import time
from pprint import pprint

from Config.Config import *

class TOPAS:
    def __init__(self, topasPath, templateFile, seqFile):
        self.directory = Config.get('working_directory') + 'XRD/' #@todo this is the problem
        self.topasPath = topasPath
        self.templateFile = templateFile
        self.seqFile = seqFile

    def setWrkDirectory(self, directory):
        self.directory = directory + 'XRD/'

    def makeNewInputFile(self, population, structureList, directory):
        population.parameterDict.clear()
        numTors = []
        numPos = []
        numOrient = []
        contents = []
        newContents = []

        for structure in structureList:
            numTors.append(len(structure.torsions))
            numPos.append(len(structure.positions))
            numOrient.append(len(structure.orientations))
            for i in range(numTors[0]):
                population.parameterDict['Tors'+str(i)].append(str(structure.torsions[i]))
            for i in range(numPos[0]):
                population.parameterDict['Pos'+str(i)].append(str(structure.positions[i]))
            for i in range(numOrient[0]):
                population.parameterDict['Orient'+str(i)].append(str(structure.orientations[i]))

        with open(self.seqFile, 'r') as inp:
            for line in inp:
                contents.append(line)

        fileOutput = '\s*out\s*-'
        numRuns = '\s*num_runs'
        rotString = '#\s*list\s*rotate_q[a-z]_list\s*{}'
        tranString = '#\s*list\s*translate_t[a-z]_list\s*{}'
        taString = '#\s*list\s*t' + '[0-9]+' + '_list\s*{}'

        file = re.compile(fileOutput)
        run = re.compile(numRuns)
        rot = re.compile(rotString)
        tran = re.compile(tranString)
        ta = re.compile(taString)

        letterList = string.ascii_lowercase
        numberList = range(1, 1000)
        x, y, z = 0, 0, 0

        for line in contents:
            a = rot.search(line)
            if a:
                rotString1 = ','.join(population.parameterDict['Orient'+str(x)]).replace(',', ' ')
                line = rot.sub('#list rotate_q' + letterList[-1-x] + '_list { ' + rotString1 + ' }', line)
                x+=1
            b = tran.search(line)
            if b:
                tranString1 = ','.join(population.parameterDict['Pos'+str(y)]).replace(',', ' ')
                line = tran.sub('#list translate_t' + letterList[y] + '_list { ' + tranString1 + ' }', line)
                y+=1
            c = ta.search(line)
            if c:
                taString1 = ','.join(population.parameterDict['Tors'+str(z)]).replace(',', ' ')
                line = ta.sub('#list t' + str(numberList[z]) + '_list { ' + taString1 + ' }', line)
                z+=1
            d = run.search(line)
            if d:
                line = run.sub('num_runs ' + str(len(structureList)), line)
            e = file.search(line)
            if e:
                line = file.sub('   out ' + '\"' + self.directory + "rwp.txt" + '\"' + " append", line)

            newContents.append(line)

        with open((directory + str(population.identifier) + '.inp'), 'w') as out:
            out.writelines(newContents)
        return directory + str(population.identifier) + '.inp'



    def makeInputFile(self, structure):
        taString = 'Rotate_about_points'
        rotString = 'rotate'
        tranString = 't[a-c]'
        taRegex = r'(\b' + taString + r'\s*\(\s*\s+)([+-]?\d+\.?\d*)'
        rotRegex = r'(\b' + rotString + r'\s*\s+)([+-]?\d+\.?\d*)'
        tranRegex = r'(\b' + tranString + r'\s*\s+)([+-]?\d+\.?\d*)'

        # Used for Lamarckian evolution
        # taRegex = r'(\b' + taString + r'\s*\(\s*@\s+)([+-]?\d+\.?\d*)'
        # rotRegex = r'(\b' + rotString + r'\s*@\s+)([+-]?\d+\.?\d*)'
        # tranRegex = r'(\b' + tranString + r'\s*@\s+)([+-]?\d+\.?\d*)'

        ta = re.compile(taRegex)
        rot = re.compile(rotRegex)
        tran = re.compile(tranRegex)

        replaceTa = []
        replaceAng = []
        replaceTran = []
        contents = []
        newContents = []

        for i, ang in enumerate(structure.torsions):
            replaceTa.append(r'\1 ' + str(structure.torsions[i]))

        for i, num in enumerate(structure.orientations):
            replaceAng.append(r'\1 ' + str(structure.orientations[i]))

        for i, num in enumerate(structure.positions):
            replaceTran.append(r'\1 ' + str(structure.positions[i]))

        with open(self.templateFile, 'r') as inp:
            for line in inp:
                contents.append(line)

        x, y, z = 0, 0, 0

        for line in contents:
            a = ta.search(line)

            if a:
                line = ta.sub(replaceTa[x], line)
                x += 1

            b = rot.search(line)

            if b:
                line = rot.sub(replaceAng[y], line)
                y += 1

            c = tran.search(line)

            if c:
                line = tran.sub(replaceTran[z], line)
                z += 1

            newContents.append(line)

        with open((self.getInputFilePath(structure.identifier)), 'w') as out:
            out.writelines(newContents)

        return self.getInputFilePath(structure.identifier)

    def makeBatchFile(self, population):
        print('Batch')
        myBat = open(self.directory + "TOPASBatch.bat", 'w+')
        for structure in population:
            print(str(self.topasPath + " " +self.getInputFilePath(structure.identifier)))
            myBat.write(self.topasPath + " " +self.getInputFilePath(structure.identifier))
        myBat.close()
        return

    def getInputFilePath(self, identifier):
        return self.directory + str(identifier) + '.inp'

    def runInputFile(self, inputFile):
        subprocess.run(os.path.normpath(self.topasPath) + ' ' + os.path.normpath(
            inputFile), stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)
        # subprocess.run(os.path.normpath(self.topasPath) + ' ' + os.path.normpath(
        #     inputFile))

    def getRwpFromInputFile(self, inputFile):
        rwpString = 'r_wp'
        rwpRegex = r'(\b' + rwpString + r'\s*\s+)([+-]?\d+\.?\d*)'
        rwp = re.compile(rwpRegex)
        fOpen = open(inputFile.replace('.inp', '.out'))
        lines = fOpen.readlines()
        for line in lines:
            match = rwp.search(line)
            if match:
                rwpValue = (re.findall("[+-]?\d+\.\d+", str(match)))
                fOpen.close()
                newRwp = rwpValue[0]
        fOpen.close()
        return newRwp

    def newEvaluate(self, inputFile):
        self.runInputFile(inputFile)
        fitnessFile = self.directory + "rwp.txt"
        fOpen = open(fitnessFile, "r")
        rwp = []
        for line in fOpen:
            rwp.append((1. /float(line),))
        # print('zap')
        # print(rwp)
        fOpen.close()
        if os.path.exists(fitnessFile):
            os.remove(fitnessFile)
        else:
            print(fitnessFile)
        return rwp



        # rwp = self.getRwpFromInputFile(inputFile)
        # self.fileRemoval(structure)

    def evaluate(self, structure):
        start = time.time()
        inputFile = self.makeInputFile(structure)
        t1 = time.time()
        time1 = t1-start
        # print("time1")
        # print(time1)
        self.runInputFile(inputFile)
        t2 = time.time()
        time2 = t2-t1
        # print('time2')
        # print(time2)
        rwp = self.getRwpFromInputFile(inputFile)
        self.fileRemoval(structure)
        return 1. / float(rwp),

    def fileRemoval(self, structure):
        os.remove(self.directory + str(structure.identifier) + '.inp')
        os.remove(self.directory + str(structure.identifier) + '.out')
