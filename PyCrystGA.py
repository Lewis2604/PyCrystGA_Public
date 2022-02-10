import sysconfig

import numpy as np

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

        self.exponentFactor = Config.get('exponent_factor')
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
        self.normFileName = Config.get('file_name_norm')
        self.graphFileNamePctDiff = Config.get('percentage_difference_name')
        self.graphDpi = Config.get('dpi')

        self.crossoverHistory = []
        self.mutationHistory = []

        self.expectedCrossoverHistory = []
        self.expectedMutationHistory = []

        self.expectedOperatorHistory = {}

        self.expectedExponentCrossover = []
        self.expectedExponentMutation = []

        self.spikeGen = []
        self.spikeCount = 0
        self.notSpikeGen = []
        self.notSpikeCount = 0

        self.population = None
        self.shouldStop = False
        #@todo figure out how to choose the type of genetic operators that you want,
        # @todo so that you can use the appropriate graph plotting method

        # Do you need all of these booleans?
        self.staticCrossover = False
        self.staticMutation = False

        self.linearDynamicCrossover = False
        self.linearDynamicMutation = False

        self.exponentialDynamicCrossover = False
        self.exponentialDynamicMutation = False

        self.lowMutHighCross = False
        self.lowMutHighCross1 = False
        self.lowMutHighCross2 = False
        self.lowMutHighCrossSF = False

        self.highMutLowCross = False

        self.exponentOperators = False
        self.exponentOpIMDC = False
        self.exponentOpDMIC = False

        self.ILMDHC_UpDown = False

        self.hasSpiked = False

        self.rollingAvgRange = Config.get('Rolling_Average_Range')
        self.spikeThreshold = Config.get('Spike_Treshold')

        self.ILMDHCSF = Config.get('ILMDHC_scale_factor')

        self.currentGeneration = 0
        self.numEvals = 0

        self.stoppingIters = Config.get('number_iterations_stop')
        self.startTime = None
        self.endTime = None
        self.timeElapsed = None

        self.phase1 = True
        self.phase2 = False
        self.phase3 = False

        self.phaseBoundaries = []

        self.phase1XoverInitial = Config.get('phase1_crossover')
        self.phase2XoverInitial = Config.get('phase2_crossover')
        self.phase3XoverInitial = Config.get('phase3_crossover')

        self.phase1MutInitial = Config.get('phase1_mutation')
        self.phase2MutInitial = Config.get('phase2_mutation')
        self.phase3MutInitial = Config.get('phase3_mutation')

        self.phase1Xover = Config.get('phase1_crossover')

        self.phase2Xover = Config.get('phase2_crossover')
        self.phase2XoverUpper = Config.get('phase2_crossover_upper')
        self.phase2XoverLower = Config.get('phase2_crossover_lower')

        self.phase3Xover = Config.get('phase3_crossover')
        self.phase3XoverUpper = Config.get('phase3_crossover_upper')
        self.phase3XoverLower = Config.get('phase3_crossover_lower')

        self.phase1Mut = Config.get('phase1_mutation')

        self.phase2Mut = Config.get('phase2_mutation')
        self.phase2MutUpper = Config.get('phase2_mutation_upper')
        self.phase2MutLower = Config.get('phase2_mutation_lower')

        self.phase3Mut = Config.get('phase3_mutation')
        self.phase3MutUpper = Config.get('phase3_mutation_upper')
        self.phase3MutLower = Config.get('phase3_mutation_lower')

        self.p2count = 0
        self.p3count = 0

    def setRollingAvgRange(self, rollAvg):
        self.rollingAvgRange = rollAvg

    def setSpikeThreshold(self, spikeThresh):
        self.spikeThreshold = spikeThresh

    def setILMDHCscaleFactor(self, sf):
        self.ILMDHCSF = sf

    def setExponentFactor(self, sf):
        self.exponentFactor = sf

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

    def setOperatorType(self, xType, mutType):
        self.crossoverType = xType
        self.mutationType = mutType

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

        #ILMDHC
        if self.crossoverType and self.mutationType == 3:
            self.lowMutHighCross = True

        if self.crossoverType and self.mutationType == 4:
            self.highMutLowCross = True

        #ILMDHC
        if self.crossoverType and self.mutationType == 5:
            self.lowMutHighCross1 = True

        #ILMDHC
        if self.crossoverType and self.mutationType == 6:
            self.lowMutHighCross2 = True

        #ILMDHC
        if self.crossoverType and self.mutationType == 7:
            self.lowMutHighCrossSF = True

        #exponent GO rates increasing mutation decreasing crossover
        if self.crossoverType and self.mutationType == 8:
            self.exponentOperators = True
            self.exponentOpIMDC = True

        #exponent GO rates decreasing mutation increasing crossover
        if self.crossoverType and self.mutationType == 9:
            self.exponentOperators = True
            self.exponentOpDMIC = True

        if self.crossoverType and self.mutationType == 10:
            self.ILMDHC_UpDown = True




    def setDynamicRates(self, p1xover, p2xover, p2xoverUB, p2xoverLB, p3xover, p3xoverUB, p3xoverLB,
                        p1mut, p2mut, p2mutUB, p2mutLB, p3mut, p3mutUB, p3mutLB):

        self.phase1XoverInitial = p1xover
        self.phase2XoverInitial = p2xover
        self.phase3XoverInitial = p3xover

        self.phase1MutInitial = p1mut
        self.phase2MutInitial = p2mut
        self.phase3MutInitial = p3mut

        self.phase1Xover = p1xover

        self.phase2Xover = p2xover
        self.phase2XoverUpper = p2xoverUB
        self.phase2XoverLower = p2xoverLB

        self.phase3Xover = p3xover
        self.phase3XoverUpper = p3xoverUB
        self.phase3XoverLower = p3xoverLB

        self.phase1Mut = p1mut

        self.phase2Mut = p2mut
        self.phase2MutUpper = p2mutUB
        self.phase2MutLower = p2mutLB

        self.phase3Mut = p3mut
        self.phase3MutUpper = p3mutUB
        self.phase3MutLower = p3mutLB

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
            self.evaluateFitness()

            Statistics.recordMutantPopulationStatistics(Statistics(), self.directory+'Statistics/',
                                                        self.population, self.currentGeneration)

            self.population.calcMutPercentageDifference()

            self.endTime = time.time()

            self.timeElapsed = self.endTime - self.startTime

            print(self.currentGeneration, file=open(self.directory + 'Statistics/' + "Time.txt", "a"))

            print(self.timeElapsed, file=open(self.directory + 'Statistics/' + "Time.txt", "a"))

            # self.simpleStoppingCriteria()

            self.newStop(20)

        Statistics.writeNumEvalsToFile(self.directory+'Statistics/', self.numEvals)

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
        # self.determinePhase()
        Statistics.createFitnessLog(Statistics())
        self.makePopulation()
        self.newEvaluateFitness(self.population.structures)
        self.setGeneticOperatorType()
        Statistics.writeRunInfoToFile(self.directory+'Statistics/', self.numGen,
                                      self.popSize, self.crossoverPercentage, self.mutationPercentage, self)

        # self.crossoverHistory.append(self.phase1XoverInitial)
        # self.mutationHistory.append(self.phase1MutInitial)
        self.calcExpectedOpHist()
        while not self.shouldStop:
            self.currentGeneration += 1
            print("Generation " + str(self.currentGeneration))

            # if self.currentGeneration == 1:
            #     self.newEvaluateFitness(self.population.structures)

            #@todo figure out how to only determine phase if crossover and mutation are dynamic c
            if self.linearDynamicCrossover and self.linearDynamicMutation:
                self.setCrossover(self.phase1XoverInitial)
                self.setMutation(self.phase1MutInitial)
                if self.currentGeneration > 1:
                    print("determine phase")
                    self.determinePhase()

            if self.lowMutHighCross:
                print("ILMDHC")
                self.ILMDHC()
            if self.lowMutHighCross1:
                print("ILMDHC1")
                self.ILMDHC1()
            if self.lowMutHighCross2:
                print("ILMDHC2")
                self.ILMDHC2()
            if self.lowMutHighCrossSF:
                print("ILMDHCSF")
                self.ILMDHCscaleFactor()

            if self.highMutLowCross:
                print("DHMILC")
                self.DHMILC()

            if self.exponentOperators:
                print("exponent operators")
                self.exponentGO()

            if self.ILMDHC_UpDown:
                print("ILMDHCUpDown")
                self.ILMDHCUpDown()

            self.operatorHistory()

            self.newCrossover()

            self.elitistSelection()

            Statistics.recordElitePopulationStatistics(Statistics(), self.directory+'Statistics/',
                                                       self.population, self.currentGeneration)

            self.population.calcEltPercentageDifference()

            self.newMutation()

            Statistics.recordMutantPopulationStatistics(Statistics(), self.directory+'Statistics/',
                                                        self.population, self.currentGeneration)

            self.population.calcMutPercentageDifference()

            self.endTime = time.time()

            self.timeElapsed = self.endTime - self.startTime


            print(self.currentGeneration, file=open(self.directory + 'Statistics/' + "Time.txt", "a"))

            print(self.timeElapsed, file=open(self.directory + 'Statistics/' + "Time.txt", "a"))

            self.newStop(self.stoppingIters)

            # self.simpleStoppingCriteria()

        Statistics.writeNumEvalsToFile(self.directory+'Statistics/', self.numEvals)

        print("Elite", file=open(self.directory + 'Statistics/' + "pct_diff.txt", "a"))
        print(self.population.eltPctDiff, file=open(self.directory + 'Statistics/' + "pct_diff.txt", "a"))
        print("Mutant", file=open(self.directory + 'Statistics/' + "pct_diff.txt", "a"))
        print(self.population.mutPctDiff, file=open(self.directory + 'Statistics/' + "pct_diff.txt", "a"))
        print("Graph plotting")
        DataVisualisation.newPlotGraph(DataVisualisation(), self, self.graphFontSize, self.graphLabelSize,
                                    self.graphFileName, self.directory, self.graphDpi)
        print("done")
        # DataVisualisation.plotNormalisedFitness(DataVisualisation(), self, self.graphFontSize, self.graphLabelSize,
        #                                         self.normFileName, self.directory, self.graphDpi)
#@todo commented this out for now as not using pctdiff to scale operators (literature paper)
        # if self.linearDynamicCrossover \
        #         or self.linearDynamicMutation \
        #         or self.exponentialDynamicCrossover \
        #         or self.exponentialDynamicMutation:
        #     DataVisualisation.plotPctDiffGraph(DataVisualisation(), self, self.graphFontSize, self.graphLabelSize,
        #                                        self.graphFileNamePctDiff, self.directory, self.graphDpi)
    """
    Stopping Criteria
    """

    #@todo put stopping criteria here KEEP self.shouldStop = True
    def simpleStoppingCriteria(self):
        if self.currentGeneration == self.numGen:
            self.shouldStop = True
            self.endTime = time.time()
        if self.currentGeneration > self.numGen*0.1:
            if np.average(self.population.eltPctDiff[math.floor(-self.numGen*0.1):]) < 1:
                print("stop1")
                self.shouldStop = True
                self.endTime = time.time()
        if self.currentGeneration > self.numGen*0.1:
            print("Elite StdDev")
            print(self.population.eltFitnessMax[math.floor(-self.numGen*0.1)])
            print(self.population.eltFitnessMax[-1])
            diff = self.population.eltFitnessMax[math.floor(-self.numGen*0.1)] - self.population.eltFitnessMax[-1]
            print(diff)
            if diff == 0:
                print("stop2")
                self.shouldStop = True
                self.endTime = time.time()

    def maxGenStop(self):
        if self.currentGeneration == self.numGen:
            print("Algorithm has ended")
            self.shouldStop = True
            self.endTime = time.time()

    def newStop(self, numIters):
        print("stop")
        if self.currentGeneration == self.numGen:
            print("stop1")
            self.shouldStop = True
            self.endTime = time.time()

        if self.phase3:
            if self.currentGeneration > numIters:
                print("stop2")
                if self.population.populationAmplitude[len(self.population.populationAmplitude)-numIters] - self.population.populationAmplitude[-1] \
                        and self.population.eltRwpStdDev[len(self.population.eltRwpStdDev)-numIters] - self.population.eltRwpStdDev[-1] < 0.0000000001:
                    print("stop3")
                    self.shouldStop = True
                    self.endTime = time.time()

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

    """
    Make Population
    """

    def makePopulation(self):
        # ????
        creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0))

        self.population = Population(self.molFile,
                                     self.numMol,
                                     self.popSize)

        for structure in self.population.structures:
            structure.fitness = creator.FitnessMax()

    """
    Evaluate Fitness
    """

    def evaluateFitness(self):
        #@todo runs input file
        fitnesses = map(self.XRDInterface.evaluate, self.population.structures)
        for structure, fit in zip(self.population.structures, fitnesses):
            structure.fitness.values = fit
            self.numEvals+=1
            #@todo can't do this as the rwp list gets longers as the algorithm proceeds
            # structure.rwp.append(1/fit[0])

    def newEvaluateFitness(self, structureList): #@todo RESUME here!!!!!
        # print('loop')
        if len(structureList) >= 1:
            x = 0
            fitnessVals = self.XRDInterface.newEvaluate(
                self.XRDInterface.makeNewInputFile(
                    self.population, structureList, self.directory)
            )

            for structure in structureList:
                structure.fitness.values = fitnessVals[x]
                self.numEvals+=1
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

    """
    Crossover
    """

    def calculateCrossoverPercentage(self):
        if self.linearDynamicCrossover:
            if self.currentGeneration > 1:
                self.dynamicCrossoverLinear()
        if self.exponentialDynamicCrossover:
            if self.currentGeneration > 1:
                self.dynamicCrossoverExponential()


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
        # self.calculateCrossoverPercentage()
        if not self.exponentOperators:
            self.crossoverHistory.append(self.crossoverPercentage)

        self.population.duplicate()

        crossoverNumber = self.popSize*self.crossoverPercentage

        while len(self.population.crossovers) < crossoverNumber:
            #@todo abstract this selection method
            bestStr = tools.selTournament(self.population.clones, 1, int(self.popSize * 0.1), fit_attr='fitness')[0]
            if bestStr not in self.population.crossovers:
                self.population.crossovers.append(bestStr)
                self.population.clones.remove(bestStr)

        if len(self.population.crossovers) > 0:
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

    """
    Mutation
    """

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


    def calculateMutationPercentage(self):
            if self.linearDynamicMutation:
                if self.currentGeneration > 1:
                    self.dynamicMutationLinear()
            if self.exponentialDynamicMutation:
                if self.currentGeneration > 1:
                    self.dynamicMutationExponential()

    def selectMutants(self): #@todo occassionally my have 1 fewer mutants
        # self.calculateMutationPercentage()
        if not self.exponentOperators:
            self.mutationHistory.append(self.mutationPercentage)

        mutantNumber = int(self.popSize * self.mutationPercentage)
        # print(self.mutationPercentage)
        # print(mutantNumber)
        bestStructure = tools.selBest(self.population.structures, 1)
        self.population.mutants = random.sample(self.population.structures, mutantNumber)

        if bestStructure[0] in self.population.mutants:
            self.population.mutants.remove(bestStructure[0])

        for structure in self.population.mutants:
            self.population.structures.remove(structure)


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


    def pctNewMutation(self):
        # self.determinePhase()

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

    """
    Dynamic Operators
    """

    def determinePhase(self):
        print("Phase determination")
        ei = 1
        ki = 50
        ed = 0.001
        kd = 150
        eph2 = 0.001
        eph3 = 0.000001

        # self.phase1 = False
        # self.phase2 = False
        # self.phase3 = False

        self.population.populationAmplitude.append(np.abs(self.population.eltFitnessMin[-1] - self.population.eltFitnessMax[-1]))
        if self.phase1:
            print("Phase 1")
            self.setCrossover(self.phase1Xover)
            self.setMutation(self.phase1Mut)
            # self.crossoverHistory.append(self.crossoverPercentage)
            # self.mutationHistory.append(self.mutationPercentage)
            if self.population.eltRwpStdDev[-1] and self.population.populationAmplitude[-1] < \
                    ei and self.currentGeneration > ki:
                self.phase1 = False
                self.phase2 = True
                self.phaseBoundaries.append(self.currentGeneration)

        if self.phase2:
            print("Phase 2")
            # print(self.p2count)
            if self.p2count < 1:
                self.setCrossover(self.phase2XoverInitial)
                self.setMutation(self.phase2MutInitial)
                self.p2count+=1
            else:
                if self.population.populationAmplitude[-1] - \
                        self.population.populationAmplitude[len(self.population.populationAmplitude)-1] < eph2:

                    self.phase2Xover += 0.01
                    self.phase2Mut += 0.01

                if self.population.populationAmplitude[-1] - \
                        self.population.populationAmplitude[len(self.population.populationAmplitude)-1] > eph2:

                    self.phase2Xover -= 0.01
                    self.phase2Mut -= 0.01

                if self.phase2Xover > self.phase2XoverUpper:
                    self.setCrossover(self.phase2XoverUpper)

                if self.phase2Xover < self.phase2XoverLower:
                    self.setCrossover(self.phase2XoverLower)

                if self.phase2XoverLower <= self.phase2Xover <= self.phase2XoverUpper:
                    self.setCrossover(self.phase2Xover)

                if self.phase2Mut > self.phase2MutUpper:
                    self.setMutation(self.phase2MutUpper)

                if self.phase2Mut < self.phase2MutLower:
                    self.setMutation(self.phase2MutLower)

                if self.phase2MutLower <= self.phase2Mut <= self.phase2MutUpper:
                    self.setMutation(self.phase2Mut)

                # self.crossoverHistory.append(self.crossoverPercentage)
                # self.mutationHistory.append(self.mutationPercentage)

                if self.population.eltRwpStdDev[-1] and self.population.populationAmplitude[-1] < \
                        ed and self.currentGeneration > kd:
                    self.phase2 = False
                    self.phase3 = True
                    self.phaseBoundaries.append(self.currentGeneration)

        #@todo phase 3
        #@todo add upper and lower limits
        if self.phase3:
            print("Phase 3")
            # print(self.p3count)
            if self.p3count < 1:
                self.setCrossover(self.phase3XoverInitial)
                self.setMutation(self.phase3MutInitial)
                self.p3count+=1
            else:
                if self.population.eltFitnessMax[-1] - \
                        self.population.populationAmplitude[len(self.population.populationAmplitude)-1] < eph3:
                    self.phase3Xover += 0.01
                    self.phase3Mut += 0.01

                if self.population.eltFitnessMax[-1] - \
                        self.population.populationAmplitude[len(self.population.populationAmplitude)-1] > eph3:
                    self.phase3Xover -= 0.01
                    self.phase3Mut -= 0.01

                if self.phase3Xover > self.phase3XoverUpper:
                    self.setCrossover(self.phase3XoverUpper)

                if self.phase3Xover < self.phase3XoverLower:
                    self.setCrossover(self.phase3XoverLower)

                if self.phase3XoverLower <= self.phase3Xover <= self.phase3XoverUpper:
                    self.setCrossover(self.phase3Xover)

                if self.phase3Mut > self.phase3MutUpper:
                    self.setMutation(self.phase3MutUpper)

                if self.phase3Mut < self.phase3MutLower:
                    self.setMutation(self.phase3MutLower)

                if self.phase3MutLower <= self.phase3Mut <= self.phase3MutUpper:
                    self.setMutation(self.phase3Mut)


    def ILMDHC(self):
        if self.currentGeneration == 1:
            self.setMutation(0)
            self.setCrossover(1)
        else:
            mutrate = self.currentGeneration/self.numGen
            xrate = 1 - mutrate
            self.setMutation(mutrate)
            self.setCrossover(xrate)


    def ILMDHC1(self):
        #@todo increases the mutation rate at a faster rate, lowers crossover rate at a faster rate
        if self.currentGeneration == 1:
            self.setMutation(0)
            self.setCrossover(1)

            expectedMutRate = 0
            expectedXoverRate = 1 - expectedMutRate

            self.expectedMutationHistory.append(expectedMutRate)
            self.expectedCrossoverHistory.append(expectedXoverRate)

        else:
            expectedMutRate = self.currentGeneration/self.numGen
            expectedXoverRate = 1 - expectedMutRate
            self.expectedMutationHistory.append(expectedMutRate)
            self.expectedCrossoverHistory.append(expectedXoverRate)
            stdDevSortList = sorted(self.population.eltRwpStdDev) #@todo orders from smallest to largest
            # print(self.population.eltRwpStdDev)
            # print(stdDevSortList)

            stdDevRange = stdDevSortList[-1] - stdDevSortList[0]
            # print(stdDevRange)

            if stdDevRange != 0:
                stdDevMinusMin = self.population.eltRwpStdDev[-1]\
                                 -stdDevSortList[0]

                stdDevNorm = stdDevMinusMin/stdDevRange

                mutrate = (self.currentGeneration/self.numGen)*(stdDevNorm+1)
                xrate = 1 - mutrate

                if mutrate <= 1:
                    self.setMutation(mutrate)
                    self.setCrossover(xrate)
                else:
                    self.setMutation(1)
                    self.setCrossover(0)


    def ILMDHC2(self):
        #@todo increases the mutation rate at a slower rate, lowers crossover rate at a slower rate
        if self.currentGeneration == 1:
            self.setMutation(0)
            self.setCrossover(1)

            expectedMutRate = 0
            expectedXoverRate = 1 - expectedMutRate

            self.expectedMutationHistory.append(expectedMutRate)
            self.expectedCrossoverHistory.append(expectedXoverRate)

        else:
            expectedMutRate = self.currentGeneration/self.numGen
            expectedXoverRate = 1 - expectedMutRate
            self.expectedMutationHistory.append(expectedMutRate)
            self.expectedCrossoverHistory.append(expectedXoverRate)

            stdDevSortList = sorted(self.population.eltRwpStdDev) #@todo orders from smallest to largest
            # print(self.population.eltRwpStdDev)
            # print(stdDevSortList)

            stdDevRange = stdDevSortList[-1] - stdDevSortList[0]
            # print(stdDevRange)

            if stdDevRange != 0:
                stdDevMinusMin = self.population.eltRwpStdDev[-1] \
                                 -stdDevSortList[0]

                stdDevNorm = stdDevMinusMin/stdDevRange

                mutrate = (self.currentGeneration/self.numGen)*(stdDevNorm)
                xrate = 1 - mutrate

                if mutrate <= 1:
                    self.setMutation(mutrate)
                    self.setCrossover(xrate)
                else:
                    self.setMutation(1)
                    self.setCrossover(0)

    def exponentGO(self):
        #@todo increases the mutation rate at a faster rate, lowers crossover rate at a faster rate
        if self.exponentOpIMDC:
            count = 1
            while len(self.expectedExponentMutation) <= self.numGen:
                self.expectedExponentMutation.append(math.exp((self.exponentFactor*count)/(self.numGen)))
                count +=1

            normalisedMutRate = (self.expectedExponentMutation[self.currentGeneration]-self.expectedExponentMutation[0])/\
                                (self.expectedExponentMutation[-1]-self.expectedExponentMutation[0])

            xOverRate = 1 - normalisedMutRate

            self.setMutation(normalisedMutRate)
            self.setCrossover(xOverRate)

            self.mutationHistory.append(normalisedMutRate)
            self.crossoverHistory.append(xOverRate)

        if self.exponentOpDMIC:
            count = 1
            while len(self.expectedExponentCrossover) <= self.numGen:
                self.expectedExponentCrossover.append(math.exp((self.exponentFactor*count)/(self.numGen)))
                count += 1

            normalisedXOverRate = (self.expectedExponentCrossover[self.currentGeneration]-self.expectedExponentCrossover[0])/ \
                                  (self.expectedExponentCrossover[-1]-self.expectedExponentCrossover[0])

            mutRate = 1 - normalisedXOverRate

            self.setMutation(mutRate)
            self.setCrossover(normalisedXOverRate)

            self.mutationHistory.append(mutRate)
            self.crossoverHistory.append(normalisedXOverRate)


    def ILMDHCscaleFactor(self):
        if self.currentGeneration == 1:
            self.setMutation(0)
            self.setCrossover(1)

            expectedMutRate = 0
            expectedXoverRate = 1 - expectedMutRate

            self.expectedMutationHistory.append(expectedMutRate)
            self.expectedCrossoverHistory.append(expectedXoverRate)

        else:
            expectedMutRate = self.currentGeneration/self.numGen
            expectedXoverRate = 1 - expectedMutRate
            self.expectedMutationHistory.append(expectedMutRate)
            self.expectedCrossoverHistory.append(expectedXoverRate)

            mutrate = self.ILMDHCSF*(self.currentGeneration/self.numGen)
            xrate = 1 - mutrate
            if mutrate > 1:
                self.setMutation(1)
            if xrate < 0:
                self.setCrossover(0)
            else:
                self.setMutation(mutrate)
                self.setCrossover(xrate)


    def DHMILC(self):
        if self.currentGeneration == 1:
            self.setMutation(1)
            self.setCrossover(0)
        else:
            xrate = self.currentGeneration/self.numGen
            mutrate = 1 - xrate
            self.setCrossover(xrate)
            self.setMutation(mutrate)


    def ILMDHCUpDown(self):

        # rollingAvgRange = 10
        # spikeThreshold = 1

        if self.currentGeneration == 1:
            self.setMutation(self.expectedMutationHistory[0])
            self.setCrossover(self.expectedCrossoverHistory[0])

        if self.currentGeneration > 1:
            if self.currentGeneration < self.rollingAvgRange:
                self.setMutation(self.expectedMutationHistory[self.currentGeneration-1])
                self.setCrossover(self.expectedCrossoverHistory[self.currentGeneration-1])

            if self.currentGeneration > self.rollingAvgRange:
                print("here1")
                """
                Calculate the rolling average for eltRwpStdDev
                this tells use the variation in fitness of the fittest
                individual amongst the population 
                """
                rollingAvg = np.mean(self.population.eltRwpStdDev[-self.rollingAvgRange:])

                self.population.eltRwpStdDevRollAvg.append(rollingAvg)

                pprint(self.population.eltRwpStdDevRollAvg)

            # if len(self.population.eltRwpStdDevRollAvg) > rollingAvgRange:
            #     print("here2")
            #     """
            #     Calculate standard deviation of the rolling average list
            #     *** why???? ***
            #     This will tell us if the fittest individual has remained the same
            #     for a given number of generations
            #     """
            #     stdDevRollingAvg = np.std(self.population.eltRwpStdDevRollAvg[-rollingAvgRange:])
            #     self.population.eltRwpStdDevRollAvgStdDev.append(stdDevRollingAvg)
            #
            #     pprint(self.population.eltRwpStdDevRollAvgStdDev)

            # if stdDevRollingAvg <= spikeThreshold:
            #     if self.population.eltRwpStdDevRollAvg[-1] <= spikeThreshold:
                if not self.hasSpiked:
                    """
                    Stagnation need to continue iterating over expected operator history
                    as the mutation rate needs to be increased 
                    """
                    print("Here4")

                    # self.notSpikeGen.clear()
                    #
                    # self.notStagCount = 0
                    #
                    # while len(self.spikeGen) < 1:
                    #     self.spikeGen.append(self.currentGeneration-1)

                    xOverVal = self.expectedOperatorHistory["Gen" + str(self.currentGeneration-1)]["CR"]
                    mutVal = self.expectedOperatorHistory["Gen" + str(self.currentGeneration-1)]["MR"]

                    self.setCrossover(xOverVal)
                    self.setMutation(mutVal)

                """
                Need to lower the mutation rate again following the spike in standard deviation 
                """

                # if stdDevRollingAvg > spikeThreshold:
                if not self.hasSpiked:
                    if self.population.eltRwpStdDevRollAvg[-1] > self.spikeThreshold:
                        self.hasSpiked = True
                    """
                    Introduction of lots of new genetic information need to 
                    lower the mutation rate and increase the crossover rate
                    """
                if self.hasSpiked:
                    while len(self.spikeGen) < 1:
                        # if len(self.spikeGen) == 1:
                        #     self.notSpikeGen.append(self.spikeGen[0])
                        if len(self.spikeGen) == 0:
                            self.spikeGen.append(self.currentGeneration-1)

                    # self.spikeGen.clear()
                    spikeGenBackwards = self.spikeGen[0]-self.spikeCount
                    if spikeGenBackwards >= 0:
                        xOverRate = self.expectedOperatorHistory["Gen" + str(spikeGenBackwards)]["CR"]
                        mutRate = self.expectedOperatorHistory["Gen" + str(spikeGenBackwards)]["MR"]
                        self.setCrossover(xOverRate)
                        self.setMutation(mutRate)
                    else:
                        xOverRate = self.expectedOperatorHistory["Gen" + str(0)]["CR"]
                        mutRate = self.expectedOperatorHistory["Gen" + str(0)]["MR"]
                        self.setCrossover(xOverRate)
                        self.setMutation(mutRate)

                    print("Here5")

                    # if 0 <= xOverRate <= 1:
                    #     self.setCrossover(xOverRate)
                    # if xOverRate > 1:
                    #     self.setCrossover(1)
                    # if xOverRate < 0:
                    #     self.setCrossover(0)
                    #
                    # if 0 <= mutRate <= 1:
                    #     self.setMutation(mutRate)
                    # if mutRate > 1:
                    #     self.setMutation(1)
                    # if mutRate < 0:
                    #     self.setMutation(0)

                    self.spikeCount += 1

    def calcExpectedOpHist(self):
        if self.ILMDHC_UpDown:
            for i in range(self.numGen):
                if i == 0:
                    expectedMutRate = 0
                    expectedXoverRate = 1 - expectedMutRate

                    self.expectedMutationHistory.append(expectedMutRate)
                    self.expectedCrossoverHistory.append(expectedXoverRate)

                    self.expectedOperatorHistory["Gen" + str(0)] = {}
                    self.expectedOperatorHistory["Gen" + str(0)]["CR"] = expectedXoverRate
                    self.expectedOperatorHistory["Gen" + str(0)]["MR"] = expectedMutRate


                else:
                    expectedMutRate = i/self.numGen
                    expectedXoverRate = 1 - expectedMutRate

                    self.expectedMutationHistory.append(expectedMutRate)
                    self.expectedCrossoverHistory.append(expectedXoverRate)

                    self.expectedOperatorHistory["Gen" + str(i)] = {}
                    self.expectedOperatorHistory["Gen" + str(i)]["CR"] = expectedXoverRate
                    self.expectedOperatorHistory["Gen" + str(i)]["MR"] = expectedMutRate


    def operatorHistory(self):
        f = open(self.directory + "Operator History.txt", "a")

        if self.phase1:
            print("Phase 1", file=f)

        if self.phase2:
            print("Phase 2", file=f)

        if self.phase3:
            print("Phase 3", file=f)

        print("Current Generation: " + str(self.currentGeneration), file=f)
        print("Crossover Rate: " + str(self.crossoverPercentage), file=f)
        print("Mutation Rate: " + str(self.mutationPercentage), file=f)
        return

    # def selection(self):
    #     return


    # def dynamicCrossoverExponential(self):
    #     #@todo decrease crossover rate
    #     if self.population.eltPctDiff[-1] <= self.pctDiffThresh:
    #         #@todo if stagnation has occurred scaleFactor1 = 1
    #         scaleFactor1 = (self.pctDiffThresh-self.population.eltPctDiff[-1])/self.pctDiffThresh
    #         #@todo negative exponent decreases the crossover rate
    #         if self.originalCrossoverPercentage*np.exp(-scaleFactor1) < self.lowerCrossoverRateLimit:
    #             setattr(self, 'crossoverPercentage', self.lowerCrossoverRateLimit)
    #             # self.crossoverHistory.append(self.crossoverPercentage)
    #             return
    #         if self.originalCrossoverPercentage * np.exp(-scaleFactor1) > self.lowerCrossoverRateLimit:
    #             setattr(self, 'crossoverPercentage', self.originalCrossoverPercentage*np.exp(-scaleFactor1))
    #             # self.crossoverHistory.append(self.crossoverPercentage)
    #             return
    #     #@todo increase crossover rate
    #     if self.population.eltPctDiff[-1] > self.pctDiffThresh:
    #     #@todo maximum value of scaleFactor2 = 1
    #     #@todo as the pctDiff increases so does scaleFactor2
    #         scaleFactor2 = (self.population.eltPctDiff[-1]-self.pctDiffThresh)/self.population.eltPctDiff[-1]
    #         if self.originalCrossoverPercentage*np.exp(scaleFactor2) > self.upperCrossoverRateLimit:
    #             setattr(self, 'crossoverPercentage', self.upperCrossoverRateLimit)
    #             # self.crossoverHistory.append(self.crossoverPercentage)
    #             return
    #         if self.originalCrossoverPercentage * np.exp(scaleFactor2) < self.upperCrossoverRateLimit:
    #             setattr(self, 'crossoverPercentage', self.originalCrossoverPercentage*np.exp(scaleFactor2))
    #             # self.crossoverHistory.append(self.crossoverPercentage)
    #             return


    # def dynamicMutationExponential(self):
    #     if self.population.eltPctDiff[-1] > self.pctDiffThresh:
    #         scaleFactor1 = (self.pctDiffThresh - self.population.eltPctDiff[-1]) / self.pctDiffThresh
    #         if self.originalMutationPercentage * np.exp(-scaleFactor1) < self.lowerMutationRateLimit:
    #             setattr(self, 'mutationPercentage', self.lowerMutationRateLimit)
    #             # self.mutationHistory.append(self.mutationPercentage)
    #             return
    #         if self.originalMutationPercentage * np.exp(-scaleFactor1) > self.lowerMutationRateLimit:
    #             setattr(self, 'mutationPercentage', self.originalMutationPercentage * np.exp(-scaleFactor1))
    #             # self.mutationHistory.append(self.mutationPercentage)
    #             return
    #     if self.population.eltPctDiff[-1] <= self.pctDiffThresh:
    #         scaleFactor2 = (self.population.eltPctDiff[-1] - self.pctDiffThresh) / self.population.eltPctDiff[-1]
    #         if self.originalMutationPercentage * np.exp(scaleFactor2) > self.upperMutationRateLimit:
    #             setattr(self, 'mutationPercentage', self.upperMutationRateLimit)
    #             # self.mutationHistory.append(self.mutationPercentage)
    #             return
    #         if self.originalMutationPercentage * np.exp(scaleFactor2) < self.upperMutationRateLimit:
    #             setattr(self, 'mutationPercentage', self.originalMutationPercentage * np.exp(scaleFactor2))
    #             # self.mutationHistory.append(self.mutationPercentage)
    #             return

    # def calculateCrossoverPercentage(self):
    #     if self.linearDynamicCrossover:
    #         if self.currentGeneration > 1:
    #             self.dynamicCrossoverLinear()
    #     if self.exponentialDynamicCrossover:
    #         if self.currentGeneration > 1:
    #             self.dynamicCrossoverExponential()

    # def crossover(self):
    #     self.calculateCrossoverPercentage()
    #
    #     self.crossoverHistory.append(self.crossoverPercentage)
    #
    #     self.population.duplicate()
    #
    #     crossoverNumber = self.popSize*self.crossoverPercentage
    #
    #     while len(self.population.crossovers) < crossoverNumber:
    #         #@todo abstract this selection method
    #         bestStr = tools.selTournament(self.population.clones, 1, int(self.popSize * 0.1), fit_attr='fitness')[0]
    #         if bestStr not in self.population.crossovers:
    #             self.population.crossovers.append(bestStr)
    #             self.population.clones.remove(bestStr)
    #
    #     for parent1 in self.population.crossovers:
    #         parent2 = random.sample(set(self.population.crossovers), 1)[0]
    #         if parent1.hasUndergoneCrossover or parent2.hasUndergoneCrossover:
    #             continue
    #
    #         toolbox.mateOnePoint(parent1.torsions, parent2.torsions)
    #         toolbox.mateOnePoint(parent1.orientations, parent2.orientations)
    #         toolbox.mateOnePoint(parent1.positions, parent2.positions)
    #
    #         parent1.hasUndergoneCrossover = True
    #         parent2.hasUndergoneCrossover = True
    #
    #         self.population.xoverOffspring.append(parent1)
    #
    #     for structure in self.population.xoverOffspring:
    #         structure.hasUndergoneCrossover = False
    #         del structure.fitness.values
    #
    #     # self.newEvaluateFitness(self.population.xoverOffspring)
    #
    #     self.mergeCrossovers()
    #
    # def newCrossover(self):
    #     # self.calculateCrossoverPercentage()
    #     if not self.exponentOperators:
    #         self.crossoverHistory.append(self.crossoverPercentage)
    #
    #     self.population.duplicate()
    #
    #     crossoverNumber = self.popSize*self.crossoverPercentage
    #
    #     while len(self.population.crossovers) < crossoverNumber:
    #         #@todo abstract this selection method
    #         bestStr = tools.selTournament(self.population.clones, 1, int(self.popSize * 0.1), fit_attr='fitness')[0]
    #         if bestStr not in self.population.crossovers:
    #             self.population.crossovers.append(bestStr)
    #             self.population.clones.remove(bestStr)
    #
    #     if len(self.population.crossovers) > 0:
    #         for parent1 in self.population.crossovers:
    #             parent2 = random.sample(set(self.population.crossovers), 1)[0]
    #             if parent1.hasUndergoneCrossover or parent2.hasUndergoneCrossover:
    #                 continue
    #
    #             toolbox.mateOnePoint(parent1.torsions, parent2.torsions)
    #             toolbox.mateOnePoint(parent1.orientations, parent2.orientations)
    #             toolbox.mateOnePoint(parent1.positions, parent2.positions)
    #
    #             parent1.hasUndergoneCrossover = True
    #             parent2.hasUndergoneCrossover = True
    #
    #             self.population.xoverOffspring.append(parent1)
    #
    #         for structure in self.population.xoverOffspring:
    #             structure.hasUndergoneCrossover = False
    #             del structure.fitness.values
    #
    #         self.newEvaluateFitness(self.population.xoverOffspring)
    #
    #         self.mergeCrossovers()

    # def determinePhase(self):
    #     print("Phase determination")
    #     ei = 1
    #     ki = 50
    #     ed = 0.001
    #     kd = 150
    #     eph2 = 0.001
    #     eph3 = 0.000001
    #
    #     # self.phase1 = False
    #     # self.phase2 = False
    #     # self.phase3 = False
    #
    #     self.population.populationAmplitude.append(np.abs(self.population.eltFitnessMin[-1] - self.population.eltFitnessMax[-1]))
    #     if self.phase1:
    #         print("Phase 1")
    #         self.setCrossover(self.phase1Xover)
    #         self.setMutation(self.phase1Mut)
    #         # self.crossoverHistory.append(self.crossoverPercentage)
    #         # self.mutationHistory.append(self.mutationPercentage)
    #         if self.population.eltRwpStdDev[-1] and self.population.populationAmplitude[-1] < \
    #                 ei and self.currentGeneration > ki:
    #             self.phase1 = False
    #             self.phase2 = True
    #             self.phaseBoundaries.append(self.currentGeneration)
    #
    #     if self.phase2:
    #         print("Phase 2")
    #         # print(self.p2count)
    #         if self.p2count < 1:
    #             self.setCrossover(self.phase2XoverInitial)
    #             self.setMutation(self.phase2MutInitial)
    #             self.p2count+=1
    #         else:
    #             if self.population.populationAmplitude[-1] - \
    #                     self.population.populationAmplitude[len(self.population.populationAmplitude)-1] < eph2:
    #
    #                 self.phase2Xover += 0.01
    #                 self.phase2Mut += 0.01
    #
    #             if self.population.populationAmplitude[-1] - \
    #                     self.population.populationAmplitude[len(self.population.populationAmplitude)-1] > eph2:
    #
    #                 self.phase2Xover -= 0.01
    #                 self.phase2Mut -= 0.01
    #
    #             if self.phase2Xover > self.phase2XoverUpper:
    #                 self.setCrossover(self.phase2XoverUpper)
    #
    #             if self.phase2Xover < self.phase2XoverLower:
    #                 self.setCrossover(self.phase2XoverLower)
    #
    #             if self.phase2XoverLower <= self.phase2Xover <= self.phase2XoverUpper:
    #                 self.setCrossover(self.phase2Xover)
    #
    #             if self.phase2Mut > self.phase2MutUpper:
    #                 self.setMutation(self.phase2MutUpper)
    #
    #             if self.phase2Mut < self.phase2MutLower:
    #                 self.setMutation(self.phase2MutLower)
    #
    #             if self.phase2MutLower <= self.phase2Mut <= self.phase2MutUpper:
    #                 self.setMutation(self.phase2Mut)
    #
    #             # self.crossoverHistory.append(self.crossoverPercentage)
    #             # self.mutationHistory.append(self.mutationPercentage)
    #
    #             if self.population.eltRwpStdDev[-1] and self.population.populationAmplitude[-1] < \
    #                     ed and self.currentGeneration > kd:
    #                 self.phase2 = False
    #                 self.phase3 = True
    #                 self.phaseBoundaries.append(self.currentGeneration)
    #
    #     #@todo phase 3
    #     #@todo add upper and lower limits
    #     if self.phase3:
    #         print("Phase 3")
    #         # print(self.p3count)
    #         if self.p3count < 1:
    #             self.setCrossover(self.phase3XoverInitial)
    #             self.setMutation(self.phase3MutInitial)
    #             self.p3count+=1
    #         else:
    #             if self.population.eltFitnessMax[-1] - \
    #                     self.population.populationAmplitude[len(self.population.populationAmplitude)-1] < eph3:
    #                 self.phase3Xover += 0.01
    #                 self.phase3Mut += 0.01
    #
    #             if self.population.eltFitnessMax[-1] - \
    #                     self.population.populationAmplitude[len(self.population.populationAmplitude)-1] > eph3:
    #                 self.phase3Xover -= 0.01
    #                 self.phase3Mut -= 0.01
    #
    #             if self.phase3Xover > self.phase3XoverUpper:
    #                 self.setCrossover(self.phase3XoverUpper)
    #
    #             if self.phase3Xover < self.phase3XoverLower:
    #                 self.setCrossover(self.phase3XoverLower)
    #
    #             if self.phase3XoverLower <= self.phase3Xover <= self.phase3XoverUpper:
    #                 self.setCrossover(self.phase3Xover)
    #
    #             if self.phase3Mut > self.phase3MutUpper:
    #                 self.setMutation(self.phase3MutUpper)
    #
    #             if self.phase3Mut < self.phase3MutLower:
    #                 self.setMutation(self.phase3MutLower)
    #
    #             if self.phase3MutLower <= self.phase3Mut <= self.phase3MutUpper:
    #                 self.setMutation(self.phase3Mut)


    # self.crossoverHistory.append(self.crossoverPercentage)
    # self.mutationHistory.append(self.mutationPercentage)

    # def mergeCrossovers(self):
    #     self.population.structures = self.population.structures + self.population.xoverOffspring
    #     self.population.crossovers = []
    #     self.population.xoverOffspring = []
    #
    # def elitistSelection(self):
    #     self.population.structures = tools.selBest(self.population.structures, self.popSize)

    # def calculateMutationPercentage(self):
    #     if self.linearDynamicMutation:
    #         if self.currentGeneration > 1:
    #             self.dynamicMutationLinear()
    #     if self.exponentialDynamicMutation:
    #         if self.currentGeneration > 1:
    #             self.dynamicMutationExponential()
    #
    # def selectMutants(self): #@todo occassionally my have 1 fewer mutants
    #     # self.calculateMutationPercentage()
    #     if not self.exponentOperators:
    #         self.mutationHistory.append(self.mutationPercentage)
    #
    #     mutantNumber = int(self.popSize * self.mutationPercentage)
    #     # print(self.mutationPercentage)
    #     # print(mutantNumber)
    #     bestStructure = tools.selBest(self.population.structures, 1)
    #     self.population.mutants = random.sample(self.population.structures, mutantNumber)
    #
    #     if bestStructure[0] in self.population.mutants:
    #         self.population.mutants.remove(bestStructure[0])
    #
    #     for structure in self.population.mutants:
    #         self.population.structures.remove(structure)
    #
    #
    # def mutation(self):
    #     self.selectMutants()
    #
    #     for mutant in self.population.mutants:
    #         tools.mutPolynomialBounded(mutant.torsions, eta=1, low=0, up=360, indpb=1/len(mutant.torsions))
    #         tools.mutPolynomialBounded(mutant.orientations, eta=1, low=0, up=360, indpb=1/len(mutant.orientations))
    #         tools.mutPolynomialBounded(mutant.positions, eta=1, low=-0.5, up=1.5, indpb=1/len(mutant.positions))
    #
    #     # for structure in self.population.mutants:
    #     #     structure.hasUndergoneCrossover = False
    #     #     del structure.fitness.values
    #
    #     # self.newEvaluateFitness(self.population.mutants)
    #
    #     self.mergeMutants()
    #
    #
    # def newMutation(self):
    #
    #     self.selectMutants()
    #
    #     for mutant in self.population.mutants:
    #         tools.mutPolynomialBounded(mutant.torsions, eta=1, low=0, up=360, indpb=1/len(mutant.torsions))
    #         tools.mutPolynomialBounded(mutant.orientations, eta=1, low=0, up=360, indpb=1/len(mutant.orientations))
    #         tools.mutPolynomialBounded(mutant.positions, eta=1, low=-0.5, up=1.5, indpb=1/len(mutant.positions))
    #
    #     for structure in self.population.mutants:
    #         structure.hasUndergoneCrossover = False
    #         del structure.fitness.values
    #
    #     self.newEvaluateFitness(self.population.mutants)
    #
    #     self.mergeMutants()
    #
    #
    # def pctNewMutation(self):
    #     # self.determinePhase()
    #
    #     self.selectMutants()
    #
    #     for mutant in self.population.mutants:
    #         tools.mutPolynomialBounded(mutant.torsions, eta=1, low=0, up=360, indpb=1/len(mutant.torsions))
    #         tools.mutPolynomialBounded(mutant.orientations, eta=1, low=0, up=360, indpb=1/len(mutant.orientations))
    #         tools.mutPolynomialBounded(mutant.positions, eta=1, low=-0.5, up=1.5, indpb=1/len(mutant.positions))
    #
    #     for structure in self.population.mutants:
    #         structure.hasUndergoneCrossover = False
    #         del structure.fitness.values
    #
    #     self.newEvaluateFitness(self.population.mutants)
    #
    #     self.mergeMutants()
    #
    #
    # def mergeMutants(self):
    #     self.population.structures = self.population.structures + self.population.mutants
    #     self.population.mutants = []


