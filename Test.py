from PyCrystGA import *
from TOPAS import *

print("Script has started")

TOPAS = TOPAS('C:/Topas-6/tc.exe', r"S:\PhD\Year_3\Algorithm\TOPAS\Template\TFB1\TFB1 GA p21n.inp")


Algorithm1 = PyCrystGA('C:/PhD/Year_3/Algorithm/TFB Crystal Structure/TFB_labels.mol', # Mol file
                        1, # Z'
                        'C:/PhD/Year_3/Algorithm/Test/LinearDynamic/1/', # Working directory
                        TOPAS, # XRD Interface
                        20, # Population Size
                        5, # Maximum Number of Generations
                        0.1, # Crossover Rate
                        0.1, # Mutation rate
                        0, # Crossover type, 0 static, 1 linear, 2 exponential
                        1, # Mutation type, 0 static, 1 linear, 2 exponential
                        5, # Percentage difference threshold for genetic operators
                        14, # Graph font size
                        12, # Graph label size
                        'PyCrystGA_Graph', # Graph file name
                        'PyCrystGA_PctDiff_Graph', # Percentage difference graph name
                        300) # Graph dpi

Algorithm1.start()


print("Script has ended")


