from PyCrystGA import *
from TOPAS import *

print("Script has started")

TOPAS = TOPAS('C:/Topas-6/tc.exe', r"C:\PhD\Year_3\Algorithm\TOPAS\Template\TFB1 GA p21n.inp")

# class PyCrystGA:
#     def __init__(self, molFile, numMol, directory,
#                  xrdInterface, popSize, numGen,
#                  crossoverPercentage, mutationPercentage,
#                  crossoverType, mutationType, # 0 static, 1 linear dynamic, 2 exponential dynamic
#                  pctDiffThresh, graphFontSize, graphLabelSize,
#                  graphFileName, graphFileNamePctDiff,  graphDpi):


for i in range(10):
    Algorithm = PyCrystGA('C:/PhD/Year_3/Algorithm/TFB Crystal Structure/TFB_labels.mol',
                           1,
                           'C:/PhD/Year_3/Algorithm/Test/LinearDynamic/' + str(i+1) + "/",
                           TOPAS,
                           100,
                           1000,
                           0.5,
                           0.1,
                           1,
                           1,
                           None,
                           14,
                           12,
                           'PyCrystGA_Graph',
                           'PyCrystGA_PctDiff_Graph',
                           300)
    # Algorithm.start()

for i in range(10):
    Algorithm = PyCrystGA('C:/PhD/Year_3/Algorithm/TFB Crystal Structure/TFB_labels.mol',
                           1,
                          'C:/PhD/Year_3/Algorithm/Test/LinearDynamic/' + str(i+11) + "/",
                           TOPAS,
                           100,
                           1000,
                           0.4,
                           0.1,
                           1,
                           1,
                           5,
                           14,
                           12,
                           'PyCrystGA_Graph',
                           'PyCrystGA_PctDiff_Graph',
                           300)
    # Algorithm.start()

for i in range(10):
    Algorithm = PyCrystGA('C:/PhD/Year_3/Algorithm/TFB Crystal Structure/TFB_labels.mol',
                           1,
                          'C:/PhD/Year_3/Algorithm/Test/LinearDynamic/' + str(i+21) + "/",
                           TOPAS,
                           100,
                           1000,
                           0.5,
                           0.2,
                           1,
                           1,
                           5,
                           14,
                           12,
                           'PyCrystGA_Graph',
                           'PyCrystGA_PctDiff_Graph',
                           300)
    # Algorithm.start()

for i in range(3):
    Algorithm = PyCrystGA('C:/PhD/Year_3/Algorithm/TFB Crystal Structure/TFB_labels.mol',
                          1,
                          'C:/PhD/Year_3/Algorithm/Test/ExponentialDynamic/' + str(i+1) + "/",
                          TOPAS,
                          100,
                          1000,
                          0.5,
                          0.1,
                          2,
                          2,
                          5,
                          14,
                          12,
                          'PyCrystGA_Graph',
                          'PyCrystGA_PctDiff_Graph',
                          300)
    # Algorithm.start()

    Algorithm1 = PyCrystGA('C:/PhD/Year_3/Algorithm/TFB Crystal Structure/TFB_labels.mol',
                          1,
                          'C:/PhD/Year_3/Algorithm/Test/ExponentialDynamic/' + str(i+2) + "/",
                          TOPAS,
                          100,
                          1000,
                          0.5,
                          0.1,
                          2,
                          2,
                          10,
                          14,
                          12,
                          'PyCrystGA_Graph',
                          'PyCrystGA_PctDiff_Graph',
                          300)
    # Algorithm1.start()

    Algorithm2 = PyCrystGA('C:/PhD/Year_3/Algorithm/TFB Crystal Structure/TFB_labels.mol',
                           1,
                           'C:/PhD/Year_3/Algorithm/Test/ExponentialDynamic/' + str(i+3) + "/",
                           TOPAS,
                           100,
                           1000,
                           0.5,
                           0.1,
                           2,
                           2,
                           15,
                           14,
                           12,
                           'PyCrystGA_Graph',
                           'PyCrystGA_PctDiff_Graph',
                           300)
    # Algorithm2.start()

for i in range(10):
    Algorithm = PyCrystGA('C:/PhD/Year_3/Algorithm/TFB Crystal Structure/TFB_labels.mol',
                          1,
                          'C:/PhD/Year_3/Algorithm/Test/ExponentialDynamic/' + str(i+11) + "/",
                          TOPAS,
                          100,
                          1000,
                          0.4,
                          0.1,
                          2,
                          2,
                          5,
                          14,
                          12,
                          'PyCrystGA_Graph',
                          'PyCrystGA_PctDiff_Graph',
                          300)
    # Algorithm.start()

for i in range(10):
    Algorithm = PyCrystGA('C:/PhD/Year_3/Algorithm/TFB Crystal Structure/TFB_labels.mol',
                          1,
                          'C:/PhD/Year_3/Algorithm/Test/ExponentialDynamic/' + str(i+21) + "/",
                          TOPAS,
                          100,
                          1000,
                          0.5,
                          0.2,
                          2,
                          2,
                          5,
                          14,
                          12,
                          'PyCrystGA_Graph',
                          'PyCrystGA_PctDiff_Graph',
                          300)
    # Algorithm.start()

# Algorithm1 = PyCrystGA('C:/PhD/Year_3/Algorithm/TFB Crystal Structure/TFB_labels.mol',
#                           1,
#                           'C:/PhD/Year_3/Algorithm/Test/ExponentialDynamic/' + str(2) + "/",
#                           TOPAS,
#                           20,
#                           5,
#                           0.5,
#                           0.2,
#                           2,
#                           2,
#                           5,
#                           14,
#                           12,
#                           'PyCrystGA_Graph',
#                           'PyCrystGA_PctDiff_Graph',
#                           300)
#
# Algorithm1.start()

print("Script has ended")


