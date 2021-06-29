from __future__ import division, print_function
import time
import numpy as np

import sys
sys.path.insert(0, "C:/Users/Lewis/Anaconda3/envs/G2GA/GSASII")

from Structure import *


import GSASIIscriptable as G2sc
import GSASIIpath
import GSASIImath as G2mth
import GSASIIspc as G2spc
import GSASIIobj
import GSASIIstrIO
import GSASIIctrlGUI as G2G
import GSASIIdataGUI as G2DG
import multiprocessing as mp
import GSASIIfiles as G2fil

from pprint import pprint

from biopandas.mol2 import PandasMol2
from rdkit import Chem
from rdkit.Chem import TorsionFingerprints


import wx

class GSASII:
    def evaluate(self):
        1./float(rwp),

    def makeG2(self):
        datadir = r"S:\PhD\Year_2\Algorithm\GSAS2"
        PathWrap = lambda fil: os.path.join(datadir, fil)
        molPath = PathWrap('TFB.mol')

        ##########################################################################
        # How to delete phases and histograms from project when no longer required
        ##########################################################################
        # This ensures that phases and histograms don't get duplicated
        time0 = time.time()
        gpx = G2sc.G2Project(newgpx=PathWrap('TFBtest.gpx'))
        # gpx = G2sc.G2Project(PathWrap('TFBtest.gpx'))

        pmol = PandasMol2().read_mol2(PathWrap('TFB.mol2'))

        rbXYZ = []
        atomType = []
        atomName = []

        for heading in pmol.df.iterrows():
            atomType.append(heading[1][1])
            rbXYZ.append([heading[1][2], heading[1][3], heading[1][4]])
            atomName.append(str(heading[1][1]) + str(heading[1][0]))

        numTorsAng = 3
        randomTorsAng = []
        for i in range(numTorsAng):
            randomTorsAng.append(random.uniform(0, 360))

        mol = Chem.MolFromMolFile(molPath)

        torsList = TorsionFingerprints.CalculateTorsionLists(
            Chem.MolFromMolFile(molPath))

        pprint('here')
        pprint(torsList)
        pprint(len(torsList))

        torsionLimits = []
        for num in randomTorsAng:
            limits = []
            limits.append(num)
            limits.append(num)
            torsionLimits.append(limits)

        pivotAtomIds = [[11, 15],
                        [10,16],
                        [9,17]]

        torsDict = []
        for i in range(numTorsAng):
            x = []
            y = torsList[0][i][0][0][1:3]
            for atomIds in y:
                x.append(atomIds)
            x.append(randomTorsAng[i])
            x.append(pivotAtomIds[i])
            torsDict.append(x)


        randPosition = []
        for i in range(3):
            randPosition.append(random.uniform(0, 1))

        randRotation = []
        for i in range(1):
            randRotation.append(random.uniform(0, 360))
        for i in range(3):
            randRotation.append(random.uniform(-1, 1))

        print('rigidBody')
        pprint(np.array(rbXYZ))

        gpx.data['Rigid bodies'] = {}
        gpx.data['Rigid bodies']['data'] = {'RBIds': {'Residue': [101], 'Vector': []},
                                            'Residue': {101: {
                                                'RBname': 'TFB',
                                                'SelSeq': [0, -23966],
                                                'atNames': atomName,
                                                'rbRef': [0, 1, 2, True],
                                                'rbSeq': torsDict,
                                                'rbTypes': atomType,
                                                'rbXYZ': np.array(rbXYZ),
                                                'useCount': 1},
                                                'AtInfo': {'C': [1.12, (144, 144, 144)],
                                                           'H': [0.98, (255, 255, 255)],
                                                           'O': [1.09, (255, 13, 13)]}},
                                            'Vector': {'AtInfo': {}}}


        time1 = time.time()
        hist0 = gpx.add_powder_histogram(PathWrap("TFB_4-49.xye"), PathWrap("TFB4-49_instrument_para.instprm"))
        time2 = time.time()
        print("Time for Hist")
        pprint(time2-time1)

        time3 = time.time()
        phase1 = gpx.add_phase(PathWrap("TFB-Dummy1.cif"), phasename="TFB-Simulation", histograms=[hist0], fmthint="CIF")
        time4 = time.time()
        print("Time add phase")
        pprint(time4-time0)
        # hist1 = gpx.add_simulated_powder_histogram(histname="TFB_Simulation", iparams=PathWrap("TFB4-49_instrument_para.instprm"), Tmin=4., Tmax=49., Tstep=0.02, phases=[phase1])


        # @todo deletes atoms from phase
        # pprint(gpx.phases()[0])
        gpx.phases()[0].data['Atoms'] = []
        gpx.phases()[0].data['Rigid bodies'] = gpx.data['Rigid bodies']['data']


        # @todo configuring of SA parameters
        gpx.phases()[0].data = {}

        # gpx.phases()[0].data['General']['NoAtoms'] = {}
        # gpx.phases()[0].data['General']['AngleRadii'] = []
        # gpx.phases()[0].data['General']['AtomMass'] = []
        # gpx.phases()[0].data['General']['AtomPtrs'] = []
        # gpx.phases()[0].data['General']['AtomTypes'] = []
        # gpx.phases()[0].data['General']['BondRadii'] = []
        # gpx.phases()[0].data['General']['Isotope'] = {}


        gpx.phases()[0].data['General']['MCSA controls'] = {'Algorithm': 'log',
                                                            'Annealing': [50.0, 0.001, 1], # [start T, End T, No. trials]
                                                            'Cycles': 1,
                                                            'Data source': 'PWDR TFB_4-49.xye',
                                                            'Jump coeff': [0.95, 0.5],
                                                            'Results': [],
                                                            'boltzmann': 1.0,
                                                            'dmin': 2.0, # used to capture a desirable number of reflections
                                                            'fast parms': [1.0, 1.0, 1.0],
                                                            'log slope': 0.9,
                                                            'newDmin': True,
                                                            'ranRange': 10.0}


        gpx.phases()[0].data['MCSA'] = {}
        gpx.phases()[0].data['MCSA']['AtInfo'] = {}
        gpx.phases()[0].data['MCSA']['AtInfo']['C'] = [1.12, (144, 144, 144)]
        gpx.phases()[0].data['MCSA']['AtInfo']['H'] = [0.98, (255, 255, 255)]
        gpx.phases()[0].data['MCSA']['AtInfo']['O'] = [1.09, (255, 13, 13)]
        gpx.phases()[0].data['MCSA']['Models'] = []

        # todo configure the rigid body for structure solution
        modelsDict1 = {'Coef': [1.0, False, [0.8, 1.2]],
                       'Type': 'MD',
                       'axis': [0, 0, 1]}
        modelsDict2 = {'MolCent': [[0.0, 0.0, 0.0], False],
                       'Ori': [randRotation, # [Oa, Oi, Oj, Ok] [rotationAngle, rotationVector]
                               [False, False, False, False],
                               [[0.0, 360.0],
                                [-1.0, 1.0],
                                [-1.0, 1.0],
                                [-1.0, 1.0]]],
                       'Ovar': '',
                       'Pos': [randPosition,
                               [False, False, False],
                               [[0.0, 1.0], [0.0, 1.0], [0.0, 1.0]]],
                       'RBId': 101,
                       'Tor': [randomTorsAng, # [0.0, 0.0, 0.0],  [torsion1, torsion2,...]
                               [True, False, False],
                               torsionLimits], #[[0.0, 360.0], [0.0, 360.0], [0.0, 360.0]]], #[[Torsion1 limits], []torsion2 limits, [...]]
                       'Type': 'Residue',
                       'name': 'TFB(1)'}
        pprint(torsionLimits)
        # print('x')
        # pprint(modelsDict1)
        # print('y')
        # pprint(modelsDict2)

        # @todo add rigid body to phase
        gpx.phases()[0].data['MCSA']['Models'].append(modelsDict1)
        gpx.phases()[0].data['MCSA']['Models'].append(modelsDict2)
        gpx.phases()[0].data['MCSA']['Results'] = []
        gpx.phases()[0].data['MCSA']['rbData'] = {'RBIds': {'Residue': [101], 'Vector': []},
                                                  'Residue': {101: {
                                                      'RBname': 'TFB',
                                                      'SelSeq': [0, -23966],
                                                      'atNames': atomName,
                                                      'rbRef': [0, 1, 2, True],
                                                      'rbSeq': torsDict,
                                                      'rbTypes': atomType,
                                                      'rbXYZ': np.array(rbXYZ),
                                                      'useCount': 1},
                                                      'AtInfo': {'C': [1.12, (144, 144, 144)],
                                                                 'H': [0.98, (255, 255, 255)],
                                                                 'O': [1.09, (255, 13, 13)]}},
                                                  'Vector': {'AtInfo': {}}}

        # @todo sets the histograms background

        hist0.set_refinements(
            {"Background": {'type': 'chebyschev-1', 'refine': False, 'no.coeffs': 20,
                            'coeffs': [5209.7714647941375, -4524.684002141375,
                                       1623.9795356450973, 104.33976239238277, -720.4412221382299,
                                       390.208847847956, 135.21844344760618, -282.4235239059763,
                                       222.05893403199647, 2.3360617905901035, -181.1109865591344,
                                       161.1621796515656, -81.78489476160603, -16.79960362542261,
                                       86.04303600357028, -47.74253635593697, 22.76231890736039,
                                       24.9031399376323, -51.51251876522956, 39.783302999707736]},
             "Sample Parameters": ["Scale"]})


        # @todo must come after the Rigid Body, MCSA, etc... dicts
        # @todo otherwise the atoms do not get removed from the phase and the rigid body doesn't get added
        gpx.data['Controls']['data']['max cyc'] = 0
        gpx.do_refinements([{}])

        print("data")
        pprint(gpx.phases()[0].data)


        result = G2mth.mcsaSearch(             data=gpx.phases()[0].data,
                                               RBdata=gpx.data['Rigid bodies']['data'],
                                               # RBdata=gpx.phases()[0].data['MCSA']['rbData'],
                                               reflType="PWDR",
                                               reflData=gpx.data["PWDR TFB_4-49.xye"]['Reflection Lists']['TFB-Simulation']['RefList'],
                                               covData=gpx.data['Covariance']['data'], pgbar=None)

        gpx.save()

        pprint(result[0][2])

startTime = time.time()

GSASII().makeG2()

endTime = time.time()

timeToComp = endTime-startTime

print(timeToComp)
