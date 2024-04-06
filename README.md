# bo1_box_stats


## Repo Contents
### 1. binomial_dist.py<br>
This file produces a binomial distribution plot using the Probability Density Function (PDF) of each success value (0->trails) using the the inputs of trials and the chance of success. <br> 
Can take optinal arguments of "marked_success" which puts a dashed red line at the target success, "gun_name" which named the saved png accordingly and save_fig, which if set to True will create a plots folder in the directory that you run this named "plots" and saves the plot in there.


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
