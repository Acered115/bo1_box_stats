import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.stats import binom

# Define the parameters of the binomial distribution
trials = 2367  # Number of trials
gun_name="tgun"

prob = 0.05  # Probability of success

marked_success=143

# Creating a binomial pmf calculation for every possible success between 0 and trials and storing it into a list
pmf_values = [binom.pmf(i,trials, prob) for i in range(trials + 1)]


############################################################################################
# This is all for displaying the graph, the math is done above ^

# Find an appropriate lower and upper cuttof for the graph
xlow=0
xhigh=0
# Find an appropriate lower and upper cutoff for the graph
xlow = next(i for i, value in enumerate(pmf_values) if value > 10e-05) - 10
xhigh = len(pmf_values) - next(i for i, value in enumerate(pmf_values[::-1]) if value > 10e-05) + 10

            

# Plot a histogram of the PMF values
plt.bar(range(trials + 1), pmf_values, align='center', alpha=0.7)

# Create a straight line at the marked success bin
plt.axvline(x=marked_success, color='red', linestyle='--', label=f'x = {marked_success}')

#Plt labelling stuff
plt.xlabel(f'Number of Successes, (bin size = 1)')
plt.ylabel(f'Probability P=x')
plt.title(f'Probability Distribution of {trials} trials with chance of {prob}')
plt.xticks(range(0,trials,5))
plt.xlim(xlow,xhigh)
plt.grid(True)

plt.legend()
plt.savefig(f"./plots/{gun_name}.png")
plt.show()