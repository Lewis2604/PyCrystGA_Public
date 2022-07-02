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

qwerty = [1, 2, 3, 4, 5, 6, 7, 8, 9]

if (len(qwerty) % 2) != 0:
    qwerty.remove(qwerty[-1])

qwerty1 = chunks(qwerty, 2)
qwerty2 = list(qwerty1)
print(qwerty1)
print(qwerty2)


# selectQuery1 = """SELECT runid, MAX(fitness) FROM AllStructures GROUP BY runid;"""
selectQuery2 = """SELECT id, MAX(crossoverRate), MAX(mutationRate) FROM Generation GROUP BY crossoverRate, mutationRate, id;"""
#
#
# bestFit = dataExtraction(selectQuery1, database)
GORates = dataExtraction(selectQuery2, database)
#
# print(len(bestFit))
# print(bestFit)
# print(len(GORates))
# print(GORates)
#
idOrder = []
for i in GORates:
    idOrder.append(i[0])
#
# print(idOrder)
#
bestFit2 = []
for i in idOrder:
    selectQuery3 = """SELECT MAX(fitness) FROM AllStructures WHERE runid = ?"""
    cur.execute(selectQuery3, (i,))
    data = cur.fetchall()
    # print(data)
    bestFit2.append(data[0][0])
#
# print(len(bestFit2))
print(bestFit2)
#
# repeatBest = list(chunks(bestFit2, 5))
# print(repeatBest)
#
# averageBest = []
# avgRwp = []
#
# for lst in repeatBest:
#     averageBest.append(listAvg(lst))
#     avgRwp.append(1/listAvg(lst))
#
# print(averageBest)
# print(avgRwp)
#
# xOverRates = []
# mutRates = []
#
# for i in GORates:
#     xOverRates.append(i[1])
#     mutRates.append(i[2])
#
# print("All Rates")
# print(xOverRates)
# print(mutRates)
#
# repXover = list(chunks(xOverRates, 5))
# repMut = list(chunks(mutRates, 5))
#
# print(repXover)
# print(repMut)
#
# avgXover = []
# avgMut = []
#
# for lst in repXover:
#     avgXover.append(listAvg(lst))
#
# for lst in repMut:
#     avgMut.append(listAvg(lst))
#
#
#
# print("X")
# print(avgXover)
# print("Y")
# print(avgMut)
# print("Z")
# print(avgRwp)

def functionZ(x, y):
    return


avgXoverX = [0.1, 0.1, 0.1, 0.1, 0.1,
             0.3, 0.3, 0.3, 0.3, 0.3,
             0.5, 0.5, 0.5, 0.5, 0.5,
             0.7, 0.7, 0.7, 0.7, 0.7,
             0.9, 0.9, 0.9, 0.9, 0.9]

avgMutY = [0.1, 0.3, 0.5, 0.7, 0.9,
           0.1, 0.3, 0.5, 0.7, 0.9,
           0.1, 0.3, 0.5, 0.7, 0.9,
           0.1, 0.3, 0.5, 0.7, 0.9,
           0.1, 0.3, 0.5, 0.7, 0.9]

avgRwpZ = [12.340940030492817, 9.934964683291414, 12.267228526985104, 12.505325241514, 12.742635954134702,
           9.643402085256847, 9.670293850431483, 10.231860596395277, 11.40941391655425, 11.8625480624449,
           9.158885073191879, 9.59757967352461, 8.427319569924913, 11.118867759376851, 12.644750718655464,
           11.439747242101735, 10.136015780084932, 9.518727262896595, 10.663827388156962, 11.963155841901044,
           9.309451871215835, 9.87935200749671, 9.490058443430987, 11.376200968171911, 11.525181025166122]

"""3D Surface Plot"""

# data = list(zip(avgXoverX, avgMutY, avgRwpZ))
#
# x, y, z = zip(*data)
#
# grid_x, grid_y = np.mgrid[min(x):max(x):100j, min(y):max(y):100j]
# grid_z = griddata((x, y), z, (grid_x, grid_y), method='cubic')
#
# fig = plt.figure()
# ax = fig.gca(projection='3d')
# ax.plot_surface(grid_x, grid_y, grid_z, cmap=plt.cm.Spectral)
#
# xTicks = [0.1, 0.3, 0.5, 0.7, 0.9]
# yTicks = [0.1, 0.3, 0.5, 0.7, 0.9]
#
# ax.set_yticks(yTicks)
# ax.set_xticks(xTicks)
#
# ax.set_xlabel("CR")
# ax.set_ylabel("MR")
# ax.set_zlabel("Rwp")
#
# plt.savefig(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\contourPlot2", dpi=300)

""""""


"""2D Contour Plot"""
# avgRwpZ1 = [[12.340940030492817, 9.934964683291414, 12.267228526985104, 12.505325241514, 12.742635954134702],
#            [9.643402085256847, 9.670293850431483, 10.231860596395277, 11.40941391655425, 11.8625480624449],
#            [9.158885073191879, 9.59757967352461, 8.427319569924913, 11.118867759376851, 12.644750718655464],
#            [11.439747242101735, 10.136015780084932, 9.518727262896595, 10.663827388156962, 11.963155841901044],
#            [9.309451871215835, 9.87935200749671, 9.490058443430987, 11.376200968171911, 11.525181025166122]]
#
# xTicks = [0.1, 0.3, 0.5, 0.7, 0.9]
# yTicks = [0.1, 0.3, 0.5, 0.7, 0.9]
#
# X, Y = np.meshgrid(xTicks, yTicks)
#
# print(X)
# print(Y)
#
# fig,ax=plt.subplots(1,1)
#
# ax.set_yticks(yTicks)
# ax.set_xticks(xTicks)
#
# ax.set_xlabel("MR")
# ax.set_ylabel("CR")
#
# cp = ax.contourf(X, Y, avgRwpZ1, 25)
# fig.colorbar(cp) # Add a colorbar to a plot
# plt.title("Rwp of Best Solution - TFB")
#
# plt.savefig(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\contourPlot1RwpBest", dpi=300)
#
# fig = plt.figure()




# ax = fig.add_subplot(projection='3d')
#
# """ Each perf list has the same crossover rate """
# perf1 = [12.340940030492817, 9.934964683291414, 12.267228526985104, 12.505325241514, 12.742635954134702]
# perf2 = [9.643402085256847, 9.670293850431483, 10.231860596395277, 11.40941391655425, 11.8625480624449]
# perf3 = [9.158885073191879, 9.59757967352461, 8.427319569924913, 11.118867759376851, 12.644750718655464]
# perf4 = [11.439747242101735, 10.136015780084932, 9.518727262896595, 10.663827388156962, 11.963155841901044]
# perf5 = [9.309451871215835, 9.87935200749671, 9.490058443430987, 11.376200968171911, 11.525181025166122]
#
# xTicks = [0.1, 0.3, 0.5, 0.7, 0.9]
# yTicks = [0.1, 0.3, 0.5, 0.7, 0.9]
#
# colours = ['b', 'g', 'r', 'c', 'm']
#
# ax.bar(xTicks, perf1, zs=0.1, zdir='y', alpha=0.5, width=0.1)
# ax.bar(xTicks, perf2, zs=0.3, zdir='y', alpha=0.5, width=0.1)
# ax.bar(xTicks, perf3, zs=0.5, zdir='y', alpha=0.5, width=0.1)
# ax.bar(xTicks, perf4, zs=0.7, zdir='y', alpha=0.5, width=0.1)
# ax.bar(xTicks, perf5, zs=0.9, zdir='y', alpha=0.5, width=0.1)
#
# ax.set_yticks(yTicks)
# ax.set_xticks(xTicks)
#
#
# plt.savefig(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\barChart", dpi=300)

"""2D Contour Plot numEvals"""

# selectQuery1 = """SELECT runid, MAX(fitness), numEvals FROM AllStructures GROUP BY runid;"""
# selectQuery2 = """SELECT id, MAX(crossoverRate), MAX(mutationRate) FROM Generation GROUP BY crossoverRate, mutationRate, id;"""
#
# data1 = dataExtraction(selectQuery1, database)
# data2 = dataExtraction(selectQuery2, database)
#
# runID1 = []
# bestFit1 = []
# numEvals1 = []
#
# for i in data1:
#     runID1.append(i[0])
#     bestFit1.append(i[1])
#     numEvals1.append(i[2])
#
# repRunID1 = list(chunks(runID1, 5))
# repBestFit1 = list(chunks(bestFit1, 5))
# repNumEvals1 = list(chunks(numEvals1, 5))
#
# # avgRunID1 = []
# avgBestFit1 = []
# avgNumEvals1 = []
#
# # for lst in repRunID1:
# #     avgRunID1.append(listAvg(lst))
#
# for lst in repBestFit1:
#     avgBestFit1.append(listAvg(lst))
#
# for lst in repNumEvals1:
#     avgNumEvals1.append(listAvg(lst))
#
# print(data1)
# print(data2)
#
# print(runID1)
# print(repRunID1)
# # print(avgRunID1)
#
# print(bestFit1)
# print(repBestFit1)
# print(avgBestFit1)
#
# print(numEvals1)
# print(repNumEvals1)
# print(avgNumEvals1)
#
#
#
# avgRwpZ1 = [[12.340940030492817, 9.934964683291414, 12.267228526985104, 12.505325241514, 12.742635954134702],
#            [9.643402085256847, 9.670293850431483, 10.231860596395277, 11.40941391655425, 11.8625480624449],
#            [9.158885073191879, 9.59757967352461, 8.427319569924913, 11.118867759376851, 12.644750718655464],
#            [11.439747242101735, 10.136015780084932, 9.518727262896595, 10.663827388156962, 11.963155841901044],
#            [9.309451871215835, 9.87935200749671, 9.490058443430987, 11.376200968171911, 11.525181025166122]]
#
# avgNumEvalsZ2 = [[42837.0, 34648.8, 42976.4, 35189.4, 29622.6],
#                  [41921.6, 42176.4, 42600.2, 42227.8, 31354.8],
#                  [30060.6, 31047.0, 37170.6, 40260.0, 32441.8],
#                  [33957.8, 25036.4, 31766.0, 26525.8, 30846.2],
#                  [33772.0, 33472.2, 21800.4, 23045.2, 24277.4]]
#
# ratioRwpEvals = list(zip(avgRwpZ1, avgNumEvalsZ2))
#
# print("ratio")
# print(ratioRwpEvals)
#
#
# xTicks = [0.1, 0.3, 0.5, 0.7, 0.9]
# yTicks = [0.1, 0.3, 0.5, 0.7, 0.9]
#
# X, Y = np.meshgrid(xTicks, yTicks)
#
# print(X)
# print(Y)
#
# fig,ax=plt.subplots(1,1)
#
# ax.set_yticks(yTicks)
# ax.set_xticks(xTicks)
#
# ax.set_xlabel("MR")
# ax.set_ylabel("CR")
#
# cp = ax.contourf(X, Y, avgNumEvalsZ2, 25)
# fig.colorbar(cp) # Add a colorbar to a plot
# plt.title("NumEvals to Find Best Solution - TFB")
#
# plt.savefig(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\contourPlot1NumEvals", dpi=300)
#
# fig = plt.figure()

"""2D Contour Plot Best/numEvals"""
# avgRwpZ1 = [[12.340940030492817, 9.934964683291414, 12.267228526985104, 12.505325241514, 12.742635954134702],
#            [9.643402085256847, 9.670293850431483, 10.231860596395277, 11.40941391655425, 11.8625480624449],
#            [9.158885073191879, 9.59757967352461, 8.427319569924913, 11.118867759376851, 12.644750718655464],
#            [11.439747242101735, 10.136015780084932, 9.518727262896595, 10.663827388156962, 11.963155841901044],
#            [9.309451871215835, 9.87935200749671, 9.490058443430987, 11.376200968171911, 11.525181025166122]]
#
# avgNumEvalsZ2 = [[42837.0, 34648.8, 42976.4, 35189.4, 29622.6],
#                  [41921.6, 42176.4, 42600.2, 42227.8, 31354.8],
#                  [30060.6, 31047.0, 37170.6, 40260.0, 32441.8],
#                  [33957.8, 25036.4, 31766.0, 26525.8, 30846.2],
#                  [33772.0, 33472.2, 21800.4, 23045.2, 24277.4]]
#
# ratioList = np.divide(avgRwpZ1, avgNumEvalsZ2)
# print(ratioList)
#
# xTicks = [0.1, 0.3, 0.5, 0.7, 0.9]
# yTicks = [0.1, 0.3, 0.5, 0.7, 0.9]
#
# X, Y = np.meshgrid(xTicks, yTicks)
#
# print(X)
# print(Y)
#
# fig,ax=plt.subplots(1,1)
#
# ax.set_yticks(yTicks)
# ax.set_xticks(xTicks)
#
# ax.set_xlabel("MR")
# ax.set_ylabel("CR")
#
# cp = ax.contourf(X, Y, ratioList, 25)
# fig.colorbar(cp) # Add a colorbar to a plot
# plt.title("Best/NumEvals to Find Best Solution - TFB")
#
# plt.savefig(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\contourPlot1Best-NumEvals", dpi=300)
#
# fig = plt.figure()

# selectQuery1 = """SELECT runid, MAX(fitness) FROM AllStructures GROUP BY runid;"""


#@todo---------------------------------------------------------------------------------------------------------


# selectQuery1 = """SELECT runid, logNval FROM Runs;"""

# data1 = dataExtraction(selectQuery1, database)
#
# pprint(data1)
#
# runID = []
# nVal = []

# for i in data1:
#     runID.append(i[0])
#     nVal.append(i[1])

# print(runID)
# print(nVal)
#
# numEvals = []
#
# for i in runID:
#     selectQuery2 = """SELECT MAX(numEvals) FROM ALLStructures WHERE runid = ?"""
#     cur.execute(selectQuery2, (i,))
#     data = cur.fetchall()
#     # print(data)
#     numEvals.append(data[0][0])
#
# maxGen = []
#
# for i in runID:
#     selectQuery3 = """SELECT MAX(genID) FROM ALLStructures WHERE runid = ?"""
#     cur.execute(selectQuery3, (i,))
#     data = cur.fetchall()
#     # print(data)
#     maxGen.append(data[0][0])

# print(numEvals)
#
# zip = zip(runID, maxGen, numEvals)
# lstZip = list(zip)
#
# pprint(lstZip)
#
#
# bestFitness = []

# for i in runID:
#     selectQuery4 = """SELECT MAX(fitness) FROM ALLStructures WHERE runid = ?"""
#     cur.execute(selectQuery4, (i,))
#     data = cur.fetchall()
#     bestFitness.append(data[0][0])
#
# worstFitness = []
#
# for i in runID:
#     selectQuery5 = """SELECT MIN(fitness) FROM ALLStructures WHERE runid = ?"""
#     cur.execute(selectQuery5, (i,))
#     data = cur.fetchall()
#     worstFitness.append(data[0][0])


# print(bestFitness)
# print(worstFitness)

# nValues = [0.25, 0.25, 0.25, 0.25, 0.25,
#            0.5, 0.5, 0.5, 0.5, 0.5,
#            0.75, 0.75, 0.75, 0.75, 0.75,
#            1.0, 1.0, 1.0, 1.0, 1.0,
#            1.25, 1.25, 1.25, 1.25, 1.25,
#            1.5, 1.5, 1.5, 1.5, 1.5,
#            1.75, 1.75, 1.75, 1.75, 1.75,
#            2.0, 2.0, 2.0, 2.0, 2.0]

nValuesNew = [0.25, 0.25, 0.25, 0.25, 0.25,
              0.5, 0.5, 0.5, 0.5, 0.5,
              0.75, 0.75, 0.75, 0.75, 0.75,
              1.0, 1.0, 1.0, 1.0, 1.0,
              1.25, 1.25, 1.25, 1.25, 1.25,
              1.5, 1.5, 1.5, 1.5, 1.5,
              1.75, 1.75, 1.75, 1.75, 1.75,
              2.0, 2.0, 2.0, 2.0, 2.0,
              2.25, 2.25, 2.25, 2.25, 2.25,
              2.5, 2.5, 2.5, 2.5, 2.5,
              2.75, 2.75, 2.75, 2.75, 2.75,
              3.0, 3.0, 3.0, 3.0, 3.0]

# bestFit = [0.07293667365210364, 0.08438355915625453, 0.06986684288015999, 0.08194555329297509, 0.07250059053543506,
#            0.09006638883587481, 0.08089904598343842, 0.07378512496602933, 0.07675182706573053, 0.07615267081352481,
#            0.08309995610909618, 0.0921402445654555, 0.08470626518539805, 0.08333237015002168, 0.08160167240342744,
#            0.07889368396810678, 0.07895879812265351, 0.0802427832068128, 0.08621159582690012, 0.08324189765821563,
#            0.09024011061560566, 0.11347221833579875, 0.11207211781607387, 0.09424825784687196, 0.09690401460638087,
#            0.08967593430979545, 0.12311789580346816, 0.12105964197078177, 0.09251520191294793, 0.0761207107616081,
#            0.08770663463854254, 0.1105101877756289, 0.0950194202591514, 0.0960058134976282, 0.08084480100666654,
#            0.11354866522800282, 0.09553931157964353, 0.10201646437189445, 0.10040577578562321, 0.10420739048066904]

bestFitNew = [0.07293667365210364, 0.08438355915625453, 0.06986684288015999, 0.08194555329297509, 0.07250059053543506,
              0.09006638883587481, 0.08089904598343842, 0.07378512496602933, 0.07675182706573053, 0.07615267081352481,
              0.08309995610909618, 0.0921402445654555, 0.08470626518539805, 0.08333237015002168, 0.08160167240342744,
              0.07889368396810678, 0.07895879812265351, 0.0802427832068128, 0.08621159582690012, 0.08324189765821563,
              0.09024011061560566, 0.11347221833579875, 0.11207211781607387, 0.09424825784687196, 0.09690401460638087,
              0.08967593430979545, 0.12311789580346816, 0.12105964197078177, 0.09251520191294793, 0.0761207107616081,
              0.08770663463854254, 0.1105101877756289, 0.0950194202591514, 0.0960058134976282, 0.08084480100666654,
              0.11354866522800282, 0.09553931157964353, 0.10201646437189445, 0.10040577578562321, 0.10420739048066904,
              0.08604572919207974, 0.09822682121072258, 0.10916194179851392, 0.09943982167496555, 0.09711421799348935,
              0.10451781986760321, 0.09516332948854449, 0.10006587536707165, 0.09929414769229974, 0.09790231178099441,
              0.09671940824357893, 0.09990011786415706, 0.10231777090406084, 0.09094029169644204, 0.12592941401211627,
              0.08554429917092946, 0.10421154927829647, 0.12949413104756854, 0.0940382495690133, 0.09536824746435141]

# worstFit = [0.04845041615419047, 0.04845072672286702, 0.04845041568470191, 0.04845081334477263, 0.04845089879324316,
#             0.04845023211537202, 0.048450790104718776, 0.048450550193546625, 0.04845074245094069, 0.04845021404020632,
#             0.04845086193768457, 0.0484505123995375, 0.048450847852772524, 0.048450565452014226, 0.048450910061195826,
#             0.04845078235803911, 0.048450511695301866, 0.04845071968044929, 0.04845072766185621, 0.04845031756179242,
#             0.048450802076864946, 0.04845063094616122, 0.048450772498632215, 0.048450980955518266, 0.048450812875276375,
#             0.04845091921641123, 0.048450593856264115, 0.0484510171070076, 0.048451161478752905, 0.04845077789783073,
#             0.04845085184349677, 0.04845097250452854, 0.04845084761802406, 0.04845054643761761, 0.04845098400726528,
#             0.04845048915977235, 0.048450875787856056, 0.04845061568765237, 0.04845062977242943, 0.04845069831846135]
#
# worstFitNew = [0.04845041615419047, 0.04845072672286702, 0.04845041568470191, 0.04845081334477263, 0.04845089879324316,
#                0.04845023211537202, 0.048450790104718776, 0.048450550193546625, 0.04845074245094069, 0.04845021404020632,
#                0.04845086193768457, 0.0484505123995375, 0.048450847852772524, 0.048450565452014226, 0.048450910061195826,
#                0.04845078235803911, 0.048450511695301866, 0.04845071968044929, 0.04845072766185621, 0.04845031756179242,
#                0.048450802076864946, 0.04845063094616122, 0.048450772498632215, 0.048450980955518266, 0.048450812875276375,
#                0.04845091921641123, 0.048450593856264115, 0.0484510171070076, 0.048451161478752905, 0.04845077789783073,
#                0.04845085184349677, 0.04845097250452854, 0.04845084761802406, 0.04845054643761761, 0.04845098400726528,
#                0.04845048915977235, 0.048450875787856056, 0.04845061568765237, 0.04845062977242943, 0.04845069831846135,
#                0.048451048328791796, 0.04845098565051383, 0.04845040793814197, 0.048450677660732674, 0.04845053962999776,
#                0.048450976025773904, 0.04845123448658092, 0.04845092766738236, 0.04845095114231766, 0.04845070348289626,
#                0.048450943160837104, 0.04845078376652614, 0.04845090090598388, 0.04845135021969804, 0.04845103518277249,
#                0.04845077672409182, 0.04845087508360986, 0.048450686111619554, 0.04845097555627449, 0.048451175094344004]

chunkNVal = list(chunks(nValuesNew, 5))
# chunkBest = list(chunks(bestFitNew, 5))
# chunkWorst = list(chunks(worstFit, 5))
#
# print(chunkNVal)
# print(chunkBest)
# print(chunkWorst)
#
avgNVal = []
#
for lst in chunkNVal:
    avgNVal.append(listAvg(lst))
#
# avgBest = []
#
# for lst in chunkBest:
#     avgBest.append(listAvg(lst))
#
# print(avgNVal)
# print(avgBest)
#
# bestFit2 = []
# for lst in chunkBest:
#     lst.sort()
#
# absBest = []
# absWorst = []
#
# for lst in chunkBest:
#     absBest.append(lst[-1])
#     absWorst.append(lst[0])
#
# print(absBest)
# print(absWorst)
#
# avgRwp = []
# for i in avgBest:
#     avgRwp.append(1/i)
#
# bestRwp = []
# for i in absBest:
#     bestRwp.append(1/i)
#
# worstRwp = []
# for i in absWorst:
#     worstRwp.append(1/i)
#
# print("here")
# print(avgRwp)
# print(bestRwp)
# print(worstRwp)
#
#
# X = avgNVal
#
# X_axis = np.arange(len(X))
#
# fig, ax = plt.subplots()
#
# rects1 = plt.bar(X_axis, avgRwp, 0.1, label='avgRwp', color="g")
# rects2 = plt.bar(X_axis + 0.2, bestRwp, 0.1, label='bestRwp', color="b")
# rects3 = plt.bar(X_axis - 0.2, worstRwp, 0.1, label='worstRwp', color="r")
#
# plt.legend(fontsize=6)
#
# plt.xticks(X_axis, X)
#
# plt.xlabel("N Value")
# plt.ylabel("$R_{wp}$")
#
# plt.title("$R_{wp}$" + " Variation with Changing Log N value")
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
# plt.savefig(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\logNval_Barchart_best_New", dpi=300)


# bestFit1 = [0.07293667365210364, 0.08438355915625453, 0.06986684288015999, 0.08194555329297509, 0.07250059053543506,
#            0.09006638883587481, 0.08089904598343842, 0.07378512496602933, 0.07675182706573053, 0.07615267081352481,
#            0.08309995610909618, 0.0921402445654555, 0.08470626518539805, 0.08333237015002168, 0.08160167240342744,
#            0.07889368396810678, 0.07895879812265351, 0.0802427832068128, 0.08621159582690012, 0.08324189765821563,
#            0.09024011061560566, 0.11347221833579875, 0.11207211781607387, 0.09424825784687196, 0.09690401460638087,
#            0.08967593430979545, 0.12311789580346816, 0.12105964197078177, 0.09251520191294793, 0.0761207107616081,
#            0.08770663463854254, 0.1105101877756289, 0.0950194202591514, 0.0960058134976282, 0.08084480100666654,
#            0.11354866522800282, 0.09553931157964353, 0.10201646437189445, 0.10040577578562321, 0.10420739048066904]

# numEvalsMin = []
# numGenMin = []
# #
# for i in bestFitNew:
#     selectQuery4 = """SELECT MIN(numEvals) FROM ALLStructures WHERE fitness = ? GROUP BY runid"""
#     cur.execute(selectQuery4, (i,))
#     data = cur.fetchall()
#     numEvalsMin.append(data[0][0])
#
# for i in bestFitNew:
#     selectQuery5 = """SELECT MIN(genID) FROM ALLStructures WHERE fitness = ? GROUP BY runid"""
#     cur.execute(selectQuery5, (i,))
#     data = cur.fetchall()
#     numGenMin.append(data[0][0])

# print(numEvalsMin)
# print(numGenMin)


#@todo---------------------------------------------------------------------------------------------------------------

# numEvalsMin = [2759.0, 2573.0, 2572.0, 19523.0, 22798.0,
#                28225.0, 2231.0, 34121.0, 26038.0, 22200.0,
#                10978.0, 10650.0, 6429.0, 9699.0, 15717.0,
#                23809.0, 33650.0, 6741.0, 17901.0, 5643.0,
#                9671.0, 21542.0, 13863.0, 20853.0, 33666.0,
#                10222.0, 8347.0, 36826.0, 6652.0, 28978.0,
#                17997.0, 17507.0, 11675.0, 8131.0, 7637.0,
#                11097.0, 19191.0, 13974.0, 10286.0, 15633.0]

numEvalsMinNew = [2759.0, 2573.0, 2572.0, 19523.0, 22798.0,
                  28225.0, 2231.0, 34121.0, 26038.0, 22200.0,
                  10978.0, 10650.0, 6429.0, 9699.0, 15717.0,
                  23809.0, 33650.0, 6741.0, 17901.0, 5643.0,
                  9671.0, 21542.0, 13863.0, 20853.0, 33666.0,
                  10222.0, 8347.0, 36826.0, 6652.0, 28978.0,
                  17997.0, 17507.0, 11675.0, 8131.0, 7637.0,
                  11097.0, 19191.0, 13974.0, 10286.0, 15633.0,
                  13486.0, 16236.0, 16944.0, 13551.0, 10459.0,
                  18621.0, 19099.0, 15184.0, 12002.0, 44525.0,
                  33329.0, 17427.0, 33207.0, 16650.0, 17355.0,
                  19692.0, 23028.0, 20315.0, 20174.0, 3516.0]

#
# numGenMin = [27.0, 26.0, 26.0, 198.0, 231.0,
#              286.0, 22.0, 346.0, 264.0, 225.0,
#              111.0, 107.0, 65.0, 98.0, 159.0,
#              241.0, 341.0, 68.0, 181.0, 57.0,
#              97.0, 218.0, 140.0, 211.0, 341.0,
#              103.0, 84.0, 373.0, 67.0, 293.0,
#              181.0, 177.0, 117.0, 82.0, 77.0,
#              112.0, 194.0, 141.0, 104.0, 158.0]

numGenMinNew = [27.0, 26.0, 26.0, 198.0, 231.0,
                286.0, 22.0, 346.0, 264.0, 225.0,
                111.0, 107.0, 65.0, 98.0, 159.0,
                41.0, 341.0, 68.0, 181.0, 57.0,
                97.0, 218.0, 140.0, 211.0, 341.0,
                103.0, 84.0, 373.0, 67.0, 293.0,
                181.0, 177.0, 117.0, 82.0, 77.0,
                112.0, 194.0, 141.0, 104.0, 158.0,
                136.0, 164.0, 170.0, 137.0, 105.0,
                188.0, 193.0, 153.0, 121.0, 451.0,
                337.0, 176.0, 336.0, 168.0, 175.0,
                199.0, 233.0, 205.0, 204.0, 35.0]

#
# evalMinChunks = list(chunks(numEvalsMin, 5))
# genMinChunks = list(chunks(numGenMin, 5))

evalMinChunksNew = list(chunks(numEvalsMinNew, 5))
genMinChunksNew = list(chunks(numGenMinNew, 5))

#
# print(evalMinChunks)
# print(genMinChunks)
#
for lst in evalMinChunksNew:
    lst.sort()

for lst in genMinChunksNew:
    lst.sort()
#
# print(evalMinChunks)
# print(genMinChunks)
#
evalsMin = []
evalsMax = []
evalAvg = []

for lst in evalMinChunksNew:
    evalsMin.append(lst[0])
    evalsMax.append(lst[-1])
    evalAvg.append(listAvg(lst))
#
genMin = []
genMax = []
genAvg = []
#
for lst in genMinChunksNew:
    genMin.append(lst[0])
    genMax.append(lst[-1])
    genAvg.append(listAvg(lst))
#
# print("here1")
# print(evalsMin)
# print(evalsMax)
# print(evalAvg)
#
#
# print("here2")
# print(genMin)
# print(genMax)
# print(genAvg)
#
#
# X = avgNVal
#
# X_axis = np.arange(len(X))
#
# fig, ax = plt.subplots()
#
# rects1 = plt.bar(X_axis, evalAvg, 0.1, label='avgEval', color="g")
# rects2 = plt.bar(X_axis + 0.2, evalsMax, 0.1, label='maxEval', color="b")
# rects3 = plt.bar(X_axis - 0.2, evalsMin, 0.1, label='minEval', color="r")
#
# plt.legend(fontsize=6)
#
# plt.xticks(X_axis, X)
#
# plt.xlabel("N Value")
# plt.ylabel("NumEvals")
#
# plt.title("Minimum Number of Fitness Evaluations \nto find Best Solution with Changing Log N value")
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
# plt.savefig(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\logNval_Barchart_evals_New", dpi=300)



# X = avgNVal
#
# X_axis = np.arange(len(X))
#
# fig, ax = plt.subplots()
#
# rects1 = plt.bar(X_axis, genAvg, 0.1, label='avgGen', color="g")
# rects2 = plt.bar(X_axis + 0.2, genMax, 0.1, label='maxGen', color="b")
# rects3 = plt.bar(X_axis - 0.2, genMin, 0.1, label='minGen', color="r")
#
# plt.legend(fontsize=6)
#
# plt.xticks(X_axis, X)
#
# plt.xlabel("N Value")
# plt.ylabel("NumGen")
#
# plt.title("Minimum Number of Generations required \nto find Best Solution with Changing Log N value")

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(np.round(height, 2)),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=6)


# autolabel(rects1)
# autolabel(rects2)
# autolabel(rects3)
#
# plt.savefig(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\logNval_Barchart_gen_New", dpi=300)
