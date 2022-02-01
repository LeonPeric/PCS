import matplotlib.pyplot as plt
from Objects.plane import Plane
from Objects.wind import Wind
from Objects.jet_stream import Jet_stream
from Objects.flight import Flight
import pickle
import Constants
from Objects.estimation import Estimate
import os


def make_plots(runs=100):
    dt = 1
    boeing = Plane(max_velocity=Constants.SPEED, empty_weight=Constants.ZERO_FUEL, fuel=Constants.FUEL, max_height=Constants.MAX_HEIGHT,
                   power=Constants.MOTOR_POWER, wing_span=Constants.WING_SPAN, thrust=Constants.THRUST, takeoff_speed=Constants.TAKEOFF_SPEED)

    # -1 for no wind
    wind = Wind(-1, dt)

    # 0 to ensure no jet streams
    jet_stream = Jet_stream(0, 0, 0)
    flight_sim = Flight(boeing, wind, jet_stream, Constants.DISTANCE, Constants.AIR_DENSITTY)
    flight_sim.run_sim(Constants.ANGLE)
    # fuel-time with no random circumstances
    fig, ax = plt.subplots(1)
    # print(usedLst)
    ax.plot(flight_sim.timeLst, flight_sim.fuelLst)
    ax.set_xlabel("Time in seconds")
    ax.set_ylabel("Fuel use in kg")
    ax.set_title("Fuel use of time in a baseline flight")
    fig.savefig(os.path.join("simulations", "baseline_fuel_usage.png"))
    plt.close(fig)

    # wind_speed
    path = os.path.join("simulations", "wind")
    usedLst = []

    # we make use of 7, because above this it is to dangerous to fly anyway.
    for i in range(7):
        used = []
        print(i)
        for j in range(runs):
            wind = Wind(i, dt)
            flight_sim = Flight(boeing, wind, jet_stream, Constants.DISTANCE, Constants.AIR_DENSITTY)
            flight_sim.run_sim(Constants.ANGLE)
            used.append(flight_sim.total_fuel_used)
        usedLst.append(used)

    with open(os.path.join(path, "wind_data.pkl"), "wb") as f:
        pickle.dump(usedLst, f)

    # 3 because a third order polynomial was a good fit for our data.
    Estimate(os.path.join(path, "wind_data.pkl"), 3, 0, os.path.join(path, "wind_plot"),
             "Fuel usage against wind power", "Wind power on the scale of Beaufort", "Fuel usage in kg").plot_estimation()

    # reset the wind so that wind doesn't influence the jet stream simulations.
    wind = Wind(-1, dt)

    # jet_stream_thickness
    path = os.path.join("simulations", "jetstream")
    usedLst = []

    # 1, 10 because average thickness is 5 km so we want to check a few values below and above it.
    for i in range(1, 10):
        used = []
        print(i)
        for j in range(runs):
            # 1000 to change from km to m
            # 60 to have an minute between each jet stream
            # 1 so the scale is 1
            jet_stream = Jet_stream(i*1000, 60, 1)
            flight_sim = Flight(boeing, wind, jet_stream, Constants.DISTANCE, Constants.AIR_DENSITTY)
            flight_sim.run_sim(Constants.ANGLE)
            used.append(flight_sim.total_fuel_used)
        usedLst.append(used)

    with open(os.path.join(path, "jet_stream_thickness_data.pkl"), "wb") as f:
        pickle.dump(usedLst, f)

    Estimate(os.path.join(path, "jet_stream_thickness_data.pkl"), 3, 1, os.path.join(path, "jet_stream_thickness"),
             "Fuel usage against jet stream thickness", "Jet stream thickness in km", "Fuel usage in kg").plot_estimation()

    # jet stream time diff
    usedLst = []

    # 1, 15 our maximum time diff is 15 minutes.
    for i in range(1, 15):
        used = []
        print(i)
        for j in range(runs):
            # 5000 average jet stream thickness is 5 km
            # 60 to change to i from seconds to minutes
            # 1 so the scale is 1
            jet_stream = Jet_stream(5000, i * 60, 1)
            flight_sim = Flight(boeing, wind, jet_stream, Constants.DISTANCE, Constants.AIR_DENSITTY)
            flight_sim.run_sim(Constants.ANGLE)
            used.append(flight_sim.total_fuel_used)
        usedLst.append(used)

    with open(os.path.join(path, "jet_stream_time_diff_data.pkl"), "wb") as f:
        pickle.dump(usedLst, f)

    Estimate(os.path.join(path, "jet_stream_time_diff_data.pkl"), 3, 1, os.path.join(path, "jet_stream_time_diff_plot"),
             "Fuel usage against jet stream time difference", "Jet stream time difference in minutes", "Fuel usage in kg").plot_estimation()


def main():
    while True:
        try:
            runs = int(input("How many runs do you want to run? "))
            break
        except TypeError:
            print("Please input an integer")
    make_plots(runs=runs)


if __name__ == "__main__":
    main()
