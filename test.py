import pickle
import numpy as np
import matplotlib.pyplot as plt

with open('used.pkl', 'rb') as f:
    test = pickle.load(f)

fig, ax = plt.subplots(1, figsize = (25,10))

# usedLst = np.array(test)
# print(usedLst.shape)
usedLst = list(np.array(test)[:,0:1000])
# usedLst = test
# print(usedLst.shape)
# print(len(usedLst))
bars = [f"WP: {i+1}" for i in range(0,7)]
# print(usedLst)

print(len(usedLst))
print(len([i*2 for i in range(7)]))
vp_1 = ax.violinplot(usedLst, [i*2 for i in range(7)], widths=2, showmeans=True, showmedians=False, showextrema=False)
ax.set_xticks([i*2 for i in range(7)])
ax.set_xticklabels(bars)
ax.title.set_text("Effect of wind on fuel usage")
ax.set_xlabel("Wind power on the scale of Beaufort")
ax.set_ylabel("Fuel ussage in kg")
fig.savefig("plots/fuel_use_wind_wf7_1000.png")
plt.close(fig)