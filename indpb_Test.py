from Toolbox import *

data1 = [1,2,3,4,5,6,7,8,9]
data2 = [1,2,3,4,5,6,7,8,9]

data3 = tools.mutPolynomialBounded(data1, eta=1, low=0, up=360, indpb=1)

data4 = tools.mutPolynomialBounded(data2, eta=0.1, low=0, up=360, indpb=1)

print(data3)
print(data4)