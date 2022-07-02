import numpy as np
import Toolbox as Toolbox
import PyCrystGA
import os


# @todo add time date/time logging whn recording statistics
class Statistics():
    def __init__(self):
        # def __init__(self, population, directory):
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
        self.logbook.chapters['fitness'].header = "std", "min", "avg", "max", "min"

    @staticmethod
    def writeRunInfoToFile(directory, numGen, popSize, crossoverPercentage, mutationPercentage, PyCrystGA):
        f = open(directory + "Run Info.txt", "a")
        # print("Degrees of Freedom: " + str())
        print("Number of Generations:  " + str(numGen), file=f)
        print("Population Size:  " + str(popSize), file=f)
        if PyCrystGA.staticCrossover:
            print("Crossover Percentage:  " + str(crossoverPercentage), file=f)
        if PyCrystGA.staticMutation:
            print("Mutation Percentage:  " + str(mutationPercentage), file=f)
        if PyCrystGA.linearDynamicCrossover or PyCrystGA.exponentialDynamicCrossover:
            print("Phase 1 Crossover:  " + str(PyCrystGA.phase1XoverInitial), file=f)

            print("Phase 2 Crossover:  " + str(PyCrystGA.phase2XoverInitial), file=f)
            print("Phase 2 Crossover Upper:  " + str(PyCrystGA.phase2XoverUpper), file=f)
            print("Phase 2 Crossover Lower:  " + str(PyCrystGA.phase2XoverLower), file=f)

            print("Phase 3 Crossover:  " + str(PyCrystGA.phase3XoverInitial), file=f)
            print("Phase 3 Crossover Upper:  " + str(PyCrystGA.phase3XoverUpper), file=f)
            print("Phase 3 Crossover Lower:  " + str(PyCrystGA.phase3XoverLower), file=f)

        if PyCrystGA.linearDynamicMutation or PyCrystGA.exponentialDynamicMutation:
            print("Phase 1 Mutation:  " + str(PyCrystGA.phase1MutInitial), file=f)

            print("Phase 2 Mutation:  " + str(PyCrystGA.phase2MutInitial), file=f)
            print("Phase 2 Mutation Upper:  " + str(PyCrystGA.phase2MutUpper), file=f)
            print("Phase 2 Mutation Lower:  " + str(PyCrystGA.phase2MutLower), file=f)

            print("Phase 3 Mutation:  " + str(PyCrystGA.phase3MutInitial), file=f)
            print("Phase 3 Mutation Upper:  " + str(PyCrystGA.phase3MutUpper), file=f)
            print("Phase 3 Mutation Lower:  " + str(PyCrystGA.phase3MutLower), file=f)
        return

    def writeNumEvalsToFile(directory, numEvals, gen):
        f = open(directory + "Run Info.txt", "a")
        # print("Degrees of Freedom: " + str())
        print("Generation:  " + str(gen), file=f)
        print("Number of Fitness Evals:  " + str(numEvals), file=f)
        return

    def writeToFile(self, content, filePath):
        # If you want to write a single line
        # Either stick it in an array ['content']
        # or add a check here whether it's a string/array

        for row in content:
            print(row, file=open(filePath, "a"))

    def recordElitePopulationStatistics(self, directory, population, generation):
        rwp = []
        for structure in population.structures:
            self.writeToFile([
                generation,
                'Elite  ',
                structure.torsions,
                structure.orientations,
                structure.positions,
                structure.fitness.values
            ], directory + "EliteFitnessHistory.txt")
            rwp.append(1/list(structure.fitness.values)[0])

        population.eltRwpStdDev.append(np.std(rwp))

        self.logbook.record(gen=generation, **self.multiStats.compile(population.structures))
        self.recordElt = self.stats.compile(population.structures)
        self.logbookElt = Toolbox.tools.Logbook()
        self.logbookElt.header = "gen", "std", "avg", "min", "max"
        self.logbookElt.record(gen=generation, **self.recordElt)

        self.writeToFile([
            'Elite',
            self.logbookElt.stream
        ], directory + 'Pop_stats.txt')

        self.hofElt = Toolbox.toolbox.bestSelect(population.structures, 1)[0]

        self.writeToFile([
            generation,
            'Elite',
            self.hofElt.torsions,
            self.hofElt.orientations,
            self.hofElt.positions,
            self.hofElt.fitness
        ], directory + "Best.txt")

        fitMin = self.logbookElt.select("min")
        fitMax = self.logbookElt.select("max")
        fitAvg = self.logbookElt.select("avg")
        fitStd = self.logbookElt.select("std")

        population.eltFitnessMin.append(1 / fitMin[0])
        population.eltFitnessMax.append(1 / fitMax[0])
        population.eltFitnessAvg.append(1 / fitAvg[0])
        population.eltFitnessStdDev.append(fitStd[0])
        # population.eltFitnessMaxNorm.append((population.eltFitnessMax[-1]-population.eltFitnessAvg[-1])/population.eltFitnessStdDev[-1])
        # population.eltFitnessMinNorm.append((population.eltFitnessMin[-1]-population.eltFitnessAvg[-1])/population.eltFitnessStdDev[-1])

        del self.hofElt
        return

    def recordMutantPopulationStatistics(self, directory, population, generation):
        rwp = []
        for structure in population.structures:
            self.writeToFile([
                generation,
                'Mutant',
                structure.torsions,
                structure.orientations,
                structure.positions,
                structure.fitness.values
            ], directory + "MutantFitnessHistory.txt")
            rwp.append(1/list(structure.fitness.values)[0])

        population.mutRwpStdDev.append(np.std(rwp))

        self.logbook.record(gen=generation, **self.multiStats.compile(population.structures))
        self.recordMut = self.stats.compile(population.structures)
        self.logbookMut = Toolbox.tools.Logbook()
        self.logbookMut.header = "gen", "std", "avg", "min", "max"
        self.logbookMut.record(gen=generation, **self.recordMut)

        self.writeToFile([
            'Mutants',
            self.logbookMut.stream
        ], directory + "Pop_stats.txt")

        self.hofElt = Toolbox.toolbox.bestSelect(population.structures, 1)[0]

        self.writeToFile([
            generation,
            'Mutant',
            self.hofElt.torsions,
            self.hofElt.orientations,
            self.hofElt.positions,
            self.hofElt.fitness
        ], directory + "Best.txt")

        gen = self.logbookMut.select("gen")
        fitMin = self.logbookMut.select("min")
        fitMax = self.logbookMut.select("max")
        fitAvg = self.logbookMut.select("avg")
        fitStd = self.logbookMut.select("std")

        population.generationNum.append(gen[0])
        population.mutFitnessMin.append(1 / fitMin[0])
        population.mutFitnessMax.append(1 / fitMax[0])
        population.mutFitnessAvg.append(1 / fitAvg[0])
        population.mutFitnessStdDev.append(fitStd[0])
        del self.hofElt
        return
