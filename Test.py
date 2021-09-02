from PyCrystGA import *
from XRDInterfaces.TOPAS import *
from Config.Config import *



TOPAS1 = TOPAS('C:/Topas-6/tc.exe', r"C:\PhD\Year_3\TFB1_GA_p21n.inp")
# TOPAS2 = TOPAS('C:/Topas-6/tc.exe', r"C:\PhD\Year_3\TFB1_GA_p21n_Rwp.inp")

# Algorithm1 = PyCrystGA()
# Algorithm1.setXrdInterface(TOPAS1)
# Algorithm1.setDirectory("C:/PhD/Year_3/Algorithm/Test/FitnessCalcComparison/3/")
# Algorithm1.start()

# Algorithm2 = PyCrystGA()
# Algorithm2.setXrdInterface(TOPAS2)
# Algorithm2.setDirectory("C:/PhD/Year_3/Algorithm/Test/FitnessCalcComparison/2/")
# Algorithm2.start()

# Algorithm1 = PyCrystGA()
# print(Algorithm1.numGen)
# Algorithm1.setXrdInterface(TOPAS1)
# Algorithm1.setDirectory("C:/PhD/Year_3/Algorithm/Test/FitnessCalcComparison/3/")
# Algorithm1.start()

# params = [{'xover': 0.9, 'mut': 0.1},
#           {'xover': 0.9, 'mut': 0.3},
#           {'xover': 0.9, 'mut': 0.5},
#           {'xover': 0.9, 'mut': 0.7},
#           {'xover': 0.9, 'mut': 0.9},
#           {'xover': 0.7, 'mut': 0.1},
#           {'xover': 0.7, 'mut': 0.3},
#           {'xover': 0.7, 'mut': 0.5},
#           {'xover': 0.7, 'mut': 0.7},
#           {'xover': 0.7, 'mut': 0.9},
#           {'xover': 0.5, 'mut': 0.1},
#           {'xover': 0.5, 'mut': 0.3},
#           {'xover': 0.5, 'mut': 0.5},
#           {'xover': 0.5, 'mut': 0.7},
#           {'xover': 0.5, 'mut': 0.9},
#           {'xover': 0.3, 'mut': 0.1},
#           {'xover': 0.3, 'mut': 0.3},
#           {'xover': 0.3, 'mut': 0.5},
#           {'xover': 0.3, 'mut': 0.7},
#           {'xover': 0.3, 'mut': 0.9},
#           {'xover': 0.1, 'mut': 0.1},
#           {'xover': 0.1, 'mut': 0.3},
#           {'xover': 0.1, 'mut': 0.5},
#           {'xover': 0.1, 'mut': 0.7},
#           {'xover': 0.1, 'mut': 0.9}]
#
# TOPAS = TOPAS('C:/Topas-6/tc.exe', "C:/PhD/Year_3/TFB1_GA_p21n.inp")
# count = 141
# for param in params:
#     for i in range(5):
#         while True:
#             try:
#                 Algorithm = PyCrystGA()
#                 Algorithm.setCrossover(params['xover'])
#                 Algorithm.setMutation(params['mut'])
#                 Algorithm.setDirectory("C:/PhD/Year_3/Algorithm/Test/Restart/Run(" + str(count) + ")/") #@ todo cannot contain whitespace
#                 TOPAS.setDirectory(Algorithm.directory)
#                 Algorithm.setXrdInterface(TOPAS)
#                 Algorithm.start()
#                 count += 1
#                 break
#             except:
#                 time.sleep(10)



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


Algorithm11 = PyCrystGA()
Algorithm11.setDirectory(r'C:/PhD/Year_3/Algorithm/Test/SequentialTest/2/')
Algorithm11.setXrdInterface(TOPAS1)
Algorithm11.XRDInterface.setDirectory(r'C:/PhD/Year_3/Algorithm/Test/SequentialTest/2/')
Algorithm11.start()

Algorithm10 = PyCrystGA()
Algorithm10.setDirectory(r'C:/PhD/Year_3/Algorithm/Test/SequentialTest/1/')
Algorithm10.setXrdInterface(TOPAS1)
Algorithm10.XRDInterface.setDirectory(r'C:/PhD/Year_3/Algorithm/Test/SequentialTest/1/')
# Algorithm10.newStart()

