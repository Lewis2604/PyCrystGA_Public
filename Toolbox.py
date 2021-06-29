from deap import base
from deap import tools

toolbox = base.Toolbox()

toolbox.register("mateOnePoint", tools.cxOnePoint)
toolbox.register("mateTwoPoint", tools.cxTwoPoint)
toolbox.register("mateUniform", tools.cxUniform, indpb=0.05)
toolbox.register("matePartMatched", tools.cxPartialyMatched)
toolbox.register("mateUniPartMatched", tools.cxUniformPartialyMatched, indpb=0.05)
toolbox.register("mateOrdered", tools.cxOrdered)
toolbox.register("mateBlend", tools.cxBlend, alpha=1) # 12|345|67 -> 32|147|65
toolbox.register("mateESBlend", tools.cxESBlend, alpha=1)
toolbox.register("mateESTwoPoint", tools.cxESTwoPoint)
toolbox.register("mateSimBin", tools.cxSimulatedBinary, eta=10)
toolbox.register("mateSimBinBound", tools.cxSimulatedBinaryBounded, eta=10, low=0, up=360)
toolbox.register("mateMessyOnePoint", tools.cxMessyOnePoint)
toolbox.register("rotateMutateStatic", tools.mutPolynomialBounded, eta=1, low=0, up=360, indpb=0.25)
toolbox.register("translateMutateStatic", tools.mutPolynomialBounded, eta=1, low=-0.5, up=1.5, indpb=100)
toolbox.register("mutateDynamic", tools.mutGaussian, mu=0, sigma=4, indpb=1)
toolbox.register("randSelect", tools.selRandom)
toolbox.register("tournSelect", tools.selTournament, fit_attr='fitness')
toolbox.register("rouletteSelect", tools.selRoulette, fit_attr='fitness')
toolbox.register("bestSelect", tools.selBest)