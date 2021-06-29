from Population import *
from Toolbox import *
from Statistics import *
from DataVisualisation import *
import time
import math
import sys


class PyCrystGA:
    def __init__(self, molFile, numMol, directory,
                 xrdInterface, popSize, numGen,
                 crossoverPercentage, mutationPercentage,
                 crossoverType, mutationType, # 0 static, 1 linear dynamic, 2 exponential dynamic
                 pctDiffThresh, graphFontSize, graphLabelSize,
                 graphFileName, graphFileNamePctDiff,  graphDpi):
        self.molFile = molFile
        self.numMol = numMol
        self.directory = directory
        self.xrdInterface = xrdInterface
        self.popSize = popSize
        self.numGen = numGen
        self.crossoverType = crossoverType
        self.mutationType = mutationType

        self.crossoverPercentage = crossoverPercentage
        self.originalCrossoverPercentage = crossoverPercentage
        self.lowerCrossoverRateLimit = 0
        self.upperCrossoverRateLimit = 1

        self.mutationPercentage = mutationPercentage
        self.originalMutationPercentage = mutationPercentage
        self.lowerMutationRateLimit = 0
        self.upperMutationRateLimit = 1

        self.pctDiffThresh = pctDiffThresh
        self.graphFontSize = graphFontSize
        self.graphLabelSize = graphLabelSize
        self.graphFileName = graphFileName
        self.graphFileNamePctDiff = graphFileNamePctDiff
        self.graphDpi = graphDpi

        self.crossoverHistory = []
        self.mutationHistory = []

        self.population = None
        self.xrdInterface.setDirectory(directory + "XRD/")
        self.shouldStop = False
#@todo figure out how to choose the type of genetic operators that you want,
        # @todo so that you can use the appropriate graph plotting method
        self.staticCrossover = False
        self.staticMutation = False

        self.linearDynamicCrossover = False
        self.linearDynamicMutation = False

        self.exponentialDynamicCrossover = False
        self.exponentialDynamicMutation = False

        self.currentGeneration = 0
        self.startTime = None
        self.endTime = None
        self.timeElapsed = None

    def setGeneticOperatorType(self):
        if self.crossoverType == 0:
            self.staticCrossover = True
        if self.mutationType == 0:
            self.staticMutation = True

        if self.crossoverType == 1:
            self.linearDynamicCrossover = True
        if self.mutationType == 1:
            self.linearDynamicMutation = True

        if self.crossoverType == 2:
            self.exponentialDynamicCrossover = True
        if self.mutationType == 2:
            self.exponentialDynamicMutation = True

    def start(self):
        self.startTime = time.time()
        Statistics.writeRunInfoToFile(self.directory+'Statistics/', self.numGen,
                                      self.popSize, self.crossoverPercentage,
                                      self.mutationPercentage, self.pctDiffThresh)
        Statistics.createFitnessLog(Statistics())
        self.makePopulation()
        self.crossoverHistory.append(self.crossoverPercentage)
        self.mutationHistory.append(self.mutationPercentage)
        self.setGeneticOperatorType()
        print("Genetic Operator Type")
        print(self.staticCrossover, self.staticMutation, self.linearDynamicCrossover,
              self.linearDynamicMutation, self.exponentialDynamicCrossover, self.exponentialDynamicMutation)
        while not self.shouldStop:
            self.currentGeneration += 1
            self.evaluateFitness()
            if self.linearDynamicCrossover:
                if self.currentGeneration > 1:
                    self.dynamicCrossoverLinear()
            if self.exponentialDynamicCrossover:
                if self.currentGeneration > 1:
                    self.dynamicCrossoverExponential()
            # if self.staticCrossover:
            #     if self.currentGeneration > 1:
            #         self.staticCrossover()
            print("crossover percent")
            print(self.crossoverPercentage)
            self.crossover()
            self.mergeCrossovers()
            self.evaluateFitness()
            self.elitistSelection()
            #@todo energetic optimisation
            Statistics.recordElitePopulationStatistics(Statistics(), self.directory+'Statistics/',
                                                       self.population, self.currentGeneration)
            self.population.calcEltPercentageDifference()
            if self.linearDynamicMutation:
                if self.currentGeneration > 1:
                    self.dynamicMutationLinear()
            if self.exponentialDynamicMutation:
                if self.currentGeneration > 1:
                    self.dynamicMutationExponential()
            self.selectMutants()
            self.mutation()
            self.mergeMutants()
            self.evaluateFitness()
            Statistics.recordMutantPopulationStatistics(Statistics(), self.directory+'Statistics/',
                                                        self.population, self.currentGeneration)
            self.population.calcMutPercentageDifference()

            self.endTime = time.time()
            self.timeElapsed = self.endTime - self.startTime
            print(self.currentGeneration, file=open(self.directory + 'Statistics/' + "Time.txt", "a"))
            print(self.timeElapsed, file=open(self.directory + 'Statistics/' + "Time.txt", "a"))
            self.simpleStoppingCriteria()


        print("Elite", file=open(self.directory + 'Statistics/' + "pct_diff.txt", "a"))
        print(self.population.eltPctDiff, file=open(self.directory + 'Statistics/' + "pct_diff.txt", "a"))
        print("Mutant", file=open(self.directory + 'Statistics/' + "pct_diff.txt", "a"))
        print(self.population.mutPctDiff, file=open(self.directory + 'Statistics/' + "pct_diff.txt", "a"))

        # self.endTime = time.time()
        # self.timeElapsed = self.endTime - self.startTime
        # print(self.currentGeneration, file=open(self.directory + 'Statistics/' + "Time.txt", "a"))
        # print(self.timeElapsed, file=open(self.directory + 'Statistics/' + "Time.txt", "a"))

        DataVisualisation.plotGraph(DataVisualisation(), self, self.graphFontSize, self.graphLabelSize,
                                    self.graphFileName, self.directory, self.graphDpi)

        if self.linearDynamicCrossover or self.linearDynamicMutation or \
                self.exponentialDynamicCrossover or self.exponentialDynamicMutation:
            DataVisualisation.plotPctDiffGraph(DataVisualisation(), self, self.graphFontSize, self.graphLabelSize,
                                    self.graphFileNamePctDiff, self.directory, self.graphDpi)

    #@todo put stopping criteria here KEEP self.shouldStop = True
    def simpleStoppingCriteria(self):
        if self.currentGeneration > 50:
            if np.average(self.population.eltPctDiff[-50:])<1:
                self.shouldStop = True
                self.endTime = time.time()
        if self.currentGeneration == self.numGen:
            self.shouldStop = True
            self.endTime = time.time()

    # def simpleStoppingCriteria(self):
    #     if self.currentGeneration == self.numGen:
    #         self.shouldStop = True
    #         self.endTime = time.time()

    # def checkStoppingCriteria(self):
    #     self.stoppingCriteria()

    def makePopulation(self):
        creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0))

        self.population = Population(self.molFile,
                                     self.numMol,
                                     self.popSize)

        for structure in self.population.structures:
            structure.fitness = creator.FitnessMax()

    def evaluateFitness(self):
        fitnesses = map(self.xrdInterface.evaluate, self.population.structures)
        for structure, fit in zip(self.population.structures, fitnesses):
            structure.fitness.values = fit

    #@todo checkGeneration has to be greater than 20 (GUI slider start at 20)
    # def dynamicCrossover(self, checkGeneration, crossoverReduction, crossoverIncrease):
    #@todo use DOF as a weighting
    # def dynamicCrossoverCheck(self, checkGeneration):
    #     crossoverPercentage = self.crossoverPercentage
    #     if self.currentGeneration >= checkGeneration:
    #         return
    #

    # def dynamicCrossoverLinear(self):
    #     if self.population.eltPctDiff[-1] <= 5:
    #         scaleFactor1 = 1 - ((5 - self.population.eltPctDiff[-1])/10) # /100 & *10
    #         newCrossoverPercentage1 = round(self.originalCrossoverPercentage*scaleFactor1, 2)
    #         setattr(self, 'crossoverPercentage', newCrossoverPercentage1)
    #         self.crossoverHistory.append(self.crossoverPercentage)
    #         return
    #     if self.population.eltPctDiff[-1] > 5:
    #         scaleFactor2 = self.population.eltPctDiff[-1]/100
    #         newCrossoverPercentage2 = round(self.originalCrossoverPercentage + \
    #                                   self.originalCrossoverPercentage*scaleFactor2, 2)
    #         setattr(self, 'crossoverPercentage', newCrossoverPercentage2)
    #         self.crossoverHistory.append(self.crossoverPercentage)
    #         return

    def dynamicCrossoverLinear(self):
        if self.population.eltPctDiff[-1] <= self.pctDiffThresh:
            scaleFactor1 = 1 - ((self.pctDiffThresh - self.population.eltPctDiff[-1])/10) # /100 & *10
            # newCrossoverPercentage1 = math.floor(self.originalCrossoverPercentage*scaleFactor1)
            newCrossoverPercentage1 = round(self.originalCrossoverPercentage*scaleFactor1, 2)
            setattr(self, 'crossoverPercentage', newCrossoverPercentage1)
            self.crossoverHistory.append(self.crossoverPercentage)
            return
        if self.population.eltPctDiff[-1] > self.pctDiffThresh:
            scaleFactor2 = self.population.eltPctDiff[-1]/100
            # newCrossoverPercentage2 = math.floor(self.originalCrossoverPercentage*(1+scaleFactor2))
            newCrossoverPercentage2 = round(self.originalCrossoverPercentage*(1+scaleFactor2), 2)
            setattr(self, 'crossoverPercentage', newCrossoverPercentage2)
            self.crossoverHistory.append(self.crossoverPercentage)
            return

    def dynamicMutationLinear(self):
        if self.population.eltPctDiff[-1] > self.pctDiffThresh:
            scaleFactor1 = 1 - ((self.pctDiffThresh - self.population.eltPctDiff[-1])/10) # /100 & *10
            # newMutationPercentage1 = math.floor(self.originalMutationPercentage*scaleFactor1)
            newMutationPercentage1 = round(self.originalMutationPercentage*scaleFactor1, 2)
            setattr(self, 'mutationPercentage', newMutationPercentage1)
            self.mutationHistory.append(self.mutationPercentage)
            return
        if self.population.eltPctDiff[-1] <= self.pctDiffThresh:
            scaleFactor2 = self.population.eltPctDiff[-1]/100
            # newMutationPercentage2 = math.floor(self.originalMutationPercentage*(1+scaleFactor2))
            newMutationPercentage2 = round(self.originalMutationPercentage*(1+scaleFactor2), 2)
            setattr(self, 'mutationPercentage', newMutationPercentage2)
            self.mutationHistory.append(self.mutationPercentage)
            return

    def dynamicCrossoverExponential(self):
        #@todo decrease crossover rate
        if self.population.eltPctDiff[-1] <= self.pctDiffThresh:
            #@todo works!!!!!!!!!!
            #@todo if stagnation has occurred scaleFactor1 = 1
            scaleFactor1 = (self.pctDiffThresh-self.population.eltPctDiff[-1])/self.pctDiffThresh
            # setattr(self, 'crossoverPercentage', math.floor(self.originalCrossoverPercentage*np.exp(-scaleFactor1)))
            setattr(self, 'crossoverPercentage', round(self.originalCrossoverPercentage*np.exp(-scaleFactor1), 2))
            self.crossoverHistory.append(self.crossoverPercentage)
            #@todo increase crossover rate
        if self.population.eltPctDiff[-1] > self.pctDiffThresh:
            #@todo worls!!!!!!!!!!!
            #@todo maximum value of scaleFactor2 = 1
            #@todo as the pctDiff increases so does scaleFactor2
            scaleFactor2 = (self.population.eltPctDiff[-1]-self.pctDiffThresh)/self.population.eltPctDiff[-1]
            newCrossoverPercentage = round(self.originalCrossoverPercentage*np.exp(scaleFactor2), 2)
            if newCrossoverPercentage > 1:
                setattr(self, 'crossoverPercentage', self.upperCrossoverRateLimit)
                self.crossoverHistory.append(self.crossoverPercentage)
            else:
                setattr(self, 'crossoverPercentage', newCrossoverPercentage)
                self.crossoverHistory.append(self.crossoverPercentage)

    def dynamicMutationExponential(self):
        if self.population.eltPctDiff[-1] < self.pctDiffThresh:
            print("sf1")
            scaleFactor1 = (self.pctDiffThresh - self.population.eltPctDiff[-1]) / self.pctDiffThresh
            newMutationPercentage = round(self.originalMutationPercentage * np.exp(scaleFactor1), 2)
            if newMutationPercentage > self.upperMutationRateLimit:
                setattr(self, 'mutationPercentage', self.upperMutationRateLimit)
                self.mutationHistory.append(self.mutationPercentage)
            else:
                setattr(self, 'mutationPercentage', newMutationPercentage)
                self.mutationHistory.append(self.mutationPercentage)

        if self.population.eltPctDiff[-1] >= self.pctDiffThresh:
            print("sf2")
            scaleFactor2 = (self.population.eltPctDiff[-1] - self.pctDiffThresh) / self.population.eltPctDiff[-1]
            # setattr(self, 'mutationPercentage', math.floor(self.originalMutationPercentage * np.exp(scaleFactor2)))
            setattr(self, 'mutationPercentage', round(self.originalMutationPercentage * np.exp(-scaleFactor2), 2))
            self.mutationHistory.append(self.mutationPercentage)

    def dynamicCrossoverExponentialLimit(self):
        #@todo decrease crossover rate
        if self.population.eltPctDiff[-1] <= self.pctDiffThresh:
            #@todo if stagnation has occurred scaleFactor1 = 1
            scaleFactor1 = (self.pctDiffThresh-self.population.eltPctDiff[-1])/self.pctDiffThresh
            # setattr(self, 'crossoverPercentage', round(self.originalCrossoverPercentage*np.exp(-scaleFactor1)))
            #@todo negative exponent decreases the crossover rate
            if self.originalCrossoverPercentage*np.exp(-scaleFactor1) < self.lowerCrossoverRateLimit:
                setattr(self, 'crossoverPercentage', self.lowerCrossoverRateLimit)
                self.crossoverHistory.append(self.crossoverPercentage)
                return
            if self.originalCrossoverPercentage * np.exp(-scaleFactor1) > self.lowerCrossoverRateLimit:
                setattr(self, 'crossoverPercentage', math.floor(self.originalCrossoverPercentage*np.exp(-scaleFactor1)))
                self.crossoverHistory.append(self.crossoverPercentage)
                return

        #@todo increase crossover rate
        if self.population.eltPctDiff[-1] > self.pctDiffThresh:
        #@todo maximum value of scaleFactor2 = 1
        #@todo as the pctDiff increases so does scaleFactor2
            scaleFactor2 = (self.population.eltPctDiff[-1]-self.pctDiffThresh)/self.population.eltPctDiff[-1]
            # setattr(self, 'crossoverPercentage', round(self.originalCrossoverPercentage*np.exp(scaleFactor2)))
            if self.originalCrossoverPercentage*np.exp(scaleFactor2) > self.upperCrossoverRateLimit:
                setattr(self, 'crossoverPercentage', self.upperCrossoverRateLimit)
                self.crossoverHistory.append(self.crossoverPercentage)
                return
            if self.originalCrossoverPercentage * np.exp(scaleFactor2) < self.upperCrossoverRateLimit:
                setattr(self, 'crossoverPercentage', math.floor(self.originalCrossoverPercentage*np.exp(scaleFactor2)))
                self.crossoverHistory.append(self.crossoverPercentage)
                return

    def dynamicMutationExponentialLimit(self):
        if self.population.eltPctDiff[-1] > self.pctDiffThresh:
            scaleFactor1 = (self.pctDiffThresh - self.population.eltPctDiff[-1]) / self.pctDiffThresh
            if self.originalMutationPercentage * np.exp(-scaleFactor1) < self.lowerMutationRateLimit:
                setattr(self, 'mutationPercentage', self.lowerMutationRateLimit)
                self.mutationHistory.append(self.mutationPercentage)
                return
            if self.originalMutationPercentage * np.exp(-scaleFactor1) > self.lowerMutationRateLimit:
                setattr(self, 'mutationPercentage', math.floor(self.originalMutationPercentage * np.exp(-scaleFactor1)))
                self.mutationHistory.append(self.mutationPercentage)
                return

        if self.population.eltPctDiff[-1] <= self.pctDiffThresh:
            scaleFactor2 = (self.population.eltPctDiff[-1] - self.pctDiffThresh) / self.population.eltPctDiff[-1]
            if self.originalMutationPercentage * np.exp(scaleFactor2) > self.upperMutationRateLimit:
                setattr(self, 'mutationPercentage', self.upperMutationRateLimit)
                self.mutationHistory.append(self.mutationPercentage)
                return
            if self.originalMutationPercentage * np.exp(scaleFactor2) < self.upperMutationRateLimit:
                setattr(self, 'mutationPercentage', math.floor(self.originalMutationPercentage * np.exp(scaleFactor2)))
                self.mutationHistory.append(self.mutationPercentage)
                return

    def crossover(self):
        self.population.duplicate()
        crossoverNumber = math.floor(self.popSize*self.crossoverPercentage)

        while len(self.population.crossovers) < crossoverNumber:
            #@todo abstract this selection method
            bestStr = tools.selTournament(self.population.clones, 1, int(self.popSize * 0.1), fit_attr='fitness')[0]
            if bestStr not in self.population.crossovers:
                self.population.crossovers.append(bestStr)
                self.population.clones.remove(bestStr)

        for parent1 in self.population.crossovers:
            parent2 = random.sample(set(self.population.crossovers), 1)[0]
            if parent1.hasUndergoneCrossover or parent2.hasUndergoneCrossover:
                continue

            toolbox.mateOnePoint(parent1.torsions, parent2.torsions)
            toolbox.mateOnePoint(parent1.orientations, parent2.orientations)
            toolbox.mateOnePoint(parent1.positions, parent2.positions)

            parent1.hasUndergoneCrossover = True
            parent2.hasUndergoneCrossover = True

            self.population.xoverOffspring.append(parent1)

        for structure in self.population.xoverOffspring:
            structure.hasUndergoneCrossover = False
            del structure.fitness.values

    def mergeCrossovers(self):
        self.population.structures = self.population.structures + self.population.xoverOffspring
        self.population.crossovers = []
        self.population.xoverOffspring = []

    def elitistSelection(self):
        self.population.structures = tools.selBest(self.population.structures, self.popSize)

    def selectMutants(self): #@todo occassionally my have 1 fewer mutants
        mutantNumber = math.floor(self.popSize * self.mutationPercentage)
        print("mutant number")
        print(mutantNumber)
        bestStructure = tools.selBest(self.population.structures, 1)
        self.population.mutants = random.sample(self.population.structures, mutantNumber)

        if bestStructure[0] in self.population.mutants:
            self.population.mutants.remove(bestStructure[0])

        for structure in self.population.mutants:
            self.population.structures.remove(structure)


        # mutantNumber = self.popSize * self.mutationPercentage
        # bestStructure = tools.selBest(self.population.structures, 1)
        #
        # idList = []
        # for structure in self.population.structures:
        #     idList.append(structure.identifier)
        # idList.remove(bestStructure[0].identifier)
        #
        # mutants = random.sample(idList, mutantNumber)
        #
        # for structure in self.population.structures:
        #     if structure.identifier in mutants:
        #         self.population.mutants.append(structure)
        #         self.population.structures.remove(structure)
        #
        # for mutantStructure in self.population.mutants:
        #     del mutantStructure.fitness.values

    def mutation(self):
        for mutant in self.population.mutants:
            tools.mutPolynomialBounded(mutant.torsions, eta=1, low=0, up=360, indpb=1/len(mutant.torsions))
            tools.mutPolynomialBounded(mutant.orientations, eta=1, low=0, up=360, indpb=1/len(mutant.orientations))
            tools.mutPolynomialBounded(mutant.positions, eta=1, low=-0.5, up=1.5, indpb=1/len(mutant.positions))

    def mergeMutants(self):
        self.population.structures = self.population.structures + self.population.mutants
        self.population.mutants = []


    def selection(self):
        return



