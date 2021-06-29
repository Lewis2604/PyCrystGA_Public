from secrets import token_hex
import random
from rdkit import Chem
from rdkit.Chem import TorsionFingerprints
import os


class Structure:
    def __init__(self, molFile, numMol):

        self.molFile = molFile
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

    # def funct1(self, arg1, **arg2):
    #
    # def funct1(self, arg1, arg2):


    def generateTorsions(self):
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

    def generateOrientations(self):
        for i in range(3 * self.numMol):
            self.orientations.append(random.uniform(0, 360))

    def generatePositions(self):
        for i in range(3 * self.numMol):
            self.positions.append(random.uniform(0, 1))





