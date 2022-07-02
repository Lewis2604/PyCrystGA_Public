import sqlite3
from pprint import pprint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
import numpy as np



database = r"D:\PhD\Year_4\AlgorithmNew\DBTFB\Databases\TFB_ILMDHCSF.db"
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

runIDs = ['c56572ef0540921faf6ceb28006b891b5baf9c97e1fd543b7c6fd94e16662a4c', '37ff0296ec86b7dd771b9c9a9042f88a4133d0de9321dbf019a4a1276bc56782', '9c445b4de03e133be680fef804e0d01154e39bbfd562ea660ee5a64852d73935', '3f90d12de6eb406b571e603ed4f8f6b161103a27016cf157fbcef998b1d4af84', 'd1333aafbd49afb3b17f20cbfd273be37647f0b0628aa370346435fe114d5f87',
          '062748aae2749eda38c8ad89b16996182b2a4ca97c31837b98c23ce7ea553e55', 'b6e7fd41cc013760637a5050b207867210365e661ad57b4f3c38e8ded21dbc6e', '8e9950434fc83ed7d0a2c4c4fd43a83ab76d0d15a66a7d94f5bbf830387b69b3', 'c1b0662ad87ee5b65b67de96143d05ed34407f38016587652c97e3f7a5ba87cd', '430d5f474ce5c29463884934f3efed27062b7ddb8e14d69c24ded74b14ba07cc',
          '3911ca9c7002ecb2d07ee4ce68f638823893b153cb68b8c98f94baeb17320ab3', 'acd33b7ffe7252e82301ae34a0c13b1fb71c5dcd3309deedcd321f697166cf31', '8c78d3c9bfd19f1e0d3d3de082756e28385d09efa1994a92a78542799c07eae6', '2035577f1a406f35736a43ddc63e417713af5ac6668e09c75ab4d6a5cfd1ada0', 'e38eb4181a2b53c7272302bbed1b082c3ef74dcb6745f71799934c6ac2077700',
          '75774a84a186eb9fec912a76acd3f5494d813f28293da6fb17b2a827133bb63a', 'd69872166894bc4ba51d7519c070bf8cdfcd2c94af31ca05f6de72f30a3ee156', 'a38345136b6b6091439d8f66a3361061f71d16cd4cf57eb6043aac854224a607', '7c55e1eec11fe6a47ffcbd424f6cc739daefcd4545599443b45e580cdef694b8', '80a84327cf12d971fb32d23be082a00f100ce973a316bf93ae89ba9f4b10adf1',
          '87669fc39a007fd75e37aed698cb112974091c529948d83efa56f593402f39b1', 'f8abebc62a69b801f795161a9594a0366fbe4fb9dab4b22c9a283d859f005191', 'abb1084b45c15f6518307d71f0d309877cef053b7558bb0c67ff7a5f21f80694', 'fd082748e8f7deed7e2d85ea7280a4ca7758aa5ee72b5c2c2d6a698fecf60b1b', '9c6b06a2fb067c0e4d4b7df916d1e97a6aacfb8dcbb9926e7ea976d90382079a',
          'e698a30b8a6d400a33d415accb8e5acd339c9e90d35c778e8d8f099c975601fd', '50ffaf13e0d9ad0155eff433d9aa066deeef82a3c296532de0802b1cf493f48f', '5b4da6a842b237bfe31da742fb671ece32fa9b6af220d1ed1663ea32c2c9ab71', '4b8743d65de542f3c08d069d3013e34cff89576a144e2c9ab2948157f5632bb3', '660c117ffc7ec515a7311b170149ce800aa1edd7e2ad2b231d807a6cb2b58d4d']
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

fitBest = [0.08792731267121207, 0.12007236362715562, 0.12198282987496173, 0.10263616525791773, 0.10409605397591921,
           0.10348733965639254, 0.09488941459522363, 0.09122181671185324, 0.0849659447571989, 0.09770904150811013,
           0.09425278648231061, 0.0963671037746792, 0.0988567992139619, 0.10921773622117668, 0.0962900131946205,
           0.09915508071773882, 0.09355634333946805, 0.07713208350973441, 0.10306923983435276, 0.08356587068893492,
           0.09226055880116926, 0.09604041688071674, 0.07825707225987283, 0.09978171054529138, 0.07605842659256325,
           0.09397340120468262, 0.09518429979140457, 0.09973493446467324, 0.09829035815129164, 0.12098943524365093]

rwpBest = [11.3730304, 8.32831111, 8.19787507, 9.74315435, 9.60651208,
           9.66301775, 10.5385833, 10.9622899, 11.7694213, 10.2344674,
           10.6097659, 10.3769851, 10.1156421, 9.15602204, 10.385293,
           10.0852119, 10.6887461, 12.9647736, 9.70221573, 11.9666078,
           10.8388678, 10.412283, 12.7783978, 10.0218767, 13.1477871,
           10.641309, 10.5059343, 10.026577, 10.1739379, 8.26518446]

numEvals1 = []

# test1 = list(zip(runIDs, fitBest))

# pprint(test1)

# for i in test1:
#     selectQuery4 = """SELECT MIN(numEvals) from AllStructures WHERE fitness = ? AND runid = ?"""
#     cur.execute(selectQuery4, (i[1], i[0]))
#     data = cur.fetchall()
#     print(data)

# for i in fitBest:
#     selectQuery3 = """SELECT MIN(numEvals) from AllStructures WHERE fitness = ? GROUP BY runid"""
#     cur.execute(selectQuery3, (i,))
#     data = cur.fetchall()
#     numEvals1.append(data[0][0])
#
# print(numEvals1)

numEvals = [42137.0, 48360.0, 49431.0, 46884.0, 49433.0,
            27682.0, 30561.0, 42258.0, 32749.0, 35138.0,
            19361.0, 18685.0, 22135.0, 20340.0, 20574.0,
            16456.0, 17158.0, 13256.0, 16353.0, 16084.0,
            15071.0, 12969.0, 13352.0, 10329.0, 18921.0,
            10502.0, 8945.0, 11572.0, 11408.0, 12287.0]

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
# plt.savefig(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\Graphs\ILMDHCSF\ILMDHCSF_rwp_V2", dpi=300)


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

plt.savefig(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\Graphs\ILMDHCSF\ILMDHCSF_numEvals_V2", dpi=300)