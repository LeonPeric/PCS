import numpy as np
import matplotlib.pyplot as plt
import pickle
import estimation

with open('used.pkl', 'rb') as f:
    usedLst = pickle.load(f)

# convert the list to an array for numpy calculations
usedLst = np.array(usedLst)
usedLst_mean = np.mean(np.array(usedLst), axis=1)

# create the matrix with the x values for all data points
A = []
# 7 because there are 7 x values
# 10000 because for every x value there are a 10000 data points
for i in range(7):
    for j in range(10000):
        A.append([i**3, i**2, i, 1])
A = np.array(A)
x_all = estimation.solve_matrix(A, usedLst.flatten())


# create the matrix with the x values for one data point per step
A = []

# 7 because there are 7 x values.
for i in range(7):
    A.append([i**3, i**2, i, 1])
A = np.array(A)

# get the 99th percentile for min and max value
sorted_use = np.sort(usedLst)
x_min_99 = estimation.solve_matrix(A, sorted_use[:, 100])
x_max_99 = estimation.solve_matrix(A, sorted_use[:, -100])

# plot the distribution of values with the fitted functions on top of it.
plt.violinplot(list(usedLst), [i for i in range(7)], widths=1, showmeans=True, showmedians=False, showextrema=False)
plt.plot(np.matmul(A, x_all), label="pred_all", zorder=10)
plt.plot(np.matmul(A, x_min_99), label="pred_min_99", zorder=20)
plt.plot(np.matmul(A, x_max_99), label="pred_max_99", zorder=30)
plt.legend()

# save plot for viewing.
path = "plots/1000_sims/"
plt.savefig(path + "fuel_usage_percentile.png")
