from xtb import *
from xtb.interface import Molecule
import numpy as np

numbers = np.array([8, 1, 1])
positions = np.array([
    [ 0.00000000000000, 0.00000000000000,-0.73578586109551],
    [ 1.44183152868459, 0.00000000000000, 0.36789293054775],
    [-1.44183152868459, 0.00000000000000, 0.36789293054775]])

mol = Molecule(numbers, positions)
len(mol)