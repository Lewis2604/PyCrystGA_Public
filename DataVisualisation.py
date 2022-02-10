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
            ax1.set_ylabel("$R_{wp}$ / %", fontsize=fontSize)
            ax2.set_ylabel(r'$\sigma$ / %', fontsize=fontSize)
            # ax2.set_ylabel(r'$\sigma$ / %$^{-1}$', fontsize=fontSize)

            ax1.tick_params(axis='both', which='major', labelsize=labelSize)
            ax2.tick_params(axis='both', which='major', labelsize=labelSize)

            ax1.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltFitnessMax, ".b-", label="$R_{wp}$ Best")
            ax1.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltFitnessAvg, ".r-", label="$R_{wp}$ Average")
            # ax2.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltFitnessStdDev, ".g-", label="Elite Standard Deviation")
            ax2.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltRwpStdDev, ".g-", label="Standard Deviation")

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

    def newPlotGraph(self, PyCrystGA, fontSize, labelSize, fileName, directory, dpi):
        if PyCrystGA.staticCrossover and PyCrystGA.staticMutation:
            print("graph1")
            fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [0.66, 0.33]},
                                        figsize=(9, 6))
            fig.subplots_adjust(hspace=0.05)

            ax2.set_xlabel("Generation", fontsize=fontSize)
            ax1.set_ylabel("$R_{wp}$ / %", fontsize=fontSize)
            ax2.set_ylabel(r'$\sigma$ / %', fontsize=fontSize)
        # ax2.set_ylabel(r'$\sigma$ / %$^{-1}$', fontsize=fontSize)

            ax1.tick_params(axis='both', which='major', labelsize=labelSize)
            ax2.tick_params(axis='both', which='major', labelsize=labelSize)

            ax1.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltFitnessMax, ".b-", label="$R_{wp}$ Best")
            ax1.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltFitnessAvg, ".r-", label="$R_{wp}$ Average")
        # ax2.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltFitnessStdDev, ".g-", label="Elite Standard Deviation")
            ax2.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltRwpStdDev, ".g-", label="Standard Deviation")

            ax1.set_title(
            "Population Size: " + str(PyCrystGA.popSize) + ', Crossover Rate: ' + str(PyCrystGA.originalCrossoverPercentage)
            + ', Mutation Rate: ' + str(PyCrystGA.originalMutationPercentage) + ',' + '\nRun Time: ' + str(format(round(PyCrystGA.timeElapsed, 3))) + ' s',
            fontsize=14)

            ax1.legend(loc="upper right")

            ax2.legend(loc='upper right')

            file = directory + fileName

            plt.savefig(file, dpi=dpi)


        if PyCrystGA.linearDynamicCrossover or PyCrystGA.linearDynamicMutation:
            fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, gridspec_kw={'height_ratios': [0.5, 0.25, 0.25]},
                                           figsize=(9, 6))
            fig.subplots_adjust(hspace=0.05)

            ax3.set_xlabel("Generation", fontsize=fontSize)
            ax1.set_ylabel("$R_{wp}$ / %", fontsize=fontSize)
            ax2.set_ylabel(r'$\sigma$ / %', fontsize=fontSize)
            ax3.set_ylabel("Rate", fontsize=fontSize)
            # ax3.set_ylabel("CR / %", fontsize=fontSize)
            # ax4 = ax3.twinx()
            # ax4.set_ylabel("MR / %", fontsize=fontsize)
            # ax2.set_ylabel(r'$\sigma$ / %$^{-1}$', fontsize=fontSize)

            ax1.tick_params(axis='both', which='major', labelsize=labelSize)
            ax2.tick_params(axis='both', which='major', labelsize=labelSize)
            ax3.tick_params(axis='both', which='major', labelsize=labelSize)

            ax1.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltFitnessMax, ".b-", label="$R_{wp}$ Best")
            ax1.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltFitnessAvg, ".r-", label="$R_{wp}$ Average")
            # ax2.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltFitnessStdDev, ".g-", label="Elite Standard Deviation")
            ax2.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltRwpStdDev, ".g-", label="Standard Deviation")
            ax3.plot(PyCrystGA.population.generationNum, PyCrystGA.crossoverHistory, ".c-", label="Crossover Rate")
            ax3.plot(PyCrystGA.population.generationNum, PyCrystGA.mutationHistory, ".m-", label="Mutation Rate")

            if len(PyCrystGA.phaseBoundaries) > 0:
                for value in PyCrystGA.phaseBoundaries:
                    plt.axvline(x=value, color="gray", linestyle='--')

            ax1.set_title(
                "Population Size: " + str(PyCrystGA.popSize) + ', Crossover Rate: ' + str(PyCrystGA.originalCrossoverPercentage)
                + ', Mutation Rate: ' + str(PyCrystGA.originalMutationPercentage) + ',' + '\nRun Time: ' + str(format(round(PyCrystGA.timeElapsed, 3))) + ' s',
                fontsize=14)

            ax1.legend(loc="upper right")

            ax2.legend(loc='upper right')

            ax3.legend(loc='upper right')

            file = directory + fileName

            plt.savefig(file, dpi=dpi)

        if PyCrystGA.lowMutHighCross or PyCrystGA.highMutLowCross:
            fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, gridspec_kw={'height_ratios': [0.5, 0.25, 0.25]},
                                                figsize=(9, 6))
            fig.subplots_adjust(hspace=0.05)

            ax3.set_xlabel("Generation", fontsize=fontSize)

            ax1.set_ylabel("$R_{wp}$ / %", fontsize=fontSize)
            ax2.set_ylabel(r'$\sigma$ / %', fontsize=fontSize)
            ax3.set_ylabel("Rate", fontsize=fontSize)
            # ax3.set_ylabel("CR / %", fontsize=fontSize)
            # ax4 = ax3.twinx()
            # ax4.set_ylabel("MR / %", fontsize=fontsize)
            # ax2.set_ylabel(r'$\sigma$ / %$^{-1}$', fontsize=fontSize)

            ax1.tick_params(axis='both', which='major', labelsize=labelSize)
            ax2.tick_params(axis='both', which='major', labelsize=labelSize)
            ax3.tick_params(axis='both', which='major', labelsize=labelSize)

            ax1.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltFitnessMax, ".b-", label="$R_{wp}$ Best")
            ax1.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltFitnessAvg, ".r-", label="$R_{wp}$ Average")
            # ax2.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltFitnessStdDev, ".g-", label="Elite Standard Deviation")
            ax2.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltRwpStdDev, ".g-", label="Standard Deviation")
            ax3.plot(PyCrystGA.population.generationNum, PyCrystGA.crossoverHistory, ".c-", label="Crossover Rate")
            ax3.plot(PyCrystGA.population.generationNum, PyCrystGA.mutationHistory, ".m-", label="Mutation Rate")

            if len(PyCrystGA.phaseBoundaries) > 0:
                for value in PyCrystGA.phaseBoundaries:
                    plt.axvline(x=value, color="gray", linestyle='--')

            ax1.set_title(
                "Population Size: " + str(PyCrystGA.popSize) + ',' + '\nRun Time: ' + str(format(round(PyCrystGA.timeElapsed, 3))) + ' s',
                fontsize=14)

            ax1.legend(loc="upper right")

            ax2.legend(loc='upper right')

            ax3.legend(loc='upper right')

            file = directory + fileName

            plt.savefig(file, dpi=dpi)

        if PyCrystGA.exponentOperators:
            fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, gridspec_kw={'height_ratios': [0.5, 0.25, 0.25]},
                                                figsize=(9, 6))
            fig.subplots_adjust(hspace=0.05)

            ax3.set_xlabel("Generation", fontsize=fontSize)

            ax1.set_ylabel("$R_{wp}$ / %", fontsize=fontSize)
            ax2.set_ylabel(r'$\sigma$ / %', fontsize=fontSize)
            ax3.set_ylabel("Rate", fontsize=fontSize)
            # ax3.set_ylabel("CR / %", fontsize=fontSize)
            # ax4 = ax3.twinx()
            # ax4.set_ylabel("MR / %", fontsize=fontsize)
            # ax2.set_ylabel(r'$\sigma$ / %$^{-1}$', fontsize=fontSize)

            ax1.tick_params(axis='both', which='major', labelsize=labelSize)
            ax2.tick_params(axis='both', which='major', labelsize=labelSize)
            ax3.tick_params(axis='both', which='major', labelsize=labelSize)

            ax1.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltFitnessMax, ".b-", label="$R_{wp}$ Best")
            ax1.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltFitnessAvg, ".r-", label="$R_{wp}$ Average")
            # ax2.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltFitnessStdDev, ".g-", label="Elite Standard Deviation")
            ax2.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltRwpStdDev, ".g-", label="Standard Deviation")
            ax3.plot(PyCrystGA.population.generationNum, PyCrystGA.crossoverHistory, ".c-", label="Crossover Rate")
            ax3.plot(PyCrystGA.population.generationNum, PyCrystGA.mutationHistory, ".m-", label="Mutation Rate")

            print(PyCrystGA.population.generationNum)
            print(PyCrystGA.expectedCrossoverHistory)
            print(PyCrystGA.expectedMutationHistory)

            if len(PyCrystGA.phaseBoundaries) > 0:
                for value in PyCrystGA.phaseBoundaries:
                    plt.axvline(x=value, color="gray", linestyle='--')

            ax1.set_title(
                "Population Size: " + str(PyCrystGA.popSize) + ','
                + '\nExponent Scale Factor: ' + str(PyCrystGA.exponentFactor)
                + '\nRun Time: ' + str(format(round(PyCrystGA.timeElapsed, 3))) + ' s',
                fontsize=14)

            ax1.legend(loc="upper right")

            ax2.legend(loc='upper right')

            ax3.legend(loc='upper right')

            file = directory + fileName

            plt.savefig(file, dpi=dpi)

        if PyCrystGA.ILMDHC_UpDown:
            fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, gridspec_kw={'height_ratios': [0.5, 0.25, 0.25]},
                                                figsize=(9, 6))
            fig.subplots_adjust(hspace=0.05)

            ax3.set_xlabel("Generation", fontsize=fontSize)

            ax1.set_ylabel("$R_{wp}$ / %", fontsize=fontSize)
            ax2.set_ylabel(r'$\sigma$ / %', fontsize=fontSize)
            ax3.set_ylabel("Rate", fontsize=fontSize)
            # ax3.set_ylabel("CR / %", fontsize=fontSize)
            # ax4 = ax3.twinx()
            # ax4.set_ylabel("MR / %", fontsize=fontsize)
            # ax2.set_ylabel(r'$\sigma$ / %$^{-1}$', fontsize=fontSize)

            ax1.tick_params(axis='both', which='major', labelsize=labelSize)
            ax2.tick_params(axis='both', which='major', labelsize=labelSize)
            ax3.tick_params(axis='both', which='major', labelsize=labelSize)

            ax1.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltFitnessMax, ".b-", label="$R_{wp}$ Best")
            ax1.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltFitnessAvg, ".r-", label="$R_{wp}$ Average")
            # ax2.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltFitnessStdDev, ".g-", label="Elite Standard Deviation")
            ax2.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltRwpStdDev, ".g-", label="Standard Deviation")

            """
            need to plot the rolling average and the standard deviation of the rolling average 
            """

            a = list(range(0, len(PyCrystGA.population.eltRwpStdDevRollAvg)))
            b = list(range(0, len(PyCrystGA.population.eltRwpStdDevRollAvgStdDev)))

            lenDiff1 = len(PyCrystGA.population.generationNum) - len(a)
            lenDiff2 = len(PyCrystGA.population.generationNum) - len(b)

            c = [x+lenDiff1 for x in a]
            d = [x+lenDiff2 for x in b]

            ax2.plot(c, PyCrystGA.population.eltRwpStdDevRollAvg, linestyle='solid', color='cyan', label="Roll. Avg.")
            # ax2.plot(d, PyCrystGA.population.eltRwpStdDevRollAvgStdDev, ".r-", label="Roll. Avg. Std. Dev.")

            ax3.plot(PyCrystGA.population.generationNum, PyCrystGA.crossoverHistory, ".c-", label="Crossover Rate")
            ax3.plot(PyCrystGA.population.generationNum, PyCrystGA.mutationHistory, ".m-", label="Mutation Rate")

            print(PyCrystGA.population.generationNum)
            print(PyCrystGA.expectedCrossoverHistory)
            print(PyCrystGA.expectedMutationHistory)

            if len(PyCrystGA.phaseBoundaries) > 0:
                for value in PyCrystGA.phaseBoundaries:
                    plt.axvline(x=value, color="gray", linestyle='--')

            ax1.set_title(
                "Population Size: " + str(PyCrystGA.popSize) + ','
                + '\nRoll Avg. Range: ' + str(PyCrystGA.rollingAvgRange) + ', '
                + 'Spike Threshold: ' + str(PyCrystGA.spikeThreshold) + ','
                + '\nExponent Scale Factor: ' + str(PyCrystGA.exponentFactor) + ', '
                + 'Run Time: ' + str(format(round(PyCrystGA.timeElapsed, 3))) + ' s',
                fontsize=14)

            ax1.legend(loc="upper right")

            ax2.legend(loc='upper right')

            ax3.legend(loc='upper right')

            file = directory + fileName

            plt.savefig(file, dpi=dpi)

        else:
            fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, gridspec_kw={'height_ratios': [0.5, 0.25, 0.25]},
                                                figsize=(9, 6))
            fig.subplots_adjust(hspace=0.05)

            ax3.set_xlabel("Generation", fontsize=fontSize)

            ax1.set_ylabel("$R_{wp}$ / %", fontsize=fontSize)
            ax2.set_ylabel(r'$\sigma$ / %', fontsize=fontSize)
            ax3.set_ylabel("Rate", fontsize=fontSize)
            # ax3.set_ylabel("CR / %", fontsize=fontSize)
            # ax4 = ax3.twinx()
            # ax4.set_ylabel("MR / %", fontsize=fontsize)
            # ax2.set_ylabel(r'$\sigma$ / %$^{-1}$', fontsize=fontSize)

            ax1.tick_params(axis='both', which='major', labelsize=labelSize)
            ax2.tick_params(axis='both', which='major', labelsize=labelSize)
            ax3.tick_params(axis='both', which='major', labelsize=labelSize)

            ax1.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltFitnessMax, ".b-", label="$R_{wp}$ Best")
            ax1.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltFitnessAvg, ".r-", label="$R_{wp}$ Average")
            # ax2.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltFitnessStdDev, ".g-", label="Elite Standard Deviation")
            ax2.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltRwpStdDev, ".g-", label="Standard Deviation")
            ax3.plot(PyCrystGA.population.generationNum, PyCrystGA.crossoverHistory, ".c-", label="Crossover Rate")
            ax3.plot(PyCrystGA.population.generationNum, PyCrystGA.mutationHistory, ".m-", label="Mutation Rate")

            print(PyCrystGA.population.generationNum)
            print(PyCrystGA.expectedCrossoverHistory)
            print(PyCrystGA.expectedMutationHistory)

            ax3.plot(PyCrystGA.population.generationNum, PyCrystGA.expectedCrossoverHistory, "c--")
            ax3.plot(PyCrystGA.population.generationNum, PyCrystGA.expectedMutationHistory, "m--")

            if len(PyCrystGA.phaseBoundaries) > 0:
                for value in PyCrystGA.phaseBoundaries:
                    plt.axvline(x=value, color="gray", linestyle='--')

            ax1.set_title(
                "Population Size: " + str(PyCrystGA.popSize) + ',' + '\nRun Time: ' + str(format(round(PyCrystGA.timeElapsed, 3))) + ' s',
                fontsize=14)

            ax1.legend(loc="upper right")

            ax2.legend(loc='upper right')

            ax3.legend(loc='upper right')

            file = directory + fileName

            plt.savefig(file, dpi=dpi)


    #def plotOperatorHistory(self, PyCrystGA):
    def plotNormalisedFitness(self, PyCrystGA, fontSize, labelSize, fileName, directory, dpi):
        print("normalised")

        print(PyCrystGA.population.eltFitnessMinNorm)
        print(PyCrystGA.population.eltFitnessMaxNorm)

        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [0.33, 0.33, 0.33]},
                                            figsize=(9, 6))
        fig.subplots_adjust(hspace=0.05)

        ax1.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltFitnessMinNorm, ".b-", label="Fitness Min Norm")


        ax2.plot(PyCrystGA.population.generationNum, PyCrystGA.population.eltFitnessMaxNorm, ".g-", label="Fitness Max Norm")

        ax1.set_ylabel("Fitness normalised", fontsize=fontSize)
        ax2.set_ylabel("Fitness normalised", fontsize=fontSize)


        ax1.tick_params(axis='both', which='major', labelsize=labelSize)
        ax2.tick_params(axis='both', which='major', labelsize=labelSize)
        ax2.tick_params(axis='both', which='major', labelsize=labelSize)

        ax1.set_title(
            "Population Size: " + str(PyCrystGA.popSize) + ', Original Crossover Rate: ' +
            str(PyCrystGA.originalCrossoverPercentage) + ', Original Mutation Rate: ' + str(PyCrystGA.originalMutationPercentage),
            fontsize=12)

        ax1.legend(loc="upper right")
        ax2.legend(loc="upper right")

        file = directory + fileName

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
        print(len(PyCrystGA.population.generationNum))
        print(len(PyCrystGA.crossoverHistory))
        print(len(PyCrystGA.mutationHistory))

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







