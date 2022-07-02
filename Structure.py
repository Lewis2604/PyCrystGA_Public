from secrets import token_hex
import random
from rdkit import Chem
from rdkit.Chem import TorsionFingerprints
import os


class Structure:
    def __init__(self, molFile, numTors, numMol):

        self.molFile = molFile
        self.numTors = numTors
        self.numMol = numMol
        self.identifier = token_hex()
        self.clone = False
        self.hasUndergoneCrossover = False

        self.torsions = []
        self.orientations = []
        self.positions = []
        self.rwp = []

        self.fitness = None

        self.generateTorsions()
        self.generatePositions()
        self.generateOrientations()

    def generateTorsions(self):
        if self.molFile is not None:
            tors_list = TorsionFingerprints.CalculateTorsionLists(
                Chem.MolFromMolFile(self.molFile)
            )

            variableTorsions = []
            for item in tors_list[0]:
                if len(item[0]) > 1:
                    variableTorsions.append(item[0][0])
                else:
                    variableTorsions.append(item[0])

            numberTorsions = variableTorsions * self.numMol

            for _ in numberTorsions:
                self.torsions.append(random.uniform(0, 360))

        if self.molFile is None:
            self.generateTorsionsNew()

    def generateTorsionsNew(self):
        for _ in range(self.numTors):
            self.torsions.append(random.uniform(0, 360))
        # print(self.torsions)

    def generateOrientations(self):
        for i in range(3 * self.numMol):
            self.orientations.append(random.uniform(0, 360))
            #self.orientatiobs = [rotate_z, rotate_y, rotate_x, rotate_w, rotate_v...]
        # print(self.orientations)

    def generatePositions(self):
        for i in range(3 * self.numMol):
            self.positions.append(random.uniform(0, 1))





