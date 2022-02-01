import estimation
import pickle
import numpy as np
import matplotlib as plt

with open('used_change_temp.pkl', 'rb') as f:
    usedLst = pickle.load(f)

# convert the list to an array for numpy calculations
usedLst = np.array(usedLst)
usedLst_mean = np.mean(np.array(usedLst), axis=1)

# create the matrix with the x values for all data points
A = []
for i in range(10):
    for j in range(1000):
        A.append([i**2, i, 1])
A = np.array(A)
x_all = estimation.solve_matrix(A, usedLst.flatten())

A = []
for i in range(10):
    A.append([i**2, i, 1])
A = np.array(A)

# get the 99th percentile for min and max value
sorted_use = np.sort(usedLst)
x_min_99 = estimation.solve_matrix(A, sorted_use[:, 10])
x_max_99 = estimation.solve_matrix(A, sorted_use[:, -10])

# plot the distribution of values with the fitted functions on top of it.
plt.scatter([i for i in range(10)], list(sorted_use[:, 10]))
plt.scatter([i for i in range(10)], list(sorted_use[:, -10]))
plt.violinplot(list(usedLst), [i for i in range(10)], widths=1, showmeans=True, showmedians=False, showextrema=False)
plt.plot(np.matmul(A, x_all), label="pred_all", zorder=10)
plt.plot(np.matmul(A, x_min_99), label="pred_min_99", zorder=20)
plt.plot(np.matmul(A, x_max_99), label="pred_max_99", zorder=30)
plt.legend()

# save plot for viewing.
path = "relevant_plots\\"
plt.savefig(path + "jet_stream_change_percentile.png")
