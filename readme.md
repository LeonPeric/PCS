# Project computional science
Planes use a lot of fuel during a flight, so airline companies are constantly trying to minimize fuel usage on their planes, because this saves them money. This project tried to simulate fuel usage of the airplane Boeing 787-9. For this we focused on two variables: wind force and jetstream influences. 

# Dependencies
We make use of the following non standard included libraries. 
- Numpy
- pickle
- matplotlib
These can be installed by making use of:

`pip install numpy`

`pip install pickle`

`pip install matplotlib`

# Getting started
- Download or clone the repository
- Type in your terminal:

`python simulation.py` 

It will then prompt you for the amount of simulations you want to run, the higher this number the longer the simulation takes. Our simulation was based on 5000 runs, this takes around 3.5 hours to run. 

This project can work both on Windows and Linux computers.
# Running experiments 
Other than amount of simulations there are no other parameters to change, the simulation it self takes care of this all. To recreate our figures you will need to run 5000 simulations.

# Figures
Our figures are as following:
![Wind simulation](simulations\wind\wind_plot_fitted_line.png)
![Jet stream thickness simulation](simulations\jetstream\jet_stream_thickness_fitted_line.png)
![Jet stream time difference simulation](simulations\jetstream\jet_stream_time_diff_plot_fitted_line.png)


After running the simulation it is possible to compare them by looking into the folder `simulations\jetstream` or `simulations\wind`. These figures will be made after the simulation is done running, see chapter "Running experiments"

# Folders and files
There are several folders and files in this project. 
- `Objects` is the folder which contanis all the files for creating the airplane, the wind and jetstream random variables and the making of the flight itself. It also contains the file for fitting lines based on our results.
- `simulations` will contain the figures after the simulation has run.
- `Constants` is a file which contains the specifications of the airplane.
- `simulation.py` is the python file which runs all the experiments by varying the wind speed and jetstream parameters. It will then also create the figures and the pickle files.
- `stats.py` creates the statistics used for the report and poster presentation.

# Authors
- Leon Peric
- Shankar Rai
- Karsten Langerak

# Support
Any questions? Email: leon.peric.lp@gmail.com

# References
1. Boeing 787 Dreamliner : Analysis. (z.d.). lissys. Geraadpleegd op 1 februari 2022, van https://www.lissys.uk/samp1/index.html
2. Britannica, T. Editors of Encyclopaedia (Invalid Date). Beaufort scale. Encyclopedia Britannica. https://www.britannica.com/science/Beaufort-scale
3. EASA. (2019, april). Type-Certificate Data Sheet for Trent 1000 series engines (EASA.E.036).
4. EASA. (2021, maart). Type-Certificate Data Sheet for BOEING 787 (EASA.IM.A.115).
5. Jet Streams. (2020, 11 april). GeoSciences. Geraadpleegd op 1 februari 2022, van https://geo.libretexts.org/Bookshelves/Meteorology_and_Climate_Science/Book%3A_Practical_Meteorology_(Stull)/11%3A_General_Circulation/11.8%3A_Jet_Streams
6. NASA. (z.d.). Re-Living The Wright Way. Geraadpleegd op 1 februari 2022, van https://wright.nasa.gov/airplane/shortw.html
7. Noordhoff Uitgevers. (z.d.). Binas (Zesde ed.). Noordhoff Uitgevers.
8. Poole, D. (2014). Linear Algebra A modern introduction (Fourth edition). Cengage Learning.