"""
This file is used to generate statistics like min value, max value and the 1th and 99th percentile for the writing of the report and poster.
"""

import pickle
import numpy as np
import os
import csv


def get_stats(list):
    min_value = min(list)
    max_value = max(list)
    average = np.mean(list)

    sorted_list = sorted(list)
    lowest_percentile = np.percentile(sorted_list, 1)
    highest_percentile = np.percentile(sorted_list, 99)

    return [min_value, max_value, average, lowest_percentile, highest_percentile]


# first for wind force
path = os.path.join("simulations", "wind", "wind_data.pkl")
with open(path, "rb") as f:
    wind_data = pickle.load(f)

wind_stats = []
for i, row in enumerate(wind_data):
    wind_stats.append([f"wind:{i} "] + get_stats(row))


path = os.path.join("simulations", "jetstream", "jet_stream_thickness_data.pkl")
with open(path, "rb") as f:
    jetstream_thickness_data = pickle.load(f)

jetstream_thickness = []
for i, row in enumerate(jetstream_thickness_data):
    jetstream_thickness.append([f"Jetstream thickness:{i+1} "] + get_stats(row))

path = os.path.join("simulations", "jetstream", "jet_stream_time_diff_data.pkl")
with open(path, "rb") as f:
    jet_stream_time_diff_data = pickle.load(f)

jet_stream_time_diff = []
for i, row in enumerate(jet_stream_time_diff_data):
    jet_stream_time_diff.append([f"Jet stream time diff:{i+1} "] + get_stats(row))

# save everything to csv file for ease of use.
with open(os.path.join("simulations", "simulations_stats.csv"), "w") as f:
    writer = csv.writer(f)

    writer.writerow(["Min_value", "Max_value", "Average", "Lowest_percentile", "Highest_percentile"])
    for row in wind_stats:
        writer.writerow(row)

    for row in jetstream_thickness:
        writer.writerow(row)

    for row in jet_stream_time_diff:
        writer.writerow(row)
