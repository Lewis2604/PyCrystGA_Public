from Population import *
from Toolbox import *
from Statistics import *
from DataVisualisation import *
import time
from Config.Config import *
from XRDInterfaces import *
from deap import creator
import sys
import math
from pprint import pprint

class PyCrystGA:
    def __init__(self):

        self.molFile = Config.get('mol_file')
        self.numMol = int(Config.get('num_mol'))
        self.directory = Config.get('working_directory')
        self.popSize = int(Config.get('population_size'))
        self.numGen = int(Config.get('number_of_generations'))
        self.crossoverType = Config.get('crossover_type')
        self.mutationType = Config.get('mutation_type')
        self.XRDInterface = None

        # Consider extracting crossover and mutation classes
        # and letting a parent class delegate
        # e.g. Mutation.mutate(structure, 'type')
        # same for crossover?
        self.crossoverPercentage = Config.get('crossover_rate')
        self.originalCrossoverPercentage = Config.get('crossover_rate')
        self.lowerCrossoverRateLimit = self.originalCrossoverPercentage*.7
        self.upperCrossoverRateLimit = self.originalCrossoverPercentage*1.3

        self.mutationPercentage = Config.get('mutation_rate')
        self.originalMutationPercentage = Config.get('mutation_rate')
        self.lowerMutationRateLimit = self.originalCrossoverPercentage*.7
        self.upperMutationRateLimit = self.originalCrossoverPercentage*1.3

        self.pctDiffThresh = Config.get('percentage_difference_threshold')

        # Consider moving this into its own class
        # Pass a structure to it & let it handle plotting
        self.graphFontSize = Config.get('font_size')
        self.graphLabelSize = Config.get('label_size')
        self.graphFileName = Config.get('file_name')
        self.graphFileNamePctDiff = Config.get('percentage_difference_name')
        self.graphDpi = Config.get('dpi')

        self.crossoverHistory = []
        self.mutationHistory = []

        self.population = None
        self.shouldStop = False
        #@todo figure out how to choose the type of genetic operators that you want,
        # @todo so that you can use the appropriate graph plotting method

        # Do you need all of these booleans?
        self.staticCrossover = True
        self.staticMutation = True

        self.linearDynamicCrossover = False
        self.linearDynamicMutation = False

        self.exponentialDynamicCrossover = False
        self.exponentialDynamicMutation = False

        self.currentGeneration = 0
        self.startTime = None
        self.endTime = None
        self.timeElapsed = None

    def setXrdInterface(self, XRDInterface):
        self.XRDInterface = XRDInterface

    def setDirectory(self, Directory):
        self.directory = Directory

    def setCrossover(self, xover):
        self.crossoverPercentage = xover
        self.originalCrossoverPercentage = xover

    def setMutation(self, mut):
        self.mutationPercentage = mut
        self.originalMutationPercentage = mut

    def setGeneticOperatorType(self):
        # Consider having a dynamic function call
        # or some sort of dict mapping to remove this
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
                                      self.popSize, self.crossoverPercentage, self.mutationPercentage)
        Statistics.createFitnessLog(Statistics())
        self.makePopulation()
        self.setGeneticOperatorType()
        while not self.shouldStop:
            self.currentGeneration += 1
            # self.XRDInterface.makeNewInputFile(self.population, self.directory)
            print("Generation")
            print(self.currentGeneration)
            # self.XRDInterface.makeBatchFile(self.population.structures)
            self.evaluateFitness()
            self.crossover()
            self.evaluateFitness()
            self.elitistSelection()

            #@todo energetic optimisation
            Statistics.recordElitePopulationStatistics(Statistics(), self.directory+'Statistics/',
                                                       self.population, self.currentGeneration)

            self.population.calcEltPercentageDifference()

            self.mutation()


            Statistics.recordMutantPopulationStatistics(Statistics(), self.directory+'Statistics/',
                                                        self.population, self.currentGeneration)

            self.population.calcMutPercentageDifference()

            self.endTime = time.time()

            self.timeElapsed = self.endTime - self.startTime

            print(self.currentGeneration, file=open(self.directory + 'Statistics/' + "Time.txt", "a"))

            print(self.timeElapsed, file=open(self.directory + 'Statistics/' + "Time.txt", "a"))

            self.simpleStoppingCriteria()


        # This could be extracted to a statistics class??
        print("Elite", file=open(self.directory + 'Statistics/' + "pct_diff.txt", "a"))
        print(self.population.eltPctDiff, file=open(self.directory + 'Statistics/' + "pct_diff.txt", "a"))
        print("Mutant", file=open(self.directory + 'Statistics/' + "pct_diff.txt", "a"))
        print(self.population.mutPctDiff, file=open(self.directory + 'Statistics/' + "pct_diff.txt", "a"))
        # Extract to some stats class?
        DataVisualisation.plotGraph(DataVisualisation(), self, self.graphFontSize, self.graphLabelSize,
                                    self.graphFileName, self.directory, self.graphDpi)
        # Again, extract some of this to a stats class?
        if self.linearDynamicCrossover \
                or self.linearDynamicMutation\
                or self.exponentialDynamicCrossover\
                or self.exponentialDynamicMutation:
            DataVisualisation.plotPctDiffGraph(DataVisualisation(), self, self.graphFontSize, self.graphLabelSize,
                                    self.graphFileNamePctDiff, self.directory, self.graphDpi)


    def newStart(self):
        self.startTime = time.time()
        Statistics.writeRunInfoToFile(self.directory+'Statistics/', self.numGen,
                                      self.popSize, self.crossoverPercentage, self.mutationPercentage)
        Statistics.createFitnessLog(Statistics())
        self.makePopulation()
        self.setGeneticOperatorType()
        while not self.shouldStop:
            self.currentGeneration += 1
            print("Generation")
            print(self.currentGeneration)
            if self.currentGeneration == 1:
                self.newEvaluateFitness(self.population.structures)
            self.newCrossover()
            # self.newEvaluateFitness()
            self.elitistSelection()

            # print('elite')
            # pprint(self.population.structures)
            # for structure in self.population.structures:
            #     pprint(structure.positions)

            Statistics.recordElitePopulationStatistics(Statistics(), self.directory+'Statistics/',
                                                       self.population, self.currentGeneration)

            self.population.calcEltPercentageDifference()
            self.newMutation()
            # self.newEvaluateFitness()
            #
            # print('mutants')
            # pprint(self.population.structures)
            # for structure in self.population.structures:
            #     pprint(structure.positions)

            Statistics.recordMutantPopulationStatistics(Statistics(), self.directory+'Statistics/',
                                                        self.population, self.currentGeneration)

            self.population.calcMutPercentageDifference()

            self.endTime = time.time()
            self.timeElapsed = self.endTime - self.startTime

            print(self.currentGeneration, file=open(self.directory + 'Statistics/' + "Time.txt", "a"))
            print(self.timeElapsed, file=open(self.directory + 'Statistics/' + "Time.txt", "a"))

            self.simpleStoppingCriteria()

        # # This could be extracted to a statistics class??
        print("Elite", file=open(self.directory + 'Statistics/' + "pct_diff.txt", "a"))
        print(self.population.eltPctDiff, file=open(self.directory + 'Statistics/' + "pct_diff.txt", "a"))
        print("Mutant", file=open(self.directory + 'Statistics/' + "pct_diff.txt", "a"))
        print(self.population.mutPctDiff, file=open(self.directory + 'Statistics/' + "pct_diff.txt", "a"))
        # Extract to some stats class?
        DataVisualisation.plotGraph(DataVisualisation(), self, self.graphFontSize, self.graphLabelSize,
                                    self.graphFileName, self.directory, self.graphDpi)
        # Again, extract some of this to a stats class?
        if self.linearDynamicCrossover \
                or self.linearDynamicMutation \
                or self.exponentialDynamicCrossover \
                or self.exponentialDynamicMutation:
            DataVisualisation.plotPctDiffGraph(DataVisualisation(), self, self.graphFontSize, self.graphLabelSize,
                                               self.graphFileNamePctDiff, self.directory, self.graphDpi)


    #@todo put stopping criteria here KEEP self.shouldStop = True
    def simpleStoppingCriteria(self):
        # print("Check 1")
        # print(self.population.eltFitnessMax)
        # print(np.std(self.population.eltFitnessMax))
        if self.currentGeneration == self.numGen:
            self.shouldStop = True
            self.endTime = time.time()
        # if self.currentGeneration > self.numGen*0.1:
        #     if np.average(self.population.eltPctDiff[math.floor(-self.numGen*0.1):]) < 1:
        #         print("stop1")
        #         self.shouldStop = True
        #         self.endTime = time.time()
        # if self.currentGeneration > self.numGen*0.1:
        #     print("Elite StdDev")
        #     print(self.population.eltFitnessMax[math.floor(-self.numGen*0.1)])
        #     print(self.population.eltFitnessMax[-1])
        #     diff = self.population.eltFitnessMax[math.floor(-self.numGen*0.1)] - self.population.eltFitnessMax[-1]
        #     print(diff)
        #     if diff == 0:
        #         print("stop2")
        #         self.shouldStop = True
        #         self.endTime = time.time()



            # if np.std(self.population.eltFitnessMax[math.floor(-self.numGen*0.1):]) == 0:
            #     print("stop2")
            #     self.shouldStop = True
            #     self.endTime = time.time()


    # def simpleStoppingCriteria(self):
    #     if self.currentGeneration == self.numGen:
    #         self.shouldStop = True
    #         self.endTime = time.time()

    # def checkStoppingCriteria(self):
    #     self.stoppingCriteria()

    def makePopulation(self):
        # ????
        creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0))

        self.population = Population(self.molFile,
                                     self.numMol,
                                     self.popSize)

        for structure in self.population.structures:
            structure.fitness = creator.FitnessMax()

    def evaluateFitness(self):
        #@todo runs input file
        fitnesses = map(self.XRDInterface.evaluate, self.population.structures)
        for structure, fit in zip(self.population.structures, fitnesses):
            structure.fitness.values = fit
            #@todo can't do this as the rwp list gets longers as the algorithm proceeds
            # structure.rwp.append(1/fit[0])

    def newEvaluateFitness(self, structureList): #@todo RESUME here!!!!!
        print('loop')
        x = 0
        fitnessVals = self.XRDInterface.newEvaluate(
            self.XRDInterface.makeNewInputFile(
                self.population, structureList, self.directory)
        )
        for structure in structureList:
            structure.fitness.values = fitnessVals[x]
            x+=1

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
            newCrossoverPercentage1 = round(self.originalCrossoverPercentage*scaleFactor1, 2)
            setattr(self, 'crossoverPercentage', newCrossoverPercentage1)
            # self.crossoverHistory.append(self.crossoverPercentage)
            return
        if self.population.eltPctDiff[-1] > self.pctDiffThresh:
            scaleFactor2 = self.population.eltPctDiff[-1]/100
            newCrossoverPercentage2 = round(self.originalCrossoverPercentage*(1+scaleFactor2), 2)
            setattr(self, 'crossoverPercentage', newCrossoverPercentage2)
            # self.crossoverHistory.append(self.crossoverPercentage)
            return

    def dynamicMutationLinear(self):
        if self.population.eltPctDiff[-1] > self.pctDiffThresh:
            scaleFactor1 = 1 - ((self.pctDiffThresh - self.population.eltPctDiff[-1])/10) # /100 & *10
            newMutationPercentage1 = round(self.originalMutationPercentage*scaleFactor1, 2)
            setattr(self, 'mutationPercentage', newMutationPercentage1)
            # self.mutationHistory.append(self.mutationPercentage)
            return

        if self.population.eltPctDiff[-1] <= self.pctDiffThresh:
            scaleFactor2 = self.population.eltPctDiff[-1]/100
            newMutationPercentage2 = round(self.originalMutationPercentage*(1+scaleFactor2), 2)
            setattr(self, 'mutationPercentage', newMutationPercentage2)
            # self.mutationHistory.append(self.mutationPercentage)
            return


    def dynamicCrossoverExponential(self):
        #@todo decrease crossover rate
        if self.population.eltPctDiff[-1] <= self.pctDiffThresh:
            #@todo if stagnation has occurred scaleFactor1 = 1
            scaleFactor1 = (self.pctDiffThresh-self.population.eltPctDiff[-1])/self.pctDiffThresh
            #@todo negative exponent decreases the crossover rate
            if self.originalCrossoverPercentage*np.exp(-scaleFactor1) < self.lowerCrossoverRateLimit:
                setattr(self, 'crossoverPercentage', self.lowerCrossoverRateLimit)
                # self.crossoverHistory.append(self.crossoverPercentage)
                return
            if self.originalCrossoverPercentage * np.exp(-scaleFactor1) > self.lowerCrossoverRateLimit:
                setattr(self, 'crossoverPercentage', self.originalCrossoverPercentage*np.exp(-scaleFactor1))
                # self.crossoverHistory.append(self.crossoverPercentage)
                return
        #@todo increase crossover rate
        if self.population.eltPctDiff[-1] > self.pctDiffThresh:
        #@todo maximum value of scaleFactor2 = 1
        #@todo as the pctDiff increases so does scaleFactor2
            scaleFactor2 = (self.population.eltPctDiff[-1]-self.pctDiffThresh)/self.population.eltPctDiff[-1]
            if self.originalCrossoverPercentage*np.exp(scaleFactor2) > self.upperCrossoverRateLimit:
                setattr(self, 'crossoverPercentage', self.upperCrossoverRateLimit)
                # self.crossoverHistory.append(self.crossoverPercentage)
                return
            if self.originalCrossoverPercentage * np.exp(scaleFactor2) < self.upperCrossoverRateLimit:
                setattr(self, 'crossoverPercentage', self.originalCrossoverPercentage*np.exp(scaleFactor2))
                # self.crossoverHistory.append(self.crossoverPercentage)
                return


    def dynamicMutationExponential(self):
        if self.population.eltPctDiff[-1] > self.pctDiffThresh:
            scaleFactor1 = (self.pctDiffThresh - self.population.eltPctDiff[-1]) / self.pctDiffThresh
            if self.originalMutationPercentage * np.exp(-scaleFactor1) < self.lowerMutationRateLimit:
                setattr(self, 'mutationPercentage', self.lowerMutationRateLimit)
                # self.mutationHistory.append(self.mutationPercentage)
                return
            if self.originalMutationPercentage * np.exp(-scaleFactor1) > self.lowerMutationRateLimit:
                setattr(self, 'mutationPercentage', self.originalMutationPercentage * np.exp(-scaleFactor1))
                # self.mutationHistory.append(self.mutationPercentage)
                return
        if self.population.eltPctDiff[-1] <= self.pctDiffThresh:
            scaleFactor2 = (self.population.eltPctDiff[-1] - self.pctDiffThresh) / self.population.eltPctDiff[-1]
            if self.originalMutationPercentage * np.exp(scaleFactor2) > self.upperMutationRateLimit:
                setattr(self, 'mutationPercentage', self.upperMutationRateLimit)
                # self.mutationHistory.append(self.mutationPercentage)
                return
            if self.originalMutationPercentage * np.exp(scaleFactor2) < self.upperMutationRateLimit:
                setattr(self, 'mutationPercentage', self.originalMutationPercentage * np.exp(scaleFactor2))
                # self.mutationHistory.append(self.mutationPercentage)
                return

    def calculateCrossoverPercentage(self):
        if self.linearDynamicCrossover:
            if self.currentGeneration > 1:
                self.dynamicCrossoverLinear()
        if self.exponentialDynamicCrossover:
            if self.currentGeneration > 1:
                self.dynamicCrossoverExponential()

    def crossover(self):
        self.calculateCrossoverPercentage()

        self.crossoverHistory.append(self.crossoverPercentage)

        self.population.duplicate()

        crossoverNumber = self.popSize*self.crossoverPercentage

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

        # self.newEvaluateFitness(self.population.xoverOffspring)

        self.mergeCrossovers()

    def newCrossover(self):
        self.calculateCrossoverPercentage()

        self.crossoverHistory.append(self.crossoverPercentage)

        self.population.duplicate()

        crossoverNumber = self.popSize*self.crossoverPercentage

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

        self.newEvaluateFitness(self.population.xoverOffspring)

        self.mergeCrossovers()

    def mergeCrossovers(self):
        self.population.structures = self.population.structures + self.population.xoverOffspring
        self.population.crossovers = []
        self.population.xoverOffspring = []

    def elitistSelection(self):
        self.population.structures = tools.selBest(self.population.structures, self.popSize)

    def calculateMutationPercentage(self):
        if self.linearDynamicMutation:
            if self.currentGeneration > 1:
                self.dynamicMutationLinear()
        if self.exponentialDynamicMutation:
            if self.currentGeneration > 1:
                self.dynamicMutationExponential()

    def selectMutants(self): #@todo occassionally my have 1 fewer mutants
        self.calculateMutationPercentage()

        self.mutationHistory.append(self.mutationPercentage)

        mutantNumber = int(self.popSize * self.mutationPercentage)
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

        self.selectMutants()

        for mutant in self.population.mutants:
            tools.mutPolynomialBounded(mutant.torsions, eta=1, low=0, up=360, indpb=1/len(mutant.torsions))
            tools.mutPolynomialBounded(mutant.orientations, eta=1, low=0, up=360, indpb=1/len(mutant.orientations))
            tools.mutPolynomialBounded(mutant.positions, eta=1, low=-0.5, up=1.5, indpb=1/len(mutant.positions))

        # for structure in self.population.mutants:
        #     structure.hasUndergoneCrossover = False
        #     del structure.fitness.values

        # self.newEvaluateFitness(self.population.mutants)

        self.mergeMutants()

    def newMutation(self):

        self.selectMutants()

        for mutant in self.population.mutants:
            tools.mutPolynomialBounded(mutant.torsions, eta=1, low=0, up=360, indpb=1/len(mutant.torsions))
            tools.mutPolynomialBounded(mutant.orientations, eta=1, low=0, up=360, indpb=1/len(mutant.orientations))
            tools.mutPolynomialBounded(mutant.positions, eta=1, low=-0.5, up=1.5, indpb=1/len(mutant.positions))

        for structure in self.population.mutants:
            structure.hasUndergoneCrossover = False
            del structure.fitness.values

        self.newEvaluateFitness(self.population.mutants)

        self.mergeMutants()


    def mergeMutants(self):
        self.population.structures = self.population.structures + self.population.mutants
        self.population.mutants = []

    def selection(self):
        return

