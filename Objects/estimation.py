import numpy as np
import pickle
import matplotlib.pyplot as plt


class Estimate():
    """
        Finding the polynomial values for the simulated data and plot polynomial in the violin plots.
        Attributes:
            input_file: str
                the location of the simulated data.
            highest_polynomial_power: int
                highest power of the polynomial you want to fit.
            x_start: int
                first x value
            output_path: str
                the location of where you want the plots to be stored.

        Methods:
            solve_matrix(A, b):
                Finding the polynomial values for a function based on given data matrix A and vector b.
            plot_estimation:
                Find the polynomial for the data and plot said polynomial in the voilin plots.

        """
    def __init__(self, input_file, highest_polynomial_power, start_x, output_path, title, xlabel, ylabel):
        self.input_file = input_file
        self.highest_polynomial_power = highest_polynomial_power
        self.start_x = start_x
        self.output_path = output_path
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel

    def solve_matrix(self, A, b):
        """
        Finding the polynomial values for a function based on given data matrix A and vector b.

        A: np.array(m,n)
            The x values of all the datapoints.
        b: np.array(m, 1):
            The y values of the corresponding x values in matrix A.
        """
        ATA = np.matmul(A.T, A)
        Inverse_ATA = np.linalg.inv(ATA)
        Inverse_AT = np.matmul(Inverse_ATA, A.T)
        x = np.matmul(Inverse_AT, b)

        return x

    def plot_estimation(self):
        """
        Find the polynomial for the data and plot said polynomial in the voilin plots.
        """
        with open(self.input_file, 'rb') as f:
            usedLst = pickle.load(f)

        # convert the list to an array for numpy calculations
        usedLst = np.array(usedLst)

        arr_shape = usedLst.shape
        x_count = arr_shape[0]
        y_count = arr_shape[1]

        # create the matrix with the x values for all data points
        A = []

        for x in range(self.start_x, self.start_x + x_count):
            for j in range(y_count):
                A.append([x**i for i in range(self.highest_polynomial_power+1)])
        A = np.array(A)
        x_all = self.solve_matrix(A, usedLst.flatten())

        # create the matrix with the x values for one data point per step
        A = []
        for x in range(self.start_x, self.start_x + x_count):
            A.append([x**i for i in range(self.highest_polynomial_power+1)])
        A = np.array(A)

        # get the 99th percentile for min and max value
        sorted_use = np.sort(usedLst)
        x_min_99 = self.solve_matrix(A, sorted_use[:, int(y_count*0.01)])
        x_max_99 = self.solve_matrix(A, sorted_use[:, -int(y_count*0.01)])

        # plot the distribution of values with the fitted functions on top of it.
        x_range = [i for i in range(self.start_x, self.start_x + x_count)]
        # save only the violinplot.
        plt.violinplot(list(usedLst), x_range, widths=1, showmeans=True, showmedians=False, showextrema=False)
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.savefig(self.output_path + "_violin.png")

        # now continue adding the scatter en fitted line.
        plt.scatter(x_range, sorted_use[:, int(y_count*0.01)], c="Orange")
        plt.scatter(x_range, sorted_use[:, -int(y_count*0.01)], c="Red")
        plt.plot(x_range, np.matmul(A, x_all), label="mean fitted line", zorder=10, c="Blue")
        plt.plot(x_range, np.matmul(A, x_min_99), label="1 percentile fitted line", zorder=20, c="Orange")
        plt.plot(x_range, np.matmul(A, x_max_99), label="99 percentile fitted line", zorder=30, c="Red")
        plt.legend()

        # save plot for viewing.
        plt.savefig(self.output_path + "_fitted_line.png")
        plt.close()
