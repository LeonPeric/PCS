import matplotlib.pyplot as plt
import math

from sklearn.preprocessing import scale
from Objects.plane import Plane
from Objects.wind import Wind
from Objects.jet_stream import Jet_stream
from Objects.temperature import Temperature
from Objects.flight import Flight
import pickle
# def test_wind(plane):


def make_plots(runs=100):
    DISTANCE = 5862.03*1000  # m (distance Amsterdam - New York)
    SPEED = 900/3.6  # m/s
    FUEL = 126370
    ZERO_FUEL = 181400  # KG
    FUEL = 80000  # KG
    MAX_HEIGHT = 13100  # m
    MOTOR_POWER = 7.7/(1000*1000)  # kg/N*S
    WING_SPAN = 360.5  # m2
    C = 0.012  # air drag coefficent of subsonic transport airplane.
    AIR_DENSITTY = 1.225  # kg/m^3
    # IMPULSE = 13200
    THRUST = 360.4 * 1000 * 2  # N/s
    ASCEND_ANGLE_NOSE = math.radians(15)
    DESCEND_ANGLE_NOSE = math.radians(-3)
    ASCEND_ANGLE_WING = math.radians(25)
    DESCEND_ANGLE_WING = math.radians(-25)
    ASCEND_ANGLE = (ASCEND_ANGLE_WING, ASCEND_ANGLE_NOSE)
    DESCEND_ANGLE = (DESCEND_ANGLE_WING, DESCEND_ANGLE_WING)
    TAKEOFF_SPEED = 100  # m/s
    JET_MINSPEED = 25  # m/s
    JET_MAXSPEED = 100  # m/s
    LATITUDE = math.radians(50)
    AVG_TEMPERATURE = 221  # K
    dt = 1
    boeing = Plane(max_velocity=SPEED, empty_weight=ZERO_FUEL, fuel=FUEL, max_height=MAX_HEIGHT,
                   power=MOTOR_POWER, wing_span=WING_SPAN, thrust=THRUST, takeoff_speed=TAKEOFF_SPEED)
    wind = Wind(-1, dt)
    temperature = Temperature(0, 0, AVG_TEMPERATURE, dt)
    jet_stream = Jet_stream(5/1000, 60, 1)
    flight_sim = Flight(boeing, wind, jet_stream, temperature, DISTANCE, AIR_DENSITTY)
    flight_sim.run_sim(ASCEND_ANGLE_NOSE)

    # fuel-time
    fig, ax = plt.subplots(1)
    # print(usedLst)
    ax.plot(flight_sim.timeLst, flight_sim.fuelLst)
    ax.set_xlabel("Time in seconds")
    ax.set_ylabel("Fuel use in kg")
    ax.set_title("Fuel use of time in a baseline flight")
    fig.savefig("plots/100_sims/fuel_use_time.png")
    plt.close(fig)
    # plt.violinplot([i for i in range(10)], usedLst)
    # plt.xticks([i for i in range(10)], bars)

    # wind_speed
    # path = "plots/1000_sims/"
    # usedLst = []
    # usedLst_diff_mean = []
    # usedLst_diff = []
    # wind = Wind(-1,dt)
    # flight_sim = Flight(boeing, wind, jet_stream, temperature, DISTANCE, AIR_DENSITTY)
    # flight_sim.run_sim(ASCEND_ANGLE_NOSE, DESCEND_ANGLE)
    # zero_fuel_use = flight_sim.total_fuel_used
    # for i in range(0,7):
    #     used = []
    #     used_diff = []
    #     print(i)
    #     for j in range(runs):
    #         wind = Wind(i, dt)
    #         flight_sim = Flight(boeing, wind, jet_stream, temperature, DISTANCE, AIR_DENSITTY)
    #         flight_sim.run_sim(ASCEND_ANGLE_NOSE, DESCEND_ANGLE)
    #         used.append(flight_sim.total_fuel_used)
    #         used_diff.append(flight_sim.total_fuel_used - zero_fuel_use)
    #     usedLst.append(used)
    #     usedLst_diff.append(used_diff)
    #     usedLst_diff_mean.append(np.mean(used_diff))

    # fig, ax = plt.subplots(1, figsize = (25,10))
    # bars = [f"WP: {i}" for i in range(0,7)]
    # # print(usedLst)
    # vp_1 = ax.violinplot(usedLst, [i*2 for i in range(7)], widths=2, showmeans=True, showmedians=False, showextrema=False)
    # ax.set_xticks([i*2 for i in range(7)])
    # ax.set_xticklabels(bars)
    # ax.title.set_text("Effect of wind on fuel usage")
    # ax.set_xlabel("Wind power on the scale of Beaufort")
    # ax.set_ylabel("Fuel useage in kg")
    # fig.savefig(path+"fuel_use_wind_wf7.png")
    # plt.close(fig)

    # wind speed against average
    # fig, ax = plt.subplots(1, figsize = (25,10))
    # plot = ax.bar([i for i in range(7)], usedLst_diff_mean)
    # ax.title.set_text("Effect of wind on fuel usage")
    # ax.set_xlabel("Wind power on the scale of Beaufort")
    # ax.set_ylabel("Fuel useage in kg")
    # fig.savefig(path+"fuel_use_wind_wf_7_diff_mean.png")
    # plt.close(fig)

    # wind_speed
    # fig, ax = plt.subplots(1, figsize = (25,10))
    # bars = [f"WP: {i}" for i in range(0,7)]
    # # print(usedLst)
    # vp_1 = ax.violinplot(usedLst_diff, [i*2 for i in range(7)], widths=2, showmeans=True, showmedians=False, showextrema=False)
    # ax.set_xticks([i*2 for i in range(7)])
    # ax.set_xticklabels(bars)
    # ax.title.set_text("Effect of wind on fuel usage")
    # ax.set_xlabel("Wind power on the scale of Beaufort")
    # ax.set_ylabel("Fuel useage in kg")
    # fig.savefig(path + "fuel_use_wind_wf_7_diff.png")
    # plt.close(fig)

    # with open(path+'used.pkl', 'wb') as f:
    #     pickle.dump(usedLst, f)
    # temperature scale
    # wind = Wind(-1, dt)
    # usedLst = []
    # for i in range(10):
    #     used = []
    #     print(i)
    #     for j in range(runs):
    #         temperature = Temperature(i, 0, AVG_TEMPERATURE, dt)
    #         flight_sim = Flight(boeing, wind, jet_stream, temperature, DISTANCE, AIR_DENSITTY)
    #         flight_sim.run_sim(ASCEND_ANGLE_NOSE)
    #         used.append(flight_sim.total_fuel_used)
    #     usedLst.append(used)

    # fig, ax = plt.subplots(1, figsize=(25, 10))
    # bars = [f"Scale: {i}" for i in range(10)]
    # # print(usedLst)
    # ax.violinplot(usedLst, [i*2 for i in range(10)], widths=2, showmeans=True, showmedians=False, showextrema=False)
    # ax.set_xticks([i*2 for i in range(10)])
    # ax.set_xticklabels(bars)
    # ax.title.set_text("Effect of temprature range/jet stream on fuel useage")
    # ax.set_xlabel("Range of temperature")
    # ax.set_ylabel("Fuel useage in kg")
    # fig.savefig("plots/fuel_use_temp_scale.png")
    # plt.close(fig)

    # with open('used_scale_temp.pkl', 'wb') as f:
    #     pickle.dump(usedLst, f)

    # temperature change
    usedLst = []
    for i in range(1,10):
        used = []
        print(i)
        for _ in range(runs):
            temperature = Temperature(1, i/100, AVG_TEMPERATURE, dt)
            jet_stream = Jet_stream(i*1000, 60, 1, scale=3)
            flight_sim = Flight(boeing, wind, jet_stream, temperature, DISTANCE, AIR_DENSITTY)
            flight_sim.run_sim(ASCEND_ANGLE_NOSE)
            used.append(flight_sim.total_fuel_used)
        usedLst.append(used)

    fig, ax = plt.subplots(1, figsize=(25, 10))
    bars = [f"Scale: {i}" for i in range(1,10)]
    # print(usedLst)
    ax.violinplot(usedLst, [i*2 for i in range(9)], widths=2, showmeans=True, showmedians=False, showextrema=False)
    ax.set_xticks([i*2 for i in range(9)])
    ax.set_xticklabels(bars)
    ax.title.set_text("Effect of longer jet streams changes on fuel useage")
    ax.set_xlabel("Jet stream lenght in km")
    ax.set_ylabel("Fuel useage in kg")
    fig.savefig("plots/fuel_use_stream_lenght_change.png")
    plt.close(fig)

    usedLst = []
    for i in range(1,16):
        used = []
        print(i)
        for _ in range(runs):
            temperature = Temperature(1, i/100, AVG_TEMPERATURE, dt)
            jet_stream = Jet_stream(5*1000, i * 60, 1, scale=3)
            flight_sim = Flight(boeing, wind, jet_stream, temperature, DISTANCE, AIR_DENSITTY)
            flight_sim.run_sim(ASCEND_ANGLE_NOSE)
            used.append(flight_sim.total_fuel_used)
        usedLst.append(used)

    fig, ax = plt.subplots(1, figsize=(25, 10))
    bars = [f"Scale: {i}" for i in range(1,16)]
    # print(usedLst)
    ax.violinplot(usedLst, [i*2 for i in range(15)], widths=2, showmeans=True, showmedians=False, showextrema=False)
    ax.set_xticks([i*2 for i in range(15)])
    ax.set_xticklabels(bars)
    ax.title.set_text("Effect of longer time between streams changes on fuel useage")
    ax.set_xlabel("Pause between different jet streams")
    ax.set_ylabel("Fuel useage in kg")
    fig.savefig("plots/fuel_use_pause_lenght_change.png")
    plt.close(fig)
    # with open('used_change_temp.pkl', 'wb') as f:
    #     pickle.dump(usedLst, f)


def main():
    make_plots(runs=5000)

    # usedLst = []
    # wind = Wind(-1)
    # # wind = Wind(-1)
    # # jet_stream = Jet_stream(0, JET_MINSPEED, JET_MAXSPEED)
    # for i in range(1,10):
    #     print(i)
    #     used = []
    #     for j in range(10):
    #         temperature = Temperature(i, 0, AVG_TEMPERATURE)
    #         jet_stream = Jet_stream(LATITUDE, MAX_HEIGHT)
    #         flight_sim = Flight(boeing, wind, jet_stream, temperature, DISTANCE, AIR_DENSITTY)
    #         flight_sim.run_sim(ASCEND_ANGLE, DESCEND_ANGLE)
    #         #plt.plot(flight_sim.timeLst, flight_sim.fuelLst, label=f"Windkracht: {i}")
    #         used.append(flight_sim.total_fuel_used)
    #     usedLst.append(used)

    # fig, axs = plt.subplots(2, figsize=(25,50))
    # bars = [f"Scale: {i}" for i in range(1,10)]
    # # print(usedLst)
    # vp_1 = axs[0].violinplot(usedLst, [i*2 for i in range(9)], widths=2, showmeans=True, showmedians=False, showextrema=False)
    # axs[0].set_xticks([i*2 for i in range(9)])
    # axs[0].set_xticklabels(bars)
    # axs[0].title.set_text("Effect of standard deviantion of temperature on fuel use")
    # # plt.violinplot([i for i in range(10)], usedLst)
    # # plt.xticks([i for i in range(10)], bars)

    # usedLst = []
    # for i in range(1,10):
    #     print(i)
    #     used = []
    #     for j in range(10):
    #         temperature = Temperature(5, i/100, AVG_TEMPERATURE)
    #         jet_stream = Jet_stream(LATITUDE, MAX_HEIGHT)
    #         flight_sim = Flight(boeing, wind, jet_stream, temperature, DISTANCE, AIR_DENSITTY)
    #         flight_sim.run_sim(ASCEND_ANGLE, DESCEND_ANGLE)
    #         used.append(flight_sim.total_fuel_used)
    #     usedLst.append(used)

    # bars = [f"Change: {i}" for i in range(1,10)]
    # vp_2 = axs[1].violinplot(usedLst, [i*2 for i in range(9)], widths=2, showmeans=True, showmedians=False, showextrema=False)
    # axs[1].set_xticks([i*2 for i in range(9)])
    # axs[1].set_xticklabels(bars)
    # axs[1].title.set_text("Effect of more random change of temperature on fuel use")
    # plt.show()

    # print(timeLst)
    # print("------------------------------------------")
    # print(height_list)
    # print("------------------------------------------")
    # print(fuelLst)
    # print("------------------------------------------")
    # print(positionLst)
    # # print("------------------------------------------")
    # wind = Wind(4)
    # flight_sim = Flight(boeing, wind, DISTANCE, AIR_DENSITTY)
    # flight_sim.run_sim(ASCEND_ANGLE, DESCEND_ANGLE)
    # plt.plot(flight_sim.timeLst, flight_sim.fuelLst)
    # plt.show()
    # plt.plot(timeLst[0:50],forward_velocityLst[:50])
    # plt.show()

    return True


if __name__ == "__main__":
    main()
