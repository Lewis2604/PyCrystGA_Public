import re
import os
import subprocess
import string

class TOPAS:
    def __init__(self, topasPath, templateFile):
        self.directory = None
        self.topasPath = topasPath
        self.templateFile = templateFile

    def setDirectory(self, directory):
        self.directory = directory

    def makeInputFile(self, structure):
        if self.directory is None:
            raise Exception('No TOPAS directory set')

        taString = 'Rotate_about_points'
        rotString = 'rotate'
        tranString = 't[a-c]'
        taRegex = r'(\b' + taString + r'\s*\(\s*\s+)([+-]?\d+\.?\d*)'
        rotRegex = r'(\b' + rotString + r'\s*\s+)([+-]?\d+\.?\d*)'
        tranRegex = r'(\b' + tranString + r'\s*\s+)([+-]?\d+\.?\d*)'

        # Used for Lamarckian evolution
        #taRegex = r'(\b' + taString + r'\s*\(\s*@\s+)([+-]?\d+\.?\d*)'
        #rotRegex = r'(\b' + rotString + r'\s*@\s+)([+-]?\d+\.?\d*)'
        #tranRegex = r'(\b' + tranString + r'\s*@\s+)([+-]?\d+\.?\d*)'

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

    def getInputFilePath(self, identifier):
        return self.directory + str(identifier) + '.inp'

    def runInputFile(self, inputFile):
        subprocess.run(os.path.normpath(self.topasPath) + ' ' + os.path.normpath(
            inputFile), stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)

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
        self.runInputFile(inputFile)
        rwp = self.getRwpFromInputFile(inputFile)
        self.fileRemoval(structure)
        return 1./float(rwp),

    def fileRemoval(self, structure):
        os.remove(self.directory + str(structure.identifier) + '.inp')
        os.remove(self.directory + str(structure.identifier) + '.out')
