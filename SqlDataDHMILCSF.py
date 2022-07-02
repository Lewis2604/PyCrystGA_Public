import sqlite3
from pprint import pprint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
import numpy as np



database = r"D:\PhD\Year_4\AlgorithmNew\DBTFB\Databases\TFB_DHMILCSF.db"
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

# selectQuery1 = """SELECT runid, DHMILCFactor From Runs;"""
#
# data1 = dataExtraction(selectQuery1, database)
#
# print(data1)
#
# runID1 = []
# ILMDHCSF1 = []
#
# for i in data1:
#     runID1.append(i[0])
#     ILMDHCSF1.append(i[1])
#
# print(runID1)
# print(ILMDHCSF1)
#
# bestFit1 = []
#
# for i in runID1:
#     selectQuery2 = """SELECT MAX(fitness) FROM ALLStructures WHERE runid = ?"""
#     cur.execute(selectQuery2, (i,))
#     data = cur.fetchall()
#     bestFit1.append(data[0][0])
#
# print(bestFit1)
#
# rwpBest1 = []
#
# for i in bestFit1:
#     rwpBest1.append(1/i)
#
# print(rwpBest1)

nVal = [0.5, 0.5, 0.5, 0.5, 0.5,
        1.0, 1.0, 1.0, 1.0, 1.0,
        1.5, 1.5, 1.5, 1.5, 1.5,
        2.0, 2.0, 2.0, 2.0, 2.0,
        2.5, 2.5, 2.5, 2.5, 2.5,
        3.0, 3.0, 3.0, 3.0, 3.0]
#
fitBest = [0.09807284409531603, 0.09410699547550505, 0.10016429237712143, 0.10616225677534265, 0.09765472223764625,
           0.12043328804311075, 0.0905221703505041, 0.12173920978757535, 0.10384524367853942, 0.09910920055882524,
           0.09810746289244641, 0.09733800131345953, 0.12226851510626464, 0.09774957602587643, 0.12114304706192713,
           0.08981221675528274, 0.1109221836413053, 0.08353454368482817, 0.09058699895209867, 0.10359067703630338,
           0.09580672640822833, 0.09344188763975565, 0.10134327244370762, 0.09564460942246886, 0.08998093025147087,
           0.09718165616939571, 0.09485291291588212, 0.07995840691605678, 0.08965565191695214, 0.08797210383474095]
#
rwpBest = [10.1965025, 10.6262026, 9.98359771, 9.41954354, 10.2401602,
           8.30335214, 11.0470175, 8.21428036, 9.62971403, 10.0898806,
           10.1929045, 10.2734799, 8.17872041, 10.2302234, 8.25470404,
           11.1343427, 9.01532919, 11.9710955, 11.0391117, 9.65337836,
           10.4376805, 10.7018386, 9.86745322, 10.4553723, 11.1134659,
           10.2900078, 10.5426388, 12.5065023, 11.1537865, 11.3672398]

# numEvals1 = []
#
# for i in fitBest:
#     selectQuery3 = """SELECT MIN(numEvals) from AllStructures WHERE fitness = ? GROUP BY runid"""
#     cur.execute(selectQuery3, (i,))
#     data = cur.fetchall()
#     numEvals1.append(data[0][0])
#
# print(numEvals1)
#
numEvals = [36029.0, 48689.0, 49011.0, 47238.0, 49054.0,
            43376.0, 47409.0, 46916.0, 21457.0, 40294.0,
            30128.0, 24816.0, 28640.0, 26455.0, 28310.0,
            20376.0, 20732.0, 20512.0, 20056.0, 23630.0,
            19106.0, 16040.0, 13967.0, 18256.0, 19081.0,
            13621.0, 13637.0, 14832.0, 12614.0, 15023.0]
#
nValSublists = list(chunks(nVal, 5))
fitBestSublists = list(chunks(fitBest, 5))
rwpBestSublists = list(chunks(rwpBest, 5))
numEvalsSublists = list(chunks(numEvals, 5))

print(nValSublists)
print(fitBestSublists)
print(rwpBestSublists)
print(numEvalsSublists)

for lst in rwpBestSublists:
    lst.sort()

for lst in numEvalsSublists:
    lst.sort()

print(rwpBestSublists)

rwpBest = []
rwpWorst = []
rwpAvg = []

for lst in rwpBestSublists:
    rwpBest.append(lst[0])
    rwpWorst.append(lst[-1])
    rwpAvg.append(listAvg(lst))

evalBest = []
evalWorst = []
evalAvg = []

for lst in numEvalsSublists:
    evalBest.append(lst[0])
    evalWorst.append(lst[-1])
    evalAvg.append(listAvg(lst))

nVals = []
for lst in nValSublists:
    nVals.append(listAvg(lst))

print(nVals)

print(rwpBest)
print(rwpWorst)
print(rwpAvg)

print(evalBest)
print(evalWorst)
print(evalAvg)

# X = nVals
#
# X_axis = np.arange(len(X))
#
# fig, ax = plt.subplots()
#
# rects1 = plt.bar(X_axis, rwpAvg, 0.1, label='avgRwp', color="g")
# rects2 = plt.bar(X_axis + 0.2, rwpBest, 0.1, label='bestRwp', color="b")
# rects3 = plt.bar(X_axis - 0.2, rwpWorst, 0.1, label='worstRwp', color="r")
#
# plt.legend(fontsize=6)
#
# plt.xticks(X_axis, X)
#
# plt.xlabel("Scale factor")
# plt.ylabel("$R_{wp}$")
#
# plt.title("$R_{wp}$" + "Variation with Changing Scale Factor - DHMILC")
#
# def autolabel(rects):
#     """Attach a text label above each bar in *rects*, displaying its height."""
#     for rect in rects:
#         height = rect.get_height()
#         ax.annotate('{}'.format(np.round(height, 2)),
#                     xy=(rect.get_x() + rect.get_width() / 2, height),
#                     xytext=(0, 3),  # 3 points vertical offset
#                     textcoords="offset points",
#                     ha='center', va='bottom', fontsize=6)
#
# 
# autolabel(rects1)
# autolabel(rects2)
# autolabel(rects3)
#
# plt.savefig(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\Graphs\DHMILCSF\DHMILCSF_rwp_V2", dpi=300)

X = nVals

X_axis = np.arange(len(X))

fig, ax = plt.subplots()

rects1 = plt.bar(X_axis, evalAvg, 0.1, label='avgEval', color="g")
rects2 = plt.bar(X_axis + 0.2, evalWorst, 0.1, label='maxEval', color="b")
rects3 = plt.bar(X_axis - 0.2, evalBest, 0.1, label='minEval', color="r")

plt.legend(fontsize=6)

plt.xticks(X_axis, X)

plt.xlabel("Scale factor")
plt.ylabel("NumEvals")

plt.title("Minimum Number of Fitness Evaluations \nto find Best Solution with Changing Scale Factor - DHMILC")

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(np.round(height, 2)),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=6)


autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

plt.savefig(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\Graphs\DHMILCSF\DHMILC_numEvals_V2", dpi=300)