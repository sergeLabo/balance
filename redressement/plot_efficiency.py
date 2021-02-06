#!python3

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator

file_name = "./log-20210205-165713.txt"
with open(file_name) as f:
    data = f.read()
f.close()

lines = data.splitlines()

step_total = []
steps = []
reward_total = []
tsecond = []

for line in lines:
    d_l = line.split(" ")
    step_total.append(int(d_l[0]))
    steps.append(int(d_l[1]))
    reward_total.append(float(d_l[2]))
    tsecond.append(float(d_l[3]))

fig, ax = plt.subplots(1, 1, figsize=(8,8), facecolor='#cccccc')

ax.set_facecolor('#eafff5')
ax.set_title('Efficacité', size=18, color='magenta')

ax.set_ylim(0, 12)

ax.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)

ax.set_xlabel('Steps (number)', color='coral', size=20)
ax.set_ylabel('Loss', color='coral', size=20)

l = ax.plot(tsecond, reward_total,
            linestyle=(0, (3, 5, 1, 5)),
            linewidth=1.5,
            color='red',
            label="Loss")

# #a = ax.plot(theures, average,
            # #linestyle=(0, (5, 5)),
            # #linewidth=1.5,
            # #color='green',
            # #label="Average")

# #ax.axhline(y=0.1, xmin=0.0, xmax=1, color='r')

# #ax.text(0, 0.2, "Objectif = 0.1", weight='bold', color='blue')

ax.legend(loc="upper right", title="Efficiency")

# #fig.savefig("efficiency.png")
plt.show()
