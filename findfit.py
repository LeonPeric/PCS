import os
from Objects.estimation import Estimate



# path = os.path.join("simulations", "fitting", "wind")
# #2
# for i in range(1,6):
#     Estimate(os.path.join(path, "wind_data.pkl"), i, 0, os.path.join(path, f"wind_plot_{i}"),
#             "Fuel ussage against wind power", "Wind power on the scale of Beaufort", "Fuel usage in kg").plot_estimation()






path = os.path.join("simulations", "fitting", "jetstream")

# 2
# for i in range(1,6):
#     Estimate(os.path.join(path, "jet_stream_thickness_data.pkl"), i, 1, os.path.join(path, f"jet_stream_thickness_{i}"),
#             "Fuel ussage against jet stream thickness", "Jet stream thickness in km", "Fuel usage in kg").plot_estimation()

for i in range(1,6):
    Estimate(os.path.join(path, "jet_stream_time_diff_data.pkl"), i, 1, os.path.join(path, f"jet_stream_time_diff_plot_{i}"),
            "Fuel ussage against jet stream time difference", "Jet stream time difference in minutes", "Fuel usage in kg").plot_estimation()
