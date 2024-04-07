# bo1_box_stats
The Purpose of this repo is to simulate and statistically analyse the Mystery Box from Call of Duty Black Ops 1.

## Repo Contents
### 1. binomial_dist.py
This file produces a binomial distribution plot using the Probability Density Function (PDF) of each success value (0->trails) using the the inputs of trials and the chance of success. <br> 
Can take optinal arguments of "marked_success" which puts a dashed red line at the target success, "gun_name" which named the saved png accordingly and save_fig, which if set to True will create a plots folder in the directory that you run this named "plots" and saves the plot in there.
### 2. box_histogram.py
This file contains the code used to create a histogram plot given a num_box_hits of each simulation and num_runs of the simulation. Also accepting an optional argument of marked_success which will mark the bin you're targetting.<br>
 It also does take an optional argument of gun_list, for when you wanna try another set of guns for another map or something. 
### 3. animated_box_histogram.py
Does essentially the same as 2. box_histogram.py, but is instead animated so that you can see it fill up the bins as the number of sims increase. (NOTE this is much slower than running 2.0 for essentially the same result once finished).
### 4.box_luck_example.py
This file can have several purposes. One of these being to visualise the ranges occupied by the following 3 for a game: a random gun, least common gun and most common gun.<br>
One of the further uses is the incr_box_hits parameter, which if set to 0, it'll just plot the same number of box hits for the whole set of num_runs, but if you set the number to any positive integer, it'll increment the number of box hits by 1 (main purpose of this is to show how the distribution of the 3 values changes with increasing box hits).


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
pip install -r requirments.txt
```

If youre using something like Anaconda or Spyder then idk, figure it out yourself :D <br>
The only dependancies for this is numpy and matplotlib, so make sure you 
do both <br>(might look like more in the requirments.txt, but thats only because matplotlib):
```
pip install numpy
pip install matplotlib
```
## Further Reading on Binomial Distribution
