import math

from PyCrystGA import *
from XRDInterfaces.TOPAS import *
import matplotlib.pyplot as plt
from rdkit.Chem import TorsionFingerprints
from Config.Config import *


"""
TOPAS(topas.exe, templateFile, sequentialInpFile, topasVersion)
"""

TOPAS1 = TOPAS(
    # "C:/Topas-6/tc.exe",
    r"C:/Topas-6/",
    None, #r"D:\PhD\Year_4\TFB1_GA_p21n.inp",
    r"C:\PhD\Year_3\TFB1_GA_p21n_sequential.inp",
    6
    )


# SQLITE1 = SQLite("dbTest", None)

# params = [
#     {'xover': 0.7, 'mut': 0.1}
# ]

# count = 4
# for param in params:
#     for i in range(5):
#         while True:
#             try:
#                 Algorithm12 = PyCrystGA()
#                 Algorithm12.setDirectory(r'C:/PhD/Year_3/Algorithm/Test/SequentialTest/' + str(count) + '/')
#                 Algorithm12.setXrdInterface(TOPAS1)
#                 Algorithm12.XRDInterface.setWrkDirectory(r'C:/PhD/Year_3/Algorithm/Test/SequentialTest/' + str(count) + '/')
#                 Algorithm12.setCrossover(param['xover'])
#                 Algorithm12.setMutation(param['mut'])
#                 Algorithm12.newStart()
#                 count += 1
#                 break
#             except:
#                 time.sleep(10)

# params = [
#     {'p1xover': 0.5,
#      'p2xover': 0.4, 'p2xoverUB': 0.5, 'p2xoverLB': 0.3,
#      'p3xover': 0.3, 'p3xoverUB': 0.4, 'p3xoverLB': 0.2,
#      'p1mut': 0.4,
#      'p2mut': 0.3, 'p2mutUB': 0.4, 'p2mutLB': 0.2,
#      'p3mut': 0.2, 'p3mutUB': 0.3, 'p3mutLB': 0.1},
#     {'p1xover': 0.6,
#      'p2xover': 0.5, 'p2xoverUB': 0.6, 'p2xoverLB': 0.4,
#      'p3xover': 0.4, 'p3xoverUB': 0.5, 'p3xoverLB': 0.3,
#      'p1mut': 0.4,
#      'p2mut': 0.3, 'p2mutUB': 0.4, 'p2mutLB': 0.2,
#      'p3mut': 0.2, 'p3mutUB': 0.3, 'p3mutLB': 0.1},
#     {'p1xover': 0.7,
#      'p2xover': 0.6, 'p2xoverUB': 0.7, 'p2xoverLB': 0.5,
#      'p3xover': 0.5, 'p3xoverUB': 0.6, 'p3xoverLB': 0.4,
#      'p1mut': 0.4,
#      'p2mut': 0.3, 'p2mutUB': 0.4, 'p2mutLB': 0.2,
#      'p3mut': 0.2, 'p3mutUB': 0.3, 'p3mutLB': 0.1},
#     {'p1xover': 0.8,
#      'p2xover': 0.7, 'p2xoverUB': 0.8, 'p2xoverLB': 0.6,
#      'p3xover': 0.6, 'p3xoverUB': 0.7, 'p3xoverLB': 0.5,
#      'p1mut': 0.4,
#      'p2mut': 0.3, 'p2mutUB': 0.4, 'p2mutLB': 0.2,
#      'p3mut': 0.2, 'p3mutUB': 0.3, 'p3mutLB': 0.1},
#     {'p1xover': 0.9,
#      'p2xover': 0.8, 'p2xoverUB': 0.9, 'p2xoverLB': 0.7,
#      'p3xover': 0.7, 'p3xoverUB': 0.8, 'p3xoverLB': 0.6,
#      'p1mut': 0.4,
#      'p2mut': 0.3, 'p2mutUB': 0.4, 'p2mutLB': 0.2,
#      'p3mut': 0.2, 'p3mutUB': 0.3, 'p3mutLB': 0.1}
# ]
#
#
# params2 = [{'p1xover': 0.9,
#  'p2xover': 0.8, 'p2xoverUB': 0.9, 'p2xoverLB': 0.7,
#  'p3xover': 0.7, 'p3xoverUB': 0.8, 'p3xoverLB': 0.6,
#  'p1mut': 0.3,
#  'p2mut': 0.2, 'p2mutUB': 0.3, 'p2mutLB': 0.1,
#  'p3mut': 0.1, 'p3mutUB': 0.2, 'p3mutLB': 0.0}
# ]
#
# params3 = [{'p1xover': 0.9,
#             'p2xover': 0.8, 'p2xoverUB': 0.9, 'p2xoverLB': 0.7,
#             'p3xover': 0.7, 'p3xoverUB': 0.8, 'p3xoverLB': 0.6,
#             'p1mut': 0.2,
#             'p2mut': 0.15, 'p2mutUB': 0.2, 'p2mutLB': 0.1,
#             'p3mut': 0.1, 'p3mutUB': 0.15, 'p3mutLB': 0.05}
#            ]
#
# count = 36
# for param in params3:
#     for i in range(1):
#         while True:
#             try:
#                 Algorithm12 = PyCrystGA()
#                 Algorithm12.setDirectory(r'C:/PhD/Year_3/Algorithm/Test/DynamicLiterature/PhaseBoundaryTest/Combinations/(' + str(count) + ')/')
#                 Algorithm12.setXrdInterface(TOPAS1)
#                 Algorithm12.XRDInterface.setWrkDirectory(Algorithm12.directory)
#                 Algorithm12.setDynamicRates(param['p1xover'],
#                                             param['p2xover'], param['p2xoverUB'], param['p2xoverLB'],
#                                             param['p3xover'], param['p3xoverUB'], param['p3xoverLB'],
#                                             param['p1mut'],
#                                             param['p2mut'], param['p2mutUB'], param['p2mutLB'],
#                                             param['p3mut'], param['p3mutUB'], param['p3mutLB'])
#                 # Algorithm12.setCrossover(param['xover'])
#                 # Algorithm12.setMutation(param['mut'])
#                 # Algorithm12.newStart()
#                 # Algorithm12.start()
#                 count += 1
#                 break
#             except:
#                 time.sleep(0)
#
# parameter = [{"xover": 0.9, "mut": 0.1}, {"xover": 0.7, "mut": 0.1},
#             {"xover": 0.9, "mut": 0.3}, {"xover": 0.7, "mut": 0.3}]
#
# newCount = 16
# for param in parameter:
#     for i in range(1):
#         while True:
#             try:
#                 newAlgorithm = PyCrystGA()
#                 newAlgorithm.setDirectory(r'C:/PhD/Year_4/Algorithm/ILMDHC/(' + str(newCount) + ')/')
#                 newAlgorithm.setXrdInterface(TOPAS1)
#                 newAlgorithm.XRDInterface.setWrkDirectory(newAlgorithm.directory)
#                 newAlgorithm.setCrossover(param["xover"])
#                 newAlgorithm.setMutation(param["mut"])
#                 # newAlgorithm.newStart()
#                 newCount += 1
#                 break
#             except:
#                 time.sleep(0)

# #@todo ILMDHC1 >>> DONE!
# newNewCount = 2
# for i in range(4):
#     while True:
#         try:
#             newAlgorithm = PyCrystGA()
#             newAlgorithm.setDirectory(r'C:/PhD/Year_4/Algorithm/Test/ILMDHC_Modified/ILMDHC1/(' + str(newNewCount) + ')/')
#             newAlgorithm.setXrdInterface(TOPAS1)
#             newAlgorithm.XRDInterface.setWrkDirectory(newAlgorithm.directory)
#             newAlgorithm.setOperatorType(5, 5)
#             # newAlgorithm.newStart()
#             newNewCount += 1
#             break
#         except:
#             time.sleep(0)
#
# #@todo ILMDHC_SF0.5
# sfCount1 = 1
# for i in range(5):
#     while True:
#         try:
#             newAlgorithm = PyCrystGA()
#             newAlgorithm.setDirectory(r'C:/PhD/Year_4/Algorithm/Test/ILMDHC_Modified/ScaleFactor/ILMDHC_SF0.5/(' + str(sfCount1) + ')/')
#             newAlgorithm.setXrdInterface(TOPAS1)
#             newAlgorithm.XRDInterface.setWrkDirectory(newAlgorithm.directory)
#             newAlgorithm.setOperatorType(7, 7)
#             newAlgorithm.setILMDHCscaleFactor(0.5)
#             # newAlgorithm.newStart()
#             sfCount1 += 1
#             break
#         except:
#             time.sleep(0)
#
# #@todo ILMDHC_SF2
# sfCount2 = 1
# for i in range(5):
#     while True:
#         try:
#             newAlgorithm = PyCrystGA()
#             newAlgorithm.setDirectory(r'C:/PhD/Year_4/Algorithm/Test/ILMDHC_Modified/ScaleFactor/ILMDHC_SF2/(' + str(sfCount2) + ')/')
#             newAlgorithm.setXrdInterface(TOPAS1)
#             newAlgorithm.XRDInterface.setWrkDirectory(newAlgorithm.directory)
#             newAlgorithm.setOperatorType(7, 7)
#             newAlgorithm.setILMDHCscaleFactor(2)
#             # newAlgorithm.newStart()
#             sfCount2 += 1
#             break
#         except:
#             time.sleep(0)
#
# #@todo ILMDHC2
# newNewNewCount = 1
# for i in range(5):
#     while True:
#         try:
#             newAlgorithm = PyCrystGA()
#             newAlgorithm.setDirectory(r'C:/PhD/Year_4/Algorithm/Test/ILMDHC_Modified/ILMDHC2/(' + str(newNewNewCount) + ')/')
#             newAlgorithm.setXrdInterface(TOPAS1)
#             newAlgorithm.XRDInterface.setWrkDirectory(newAlgorithm.directory)
#             newAlgorithm.setOperatorType(6, 6)
#             # newAlgorithm.newStart()
#             newNewNewCount += 1
#             break
#         except:
#             time.sleep(0)
#
# #@todo exponential IMDC Done!!!
# IMDCCount = 1
# for i in range(5):
#     repeatCountIMDC = 1
#     for x in range(5):
#         while True:
#             try:
#                 newAlgorithm = PyCrystGA()
#                 newAlgorithm.setDirectory(r'C:/PhD/Year_4/Algorithm/Test/Exponent/IMDC/' + str(IMDCCount) + '/(' + str(repeatCountIMDC) + ')/')
#                 newAlgorithm.setXrdInterface(TOPAS1)
#                 newAlgorithm.XRDInterface.setWrkDirectory(newAlgorithm.directory)
#                 newAlgorithm.setOperatorType(8, 8)
#                 newAlgorithm.setExponentFactor(IMDCCount)
#                 newAlgorithm.newStart()
#                 repeatCountIMDC += 1
#                 break
#             except:
#                 time.sleep(5)
#     IMDCCount +=1

#@todo exponential DMIC
# DMICCount = 1
# for i in range(5):
#     repeatCountDMIC = 1
#     for x in range(5):
#         while True:
#             try:
#                 newAlgorithm1 = PyCrystGA()
#                 newAlgorithm1.setDirectory(r'C:/PhD/Year_4/Algorithm/Test/Exponent/DMIC/' + str(DMICCount) + '/(' + str(repeatCountDMIC) + ')/')
#                 newAlgorithm1.setXrdInterface(TOPAS1)
#                 newAlgorithm1.XRDInterface.setWrkDirectory(newAlgorithm1.directory)
#                 newAlgorithm1.setOperatorType(9, 9)
#                 newAlgorithm1.setExponentFactor(DMICCount)
#                 newAlgorithm1.newStart()
#                 repeatCountDMIC += 1
#                 break
#             except:
#                 print("TOPAS FAILED")
#                 time.sleep(60)
#     DMICCount +=1
#
# for i in range(5):
#     while True:
#         try:
#             newAlgorithm = PyCrystGA()
#             newAlgorithm.setDirectory(r'C:/PhD/Year_4/Algorithm/Test/ILMDHC_Modified/ILMDHCUpDown/Trial1/('+str(i+1)+')/')
#             newAlgorithm.setXrdInterface(TOPAS1)
#             newAlgorithm.XRDInterface.setWrkDirectory(newAlgorithm.directory)
#             newAlgorithm.setOperatorType(10, 10)
#             newAlgorithm.setRollingAvgRange(10)
#             newAlgorithm.setSpikeThreshold(1)
#             newAlgorithm.setExponentFactor(1)
#             newAlgorithm.newStart()
#             break
#         except:
#             print("TOPAS FAILED")
#             time.sleep(60)
#
# for i in range(5):
#     # while True:
#     #     try:
#     newAlgorithm1 = PyCrystGA()
#     newAlgorithm1.setDirectory(r'C:/PhD/Year_4/Algorithm/Test/ILMDHC_Modified/ILMDHCUpDown/Trial3/('+str(i+1)+')/')
#     newAlgorithm1.setXrdInterface(TOPAS1)
#     newAlgorithm1.XRDInterface.setWrkDirectory(newAlgorithm1.directory)
#     newAlgorithm1.setOperatorType(10, 10)
#     newAlgorithm1.setRollingAvgRange(10)
#     newAlgorithm1.setSpikeThreshold(1.2)
#     # newAlgorithm.setExponentFactor(1)
#     newAlgorithm1.newStart()
#
# for i in range(5):
#     # while True:
#     #     try:
#     newAlgorithm2 = PyCrystGA()
#     newAlgorithm2.setDirectory(r'C:/PhD/Year_4/Algorithm/Test/ILMDHC_Modified/ILMDHCUpDown/Trial4/('+str(i+1)+')/')
#     newAlgorithm2.setXrdInterface(TOPAS1)
#     newAlgorithm2.XRDInterface.setWrkDirectory(newAlgorithm2.directory)
#     newAlgorithm2.setOperatorType(10, 10)
#     newAlgorithm2.setRollingAvgRange(10)
#     newAlgorithm2.setSpikeThreshold(1.4)
    # newAlgorithm.setExponentFactor(1)
    # newAlgorithm2.start()

# parameters = [{"xover": 0.0, "mut": 0.0}, {"xover": 1.0, "mut": 0.0},
#             {"xover": 0.0, "mut": 1.0}, {"xover": 1.0, "mut": 1.0}]
#
# x = 0
# for param in parameters: # iterates over dictionary list (4 items in the list), parameter setting
#     x += 1
#     for i in range(5): # run repeats >>> [0,1,2,3,4]
#         while True:
#             try:
#                 newAlgorithm = PyCrystGA1()
#                 newAlgorithm.setDirectory(r'C:/PhD/Year_4/Algorithm/Alan/' + str(x) + '/(' + str(i+1) + ')/')
#                 newAlgorithm.setXrdInterface(TOPAS1)
#                 newAlgorithm.XRDInterface.setWrkDirectory(newAlgorithm.directory)
#                 newAlgorithm.setCrossover(param["xover"])
#                 newAlgorithm.setMutation(param["mut"])
#                 newAlgorithm.setOperatorType(0, 0)
#                 newAlgorithm.setPopSize(100)
#                 newAlgorithm.setNumGen(500)
#                 newAlgorithm.newStart()
#                 break
#             except:
#                 time.sleep(10)

# TOPAS1.runInputFile("D:/PhD/Year_4/Algorithm/ILMDHC/(10)/TFB1_GA_p21n_RUN10.inp")

# for i in range(1):
#     newAlgorithm2 = PyCrystGA1()
#     newAlgorithm2.setDirectory(r'D:/PhD/Year_4/Algorithm/Test/ILMDHC_Modified/ILMDHCLog/('+str(i+2)+')/')
#     newAlgorithm2.setXrdInterface(TOPAS1)
#     newAlgorithm2.XRDInterface.setWrkDirectory(newAlgorithm2.directory)
#     newAlgorithm2.setOperatorType(11, 11)
#     newAlgorithm2.setLogILMDHCNVal(1)
#     newAlgorithm2.setPopSize(100)
#     newAlgorithm2.setNumGen(1600)
#     # newAlgorithm2.setRollingAvgRange(10)
#     # newAlgorithm2.setSpikeThreshold(1.4)
#     # newAlgorithm.setExponentFactor(1)
#     newAlgorithm2.newStart()


# for i in range(1):
#     newAlgorithm2 = PyCrystGA1()
#     newAlgorithm2.setDirectory(r'D:/PhD/Year_4/Algorithm/Test/ILMDHC_Modified/ILMDHCLog/('+str(i+3)+')/')
#     newAlgorithm2.setXrdInterface(TOPAS1)
#     newAlgorithm2.XRDInterface.setWrkDirectory(newAlgorithm2.directory)
#     newAlgorithm2.setOperatorType(11, 11)
#     newAlgorithm2.setLogILMDHCNVal(1.5)
#     newAlgorithm2.setPopSize(100)
#     newAlgorithm2.setNumGen(1600)
#     # newAlgorithm2.setRollingAvgRange(10)
#     # newAlgorithm2.setSpikeThreshold(1.4)
#     # newAlgorithm.setExponentFactor(1)
#     newAlgorithm2.newStart()

# for i in range(1):
#     newAlgorithm2 = PyCrystGA1()
#     newAlgorithm2.setDirectory(r'D:/PhD/Year_4/Algorithm/Test/ILMDHC_Modified/ILMDHCLog/('+str(i+4)+')/')
#     newAlgorithm2.setXrdInterface(TOPAS1)
#     newAlgorithm2.XRDInterface.setWrkDirectory(newAlgorithm2.directory)
#     newAlgorithm2.setOperatorType(11, 11)
#     newAlgorithm2.setLogILMDHCNVal(2)
#     newAlgorithm2.setPopSize(10)
#     newAlgorithm2.setNumGen(20)
#     newAlgorithm2.setRollingAvgRange(10)
#     # newAlgorithm2.setSpikeThreshold(1.4)
#     # newAlgorithm.setExponentFactor(1)
#     newAlgorithm2.newStart()
#
# for i in range(1):
#     newAlgorithm2 = PyCrystGA1()
#     newAlgorithm2.setDirectory(r'D:/PhD/Year_4/Algorithm/Test/ILMDHC_Modified/ILMDHCLog/('+str(i+5)+')/')
#     newAlgorithm2.setXrdInterface(TOPAS1)
#     newAlgorithm2.XRDInterface.setWrkDirectory(newAlgorithm2.directory)
#     newAlgorithm2.setOperatorType(11, 11)
#     newAlgorithm2.setLogILMDHCNVal(2.5)
#     newAlgorithm2.setPopSize(100)
#     newAlgorithm2.setNumGen(1600)
#     # newAlgorithm2.setRollingAvgRange(10)
#     # newAlgorithm2.setSpikeThreshold(1.4)
#     # newAlgorithm.setExponentFactor(1)
#     newAlgorithm2.newStart()

parameters1 = [{"xover": 0.0, "mut": 0.0},
              {"xover": 0.1, "mut": 0.0},
              {"xover": 0.2, "mut": 0.0},
              {"xover": 0.3, "mut": 0.0},
              {"xover": 0.4, "mut": 0.0},
              {"xover": 0.5, "mut": 0.0},
              {"xover": 0.6, "mut": 0.0},
              {"xover": 0.7, "mut": 0.0},
              {"xover": 0.8, "mut": 0.0},
              {"xover": 0.9, "mut": 0.0},
              {"xover": 1.0, "mut": 0.0},
              {"xover": 0.0, "mut": 0.1},
              {"xover": 0.1, "mut": 0.1},
              {"xover": 0.2, "mut": 0.1},
              {"xover": 0.3, "mut": 0.1},
              {"xover": 0.4, "mut": 0.1},
              {"xover": 0.5, "mut": 0.1},
              {"xover": 0.6, "mut": 0.1},
              {"xover": 0.7, "mut": 0.1},
              {"xover": 0.8, "mut": 0.1},
              {"xover": 0.9, "mut": 0.1},
              {"xover": 1.0, "mut": 0.1},
              {"xover": 0.0, "mut": 0.2},
              {"xover": 0.1, "mut": 0.2},
              {"xover": 0.2, "mut": 0.2},
              {"xover": 0.3, "mut": 0.2},
              {"xover": 0.4, "mut": 0.2},
              {"xover": 0.5, "mut": 0.2},
              {"xover": 0.6, "mut": 0.2},
              {"xover": 0.7, "mut": 0.2},
              {"xover": 0.8, "mut": 0.2},
              {"xover": 0.9, "mut": 0.2},
              {"xover": 1.0, "mut": 0.2},
              {"xover": 0.0, "mut": 0.3},
              {"xover": 0.1, "mut": 0.3},
              {"xover": 0.2, "mut": 0.3},
              {"xover": 0.3, "mut": 0.3},
              {"xover": 0.4, "mut": 0.3},
              {"xover": 0.5, "mut": 0.3},
              {"xover": 0.6, "mut": 0.3},
              {"xover": 0.7, "mut": 0.3},
              {"xover": 0.8, "mut": 0.3},
              {"xover": 0.9, "mut": 0.3},
              {"xover": 1.0, "mut": 0.3},
              {"xover": 0.0, "mut": 0.4},
              {"xover": 0.1, "mut": 0.4},
              {"xover": 0.2, "mut": 0.4},
              {"xover": 0.3, "mut": 0.4},
              {"xover": 0.4, "mut": 0.4},
              {"xover": 0.5, "mut": 0.4},
              {"xover": 0.6, "mut": 0.4},
              {"xover": 0.7, "mut": 0.4},
              {"xover": 0.8, "mut": 0.4},
              {"xover": 0.9, "mut": 0.4},
              {"xover": 1.0, "mut": 0.4},
              {"xover": 0.0, "mut": 0.5},
              {"xover": 0.1, "mut": 0.5},
              {"xover": 0.2, "mut": 0.5},
              {"xover": 0.3, "mut": 0.5},
              {"xover": 0.4, "mut": 0.5},
              {"xover": 0.5, "mut": 0.5},
              {"xover": 0.6, "mut": 0.5},
              {"xover": 0.7, "mut": 0.5},
              {"xover": 0.8, "mut": 0.5},
              {"xover": 0.9, "mut": 0.5},
              {"xover": 1.0, "mut": 0.5},
              {"xover": 0.0, "mut": 0.6},
              {"xover": 0.1, "mut": 0.6},
              {"xover": 0.2, "mut": 0.6},
              {"xover": 0.3, "mut": 0.6},
              {"xover": 0.4, "mut": 0.6},
              {"xover": 0.5, "mut": 0.6},
              {"xover": 0.6, "mut": 0.6},
              {"xover": 0.7, "mut": 0.6},
              {"xover": 0.8, "mut": 0.6},
              {"xover": 0.9, "mut": 0.6},
              {"xover": 1.0, "mut": 0.6},
              {"xover": 0.0, "mut": 0.7},
              {"xover": 0.1, "mut": 0.7},
              {"xover": 0.2, "mut": 0.7},
              {"xover": 0.3, "mut": 0.7},
              {"xover": 0.4, "mut": 0.7},
              {"xover": 0.5, "mut": 0.7},
              {"xover": 0.6, "mut": 0.7},
              {"xover": 0.7, "mut": 0.7},
              {"xover": 0.8, "mut": 0.7},
              {"xover": 0.9, "mut": 0.7},
              {"xover": 1.0, "mut": 0.7},
              {"xover": 0.0, "mut": 0.8},
              {"xover": 0.1, "mut": 0.8},
              {"xover": 0.2, "mut": 0.8},
              {"xover": 0.3, "mut": 0.8},
              {"xover": 0.4, "mut": 0.8},
              {"xover": 0.5, "mut": 0.8},
              {"xover": 0.6, "mut": 0.8},
              {"xover": 0.7, "mut": 0.8},
              {"xover": 0.8, "mut": 0.8},
              {"xover": 0.9, "mut": 0.8},
              {"xover": 1.0, "mut": 0.8},
              {"xover": 0.0, "mut": 0.9},
              {"xover": 0.1, "mut": 0.9},
              {"xover": 0.2, "mut": 0.9},
              {"xover": 0.3, "mut": 0.9},
              {"xover": 0.4, "mut": 0.9},
              {"xover": 0.5, "mut": 0.9},
              {"xover": 0.6, "mut": 0.9},
              {"xover": 0.7, "mut": 0.9},
              {"xover": 0.8, "mut": 0.9},
              {"xover": 0.9, "mut": 0.9},
              {"xover": 1.0, "mut": 0.9},
              {"xover": 0.0, "mut": 1.0},
              {"xover": 0.1, "mut": 1.0},
              {"xover": 0.2, "mut": 1.0},
              {"xover": 0.3, "mut": 1.0},
              {"xover": 0.4, "mut": 1.0},
              {"xover": 0.5, "mut": 1.0},
              {"xover": 0.6, "mut": 1.0},
              {"xover": 0.7, "mut": 1.0},
              {"xover": 0.8, "mut": 1.0},
              {"xover": 0.9, "mut": 1.0},
              {"xover": 1.0, "mut": 1.0},
              ]

parameters2 = [{"xover": 0.9, "mut": 0.1},
               {"xover": 0.7, "mut": 0.1},
               {"xover": 0.5, "mut": 0.1},
               {"xover": 0.3, "mut": 0.1},
               {"xover": 0.1, "mut": 0.1},
               {"xover": 0.9, "mut": 0.3},
               {"xover": 0.7, "mut": 0.3},
               {"xover": 0.5, "mut": 0.3},
               {"xover": 0.3, "mut": 0.3},
               {"xover": 0.1, "mut": 0.3},
               {"xover": 0.9, "mut": 0.5},
               {"xover": 0.7, "mut": 0.5},
               {"xover": 0.5, "mut": 0.5},
               {"xover": 0.3, "mut": 0.5},
               {"xover": 0.1, "mut": 0.5},
               {"xover": 0.9, "mut": 0.7},
               {"xover": 0.7, "mut": 0.7},
               {"xover": 0.5, "mut": 0.7},
               {"xover": 0.3, "mut": 0.7},
               {"xover": 0.1, "mut": 0.7},
               {"xover": 0.9, "mut": 0.9},
               {"xover": 0.7, "mut": 0.9},
               {"xover": 0.5, "mut": 0.9},
               {"xover": 0.3, "mut": 0.9},
               {"xover": 0.1, "mut": 0.9},
                             ]

# parameters2 = [
#                {"xover": 0.1, "mut": 0.1},
#                {"xover": 0.9, "mut": 0.3},
#                {"xover": 0.7, "mut": 0.3},
#                {"xover": 0.5, "mut": 0.3},
#                {"xover": 0.3, "mut": 0.3},
#                {"xover": 0.1, "mut": 0.3},
#                {"xover": 0.9, "mut": 0.5},
#                {"xover": 0.7, "mut": 0.5},
#                {"xover": 0.5, "mut": 0.5},
#                {"xover": 0.3, "mut": 0.5},
#                {"xover": 0.1, "mut": 0.5},
#                {"xover": 0.9, "mut": 0.7},
#                {"xover": 0.7, "mut": 0.7},
#                {"xover": 0.5, "mut": 0.7},
#                {"xover": 0.3, "mut": 0.7},
#                {"xover": 0.1, "mut": 0.7},
#                {"xover": 0.9, "mut": 0.9},
#                {"xover": 0.7, "mut": 0.9},
#                {"xover": 0.5, "mut": 0.9},
#                {"xover": 0.3, "mut": 0.9},
#                {"xover": 0.1, "mut": 0.9},
#                ]

# parameters3 = [{"xover": 0.3, "mut": 0.1}]

#
# for i in range(1):
#     newAlgorithm2 = PyCrystGA1()
#     newAlgorithm2.setDirectory(r'D:/PhD/Year_4/AlgorithmNew/ILMDHC/ILMDHCLog/('+str(i+5)+')/')
#     newAlgorithm2.setXrdInterface(TOPAS1)
#     newAlgorithm2.XRDInterface.setWrkDirectory(newAlgorithm2.directory)
#     newAlgorithm2.setOperatorType(11, 11)
#     newAlgorithm2.setLogILMDHCNVal(2)
#     newAlgorithm2.setPopSize(100)
#     newAlgorithm2.setNumGen(1600)
#     newAlgorithm2.setRollingAvgRange(10)
#     # newAlgorithm2.setSpikeThreshold(1.4)
#     # newAlgorithm.setExponentFactor(1)
#     newAlgorithm2.newStart()
#
# for i in range(1):
#     newAlgorithm2 = PyCrystGA1()
#     newAlgorithm2.setDirectory(r'D:/PhD/Year_4/AlgorithmNew/ILMDHC/ILMDHCLog/('+str(i+6)+')/')
#     newAlgorithm2.setXrdInterface(TOPAS1)
#     newAlgorithm2.XRDInterface.setWrkDirectory(newAlgorithm2.directory)
#     newAlgorithm2.setOperatorType(11, 11)
#     newAlgorithm2.setLogILMDHCNVal(3)
#     newAlgorithm2.setPopSize(100)
#     newAlgorithm2.setNumGen(1600)
#     newAlgorithm2.setRollingAvgRange(10)
#     # newAlgorithm2.setSpikeThreshold(1.4)
#     # newAlgorithm.setExponentFactor(1)
#     newAlgorithm2.newStart()

# for i in range(5):
#     newAlgorithm2 = PyCrystGA1()
#     newAlgorithm2.setDirectory(r'D:/PhD/Year_4/AlgorithmNew/Static/GeneticAlgorithm/Redo/('+str(i+16)+')/')
#     newAlgorithm2.setXrdInterface(TOPAS1)
#     newAlgorithm2.XRDInterface.setWrkDirectory(newAlgorithm2.directory)
#     newAlgorithm2.setOperatorType(0, 0)
#     # newAlgorithm2.setLogILMDHCNVal(1)
#     newAlgorithm2.setPopSize(100)
#     newAlgorithm2.setNumGen(500)
#     newAlgorithm2.setRollingAvgRange(10)
#     newAlgorithm2.setCrossover(0.3)
#     newAlgorithm2.setMutation(0.1)
#     # newAlgorithm2.setSpikeThreshold(1.4)
#     # newAlgorithm.setExponentFactor(1)
#     newAlgorithm2.newStart()

# from subprocess import Popen
#
# p = Popen("C:/Topas-6/TOPASBatch.bat", cwd=r"C:/Topas-6/")
# stdout, stderr = p.communicate()

# os.system("C:/Topas-6/TOPASBatch.bat")


# counter = 1
# for param in parameters2:
#     for i in range(1):
#         while True:
#             try:
#                 newAlgorithm2 = PyCrystGA1()
#                 newAlgorithm2.setDirectory(r'D:/PhD/Year_4/AlgorithmNew/Static/GeneticAlgorithm/Redo/('+str(counter)+')/')
#                 newAlgorithm2.setXrdInterface(TOPAS1)
#                 newAlgorithm2.XRDInterface.setWrkDirectory(newAlgorithm2.directory)
#                 newAlgorithm2.setOperatorType(0, 0)
#                 # newAlgorithm2.setLogILMDHCNVal(1)
#                 newAlgorithm2.setPopSize(100)
#                 newAlgorithm2.setNumGen(500)
#                 newAlgorithm2.setRollingAvgRange(10)
#                 newAlgorithm2.setCrossover(param["xover"])
#                 newAlgorithm2.setMutation(param["mut"])
#                 # newAlgorithm2.setSpikeThreshold(1.4)
#                 # newAlgorithm.setExponentFactor(1)
#                 newAlgorithm2.newStart()
#                 counter+=1
#                 break
#             except:
#                 time.sleep(10)

# counter = 14
# for param in parameters2:
#     for i in range(5):
#         while True:
#             try:
#                 newAlgorithm2 = PyCrystGA1()
#                 newAlgorithm2.setDirectory(r'D:/PhD/Year_4/AlgorithmNew/Static/GeneticAlgorithm/Redo/('+str(counter)+')/')
#                 newAlgorithm2.setXrdInterface(TOPAS1)
#                 newAlgorithm2.XRDInterface.setWrkDirectory(newAlgorithm2.directory)
#                 newAlgorithm2.setOperatorType(0, 0)
#                 # newAlgorithm2.setLogILMDHCNVal(1)
#                 newAlgorithm2.setPopSize(100)
#                 newAlgorithm2.setNumGen(500)
#                 newAlgorithm2.setRollingAvgRange(10)
#                 newAlgorithm2.setCrossover(param["xover"])
#                 newAlgorithm2.setMutation(param["mut"])
#                 # newAlgorithm2.setSpikeThreshold(1.4)
#                 # newAlgorithm.setExponentFactor(1)
#                 newAlgorithm2.newStart()
#                 counter+=1
#                 break
#             except:
#                 time.sleep(10)

# counter = 21
# for param in parameters2:
#     for i in range(5):
#         while True:
#             try:
#                 newAlgorithm2 = PyCrystGA1()
#                 newAlgorithm2.setDirectory(r'D:/PhD/Year_4/AlgorithmNew/Static/GeneticAlgorithm/Redo/('+str(counter)+')/')
#                 newAlgorithm2.setXrdInterface(TOPAS1)
#                 newAlgorithm2.XRDInterface.setWrkDirectory(newAlgorithm2.directory)
#                 newAlgorithm2.setOperatorType(0, 0)
#                 # newAlgorithm2.setLogILMDHCNVal(1)
#                 newAlgorithm2.setPopSize(100)
#                 newAlgorithm2.setNumGen(500)
#                 newAlgorithm2.setRollingAvgRange(10)
#                 newAlgorithm2.setCrossover(param["xover"])
#                 newAlgorithm2.setMutation(param["mut"])
#                 # newAlgorithm2.setSpikeThreshold(1.4)
#                 # newAlgorithm.setExponentFactor(1)
#                 newAlgorithm2.newStart()
#                 counter+=1
#                 break
#             except:
#                 time.sleep(10)


# counter = 1
# for param in parameters2:
#     for i in range(1):
#         while True:
#             try:
#                 newAlgorithm2 = PyCrystGA1()
#                 newAlgorithm2.setDirectory(r'D:/PhD/Year_4/AlgorithmNew/DBTest/'+str(counter)+'/')
#                 newAlgorithm2.setXrdInterface(TOPAS1)
#                 newAlgorithm2.XRDInterface.setWrkDirectory(newAlgorithm2.directory)
#                 SQLITE1 = SQLite("D:/PhD/Year_4/dbTest.db", newAlgorithm2)
#                 newAlgorithm2.setSQL(SQLITE1)
#                 newAlgorithm2.dbClass.setDirectory(newAlgorithm2.directory)
#                 newAlgorithm2.setOperatorType(0, 0)
#                 # newAlgorithm2.setLogILMDHCNVal(1)
#                 newAlgorithm2.setPopSize(10)
#                 newAlgorithm2.setNumGen(20)
#                 newAlgorithm2.setRollingAvgRange(10)
#                 newAlgorithm2.setCrossover(param["xover"])
#                 newAlgorithm2.setMutation(param["mut"])
#                 # newAlgorithm2.setSpikeThreshold(1.4)
#                 # newAlgorithm.setExponentFactor(1)
#                 newAlgorithm2.newStart()
#                 counter+=1
#                 break
#             except:
#                 time.sleep(10)



# counter = 1
# for param in parameters3:
#     for i in range(5):
#         while True:
#             try:
#                 newAlgorithm2 = PyCrystGA1()
#                 newAlgorithm2.setDirectory(r'D:/PhD/Year_4/AlgorithmNew/DBAVS_03_33/Static/('+str(counter)+')/')
#                 newAlgorithm2.setXrdInterface(TOPAS2)
#                 newAlgorithm2.XRDInterface.setWrkDirectory(newAlgorithm2.directory)
#                 SQLITE1 = SQLite(r"D:\PhD\Year_4\AlgorithmNew\DBAVS_03_33\AVS_03_33.db", newAlgorithm2)
#                 newAlgorithm2.setSQL(SQLITE1)
#                 newAlgorithm2.setOperatorType(0, 0)
#                 # newAlgorithm2.setLogILMDHCNVal(1)
#                 newAlgorithm2.setPopSize(10)
#                 newAlgorithm2.setNumGen(15)
#                 newAlgorithm2.setRollingAvgRange(10)
#                 newAlgorithm2.setCrossover(param["xover"])
#                 newAlgorithm2.setMutation(param["mut"])
#                 # newAlgorithm2.setSpikeThreshold(1.4)
#                 # newAlgorithm.setExponentFactor(1)
#                 newAlgorithm2.newStart()
#                 counter+=1
#                 break
#             except:
#                 time.sleep(10)



# class TOPAS:
#     def __init__(self, topasPath, templateFile, seqFile, topasVersion):


TOPAS2 = TOPAS(
    # "C:/Topas-6/tc.exe",
    r"C:/Topas-6/",
    None,
    r"D:\PhD\Year_4\AVS-03-33_GA_sequential.inp",
    6
)

# parameters3 = [{"xover": 1, "mut": 0}]

# logNValue = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2]

# counter = 1
# for n in logNValue:
#     for i in range(5):
#         while True:
#             try:
#                 newAlgorithm2 = PyCrystGA1()
#                 newAlgorithm2.setDirectory(r'D:/PhD/Year_4/AlgorithmNew/DBTFB/Log/('+str(counter)+')/')
#                 newAlgorithm2.setXrdInterface(TOPAS1)
#                 newAlgorithm2.XRDInterface.setWrkDirectory(newAlgorithm2.directory)
#                 SQLITE1 = SQLite(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\TFB_Log.db", newAlgorithm2)
#                 newAlgorithm2.setSQL(SQLITE1)
#                 newAlgorithm2.setOperatorType(11, 11)
#                 newAlgorithm2.setLogNVal(n)
#                 newAlgorithm2.setPopSize(100)
#                 newAlgorithm2.setNumGen(500)
#                 newAlgorithm2.setRollingAvgRange(10)
#                 newAlgorithm2.newStart()
#                 counter+=1
#                 break
#             except:
#                 time.sleep(10)

# trigNValue = [0.25, 0.5, 0.75, 1]
# #
# counter = 1
# for n in trigNValue:
#     for i in range(1):
#         while True:
#             try:
#                 newAlgorithm2 = PyCrystGA1()
#                 newAlgorithm2.setDirectory(r'D:/PhD/Year_4/AlgorithmNew/DBTFB/Trig/Type1/('+str(counter)+')/')
#                 newAlgorithm2.setXrdInterface(TOPAS1)
#                 newAlgorithm2.XRDInterface.setWrkDirectory(newAlgorithm2.directory)
#                 SQLITE1 = SQLite(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\TFB_Trig.db", newAlgorithm2)
#                 newAlgorithm2.setSQL(SQLITE1)
#                 newAlgorithm2.setOperatorType(12, 12)
#                 newAlgorithm2.setTrigNVal(n)
#                 newAlgorithm2.setPopSize(100)
#                 newAlgorithm2.setNumGen(500)
#                 newAlgorithm2.setRollingAvgRange(10)
#                 newAlgorithm2.newStart()
#                 counter+=1
#                 break
#             except:
#                 time.sleep(10)
#
# counter1 = 1
# for n in trigNValue:
#     for i in range(1):
#         while True:
#             try:
#                 newAlgorithm2 = PyCrystGA1()
#                 newAlgorithm2.setDirectory(r'D:/PhD/Year_4/AlgorithmNew/DBTFB/Trig/Type2/('+str(counter1)+')/')
#                 newAlgorithm2.setXrdInterface(TOPAS1)
#                 newAlgorithm2.XRDInterface.setWrkDirectory(newAlgorithm2.directory)
#                 SQLITE1 = SQLite(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\TFB_Trig.db", newAlgorithm2)
#                 newAlgorithm2.setSQL(SQLITE1)
#                 newAlgorithm2.setOperatorType(13, 13)
#                 newAlgorithm2.setTrigNVal(n)
#                 newAlgorithm2.setPopSize(100)
#                 newAlgorithm2.setNumGen(500)
#                 newAlgorithm2.setRollingAvgRange(10)
#                 newAlgorithm2.newStart()
#                 counter1+=1
#                 break
#             except:
#                 time.sleep(10)
#
# counter2 = 1
# for n in trigNValue:
#     for i in range(1):
#         while True:
#             try:
#                 newAlgorithm2 = PyCrystGA1()
#                 newAlgorithm2.setDirectory(r'D:/PhD/Year_4/AlgorithmNew/DBTFB/Trig/Type3/('+str(counter2)+')/')
#                 newAlgorithm2.setXrdInterface(TOPAS1)
#                 newAlgorithm2.XRDInterface.setWrkDirectory(newAlgorithm2.directory)
#                 SQLITE1 = SQLite(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\TFB_Trig.db", newAlgorithm2)
#                 newAlgorithm2.setSQL(SQLITE1)
#                 newAlgorithm2.setOperatorType(14, 14)
#                 newAlgorithm2.setTrigNVal(n)
#                 newAlgorithm2.setPopSize(100)
#                 newAlgorithm2.setNumGen(500)
#                 newAlgorithm2.setRollingAvgRange(10)
#                 newAlgorithm2.newStart()
#                 counter2+=1
#                 break
#             except:
#                 time.sleep(10)

# numGen = 500
#
# n = 0.5
#
# mutRate = []
# xoverRate = []
#
# pi = math.pi
#
# genList = list(range(0, 500, 1))
#
# print(len(genList))
#
# ratioList = []
#
# for i in genList:
#     ratioList.append(i/numGen)
#
# degRatio = []
#
# for i in ratioList:
#     degRatio.append(i*360)
#
# radians = []
#
# for i in degRatio:
#     radians.append(i*(pi/180))
#
# sinRadSquared = []
#
# for i in radians:
#     sinRadSquared.append(math.sin(i/n)**2)
#
# for i in sinRadSquared:
#     mutRate.append(i)
#     xoverRate.append(1-i)
#
# scaledMutRate = []
# scaledXoverRate1 = []
# scaledXoverRate2 = []
#
#
# for i in genList:
#     scaledMutRate.append(mutRate[i]*((numGen - i)/numGen))
#     scaledXoverRate1.append(xoverRate[i]*((numGen - i)/numGen))
#
# for i in scaledMutRate:
#     scaledXoverRate2.append(1-i)
#
#
# plt1 = plt
# plt2 = plt
# plt3 = plt
#
# plt1.scatter(genList, mutRate, c="b", label="mutRate")
# plt1.scatter(genList, xoverRate, c="r", label="xoverRate")
# plt1.legend(fontsize=8)
# plt1.savefig(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\trigRate", dpi=300)
#
# plt.clf()
#
# plt2.scatter(genList, scaledMutRate, c="b", label="mutRate")
# plt2.scatter(genList, scaledXoverRate1, c="r", label="xoverRate")
# plt2.legend(fontsize=8)
# plt2.savefig(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\trigRate2", dpi=300)
#
# plt.clf()
#
# plt3.scatter(genList, scaledMutRate, c="b", label="mutRate")
# plt3.scatter(genList, scaledXoverRate2, c="r", label="xoverRate")
# plt3.legend(fontsize=8)
# plt3.savefig(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\trigRate3", dpi=300)

#
# TOPAS2.runInputFile(r"D:\PhD\Year_4\AlgorithmNew\DBAVS_03_33\Static\(1)\XRD\NOT_WORKING.inp")


# counter = 1
# for param in parameters2:
#     # print("here")
#     for i in range(5):
#         # print("here1")
#         while True:
#             # print("here2")
#             try:
#                 # print("here3")
#                 newAlgorithm2 = PyCrystGA1()
#                 # print("here4")
#                 newAlgorithm2.setDirectory(r'D:/PhD/Year_4/AlgorithmNew/DBAVS_03_33/Static/('+str(counter)+')/')
#                 # print("here5")
#                 newAlgorithm2.setXrdInterface(TOPAS2)
#                 # print("here6")
#                 newAlgorithm2.XRDInterface.setWrkDirectory(newAlgorithm2.directory)
#                 # print("here7")
#                 SQLITE1 = SQLite(r"D:\PhD\Year_4\AlgorithmNew\DBAVS_03_33\AVS_03_33.db", newAlgorithm2)
#                 newAlgorithm2.setSQL(SQLITE1)
#                 # print("here8")
#                 newAlgorithm2.setOperatorType(0, 0)
#                 # print("here9")
#                 newAlgorithm2.setPopSize(100)
#                 # print("here10")
#                 newAlgorithm2.setNumGen(500)
#                 # print("here11")
#                 newAlgorithm2.setRollingAvgRange(10)
#                 # print("here12")
#                 newAlgorithm2.setCrossover(param["xover"])
#                 # print("here13")
#                 newAlgorithm2.setMutation(param["mut"])
#                 # print("here14")
#                 newAlgorithm2.newStart()
#                 # print("here15")
#                 counter+=1
#                 break
#             except:
#                 time.sleep(10)

ILMDHCSF = [0.5, 1, 1.5, 2]
DHMILCSF = [0.5, 1, 1.5, 2]

ILMDHCSF2 = [2.5, 3.0]
DHMILCSF2 = [2.5, 3.0]

# counter1 = 21
# for sf in DHMILCSF2:
#     for i in range(5):
#         while True:
#             try:
#                 newAlgorithm2 = PyCrystGA1()
#                 newAlgorithm2.setDirectory(r'D:/PhD/Year_4/AlgorithmNew/DBTFB/DHMILCSF/('+str(counter1)+')/')
#                 newAlgorithm2.setXrdInterface(TOPAS1)
#                 newAlgorithm2.XRDInterface.setWrkDirectory(newAlgorithm2.directory)
#                 SQLITE1 = SQLite(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\Databases\TFB_DHMILCSF.db", newAlgorithm2)
#                 newAlgorithm2.setSQL(SQLITE1)
#                 newAlgorithm2.setOperatorType(15, 15)
#                 newAlgorithm2.setDHMILCscaleFactor(sf)
#                 newAlgorithm2.setPopSize(100)
#                 newAlgorithm2.setNumGen(500)
#                 newAlgorithm2.setRollingAvgRange(10)
#                 newAlgorithm2.setNumTors(3)
#                 newAlgorithm2.newStart()
#                 counter1+=1
#                 break
#             except:
#                 time.sleep(10)

# counter2 = 21
# for sf in ILMDHCSF2:
#     for i in range(5):
#         while True:
#             try:
#                 newAlgorithm2 = PyCrystGA1()
#                 newAlgorithm2.setDirectory(r'D:/PhD/Year_4/AlgorithmNew/DBTFB/ILMDHCSF/('+str(counter2)+')/')
#                 newAlgorithm2.setXrdInterface(TOPAS1)
#                 newAlgorithm2.XRDInterface.setWrkDirectory(newAlgorithm2.directory)
#                 SQLITE2 = SQLite(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\Databases\TFB_ILMDHCSF.db", newAlgorithm2)
#                 newAlgorithm2.setSQL(SQLITE2)
#                 newAlgorithm2.setOperatorType(7, 7)
#                 newAlgorithm2.setILMDHCscaleFactor(sf)
#                 newAlgorithm2.setPopSize(100)
#                 newAlgorithm2.setNumGen(500)
#                 newAlgorithm2.setRollingAvgRange(10)
#                 newAlgorithm2.setNumTors(3)
#                 newAlgorithm2.newStart()
#                 counter2+=1
#                 break
#             except:
#                 time.sleep(10)


# counter2 = 21
# for sf in ILMDHCSF2:
#     for i in range(1):
#         while True:
#             try:
#                 newAlgorithm2 = PyCrystGA1()
#                 newAlgorithm2.setDirectory(r'D:/PhD/Year_4/AlgorithmNew/DBAVS_03_33/ILMDHCSF/('+str(counter2)+')/')
#                 newAlgorithm2.setXrdInterface(TOPAS2)
#                 newAlgorithm2.XRDInterface.setWrkDirectory(newAlgorithm2.directory)
#                 SQLITE1 = SQLite(r"D:\PhD\Year_4\AlgorithmNew\DBAVS_03_33\DBAVS_03_33_ILMDHCSF_Test.db", newAlgorithm2)
#                 newAlgorithm2.setSQL(SQLITE1)
#                 newAlgorithm2.setOperatorType(7, 7)
#                 newAlgorithm2.setILMDHCscaleFactor(sf)
#                 newAlgorithm2.setPopSize(10)
#                 newAlgorithm2.setNumGen(10)
#                 newAlgorithm2.setRollingAvgRange(10)
#                 newAlgorithm2.setNumTors(7)
#                 newAlgorithm2.newStart()
#                 counter2+=1
#                 break
#             except:
#                 time.sleep(10)

parameters3 = [{"xover": 0.9, "mut": 0.1},
               {"xover": 0.7, "mut": 0.1},
               {"xover": 0.5, "mut": 0.1},
               {"xover": 0.3, "mut": 0.1},
               {"xover": 0.1, "mut": 0.1},
               {"xover": 0.9, "mut": 0.3},
               {"xover": 0.7, "mut": 0.3},
               {"xover": 0.5, "mut": 0.3},
               {"xover": 0.3, "mut": 0.3},
               {"xover": 0.1, "mut": 0.3}
               ]

# counter3 = 1
# for param in parameters3:
#     for i in range(5):
#         while True:
#             try:
#                 newAlgorithm2 = PyCrystGA1()
#                 newAlgorithm2.setDirectory(r'D:/PhD/Year_4/AlgorithmNew/DBTFB/Static/PolynomialBounded/Probability1.00/('+str(counter3)+')/')
#                 newAlgorithm2.setXrdInterface(TOPAS1)
#                 newAlgorithm2.XRDInterface.setWrkDirectory(newAlgorithm2.directory)
#                 SQLITE1 = SQLite(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\Databases\TFB_Static_Polynomial_bounded_1.00.db", newAlgorithm2)
#                 newAlgorithm2.setSQL(SQLITE1)
#                 newAlgorithm2.setOperatorType(0, 0)
#                 newAlgorithm2.setCrossover(param['xover'])
#                 newAlgorithm2.setMutation(param['mut'])
#                 newAlgorithm2.setPopSize(100)
#                 newAlgorithm2.setNumGen(500)
#                 newAlgorithm2.setRollingAvgRange(10)
#                 newAlgorithm2.setNumTors(3)
#                 newAlgorithm2.newStart()
#                 counter3+=1
#                 break
#             except:
#                 time.sleep(10)
#
#
parameters4 = [{"xover": 0.9, "mut": 0.3},
               {"xover": 0.7, "mut": 0.3},
               {"xover": 0.5, "mut": 0.3},
               {"xover": 0.3, "mut": 0.3},
               {"xover": 0.1, "mut": 0.3}
               ]
#
# counter4 = 26
# for param in parameters4:
#     for i in range(5):
#         while True:
#             try:
#                 newAlgorithm2 = PyCrystGA1()
#                 newAlgorithm2.setDirectory(r'D:/PhD/Year_4/AlgorithmNew/DBTFB/Static/PolynomialBounded/Probability0.66/('+str(counter4)+')/')
#                 newAlgorithm2.setXrdInterface(TOPAS1)
#                 newAlgorithm2.XRDInterface.setWrkDirectory(newAlgorithm2.directory)
#                 SQLITE1 = SQLite(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\Databases\TFB_Static_Polynomial_bounded_0.66.db", newAlgorithm2)
#                 newAlgorithm2.setSQL(SQLITE1)
#                 newAlgorithm2.setOperatorType(0, 0)
#                 newAlgorithm2.setCrossover(param['xover'])
#                 newAlgorithm2.setMutation(param['mut'])
#                 newAlgorithm2.setPopSize(100)
#                 newAlgorithm2.setNumGen(500)
#                 newAlgorithm2.setRollingAvgRange(10)
#                 newAlgorithm2.setNumTors(3)
#                 newAlgorithm2.newStart()
#                 counter4+=1
#                 break
#             except:
#                 time.sleep(10)


counter5 = 1

# for param in parameters3:
#     for i in range(5):
#         while True:
#             try:
#                 newAlgorithm2 = PyCrystGA1()
#                 newAlgorithm2.setDirectory(r'D:/PhD/Year_4/AlgorithmNew/DBAVS_03_33/Static/Polynomial_Bounded_7-7/('+str(counter5)+')/')
#                 newAlgorithm2.setXrdInterface(TOPAS2)
#                 newAlgorithm2.XRDInterface.setWrkDirectory(newAlgorithm2.directory)
#                 SQLITE1 = SQLite(r"D:\PhD\Year_4\AlgorithmNew\DBAVS_03_33\Databases\AVS_03_33_Static_Polynomial_bounded_1.00.db", newAlgorithm2)
#                 newAlgorithm2.setSQL(SQLITE1)
#                 newAlgorithm2.setOperatorType(0, 0)
#                 newAlgorithm2.setCrossover(param['xover'])
#                 newAlgorithm2.setMutation(param['mut'])
#                 newAlgorithm2.setPopSize(100)
#                 newAlgorithm2.setNumGen(500)
#                 newAlgorithm2.setRollingAvgRange(10)
#                 newAlgorithm2.setNumTors(7)
#                 # newAlgorithm2.newStart()
#                 counter5+=1
#                 break
#             except:
#                 time.sleep(10)

# parameters5 = [
#     {"xover": 1.0, "mut": 0.0},
#     {"xover": 0.1, "mut": 0.0}
#                ]
#
# for param in parameters5:
#     for i in range(5):
#         newAlgorithm2 = PyCrystGA1()
#         newAlgorithm2.setDirectory(r'D:/PhD/Year_4/AlgorithmNew/DBTFB/Static/PolynomialBounded/PairwiseComparison/Probability1.00/('+str(counter5)+')/')
#         newAlgorithm2.setXrdInterface(TOPAS1)
#         newAlgorithm2.XRDInterface.setWrkDirectory(newAlgorithm2.directory)
#         SQLITE1 = SQLite(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\Databases\TFB_Static_Polynomial_bounded_1.00__Pairwise_Crossover_Comparison.db", newAlgorithm2)
#         newAlgorithm2.setSQL(SQLITE1)
#         newAlgorithm2.setOperatorType(0, 0)
#         newAlgorithm2.setCrossover(param['xover'])
#         newAlgorithm2.setMutation(param['mut'])
#         newAlgorithm2.setPopSize(100)
#         newAlgorithm2.setNumGen(500)
#         newAlgorithm2.setRollingAvgRange(10)
#         newAlgorithm2.setNumTors(3)
#         newAlgorithm2.newStart()
#         counter5+=1

parameters6 = [{"xover": 0.9, "mut": 0.5},
                {"xover": 0.7, "mut": 0.5},
                {"xover": 0.5, "mut": 0.5},
                {"xover": 0.3, "mut": 0.5},
                {"xover": 0.1, "mut": 0.5},
                {"xover": 0.9, "mut": 0.7},
                {"xover": 0.7, "mut": 0.7},
                {"xover": 0.5, "mut": 0.7},
                {"xover": 0.3, "mut": 0.7},
                {"xover": 0.1, "mut": 0.7},
                {"xover": 0.9, "mut": 0.9},
                {"xover": 0.7, "mut": 0.9},
                {"xover": 0.5, "mut": 0.9},
                {"xover": 0.3, "mut": 0.9},
                {"xover": 0.1, "mut": 0.9}
               ]

counter6 = 51
for param in parameters6:
    for i in range(5):
        while True:
            try:
                newAlgorithm2 = PyCrystGA1()
                newAlgorithm2.setDirectory(r'D:/PhD/Year_4/AlgorithmNew/DBTFB/Static/PolynomialBounded/PairwiseCrossover/Probability0.66/('+str(counter6)+')/')
                newAlgorithm2.setXrdInterface(TOPAS1)
                newAlgorithm2.XRDInterface.setWrkDirectory(newAlgorithm2.directory)
                SQLITE1 = SQLite(r"D:\PhD\Year_4\AlgorithmNew\DBTFB\Databases\TFB_Static_Polynomial_bounded_0.66.db", newAlgorithm2)
                newAlgorithm2.setSQL(SQLITE1)
                newAlgorithm2.setOperatorType(0, 0)
                newAlgorithm2.setCrossover(param['xover'])
                newAlgorithm2.setMutation(param['mut'])
                newAlgorithm2.setPopSize(100)
                newAlgorithm2.setNumGen(500)
                newAlgorithm2.setRollingAvgRange(10)
                newAlgorithm2.setNumTors(3)
                newAlgorithm2.newStart()
                counter6+=1
                break
            except:
                time.sleep(10)

