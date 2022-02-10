from PyCrystGA import *
from XRDInterfaces.TOPAS import *
from Config.Config import *


"""
TOPAS(topas.exe, inpFile, sequentialInpFile)
"""

TOPAS1 = TOPAS("C:/Topas-6/tc.exe", r"C:\PhD\Year_3\TFB1_GA_p21n.inp", r"C:\PhD\Year_3\TFB1_GA_p21n_sequential.inp")


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

# for i in range(5):
#     # while True:
#     #     try:
#     newAlgorithm = PyCrystGA()
#     newAlgorithm.setDirectory(r'C:/PhD/Year_4/Algorithm/Test/ILMDHC_Modified/ILMDHCUpDown/Trial1/('+str(i+1)+')/')
#     newAlgorithm.setXrdInterface(TOPAS1)
#     newAlgorithm.XRDInterface.setWrkDirectory(newAlgorithm.directory)
#     newAlgorithm.setOperatorType(10, 10)
#     newAlgorithm.setRollingAvgRange(10)
#     newAlgorithm.setSpikeThreshold(1)
#     # newAlgorithm.setExponentFactor(1)
#     newAlgorithm.newStart()
#         #     break
#         # except:
#         #     print("TOPAS FAILED")
#         #     time.sleep(60)
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


newAlgorithm2 = PyCrystGA()
newAlgorithm2.setDirectory(r'C:/PhD/Year_4/Algorithm/Test/ILMDHC_Modified/ILMDHCUpDown/Trial4/('+str(6)+')/')
newAlgorithm2.setXrdInterface(TOPAS1)
newAlgorithm2.XRDInterface.setWrkDirectory(newAlgorithm2.directory)
newAlgorithm2.setOperatorType(10, 10)
newAlgorithm2.setRollingAvgRange(10)
newAlgorithm2.setSpikeThreshold(1.4)
# newAlgorithm.setExponentFactor(1)
newAlgorithm2.newStart()