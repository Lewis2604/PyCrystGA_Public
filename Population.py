from Structure import *
import copy
import collections


class Population:
    def __init__(self, molFile, numTors, numMol, popSize):
        self.molFile = molFile
        self.numTors = numTors
        self.numMol = numMol
        self.popSize = popSize
        self.identifier = token_hex()

        self.structures = []
        self.clones = []
        self.crossovers = []
        self.xoverOffspring = []
        self.mutants = []

        self.rwpVals = []

        self.parameterDict = collections.defaultdict(list)

        self.eltPctDiff = []
        self.mutPctDiff = []
        self.generationNum = []
        self.populationAmplitude = []

        self.eltFitnessMin = []
        self.eltFitnessMax = []
        self.eltFitnessAvg = []
        self.eltFitnessMinNorm = []
        self.eltFitnessMaxNorm = []
        self.eltFitnessStdDev = []
        #@todo add values to this list

        self.eltRwpStdDev = []
        self.eltRwpStdDevRollAvg = []
        self.eltRwpStdDevRollAvgStdDev = []

        self.mutFitnessMin = []
        self.mutFitnessMax = []
        self.mutFitnessAvg = []
        self.mutFitnessStdDev = []
        #@todo add values to this list
        self.mutRwpStdDev = []


        self.make(self.molFile, self.numTors, self.numMol, self.popSize)

    def make(self, molFile, numTors, numMol, popSize):
        for structure in range(popSize):
            self.structures.append(Structure(molFile, numTors, numMol))

    def clearClones(self):
        self.clones = []

    def duplicate(self):
        self.clearClones()

        for structure in self.structures:
            structure = copy.deepcopy(structure)
            structure.clone = True
            self.clones.append(structure)

    def mergeMutants(self):
        self.structures = self.structures + self.mutants
        self.mutants = []

    def mergeCrossovers(self):
        self.structures = self.structures + self.xoverOffspring
        self.crossovers = []
        self.xoverOffspring = []

    def calcEltPercentageDifference(self):
        pctDiff = (abs(self.eltFitnessMax[-1]-self.eltFitnessAvg[-1])/
                   ((self.eltFitnessMax[-1]+self.eltFitnessAvg[-1])/2))*100

        self.eltPctDiff.append(pctDiff)

    def calcMutPercentageDifference(self):
        pctDiff = (abs(self.mutFitnessMax[-1]-self.mutFitnessAvg[-1])/
                   ((self.mutFitnessMax[-1]+self.mutFitnessAvg[-1])/2))*100

        self.mutPctDiff.append(pctDiff)

