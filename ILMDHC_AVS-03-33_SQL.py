import sqlite3
from pprint import pprint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
import numpy as np



database = r"D:\PhD\Year_4\AlgorithmNew\DBAVS_03_33\Databases\DBAVS_03_33_ILMDHCSF.db"
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

# selectQuery1 = """SELECT runid, ILMDHCFactor From Runs;"""
#
# data1 = dataExtraction(selectQuery1, database)
#
# print(data1)
# #
# runID1 = []
# ILMDHCSF1 = []
#
# for i in data1:
#     runID1.append(i[0])
#     ILMDHCSF1.append(i[1])
#
# print(runID1)
# print(ILMDHCSF1)

runIDs = ['a8f6d133ef063438ad5d594dbab0b613d7af6cc9b89b30372af3a0ca14e9b050', '6bed2e96536557b26bcc3d21d79ae7309f93195c305bb2ff3805b07853c59a27', '9a83c9e1b050870a9f38b0eb1aef409dca55c1c04d0446ea6b33196eb8d97449', 'fe26ea45a482c715b660b90d9f30026532ca54782fedc5f3eceaf9d270d934e5', 'e2ea1c0cdb558906c489634a5a7092f01d73bf7ab4ea6eb3055b201a2c212555',
          '08901c4b5a967bab1a94a110088229c68ea6447715bda3a20db475c64b76cca1', '9337052db0861bfaa62f3d5d60cd9d234e540242a87cad0909109ffc565d53ce', '6279c56e7e520eeca489b04fdc1350bb17193e387da5ad4d63fc5fad0c1dbc27', '2eb1f0596cd3440763bcf8a2bf07caaa46a7d49a823593b18d3d76a39768778f', '9534c9c4307eacee9d4dc2d6e131b4e0ae7065b0b0ea7df9af5da7e28db8fb1c',
          '2dcccb24a08cce2bb9e9d784c9ed1880bf92edad3e9c84dc8ba66f2aec04f771', '5ff43d3cd3dd04c975cb4a66ea79b7f7050861ecfb368e19807dcffc8ea86aca', 'f16d91ddcb2bd473e7d3c8894c375426a7b0ec375ef681a35f87f4b26d8c2d94', '25a6f62f03d3c96b4c278375610afbde12ac82306d81fd9bb6202d912fe2f74a', 'd86647e7fdd3d5de3df2b541c00e78bbbc196b63d0102485e6cf91853b7a3a1a',
          'da5b30ea0aa1c53b1a070414e0790d6514b56f21b1dc8f03307fcb1cac263664', 'af68595de56dfb0547e13d82e83bb4bca710064a131e7288ce5c020ad65463e3', '618e55c500023a3db1e80ebd1b4ef72785a43d718d37c86f09db9e9b967c8b6b', '09bab55c649a03423f3ffc7e4e77badabeb4f9c87b5b702a50f9e28fe11386e7', '47aea4e42d49171ede1718f2e9be5db56d63674972fc59d55f1c659bb5ba5b94']

nVals = [0.5, 0.5, 0.5, 0.5, 0.5,
             1.0, 1.0, 1.0, 1.0, 1.0,
             1.5, 1.5, 1.5, 1.5, 1.5,
             2.0, 2.0, 2.0, 2.0, 2.0]

#
# bestFit1 = []
#
# for i in runIDs:
#     selectQuery2 = """SELECT MAX(fitness) FROM ALLStructures WHERE runid = ?"""
#     cur.execute(selectQuery2, (i,))
#     data = cur.fetchall()
#     bestFit1.append(data[0][0])
#
# print(bestFit1)
# #
# rwpBest1 = []
#
# for i in bestFit1:
#     rwpBest1.append(1/i)
#
# print(rwpBest1)

# nVal = [0.5, 0.5, 0.5, 0.5, 0.5,
#         1.0, 1.0, 1.0, 1.0, 1.0,
#         1.5, 1.5, 1.5, 1.5, 1.5,
#         2.0, 2.0, 2.0, 2.0, 2.0,
#         2.5, 2.5, 2.5, 2.5, 2.5,
#         3.0, 3.0, 3.0, 3.0, 3.0]
#
fitBest = [0.06943484266651376, 0.06881143893836336, 0.0709691203847344, 0.06951759529962062, 0.06662585477723669,
           0.0670483343933228, 0.07289828042943532, 0.06396058063363931, 0.06421758850651069, 0.06808356833171252,
           0.07169417221948188, 0.06829318030106434, 0.06979044365457016, 0.06452669559088701, 0.06465144910339883,
           0.06205203742187113, 0.06492475454677145, 0.06731028809011964, 0.06942400582428532, 0.06978102498039973]
#
rwpBest = [14.4019913, 14.5324675, 14.090635399999998, 14.384847400000002, 15.0091883,
           14.9146136, 13.717744699999999, 15.634629799999999, 15.572057799999998, 14.6878318,
           13.948135099999998, 14.6427505, 14.328609300000002, 15.497461800000002, 15.4675574,
           16.1155063, 15.402445600000002, 14.8565699, 14.4042394, 14.3305433]
#
# numEvals1 = []

# test1 = list(zip(runIDs, fitBest))

# pprint(test1)

# minEvals = []
#
# for i in test1:
#     selectQuery4 = """SELECT MIN(numEvals) from AllStructures WHERE fitness = ? AND runid = ?"""
#     cur.execute(selectQuery4, (i[1], i[0]))
#     data = cur.fetchall()
#     minEvals.append(data[0][0])
#
# print(minEvals)

# for i in fitBest:
#     selectQuery3 = """SELECT MIN(numEvals) from AllStructures WHERE fitness = ? GROUP BY runid"""
#     cur.execute(selectQuery3, (i,))
#     data = cur.fetchall()
#     numEvals1.append(data[0][0])
#
# print(numEvals1)

numEvals = [44743.0, 48681.0, 49038.0, 48588.0, 43860.0,
            29672.0, 26444.0, 27408.0, 37934.0, 28794.0,
            18631.0, 17041.0, 14519.0, 20560.0, 2257.0,
            38026.0, 5113.0, 14025.0, 13080.0, 13027.0]
#
nValSublists = list(chunks(nVals, 5))
fitBestSublists = list(chunks(fitBest, 5))
rwpBestSublists = list(chunks(rwpBest, 5))
numEvalsSublists = list(chunks(numEvals, 5))
#
# print(nValSublists)
# print(fitBestSublists)
# print(rwpBestSublists)
# print(numEvalsSublists)
#
for lst in rwpBestSublists:
    lst.sort()
#
for lst in numEvalsSublists:
    lst.sort()
#
# print(rwpBestSublists)
#
rwpBest = []
rwpWorst = []
rwpAvg = []
#
for lst in rwpBestSublists:
    rwpBest.append(lst[0])
    rwpWorst.append(lst[-1])
    rwpAvg.append(listAvg(lst))
#
evalBest = []
evalWorst = []
evalAvg = []
#
for lst in numEvalsSublists:
    evalBest.append(lst[0])
    evalWorst.append(lst[-1])
    evalAvg.append(listAvg(lst))
#
nVals1 = []
for lst in nValSublists:
    nVals1.append(listAvg(lst))
#
print(nVals1)

print(rwpBest)
print(rwpWorst)
print(rwpAvg)

print(evalBest)
print(evalWorst)
print(evalAvg)

# X = nVals1
#
# X_axis = np.arange(len(X))
#
# fig, ax = plt.subplots()
#
# rects1 = plt.bar(X_axis, rwpAvg, 0.1, label='avgRwp', color="g")
# rects2 = plt.bar(X_axis + 0.2, rwpBest, 0.1, label='bestRwp', color="b")
# rects3 = plt.bar(X_axis - 0.2, rwpWorst, 0.1, label='worstRwp', color="r")
#
# print(rects1)
# print(rects2)
# print(rects3)
#
# plt.legend(fontsize=6)
#
# plt.xticks(X_axis, X)
#
# plt.xlabel("Scale factor")
# plt.ylabel("$R_{wp}$")
#
# plt.title("$R_{wp}$" + "Variation with Changing Scale Factor - ILMDHC")
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
# plt.savefig(r"D:\PhD\Year_4\AlgorithmNew\DBAVS_03_33\Graphs\ILMDHCSF\ILMDHCSF_rwp", dpi=300)


X = nVals1

X_axis = np.arange(len(X))

fig, ax = plt.subplots()

rects1 = plt.bar(X_axis, evalAvg, 0.1, label='avgEval', color="g")
rects2 = plt.bar(X_axis + 0.2, evalWorst, 0.1, label='maxEval', color="b")
rects3 = plt.bar(X_axis - 0.2, evalBest, 0.1, label='minEval', color="r")

plt.legend(fontsize=6)

plt.xticks(X_axis, X)

plt.xlabel("Scale factor")
plt.ylabel("NumEvals")

plt.title("Minimum Number of Fitness Evaluations \nto find Best Solution with Changing Scale Factor - ILMDHC")

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

plt.savefig(r"D:\PhD\Year_4\AlgorithmNew\DBAVS_03_33\Graphs\ILMDHCSF\numEvals", dpi=300)