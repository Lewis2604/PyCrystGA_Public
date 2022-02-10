import re
from pprint import pprint
import matplotlib.pyplot as plt
from matplotlib import ticker
from copy import deepcopy
import numpy as np
# print("Script has started")
#
# TOPAS = TOPAS('C:/Topas-6/tc.exe', r"S:\PhD\Year_3\Algorithm\TOPAS\Template\TFB1\TFB1 GA p21n.inp")
#
# Algorithm2 = PyCrystGA()
# Algorithm2.setXrdInterface(TOPAS)
# Algorithm2.setDirectory("C:/PhD/Year_3/Algorithm/Test/LinearDynamic/2/")
# Algorithm2.start()
#
# print("Script has ended")


# Algorithm1 = PyCrystGA('C:/PhD/Year_3/Algorithm/TFB Crystal Structure/TFB_labels.mol', # Mol file
#                        1, # Z'
#                        'C:/PhD/Year_3/Algorithm/Test/LinearDynamic/1/', # Working directory
#                        TOPAS, # XRD Interface
#                        20, # Population Size
#                        5, # Maximum Number of Generations
#                        0.1, # Crossover Rate
#                        0.1, # Mutation rate
#                        0, # Crossover type, 0 static, 1 linear, 2 exponential
#                        1, # Mutation type, 0 static, 1 linear, 2 exponential
#                        5, # Percentage difference threshold for genetic operators
#                        14, # Graph font size
#                        12, # Graph label size
#                        'PyCrystGA_Graph', # Graph file name
#                        'PyCrystGA_PctDiff_Graph', # Percentage difference graph name
#                        300) # Graph dpi

'''Dynamic class attribute creation
this creates a nested list class attribute
to store the parameters to track'''
# class Test:
#     def __init__(self):
#         self.qwerty = True
#
# test = Test()
# test.parameters = [[] for i in range(3)]
#
# print(test.parameters)

# d = [[] for i in range(3)]
#
# gen = [1,2,3,4]
# fit = gen*2
# param = gen*3
#
# params = [gen, fit, param]
#
# for i in range(len(d)):
#     print(i)
#     d[i].append(params[i])
#
# newD = [i[0] for i in d]
# print(newD)

"""
1
Elite  
[120.36189971122826, 197.09505037561075, 334.06282281761213]
[46.749111352316795, 238.52641707503471, 178.49969956736723]
[0.862499514482623, 0.5110442237516641, 0.8767148970546658]
(0.056833323055026856,)

generation
'Elite  '
torsions
orientations
positions
fitness
"""

def getMaxListIndex(list):
    maxVal = max(list)
    maxIndex = list.index(maxVal)
    return maxIndex


def getMinListIndex(list):
    minVal = min(list)
    minIndex = list.index(minVal)
    return minIndex


def makeNewList(nestedList, listToMake, indexValueList):
    a = 0
    for i in nestedList:
        listToMake.append(i[indexValueList[a]])

def plotPopulation(popSize, directory, M, xMin, xMax, xStep, colour1, colour2, colour3, colour4, colour5):
    # popSize = 100
    # directory = r'C:\PhD\Year_4\Algorithm\Test\Exponent\IMDC\1\(1)'
    # M = 10
    # xMin = 0
    # xMax = 1600

    file = open(directory + r"\Statistics\FitnessHistory.txt", "r")

    lines = []
    for line in file:
        lines.append(line.strip("\n"))

    counter1 = 0

    newLines = []
    for i in lines:
        newLines.append(i)
        counter1 += 1
        print(counter1)
        """
        Uncomment below for data subset plotting"""
        # if len(newLines) == 1920000:
        #     break

    countery1 = 0
    newLines2 = []

    print(newLines)

    for i in newLines:
        if i == "Mutant" or i == "Elite  ":
            pass
        else:
            countery1+=1
            print(countery1)
            newLines2.append(i)
    # #
    # #
    for i in newLines2:
        print(i)


    gen = []
    tors = []
    orient = []
    pos = []
    fit = []

    count2 = 0
    for i in newLines2:
        gen.append(newLines2[count2])
        tors.append(newLines2[count2+1])
        orient.append(newLines2[count2+2])
        pos.append(newLines2[count2+3])
        fit.append(newLines2[count2+4])
        count2+=5
        if count2 == len(newLines2):
            break

    gen1 = []
    tors1 = []
    orient1 = []
    pos1 = []
    fit1 = []

    gen2 = []
    tors2 = []
    orient2 = []
    pos2 = []
    fit2 = []

    numInd = len(gen)
    numGen = int(numInd/(popSize*2))
    numPop = int(numGen*2)

    print(numInd)
    print(numGen)


    count3 = 0
    count4 = popSize

    count3List = []
    count4List = []
    for i in range(numGen):
        count3List.append(count3)
        count3 += popSize*2
        count4List.append(count4)
        count4 += popSize*2


    for i in count3List:
        count = 0
        while count < popSize:
            gen1.append(gen[i + count])
            tors1.append(tors[i + count])
            orient1.append(orient[i + count])
            pos1.append(pos[i + count])
            fit1.append(fit[i + count])
            count += 1
    """
    Generation
    """

    #@todo gen1

    """
    Torsions
    """

    tors1a = [s.replace("[", "") for s in tors1]
    tors1b = [s.replace("]", "") for s in tors1a]
    tors1c = [s.replace(",", "") for s in tors1b]
    tors1d = [s.split(" ") for s in tors1c]

    torsFinal = []

    for list in tors1d:
        for element in list:
            torsFinal.append(float(element))

    torsAng1 = torsFinal[::3]
    torsAng2 = torsFinal[1::3]
    torsAng3 = torsFinal[2::3]

    """
    Orientation
    """

    orient1a = [s.replace("[", "") for s in orient1]
    orient1b = [s.replace("]", "") for s in orient1a]
    orient1c = [s.replace(",", "") for s in orient1b]
    orient1d = [s.split(" ") for s in orient1c]

    orientFinal = []

    for list in orient1d:
        for element in list:
            orientFinal.append(float(element))

    orientTht = orientFinal[::3]
    orientPhi = orientFinal[1::3]
    orientPsi = orientFinal[2::3]

    """
    Position
    """

    pos1a = [s.replace("[", "") for s in pos1]
    pos1b = [s.replace("]", "") for s in pos1a]
    pos1c = [s.replace(",", "") for s in pos1b]
    pos1d = [s.split(" ") for s in pos1c]

    posFinal = []

    for list in pos1d:
        for element in list:
            posFinal.append(float(element))

    posX = posFinal[::3]
    posY = posFinal[1::3]
    posZ = posFinal[2::3]

    """
    Fitness
    """

    fit1a = [s.replace("(", "") for s in fit1]
    fitFinal = [s.replace(",)", "") for s in fit1a]
    rwp = []
    for i in fitFinal:
        rwp.append(1/float(i))

    """
    Sublist Generation
    """

    torsAng1Pops = [torsAng1[x:x+popSize] for x in range(0, len(torsAng1), popSize)]
    torsAng2Pops = [torsAng2[x:x+popSize] for x in range(0, len(torsAng2), popSize)]
    torsAng3Pops = [torsAng3[x:x+popSize] for x in range(0, len(torsAng3), popSize)]

    orientThtPops = [orientTht[x:x+popSize] for x in range(0, len(orientTht), popSize)]
    orientPhiPops = [orientPhi[x:x+popSize] for x in range(0, len(orientPhi), popSize)]
    orientPsiPops = [orientPsi[x:x+popSize] for x in range(0, len(orientPsi), popSize)]

    posXPops = [posX[x:x+popSize] for x in range(0, len(posX), popSize)]
    posYPops = [posY[x:x+popSize] for x in range(0, len(posY), popSize)]
    posZPops = [posZ[x:x+popSize] for x in range(0, len(posZ), popSize)]

    fitFinalPops = [fitFinal[x:x+popSize] for x in range(0, len(fitFinal), popSize)]
    rwpFinalPops = [rwp[x:x+popSize] for x in range(0, len(rwp), popSize)]

    genFinal = [gen1[x:x+popSize] for x in range(0, len(gen1), popSize)]

    """
    Best Values
    """
    torsAng1BestA = []
    torsAng2BestA = []
    torsAng3BestA = []

    orientThtBestA = []
    orientPhiBestA = []
    orientPsiBestA = []

    posXBestA = []
    posYBestA = []
    posZBestA = []

    fitBestIndexA = []

    genBestA = []

    RwpBestA = []

    for i in rwpFinalPops:
        fitBestIndexA.append(getMinListIndex(i))

    makeNewList(torsAng1Pops, torsAng1BestA, fitBestIndexA)
    makeNewList(torsAng2Pops, torsAng2BestA, fitBestIndexA)
    makeNewList(torsAng3Pops, torsAng3BestA, fitBestIndexA)

    makeNewList(orientThtPops, orientThtBestA, fitBestIndexA)
    makeNewList(orientPhiPops, orientPhiBestA, fitBestIndexA)
    makeNewList(orientPsiPops, orientPsiBestA, fitBestIndexA)

    makeNewList(posXPops, posXBestA, fitBestIndexA)
    makeNewList(posYPops, posYBestA, fitBestIndexA)
    makeNewList(posZPops, posZBestA, fitBestIndexA)

    makeNewList(genFinal, genBestA, fitBestIndexA)

    makeNewList(rwpFinalPops, RwpBestA, fitBestIndexA)

    torsAng1BestFirst = torsAng1BestA[0]
    torsAng2BestFirst = torsAng2BestA[0]
    torsAng3BestFirst = torsAng3BestA[0]

    orientThtBestFirst = orientThtBestA[0]
    orientPhiBestFirst = orientPhiBestA[0]
    orientPsiBestFirst = orientPsiBestA[0]

    posXBestFirst = posXBestA[0]
    posYBestFirst = posYBestA[0]
    posZBestFirst = posZBestA[0]

    genBestFirst = 0

    rwpBestFirst = RwpBestA[0]

    torsAng1BestACopy = torsAng1BestA.copy()
    torsAng2BestACopy = torsAng2BestA.copy()
    torsAng3BestACopy = torsAng3BestA.copy()

    orientThtBestACopy = orientThtBestA.copy()
    orientPhiBestACopy = orientPhiBestA.copy()
    orientPsiBestACopy = orientPsiBestA.copy()

    posXBestACopy = posXBestA.copy()
    posYBestACopy = posYBestA.copy()
    posZBestACopy = posZBestA.copy()

    genBestACopy = genBestA.copy()

    RwpBestACopy = RwpBestA.copy()

    torsAng1Best = [torsAng1BestFirst] + torsAng1BestACopy
    torsAng2Best = [torsAng2BestFirst] + torsAng2BestACopy
    torsAng3Best = [torsAng3BestFirst] + torsAng3BestACopy

    orientThtBest = [orientThtBestFirst] + orientThtBestACopy
    orientPhiBest = [orientPhiBestFirst] + orientPhiBestACopy
    orientPsiBest = [orientPsiBestFirst] + orientPsiBestACopy

    posXBest = [posXBestFirst] + posXBestACopy
    posYBest = [posYBestFirst] + posYBestACopy
    posZBest = [posZBestFirst] + posYBestACopy

    fitBestIndex = fitBestIndexA

    genBest = [genBestFirst] + genBestACopy

    RwpBest = [rwpBestFirst] + RwpBestACopy


    """
    Worst Values
    """
    torsAng1WorstA = []
    torsAng2WorstA = []
    torsAng3WorstA = []

    orientThtWorstA = []
    orientPhiWorstA = []
    orientPsiWorstA = []

    posXWorstA = []
    posYWorstA = []
    posZWorstA = []

    fitWorstIndexA = []

    genWorstA = []

    RwpWorstA = []


    for i in rwpFinalPops:
        fitWorstIndexA.append(getMaxListIndex(i))

    makeNewList(torsAng1Pops, torsAng1WorstA, fitWorstIndexA)
    makeNewList(torsAng2Pops, torsAng2WorstA, fitWorstIndexA)
    makeNewList(torsAng3Pops, torsAng3WorstA, fitWorstIndexA)

    makeNewList(orientThtPops, orientThtWorstA, fitWorstIndexA)
    makeNewList(orientPhiPops, orientPhiWorstA, fitWorstIndexA)
    makeNewList(orientPsiPops, orientPsiWorstA, fitWorstIndexA)

    makeNewList(posXPops, posXWorstA, fitWorstIndexA)
    makeNewList(posYPops, posYWorstA, fitWorstIndexA)
    makeNewList(posZPops, posZWorstA, fitWorstIndexA)

    makeNewList(genFinal, genWorstA, fitWorstIndexA)

    makeNewList(rwpFinalPops, RwpWorstA, fitWorstIndexA)

    torsAng1WorstFirst = torsAng1WorstA[0]
    torsAng2WorstFirst = torsAng2WorstA[0]
    torsAng3WorstFirst = torsAng3WorstA[0]

    orientThtWorstFirst = orientThtWorstA[0]
    orientPhiWorstFirst = orientPhiWorstA[0]
    orientPsiWorstFirst = orientPsiWorstA[0]

    posXWorstFirst = posXWorstA[0]
    posYWorstFirst = posYWorstA[0]
    posZWorstFirst = posZWorstA[0]

    genWorstFirst = 0

    torsAng1WorstACopy = torsAng1WorstA.copy()
    torsAng2WorstACopy = torsAng2WorstA.copy()
    torsAng3WorstACopy = torsAng3WorstA.copy()

    orientThtWorstACopy = orientThtWorstA.copy()
    orientPhiWorstACopy = orientPhiWorstA.copy()
    orientPsiWorstACopy = orientPsiWorstA.copy()

    posXWorstACopy = posXWorstA.copy()
    posYWorstACopy = posYWorstA.copy()
    posZWorstACopy = posZWorstA.copy()

    genWorstACopy = genWorstA.copy()

    RwpWorstACopy = RwpWorstA.copy()

    rwpWorstFirst = RwpWorstA[0]

    print(RwpWorstACopy)
    print("qwerty")
    print(rwpWorstFirst)

    torsAng1Worst = [torsAng2WorstFirst] + torsAng1WorstACopy
    torsAng2Worst = [torsAng2WorstFirst] + torsAng2WorstACopy
    torsAng3Worst = [torsAng3WorstFirst] + torsAng3WorstACopy

    orientThtWorst = [orientThtWorstFirst] + orientThtWorstACopy
    orientPhiWorst = [orientPhiWorstFirst] + orientPhiWorstACopy
    orientPsiWorst = [orientPsiWorstFirst] + orientPsiWorstACopy

    posXWorst = [posXWorstFirst] + posXWorstACopy
    posYWorst = [posYWorstFirst] + posYWorstACopy
    posZWorst = [posZWorstFirst] + posYWorstACopy

    fitWorstIndex = fitWorstIndexA

    genWorst = [genWorstFirst] + genWorstACopy

    RwpWorst = [rwpWorstFirst] + RwpWorstACopy
    # RwpWorst = RwpWorstACopy.insert(0, rwpWorstFirst)

    print(rwpWorstFirst)
    print(RwpWorst)


    """
    Graph Plotting
    """
    fontSize = 12

    """
    Pos Graph
    """
    fig1, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, gridspec_kw={'height_ratios': [0.33, 0.33, 0.33]},
                                        figsize=(9, 9))

    # ax1.set_ylim([0, 1])
    # ax2.set_ylim([0, 1])
    # ax3.set_ylim([0, 1])

    ax1.set_xlim([0, popSize])

    ax1.set_title("Fractional Coordinate Variation vs. \nGeneration for Structure Solution of TFB",
        fontsize=fontSize)

    """
    All Data Points
    """
    ax1.scatter(gen1, posX, s=1, c=colour1)
    ax2.scatter(gen1, posY, s=1, c=colour2)
    ax3.scatter(gen1, posZ, s=1, c=colour3)


    """
    Best Individual
    """

    ax1.scatter(genBest, posXBest, s=1, c=colour4, label="Best")
    ax2.scatter(genBest, posYBest, s=1, c=colour4, label="Best")
    ax3.scatter(genBest, posZBest, s=1, c=colour4, label="Best")

    # ax1.scatter(genBest, posXBest, s=0.5, c="c", label="Best")
    # ax2.scatter(genBest, posYBest, s=0.5, c="c", label="Best")
    # ax3.scatter(genBest, posZBest, s=0.5, c="c", label="Best")


    """
    Worst Individual
    """
    ax1.scatter(genWorst, posXWorst, s=1, c=colour5, label="Worst")
    ax2.scatter(genWorst, posYWorst, s=1, c=colour5, label="Worst")
    ax3.scatter(genWorst, posZWorst, s=1, c=colour5, label="Worst")


    ax1.set_ylabel("a Fract. Coord.", fontsize=fontSize)
    ax2.set_ylabel("b Fract. Coord.", fontsize=fontSize)
    ax3.set_ylabel("c Fract. Coord.", fontsize=fontSize)

    ax3.set_xlabel("Generation", fontsize=fontSize)

    ax1.legend(loc="upper right")
    ax2.legend(loc="upper right")
    ax3.legend(loc="upper right")

    yticks = ticker.MaxNLocator(M)
    xticks = ticker.MaxNLocator(M)

    # Set the yaxis major locator using your ticker object. You can also choose the minor
    # tick positions with set_minor_locator.
    ax1.yaxis.set_major_locator(yticks)
    ax2.yaxis.set_major_locator(yticks)
    ax3.yaxis.set_major_locator(yticks)

    ax1.set_xticks(np.arange(xMin-1, xMax, xStep))
    ax2.set_xticks(np.arange(xMin-1, xMax, xStep))
    ax3.set_xticks(np.arange(xMin-1, xMax, xStep))

    plt.savefig(directory + r'\Pos', dpi=300)

    """
    Orientation Graph
    """
    fig2, (ax4, ax5, ax6) = plt.subplots(3, 1, sharex=True, gridspec_kw={'height_ratios': [0.33, 0.33, 0.33]},
                                        figsize=(9, 9))

    ax4.set_title("Molecular Orientation vs. \nGeneration for Structure Solution of TFB",
        fontsize=fontSize)

    # ax4.set_ylim([0, 360])
    # ax5.set_ylim([0, 360])
    # ax6.set_ylim([0, 360])

    ax4.set_xlim([0, popSize])

    ax4.scatter(gen1, orientTht, s=1, c=colour1)
    ax5.scatter(gen1, orientPhi, s=1, c=colour2)
    ax6.scatter(gen1, orientPsi, s=1, c=colour3)

    """
    Best Individual
    """
    ax4.scatter(genBest, orientThtBest, s=1, c=colour4, label="Best")
    ax5.scatter(genBest, orientPhiBest, s=1, c=colour4, label="Best")
    ax6.scatter(genBest, orientPsiBest, s=1, c=colour4, label="Best")

    # ax4.scatter(genBest, orientThtBest, s=0.5, c="c", label="Best")
    # ax5.scatter(genBest, orientPhiBest, s=0.5, c="c", label="Best")
    # ax6.scatter(genBest, orientPsiBest, s=0.5, c="c", label="Best")


    """
    Worst Individual
    """
    ax4.scatter(genWorst, orientThtWorst, s=1, c=colour5, label="Worst")
    ax5.scatter(genWorst, orientPhiWorst, s=1, c=colour5, label="Worst")
    ax6.scatter(genWorst, orientPsiWorst, s=1, c=colour5, label="Worst")

    degree_sign = u"\N{DEGREE SIGN}"

    ax4.set_ylabel("Theta / " + str(degree_sign), fontsize=fontSize)
    ax5.set_ylabel("Phi / " + str(degree_sign), fontsize=fontSize)
    ax6.set_ylabel("Psi / " + str(degree_sign), fontsize=fontSize)

    ax6.set_xlabel("Generation", fontsize=fontSize)

    ax4.legend(loc="upper right")
    ax5.legend(loc="upper right")
    ax6.legend(loc="upper right")

    yticks = ticker.MaxNLocator(M)

    # Set the yaxis major locator using your ticker object. You can also choose the minor
    # tick positions with set_minor_locator.
    ax4.yaxis.set_major_locator(yticks)
    ax5.yaxis.set_major_locator(yticks)
    ax6.yaxis.set_major_locator(yticks)

    ax4.set_xticks(np.arange(xMin-1, xMax, xStep))
    ax5.set_xticks(np.arange(xMin-1, xMax, xStep))
    ax6.set_xticks(np.arange(xMin-1, xMax, xStep))


    plt.savefig(directory + r'\Orientation', dpi=300)

    """
    Torsion Angle Graph
    """
    fig3, (ax7, ax8, ax9) = plt.subplots(3, 1, sharex=True, gridspec_kw={'height_ratios': [0.33, 0.33, 0.33]},
                                        figsize=(9, 9))

    ax7.set_title("Torsion Angle Variation vs. \nGeneration for Structure Solution of TFB",
        fontsize=fontSize)

    # ax7.set_ylim([0, 360])
    # ax8.set_ylim([0, 360])
    # ax9.set_ylim([0, 360])

    ax7.set_xlim([0, popSize])

    ax7.scatter(gen1, torsAng1, s=1, c=colour1)
    ax8.scatter(gen1, torsAng2, s=1, c=colour2)
    ax9.scatter(gen1, torsAng3, s=1, c=colour3)

    """
    Best Individual
    """
    ax7.scatter(genBest, torsAng1Best, s=1, c=colour4, label="Best")
    ax8.scatter(genBest, torsAng2Best, s=1, c=colour4, label="Best")
    ax9.scatter(genBest, torsAng3Best, s=1, c=colour4, label="Best")

    # ax7.scatter(genBest, torsAng1Best, s=0.5, c="c", label="Best")
    # ax8.scatter(genBest, torsAng2Best, s=0.5, c="c", label="Best")
    # ax9.scatter(genBest, torsAng3Best, s=0.5, c="c", label="Best")


    """
    Worst Individual
    """
    ax7.scatter(genWorst, torsAng1Worst, s=1, c=colour5, label="Worst")
    ax8.scatter(genWorst, torsAng2Worst, s=1, c=colour5, label="Worst")
    ax9.scatter(genWorst, torsAng3Worst, s=1, c=colour5, label="Worst")

    ax7.set_ylabel("Tors. Ang. 1 / " + str(degree_sign), fontsize=fontSize)
    ax8.set_ylabel("Tors. Ang. 2 / " + str(degree_sign), fontsize=fontSize)
    ax9.set_ylabel("Tors. Ang. 3 / " + str(degree_sign), fontsize=fontSize)

    ax9.set_xlabel("Generation", fontsize=fontSize)

    ax7.legend(loc="upper right")
    ax8.legend(loc="upper right")
    ax9.legend(loc="upper right")

    yticks = ticker.MaxNLocator(M)

    # Set the yaxis major locator using your ticker object. You can also choose the minor
    # tick positions with set_minor_locator.
    ax7.yaxis.set_major_locator(yticks)
    ax8.yaxis.set_major_locator(yticks)
    ax9.yaxis.set_major_locator(yticks)

    ax7.set_xticks(np.arange(xMin-1, xMax, xStep))
    ax8.set_xticks(np.arange(xMin-1, xMax, xStep))
    ax9.set_xticks(np.arange(xMin-1, xMax, xStep))


    plt.savefig(directory + r'\Torsion Angles', dpi=300)


    """
    Fitness Graph
    """
    fig, ax = plt.subplots()

    ax.set_title("Fitness Variation vs. \nGeneration for Structure Solution of TFB",
        fontsize=fontSize)

    # ax.set_xlim(xMin, xMax)
    ax.set_xticks(np.arange(xMin-1, xMax, 200))

    yticks = ticker.MaxNLocator(M)

    # Set the yaxis major locator using your ticker object. You can also choose the minor
    # tick positions with set_minor_locator.
    ax7.yaxis.set_major_locator(yticks)


    ax.scatter(gen1, rwp, s=1, c=colour1)
    """
    Best Individual
    """
    ax.scatter(genBest, RwpBest, s=1, c=colour4, label="Best")

    """
    Worst Individual
    """
    ax.scatter(genWorst, RwpWorst, s=1, c=colour5, label="Worst")


    ax.set_ylabel("Rwp / %", fontsize=fontSize)
    ax.set_xlabel("Generation", fontsize=fontSize)

    ax.legend(loc="upper right")

    plt.savefig(directory + r'\Fitness', dpi=300)


# for i in range(5):
#     for x in range(5):
#         plotPopulation(100, r"C:/PhD/Year_4/Algorithm/Test/Exponent/DMIC/" + str(i+1) + "/(" + str(x+1) + ")/", 10, 0, 1600, 200, "red", "green", "blue", "lime", "cyan")
#
# for i in range(5):
#     for x in range(5):
#         plotPopulation(100, r"C:/PhD/Year_4/Algorithm/Test/Exponent/IMDC/" + str(i+1) + "/(" + str(x+1) + ")/", 10, 0, 1600, 200, "red", "green", "blue", "lime", "cyan")
#
# for x in range(10):
#     plotPopulation(100, r"C:/PhD/Year_4/Algorithm/Test/DynamicLiterature/ILMDHC/(" + str(x+1) + ")/", 10, 0, 1600, 200, "red", "green", "blue", "lime", "cyan")
#
# for x in range(15):
#     plotPopulation(100, "C:/PhD/Year_4/Algorithm/Test/DynamicLiterature/PhaseBoundaryTest/" + str(x+1), 10, 0, 500, 100, "red", "green", "blue", "lime", "cyan")

# for x in range(35):
#     plotPopulation(100, "C:/PhD/Year_4/Algorithm/Test/DynamicLiterature/PhaseBoundaryTest/Combinations/(" + str(x+1) + ")/", 10, 0, 500, 100, "red", "green", "blue", "lime", "cyan")

# for x in range(2):
#     plotPopulation(100, r"C:/PhD/Year_4/Algorithm/Test/DynamicLiterature/DHMILC/(" + str(x+11) + ")", 10, 0, 1600, 200, "red", "green", "blue", "lime", "cyan")

for x in range(5):
    plotPopulation(100, r"C:/PhD/Year_4/Algorithm/Test/ILMDHC_Modified/ScaleFactor/ILMDHC_SF0.5/(" + str(x+1) + ")", 10, 0, 1600, 200, "red", "green", "blue", "lime", "cyan")

for x in range(5):
    plotPopulation(100, r"C:/PhD/Year_4/Algorithm/Test/ILMDHC_Modified/ScaleFactor/ILMDHC_SF2/(" + str(x+1) + ")", 10, 0, 1600, 200, "red", "green", "blue", "lime", "cyan")

