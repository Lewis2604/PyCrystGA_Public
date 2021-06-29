import math
import numpy as np
import xrdtools

pi = math.pi
lamda = 1.5406

data = xrdtools.read_xrdml(
    r'S:\PhD\Elliot\E6_p-benzoquione_SYC_HTTrans_4-40_30min_batch.xrdml')


# Collect two theta data
two_theta = data['x']

print(two_theta)

# Collect intensity data
intensity = data['data']


# Convert the data into d spacing


def Convert_Data_to_d_space(two_theta, intensity, pi, lamda):
    d_space = lamda / (2 * np.sin((two_theta / 2) * pi / 180))
    return d_space


Convert_Data_to_d_space(two_theta, intensity, pi, lamda)

dspace = Convert_Data_to_d_space(two_theta, intensity, pi, lamda)
print(dspace)

# new xy file (d,intensity)


import csv

with open(r'S:\PhD\Elliot\newxy_dspace.csv', 'w') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerows(zip(intensity, dspace))