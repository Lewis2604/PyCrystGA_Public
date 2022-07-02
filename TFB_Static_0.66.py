import sqlite3
from pprint import pprint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
import numpy as np



database = r"D:\PhD\Year_4\AlgorithmNew\DBTFB\Databases\TFB_Static_Polynomial_bounded_0.66.db"
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
#
#
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
# #
# print(bestFit)
# print(numEval)

bestFit1 = [0.0810218468847355, 0.09961251131548322, 0.09360222256605438, 0.09624685670999927, 0.0896883662018325,
            0.08784292329020975, 0.08108795186048319, 0.08843340028007035, 0.0815849854517246, 0.08435149097586661,
            0.08511392878124352, 0.08611073313283195, 0.0869902686683139, 0.09118136177102508, 0.09988752764274954,
            0.09302118425381299, 0.08957843180682876, 0.08851557504125623, 0.08147782391178911, 0.08047380141595907,
            0.08341590395612938, 0.07539692428048998, 0.07569847990412394, 0.08677122443022305, 0.08014049076818411,
            0.10272982864167371, 0.09876007418185205, 0.0832751274890155, 0.09269076498643058, 0.08350542548945328,
            0.07683312719901693, 0.074020983483202, 0.08273395889472461, 0.07975027064051846, 0.08850390790332906,
            0.07502992024402011, 0.07872998581411624, 0.08526577337297066, 0.06941466218004534, 0.09023801539893685,
            0.0730810680102358, 0.07070228573348845, 0.06721968661348576, 0.07365237657364195, 0.0832950092995546,
            0.0888715664381435, 0.07146437303762405, 0.08444737364234486, 0.08622642832440218, 0.08312779984820864]

numEval1 = [37269.0, 37076.0, 48840.0, 32428.0, 49129.0,
            21630.0, 37647.0, 39243.0, 36363.0, 22090.0,
            17465.0, 26987.0, 12765.0, 22779.0, 20503.0,
            17925.0, 9304.0, 7708.0, 15837.0, 10641.0,
            7182.0, 9306.0, 1907.0, 7261.0, 9079.0,
            55199.0, 46926.0, 14672.0, 59134.0, 6154.0,
            10057.0, 39756.0, 40830.0, 45475.0, 4140.0,
            1887.0, 2358.0, 2839.0, 774.0, 2411.0,
            17573.0, 1857.0, 6419.0, 20989.0, 1799.0,
            16185.0, 11601.0, 13644.0, 13326.0, 17189.0]

bestRwp1 = [12.3423501, 10.0388996, 10.683507, 10.3899497, 11.1497181,
            11.3839563, 12.332288299999998, 11.3079447, 12.2571573, 11.855155000000002,
            11.7489583, 11.6129542, 11.4955387, 10.9671536, 10.0112599,
            10.7502394, 11.1634015, 11.2974468, 12.2732782, 12.4264044,
            11.9881216, 13.263140499999999, 13.210304899999999, 11.5245579, 12.4780868,
            9.73427108, 10.1255493, 12.0083875, 10.7885613, 11.9752698,
            13.015219299999998, 13.509682700000003, 12.086935200000001, 12.539142399999998, 11.2989361,
            13.3280163, 12.7016408, 11.7280353, 14.406178300000002, 11.081804,
            13.6834344, 14.1438143, 14.876594200000001, 13.577294400000001, 12.0055212,
            11.2521928, 13.9929864, 11.8416945, 11.5973724, 12.02967]

# for i in bestFit1:
#     bestRwp1.append(1/i)
#
# print(bestRwp1)

#
bestFit2 = list(chunks(bestFit1, 5))
numEval2 = list(chunks(numEval1, 5))
bestRwp2 = list(chunks(bestRwp1, 5))
#
# # print(bestFit2)
# # print(numEval2)
#
bestFitAvg1 = []
numEvalAvg1 = []
bestRwpAvg1 = []
#
for lst in bestFit2:
    bestFitAvg1.append(listAvg(lst))

for lst in numEval2:
    numEvalAvg1.append(listAvg(lst))

for lst in bestRwp2:
    bestRwpAvg1.append(listAvg(lst))
#
# # print("Here1")
# # print(bestFitAvg1)
# # print(numEvalAvg1)
# # print(bestRwpAvg1)
#
numEvalAvg1Chunks = list(chunks(numEvalAvg1, 5))
bestRwpAvg1Chunks = list(chunks(bestRwpAvg1, 5))
#
xOverRates1 = []
mutRates1 = []

for i in runIDs:
    selectQuery3 = """SELECT MAX(crossoverRate), (mutationRate) FROM Generation WHERE id = ?"""
    cur.execute(selectQuery3, (i, ))
    data = cur.fetchall()
    xOverRates1.append(data[0][0])
    mutRates1.append(data[0][1])
#
# # print(xOverRates1)
# # print(mutRates1)
#
xOverRates2 = list(chunks(xOverRates1, 5))
mutRates2 = list(chunks(mutRates1, 5))
#
xOverRates2Avg = []
mutRates2Avg = []
#
for lst in xOverRates2:
    xOverRates2Avg.append(listAvg(lst))

for lst in mutRates2:
    mutRates2Avg.append(listAvg(lst))
#
# print("Rates")
# print(xOverRates2Avg)
# print(mutRates2Avg)
#
comparison1 = list(zip(xOverRates2Avg, mutRates2Avg, bestRwpAvg1))
comparison2 = list(zip(xOverRates2Avg, mutRates2Avg, numEvalAvg1))
#
pprint(comparison2)
"""2D contour plot Rwp"""
# #
# xTicks = [0.9, 0.7, 0.5, 0.3, 0.1]
# yTicks = [0.1, 0.3]
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
# cp = ax.contourf(X, Y, bestRwpAvg1Chunks, 25)
# cbar = fig.colorbar(cp) # Add a colorbar to a plot
# cbar.set_label("$R_{wp}$ / %")
# plt.title("$R_{wp}$ of Best Solution - TFB")
#
# plt.savefig(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\Graphs\Static\indpb_0.66\rwp", dpi=300)

"""2D contour plot numEvals"""
#
xTicks = [0.9, 0.7, 0.5, 0.3, 0.1]
yTicks = [0.1, 0.3]

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

cp = ax.contourf(X, Y, numEvalAvg1Chunks, 25)
cbar = fig.colorbar(cp) # Add a colorbar to a plot
cbar.set_label("numEval")
plt.title("Average numEvals to find Best Solution - TFB")

plt.savefig(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\Graphs\Static\indpb_0.66\numEvals", dpi=300)


