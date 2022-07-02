import math
import matplotlib.pyplot as plt

file = "D:/PhD/Year_4/Algorithm/" + "logPlot"

numGen = 1600

genList = [i+1 for i in range(numGen)]

y1 = []
y2 = []
y3 = []
y4 = []
y5 = []

y11 = []
y22 = []
y33 = []
y44 = []
y55 = []

for i in genList:
    y1.append(math.log(i, numGen))
    y2.append(math.log(i, numGen)**2)
    y3.append(math.log(i, numGen)**3)
    y4.append(math.log(i, numGen)**4)
    y5.append(math.log(i, numGen)**5)

for i in y1:
    y11.append(1-i)

for i in y2:
    y22.append(1-i)

for i in y3:
    y33.append(1-i)

for i in y4:
    y44.append(1-i)

for i in y5:
    y55.append(1-i)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,4))

# plt.figure = (figszie=(2,1))

ax1.set_ylabel("GO Rate", fontsize=12)
ax1.set_xlabel("Generation", fontsize=12)
ax2.set_xlabel("Generation", fontsize=12)

ax1.set_title("ILMDHC")
ax2.set_title("DHMILC")

ax1.plot(genList, y1, color="tab:blue", label="MR1", linestyle='dashed')
ax1.plot(genList, y2, color="tab:orange", label="MR2", linestyle='dashed')
ax1.plot(genList, y3, color='tab:green', label="MR3", linestyle='dashed')
ax1.plot(genList, y4, color='tab:red', label="MR4", linestyle='dashed')
ax1.plot(genList, y5, color='tab:purple', label="MR5", linestyle='dashed')

ax1.plot(genList, y11, color="tab:blue", label="CR1")
ax1.plot(genList, y22, color="tab:orange", label="CR2")
ax1.plot(genList, y33, color='tab:green', label="CR3")
ax1.plot(genList, y44, color='tab:red', label="CR4")
ax1.plot(genList, y55, color='tab:purple', label="CR5")


ax2.plot(genList, y11, color="tab:blue", label="MR1", linestyle='dashed')
ax2.plot(genList, y22, color="tab:orange", label="MR2", linestyle='dashed')
ax2.plot(genList, y33, color='tab:green', label="MR3", linestyle='dashed')
ax2.plot(genList, y44, color='tab:red', label="MR4", linestyle='dashed')
ax2.plot(genList, y55, color='tab:purple', label="MR5", linestyle='dashed')

ax2.plot(genList, y1, color="tab:blue", label="CR1")
ax2.plot(genList, y2, color="tab:orange", label="CR2")
ax2.plot(genList, y3, color='tab:green', label="CR3")
ax2.plot(genList, y4, color='tab:red', label="CR4")
ax2.plot(genList, y5, color='tab:purple', label="CR5")

ax1.legend(loc="center right")
ax2.legend(loc="center right")

plt.savefig(file, dpi=300)
