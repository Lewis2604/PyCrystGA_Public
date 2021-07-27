import re
import os
import subprocess
import string
from Config.Config import *

class TOPAS:
    def __init__(self, topasPath, templateFile):
        self.directory = None # Config.get('working_directory') + 'XRD/' #@todo this is the problem
        self.topasPath = topasPath
        self.templateFile = templateFile

    def setDirectory(self, directory):
        self.directory = directory + 'XRD/'

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
        print(self.directory)
        return self.directory + str(identifier) + '.inp'

    def runInputFile(self, inputFile):
        # subprocess.run(os.path.normpath(self.topasPath) + ' ' + os.path.normpath(
        #     inputFile), stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)
        subprocess.run(os.path.normpath(self.topasPath) + ' ' + os.path.normpath(
            inputFile))

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

    def evaluate(self, structure):
        inputFile = self.makeInputFile(structure)
        print("q")
        self.runInputFile(inputFile)
        print("q1")
        rwp = self.getRwpFromInputFile(inputFile)
        print('q2')
        self.fileRemoval(structure)
        print("q3")
        return 1. / float(rwp),

    def fileRemoval(self, structure):
        os.remove(self.directory + str(structure.identifier) + '.inp')
        os.remove(self.directory + str(structure.identifier) + '.out')
