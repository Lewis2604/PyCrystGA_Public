import numpy as np
import Toolbox
import PyCrystGA
import os

#@todo add time date/time logging whn recording statistics
class Statistics():
    def __init__(self):
    #def __init__(self, population, directory):
        # self.population = population
        # self.directory = directory
        self.stats = None
        self.multiStats = None
        self.logbook = None
        self.recordElt = None
        self.logbookElt = None
        self.recordMut = None
        self.logbookMut = None
        self.hofElt = None

        self.createFitnessLog()

    def createFitnessLog(self):
        self.stats = Toolbox.tools.Statistics(key=lambda structure: structure.fitness.values)
        self.multiStats = Toolbox.tools.MultiStatistics(fitness=self.stats)
        self.multiStats.register("avg", np.mean)
        self.multiStats.register("std", np.std)
        self.multiStats.register("min", np.min)
        self.multiStats.register("max", np.max)

        self.logbook = Toolbox.tools.Logbook()
        self.logbook.header = "gen", 'fitness'
        self.logbook.chapters['fitness'].header = "std", "min", "avg", "max"

    @staticmethod
    def writeRunInfoToFile(directory, numGen, popSize, crossoverPercentage, mutationPercentage, pctDiffThresh):
        f = open(directory + "Run Info.txt", "a")
        # print("Degrees of Freedom: " + str())
        print("Number of Generations:  " + str(numGen), file=f)
        print("Population Size:  " + str(popSize), file=f)
        print("Crossover Percentage:  " + str(crossoverPercentage), file=f)
        print("Mutation Percentage:  " + str(mutationPercentage), file=f)
        print("Percentage Difference Threshold:  " + str(pctDiffThresh), file=f)
        return

    def recordElitePopulationStatistics(self, directory, population, generation):
        # for structure in population.structures:
        for structure in population.structures:
            print(generation, file=open(directory + "FitnessHistory.txt", "a"))
            print("Elite ", file=open(directory + "FitnessHistory.txt", "a"))
            print(structure.torsions, file=open(directory + "FitnessHistory.txt", "a"))
            print(structure.orientations, file=open(directory + "FitnessHistory.txt", "a"))
            print(structure.positions, file=open(directory + "FitnessHistory.txt", "a"))
            print(structure.fitness.values, file=open(directory + "FitnessHistory.txt", "a"))

        self.logbook.record(gen=generation, **self.multiStats.compile(population.structures))
        # self.recordElt = self.stats.compile(population.structures)
        self.recordElt = self.stats.compile(population.structures)
        self.logbookElt = Toolbox.tools.Logbook()
        self.logbookElt.header = "gen", "std", "min", "avg", "max"
        self.logbookElt.record(gen=generation, **self.recordElt)

        print("Elite", file=open(directory + "Pop_stats.txt", "a"))
        print(self.logbookElt.stream, file=open(directory + "Pop_stats.txt", "a"))

        self.hofElt = Toolbox.toolbox.bestSelect(population.structures, 1)[0]
        # self.hofElt = Toolbox.toolbox.bestSelect(population, 1)[0]
        print(generation, file=open(directory + "Best.txt", "a"))
        print("Elite", file=open(directory + "Best.txt", "a"))
        print(self.hofElt.torsions, file=open(directory + "Best.txt", "a"))
        print(self.hofElt.orientations, file=open(directory + "Best.txt", "a"))
        print(self.hofElt.positions, file=open(directory + "Best.txt", "a"))
        print(self.hofElt.fitness, file=open(directory + "Best.txt", "a"))
        # print(self.hofElt.scale, file=open(directory + "Best.txt", "a"))
        # print(self.hofElt.disp, file=open(directory + "Best.txt", "a"))

        fitMax = self.logbookElt.select("max")
        fitAvg = self.logbookElt.select("avg")
        fitStd = self.logbookElt.select("std")

        population.eltFitnessMax.append(1/fitMax[0])
        population.eltFitnessAvg.append(1/fitAvg[0])
        population.eltFitnessStdDev.append(fitStd[0])

        del self.hofElt
        return

    def recordMutantPopulationStatistics(self, directory, population, generation):
        # for structure in population.structures:
        for structure in population.structures:
            print("Mutant", file=open(directory + "FitnessHistory.txt", "a"))
            print(generation, file=open(directory + "FitnessHistory.txt", "a"))
            print(structure.torsions, file=open(directory + "FitnessHistory.txt", "a"))
            print(structure.orientations, file=open(directory + "FitnessHistory.txt", "a"))
            print(structure.positions, file=open(directory + "FitnessHistory.txt", "a"))
            print(structure.fitness.values, file=open(directory + "FitnessHistory.txt", "a"))

        # self.logbook.record(gen=gen, **mstats.compile(population.structures))
        # self.recordMut = self.stats.compile(population.structures)


        # print('qwerty')
        # print(generation)
        # print(self.multiStats.compile(population.structures))
        self.logbook.record(gen=generation, **self.multiStats.compile(population.structures))
        self.recordMut = self.stats.compile(population.structures)
        self.logbookMut = Toolbox.tools.Logbook()
        self.logbookMut.header = "gen", "std", "min", "avg", "max"
        self.logbookMut.record(gen=generation, **self.recordMut)

        print("Mutants", file=open(directory + "Pop_stats.txt", "a"))
        print(self.logbookMut.stream, file=open(directory + "Pop_stats.txt", "a"))
        # print(self.multiStats.compile(population.structures), file=open(directory + "Pop_stats.txt", "a"))

        self.hofElt = Toolbox.toolbox.bestSelect(population.structures, 1)[0]
        # self.hofElt = Toolbox.toolbox.bestSelect(population, 1)[0]
        print(generation, file=open(directory + "Best.txt", "a"))
        print("Mutants", file=open(directory + "Best.txt", "a"))
        print(self.hofElt.torsions, file=open(directory + "Best.txt", "a"))
        print(self.hofElt.orientations, file=open(directory + "Best.txt", "a"))
        print(self.hofElt.positions, file=open(directory + "Best.txt", "a"))
        print(self.hofElt.fitness, file=open(directory + "Best.txt", "a"))
        # print(self.hofElt.scale, file=open(directory + "Best.txt", "a"))
        # print(self.hofElt.disp, file=open(directory + "Best.txt", "a"))

        gen = self.logbookMut.select("gen")
        fitMax = self.logbookMut.select("max")
        fitAvg = self.logbookMut.select("avg")
        fitStd = self.logbookMut.select("std")

        population.generationNum.append(gen[0])
        population.mutFitnessMax.append(1/fitMax[0])
        population.mutFitnessAvg.append(1/fitAvg[0])
        population.mutFitnessStdDev.append(fitStd[0])
        del self.hofElt
        return