import sqlite3
from pprint import pprint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
import numpy as np



database = r"D:\PhD\Year_4\AlgorithmNew\DBTFB\Databases\TFB.db"
conn = sqlite3.connect(database)
cur = conn.cursor()

def dataExtraction(query, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(query)
    data = cur.fetchall()
    return data

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def listAvg(lst):
    return sum(lst) / len(lst)

selectQuery1 = """SELECT runid FROM Runs;"""

data1 = dataExtraction(selectQuery1, database)


runIDs = []

for i in data1:
    runIDs.append(i[0])

# print(runIDs)

# selectQuery2 = """SELECT MAX(fitness), numEvals FROM AllStructures) WHERE runid = ?"""

# bestFit = []
# numEval = []

# for i in runIDs:
#     selectQuery2 = """SELECT MAX(fitness), numEvals FROM AllStructures WHERE runid = ?"""
#     cur.execute(selectQuery2, (i,))
#     data = cur.fetchall()
#     print(data)
#     bestFit.append(data[0][0])
#     numEval.append(data[0][1])
#
# print(bestFit)
# print(numEval)

bestFit1 = [0.10521709650800176, 0.10147065097847738, 0.12494735858453894, 0.1067031401332062, 0.0987503030646801, 0.0903447116022892, 0.09382679811388245, 0.09056718414551887, 0.08410195936203416, 0.07823194061807677, 0.12557848750594827, 0.09727222230609249, 0.09748600459235121, 0.1263238665419274, 0.09925739488187779, 0.10152541808692563, 0.09925514571429582, 0.0949748087867426, 0.12628254095555588, 0.0964513038296897, 0.07136470053134374, 0.0905504067537854, 0.08139738206809487, 0.07252195279398148, 0.08932107985076769, 0.10141447884941007, 0.09822337006052474, 0.10294381987107817, 0.11021909851695717, 0.0933053008131641, 0.10375381898094443, 0.10083313986814897, 0.09617068619582993, 0.09745525804739229, 0.09507756808314495, 0.1000095977210741, 0.09850507709943132, 0.09776920398347717, 0.12654858451991402, 0.09813221423879587, 0.09600927741488031, 0.11164480092262191, 0.1076853604126981, 0.09075367935835697, 0.11095425163366655, 0.11011613087214941, 0.10764970018939513, 0.09970110506012919, 0.08890120941116382, 0.09690490670145785, 0.11467555600079232, 0.11300109753332989, 0.10584303623789311, 0.09761731365665047, 0.09573014178485997, 0.1022422762813058, 0.09742907565187481, 0.11182922233810053, 0.11827472959454731, 0.09550500535047692, 0.1273898347327215, 0.10047542973891402, 0.12084789006593122, 0.12622448208476172, 0.11837082385706332, 0.09545204964377105, 0.09416110384836056, 0.09086901767229742, 0.1143436299223229, 0.09384387466718856, 0.08175055872214983, 0.07659911393362165, 0.08224388626706802, 0.08087371366618004, 0.08612275387874707, 0.08439601276101472, 0.08054108467175501, 0.08696336764667222, 0.09420766614129564, 0.09340590461502976, 0.10151192840683654, 0.08882956416316204, 0.09683938988666548, 0.08914949624338733, 0.09254442750254176, 0.08441543438633513, 0.08243737508779787, 0.089133543431197, 0.0918421545993132, 0.10185756739118962, 0.09230904058774052, 0.0829078165646982, 0.09059338695634422, 0.08749273963373334, 0.08493162116960407, 0.07286662498064207, 0.08060840190884888, 0.07953564355267809, 0.0819716449587717, 0.08484734943668149, 0.0821285249819574, 0.09395256907897874, 0.09094591491003798, 0.08203290264254723, 0.08477275349448125, 0.07929929682220835, 0.08484518185126605, 0.08220595538084342, 0.08411138042453638, 0.08748810325835879, 0.07279383064132405, 0.07987776848257935, 0.08208380239096162, 0.07996728314538129, 0.08069831740215395, 0.08325921736568802, 0.08419888382591645, 0.08852036013871176, 0.08141396915862995, 0.08410217367870923, 0.07524362361643624, 0.08175394722159741, 0.08011050314627191, 0.07786005136941465, 0.077415367198118]
numEval1 = [38399.0, 32511.0, 37998.0, 38046.0, 38117.0, 31058.0, 31131.0, 29627.0, 31062.0, 3749.0, 22334.0, 23717.0, 22896.0, 23406.0, 23903.0, 12295.0, 15453.0, 16671.0, 9587.0, 16499.0, 8190.0, 8451.0, 8704.0, 8933.0, 8995.0, 40406.0, 47070.0, 44871.0, 43077.0, 26621.0, 41256.0, 40172.0, 39024.0, 35805.0, 41431.0, 32131.0, 31329.0, 31728.0, 32795.0, 33548.0, 25994.0, 26589.0, 25908.0, 26620.0, 25621.0, 18951.0, 18902.0, 18046.0, 17915.0, 19073.0, 58607.0, 54136.0, 50788.0, 49740.0, 53234.0, 41784.0, 38679.0, 49580.0, 47833.0, 47915.0, 42448.0, 42559.0, 43372.0, 40868.0, 39117.0, 33630.0, 35558.0, 32572.0, 35281.0, 35051.0, 20542.0, 21840.0, 16677.0, 17019.0, 26412.0, 65015.0, 36114.0, 24570.0, 60563.0, 39765.0, 50844.0, 37913.0, 48883.0, 49482.0, 50543.0, 46694.0, 21456.0, 39171.0, 31428.0, 42608.0, 32680.0, 24481.0, 16516.0, 18076.0, 31916.0, 23218.0, 31501.0, 33588.0, 36864.0, 18261.0, 48677.0, 74335.0, 5510.0, 45367.0, 44595.0, 63255.0, 69857.0, 64862.0, 42639.0, 16855.0, 52832.0, 53445.0, 38928.0, 21188.0, 20116.0, 47039.0, 42891.0, 17139.0, 52050.0, 29024.0, 43899.0, 35271.0, 23470.0, 16708.0, 21213.0]
bestRwp1 = []

for i in bestFit1:
    bestRwp1.append(1/i)

bestFit2 = list(chunks(bestFit1, 5))
numEval2 = list(chunks(numEval1, 5))
bestRwp2 = list(chunks(bestRwp1, 5))

# print(bestFit2)
# print(numEval2)

bestFitAvg1 = []
numEvalAvg1 = []
bestRwpAvg1 = []

for lst in bestFit2:
    bestFitAvg1.append(listAvg(lst))

for lst in numEval2:
    numEvalAvg1.append(listAvg(lst))

for lst in bestRwp2:
    bestRwpAvg1.append(listAvg(lst))

# print("Here1")
# print(bestFitAvg1)
# print(numEvalAvg1)
# print(bestRwpAvg1)

numEvalAvg1Chunks = list(chunks(numEvalAvg1, 5))
bestRwpAvg1Chunks = list(chunks(bestRwpAvg1, 5))

xOverRates1 = []
mutRates1 = []

for i in runIDs:
    selectQuery3 = """SELECT MAX(crossoverRate), (mutationRate) FROM Generation WHERE id = ?"""
    cur.execute(selectQuery3, (i, ))
    data = cur.fetchall()
    xOverRates1.append(data[0][0])
    mutRates1.append(data[0][1])

# print(xOverRates1)
# print(mutRates1)

xOverRates2 = list(chunks(xOverRates1, 5))
mutRates2 = list(chunks(mutRates1, 5))

xOverRates2Avg = []
mutRates2Avg = []

for lst in xOverRates2:
    xOverRates2Avg.append(listAvg(lst))

for lst in mutRates2:
    mutRates2Avg.append(listAvg(lst))

print("Rates")
print(xOverRates2Avg)
print(mutRates2Avg)

comparison1 = list(zip(xOverRates2Avg, mutRates2Avg, bestRwpAvg1))
comparison2 = list(zip(xOverRates2Avg, mutRates2Avg, numEvalAvg1))

pprint(comparison2)

"""2D contour plot Rwp"""
# #
xTicks = [0.9, 0.7, 0.5, 0.3, 0.1]
yTicks = [0.1, 0.3, 0.5, 0.7, 0.9]

X, Y = np.meshgrid(xTicks, yTicks)

print("X")
print(X)
print("Y")
print(Y)

fig,ax=plt.subplots(1,1)

ax.set_yticks(yTicks)
ax.set_xticks(xTicks)

ax.set_xlabel("CR")
ax.set_ylabel("MR")

cp = ax.contourf(X, Y, bestRwpAvg1Chunks, 25)
cbar = fig.colorbar(cp) # Add a colorbar to a plot
cbar.set_label("$R_{wp}$ / %")
plt.title("$R_{wp}$ of Best Solution - TFB")

plt.savefig(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\Graphs\Static\contourPlot1RwpBest_fixedV2", dpi=300)

"""2D contour plot numEvals"""
#
# xTicks = [0.9, 0.7, 0.5, 0.3, 0.1]
# yTicks = [0.1, 0.3, 0.5, 0.7, 0.9]
#
# X, Y = np.meshgrid(xTicks, yTicks)
#
# print("X")
# print(X)
# print("Y")
# print(Y)
#
# fig,ax=plt.subplots(1,1)
#
# ax.set_yticks(yTicks)
# ax.set_xticks(xTicks)
#
# ax.set_xlabel("CR")
# ax.set_ylabel("MR")
#
# cp = ax.contourf(X, Y, numEvalAvg1Chunks, 25)
# cbar = fig.colorbar(cp) # Add a colorbar to a plot
# cbar.set_label("numEval")
# plt.title("Average numEvals to find Best Solution - TFB")
#
# plt.savefig(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\Graphs\Static\contourNumEvals_fixedV2", dpi=300)


