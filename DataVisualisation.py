# from Statistics import *
import matplotlib.pyplot as plt

#@todo figure out where to store the list of population statistics values across generations

class DataVisualisation():
    def __init__(self):
        self.genElt = None
        self.fitnessMaxElt = None
        self.fitnessAvgElt = None
        self.fitnessStdDevElt = None
        self.genMut = None
        self.fitnessMaxMut = None
        self.fitnessAvgMut = None
        self.fitnessStdDevMut = None

    def plotGraph(self, PyCrystGA, fontSize, labelSize, fileName, directory, dpi):
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [0.66, 0.33]},
                                       figsize=(9, 6))
        fig.subplots_adjust(hspace=0.05)

        ax2.set_xlabel("Generation", fontsize=fontSize)
        ax1.set_ylabel("Fitness / %", fontsize=fontSize)
        ax2.set_ylabel(r'$\sigma$ / %$^{-1}$', fontsize=fontSize)

        ax1.tick_params(axis='both', which='major', labelsize=labelSize)
        ax2.tick_params(axis='both', which='major', labelsize=labelSize)

        ax1.plot(PyCrystGA.population.generationNum, PyCrystGA.population.mutFitnessMax, ".b-", label="Best Fitness")
        ax1.plot(PyCrystGA.population.generationNum, PyCrystGA.population.mutFitnessAvg, ".r-", label="Average Fitness")
        # ax2.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltFitnessStdDev, ".g-", label="Elite Standard Deviation")
        ax2.plot(PyCrystGA.population.generationNum, PyCrystGA.population.mutFitnessStdDev, ".g-", label="Standard Deviation")

        ax1.set_title(
            "Population Size: " + str(PyCrystGA.popSize) + ', Crossover Rate: ' + str(PyCrystGA.originalCrossoverPercentage)
            + ', Mutation Rate: ' + str(PyCrystGA.originalMutationPercentage) + ',' + '\nRun Time: ' + str(format(round(PyCrystGA.timeElapsed, 3))) + ' s',
            fontsize=14)

        ax1.legend(loc="upper right")

        ax2.legend(loc='upper right')

        file = directory + fileName
        print(file)
        print(dpi)

        plt.savefig(file, dpi=dpi)

    def plotPctDiffGraph(self,  PyCrystGA, fontSize, labelSize, fileName, directory, dpi):
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, gridspec_kw={'height_ratios': [0.33, 0.33, 0.33]},
                                       figsize=(9, 6))
        fig.subplots_adjust(hspace=0.05)

        ax1.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltPctDiff, ".b-", label="Elite Pct Diff")
        ax1.hlines(y=PyCrystGA.pctDiffThresh, xmin=1, xmax=len(PyCrystGA.population.generationNum), colors='b', linestyles='--', lw=2)
    # ax1.plot(PyCrystGA.population.generationNum, PyCrystGA.population.mutPctDiff, ".r-", label="Mutant Pct Diff")

        #
        # print(PyCrystGA.population.generationNum)
        # print(PyCrystGA.crossoverHistory)
        ax2.plot(PyCrystGA.population.generationNum, PyCrystGA.crossoverHistory, ".g-", label="Crossover Rate")
        ax2.hlines(y=PyCrystGA.originalCrossoverPercentage, xmin=1, xmax=len(PyCrystGA.population.generationNum), colors='g', linestyles='--', lw=2)

        ax3.plot(PyCrystGA.population.generationNum, PyCrystGA.mutationHistory, ".r-", label="Mutation Rate")
        ax3.hlines(y=PyCrystGA.originalMutationPercentage, xmin=1, xmax=len(PyCrystGA.population.generationNum), colors='r', linestyles='--', lw=2)

        ax3.set_xlabel("Generation", fontsize=fontSize)

        ax1.set_ylabel("Pct Diff / %", fontsize=fontSize)
        ax2.set_ylabel("C R", fontsize=fontSize)
        ax3.set_ylabel("M R", fontSize=fontSize)

        ax1.tick_params(axis='both', which='major', labelsize=labelSize)
        ax2.tick_params(axis='both', which='major', labelsize=labelSize)
        ax2.tick_params(axis='both', which='major', labelsize=labelSize)

        ax1.set_title(
            "Population Size: " + str(PyCrystGA.popSize) + ', Original Crossover Rate: ' +
            str(PyCrystGA.originalCrossoverPercentage) + ', Original Mutation Rate: ' + str(PyCrystGA.originalMutationPercentage),
            fontsize=12)

        ax1.legend(loc="upper right")
        ax2.legend(loc="upper right")
        ax3.legend(loc="upper right")


        file = directory + fileName

        plt.savefig(file, dpi=dpi)





