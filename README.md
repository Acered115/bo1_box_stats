# bo1_box_stats
The Purpose of this repo is to simulate and statistically analyse the Mystery Box from Call of Duty Black Ops 1.

## Installation Guide
To run this file you need to have python3 installed, I wrote this in python 3.10 but I think it works on older versions.


I suggest creating a venv **(Look up python venv for {your OS},
 plenty of tutorials online)** and running this through it
```
python3 -m venv .venv
```
If you're on windows run the script in \.venv\Scripts for your respective terminal<br>
If you're on BASH and Linux run this command to enter the .venv:
```
source .venv/bin/activate
```
Only the pip packages left: <br>
Install the pip requirments using 
```
pip install -r requirements.txt
```

If youre using something like Anaconda or Spyder then idk, figure it out yourself :D <br>

If you wanna manually install the dependencies, just go through them in the [requirements.txt](requirements.txt)<br>
Example:
```
pip install numpy
pip install matplotlib
pip install scipy
... and so on
```

## Repo Contents
### [1. single_gun_binomial_dist.py](single_gun_binomial_dist.py)
This file produces a binomial distribution plot using the Probability Density Function (PDF) of each success value (0->trails) using the the inputs of trials and the chance of success. <br> 
It also an argument of "marked_success" which puts a dashed red line at the target success, optional argument of  "gun_name" which named the saved png accordingly and save_fig, which if set to True will create a plots folder in the directory that you run this named "plots" and saves the plot in there.<br>

The produced bar graph is also coloured in colours which should help!
### 2. [Utils Folder](utils)
This folder contains a lot of the core functions, such as run_box_hits and run_box_hits_inv. As well as other various helper files used in the chi-squared calculation
### 3. [single_gun_box_histogram.py](single_gun_box_histogram.py)
This file creates a histogram from running the run_box_hits function for num_runs amount of times. <br>(NOTE: this is with each gun having the same sample sizes, including the tacticals)<br>

### 4. [single_gun_animated_box_histogram.py](single_gun_animated_box_histogram.py)
Does essentially the same as 2. box_histogram.py, but is instead animated so that you can see it fill up the bins as the number of sims increase. (NOTE this is much slower than running 2.0 for essentially the same result once finished).
### 5. [generate_and_plot_trade_ratios.py](generate_and_plot_trade_ratios.py)
This file can have several purposes. One of these being to visualise the ranges occupied by the following 3 for a game: a random gun, least common gun and most common gun.<br>
One of the further uses is the incr_box_hits parameter, which if set to 0, it'll just plot the same number of box hits for the whole set of num_runs, but if you set the number to any positive integer, it'll increment the number of box hits by that integer.
### 6. [generate_seperate_games.py](generate_seperate_games.py)
This script is an attempt to simulate the chance of all target guns occuring at the same time by using the run_box_hits function (independent one). <br> (NOTE: Does this by simulating different games, one for each gun and their sample sizes, meaning these distributions are independent and not interdependent as they are in the game.)
### 7. [generate_combined_games.py](generate_seperate_games.py)
This script is an attempt to simulate the chance of all target guns occuring at the same time by using the run_box_hits_inv function. It does this by generating a game and comparing its target guns to an inputted target luck, and if equal or better, it increments a counter.  <br> (NOTE: This is much more true to the game compared to the seperate games, but it takes much longer to run as there is no shortcuts it can take lol.) 
### 8. [find_average_game_for_targets.py](find_average_game_for_targets.py)
This script does essentially the same as [generate_combined_games.py](generate_seperate_games.py) but instead it does not have a target and just runs for the inputted amount, and then calculates the average "equal or better" luck for the number of games you generated.
### 8. [chi_squared_main.py](chi_squared_main.py)
This script calculates the chi-squared statistic for your inputted weapons, it also prints a lot of useful information, as well as creating a plot. It uses a lot of helper functions from [utils/chi_squared_utils.py](utils/chi_squared_utils.py) and [utils/utils.py](utils/utils.py).


## Further Reading 
My Videos:<br>
Video 1: https://www.youtube.com/watch?v=DO41-NiE9LE <br>
Video 2: [Placeholder]


My gathered findings and thoughts on these simulations: <br>
https://docs.google.com/document/d/13-u6NkEz4-t2wXBl9wIzZkgoLek8_5Zhhlwcz4tjIFU/edit#heading=h.ov9taae61k37

My Excel Calculator <br>
https://docs.google.com/spreadsheets/d/1uoSY4sGly_Sag6dwRtMx0XY-0Qj8NbAfkHFYHWBCOsE/edit?usp=sharing

My Excel Chi-Squared Calculator
https://docs.google.com/spreadsheets/d/1HJ23HNvsFCkMB2NS5k3ooQ8LneaAt8bLrOjzCyWpxA8/edit?usp=sharing

