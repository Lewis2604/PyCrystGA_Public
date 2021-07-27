import regex as re
from XRDInterfaces.TOPAS import *
from ase.io import read, write


# -------------------------------------------------------------------------
# f = open(r"C:\PhD\Year_3\TFB1 GA p21n.inp")
# lines = f.readlines()
#
# tranString = 't[a-c]'
# tranRegex = r'(\b' + tranString + r'\s*\s+)([+-]?\d+\.?\d*)'
# tran = re.compile(tranRegex)
#
#
# numbers = []
# for num, line in enumerate(lines):
#     match = tran.search(line)
#     if match:
#         numbers.append(num)
#
# lastNumber = numbers[-1]
# cifLineNumber = lastNumber + 1
# -------------------------------------------------------------------------

# file = r"C:\PhD\Year_3\TFB1_GA_p21n.inp"
# cifFile = r"C:\PhD\Year_3\TFB1_GA_p21n.cif"
xyzFile = r"C:\PhD\Year_3\TFB1_GA_p21n.xyz"
xyzFile1 = r"C:\Users\Lewis\Documents\XTB\coords.xyz"
# molFile = "C:/PhD/Year_3/Algorithm/TFB Crystal Structure/TFB_labels.mol"
xyzMol = r"C:\Users\Lewis\Documents\XTB\TFB_labels.xyz"
peridoicFile = r"C:PhD\Year_3\TFB1_GA_p21n_MOD.xyz"
POSCARFile = r"C:PhD\Year_3\amonia.poscar"

def makeCIF(file, cifFile):
    with open(file, "a+") as file_object:
        file_object.seek(0)
        data = file_object.read(100)
        if len(data) > 0 :
            file_object.write("\n")
        file_object.write("Out_CIF_STR" + "(" + '\"' + str(cifFile) +'\"' + ")")

    TOPAS('C:/Topas-6/tc.exe', r"C:\PhD\Year_3\TFB1_GA_p21n.inp").runInputFile(file)


def makeXYZ(initialFile, xyzFile):
    write(xyzFile, read(initialFile))


def runEnergyOptMol(xyzFile, level, wrkDir):
    subprocess.run(os.path.normpath(r"C:\Users\Lewis\Documents\XTB\xtb.exe") + ' '
                            + os.path.normpath(xyzFile + " --opt " + level), cwd=wrkDir)


# runEnergyOptMol(xyzFile1, "crude", "S:/PhD/Year_3/PhD/Year_3/Algorithm/Test/")


def runEnergyOptCryst(poscarFile, level, wrkDir):
    subprocess.run(os.path.normpath(r"C:\Users\Lewis\Documents\XTB\xtb.exe") + " --opt " + os.path.normpath(
        level + poscarFile), cwd=wrkDir)

runEnergyOptCryst(POSCARFile, "0", "S:/PhD/Year_3/PhD/Year_3/Algorithm/Test/")
# makeCIF(r"C:\PhD\Year_3\TFB1_GA_p21n.inp", r"C:\PhD\Year_3\TFB1_GA_p21n.cif")

# makeXYZ(r"S:\PhD\Year_3\Crystal Structures\TFB\TFB_labels.mol",
#         r"S:\PhD\Year_3\Crystal Structures\TFB\TFB_labels.xyz")

# runEnergyOpt(xyzMol, "crude", "S:/PhD/Year_3/PhD/Year_3/Algorithm/Test/")


# def extractEnergy(file):


# cifFile1 = r"C:\PhD\Year_3\TFB1_GA_p21n(1).cif"
# xyzFile1 = r"C:\PhD\Year_3\xtblast.xyz"
#
# write(cifFile1, read(xyzFile1))
