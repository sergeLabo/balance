#!python3

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator

file_name = "./log/log-20210208-104017.txt"
with open(file_name) as f:
    data = f.read()
f.close()

lines = data.splitlines()

step_total = []
steps = []
reward_t = []
tsecond = []

for line in lines:
    d_l = line.split(" ")
    step_total.append(int(d_l[0]))
    steps.append(int(d_l[1]))
    reward_t.append(int(float(d_l[2])))
    tsecond.append(float(d_l[3]))
# Moyenne des reward sur 10 épisodes
reward = []
x = []
n = 10
for k in range(int(len(reward_t)/n)):
    somme = 0
    for j in range(10):
        reward_t[-1] = 0
        somme += reward_t[k*n + j] - reward_t[k*n + j -1]
    # #print(somme/n)
    reward.append(somme/n)
    x.append(k)

fig, ax = plt.subplots(1, 1, figsize=(16,20), facecolor='#cccccc')

ax.set_facecolor('#eafff5')
ax.set_title('Moyenne des Récompenses de 10 épisodes', size=24, color='magenta')
# #ax.set_ylim(0, 12)
ax.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)
ax.set_xlabel('10 Episodes', color='coral', size=20)
ax.set_ylabel('Récompense', color='coral', size=20)

l = ax.plot(x, reward,
            linestyle=(0, (3, 5, 1, 5)),
            linewidth=1.5,
            color='red',
            label="Loss")

# #a = ax.plot(step_total, tsecond,
            # #linestyle=(0, (5, 5)),
            # #linewidth=1.5,
            # #color='green',
            # #label="Average")

# #ax.axhline(y=0.1, xmin=0.0, xmax=1, color='r')
# #ax.text(0, 0.2, "Objectif = 0.1", weight='bold', color='blue')

# #ax.legend(loc="upper right", title="Efficiency")

fig.savefig("efficiency.png")
plt.show()
