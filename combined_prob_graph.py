import matplotlib.pyplot as plt
import numpy as np
from box_calc_utils import run_box_hits
import time
from scipy.stats import binom
from pprint import pprint


def prob_this_or_better(value, trials, prob):

    return 1 - binom.cdf(value - 1, trials, prob)


num_runs = 15000
prob = 0.05

tgun_box_hits = 2367
gersch_box_hits = 687
dolls_box_hits = 1730


target_tgun_prob = 0.01308961635
target_gersch_prob = 0.04200551349
target_dolls_prob = 0.01216987807

prod_array = []
target_guns_array = []

counter = 0
i = 0
t0 = time.time()
while i < num_runs:
    tgun_count_dict = run_box_hits(num_box_hits=tgun_box_hits)
    gersch_count_dict = run_box_hits(num_box_hits=gersch_box_hits)
    dolls_count_dict = run_box_hits(num_box_hits=dolls_box_hits)

    curr_game = [
        prob_this_or_better(tgun_count_dict["tgun"], tgun_box_hits, prob),
        prob_this_or_better(gersch_count_dict["gersch"], gersch_box_hits, prob),
        prob_this_or_better(dolls_count_dict["dolls"], dolls_box_hits, prob),
    ]

    if (
        curr_game[0] <= target_tgun_prob
        and curr_game[1] <= target_gersch_prob
        and curr_game[2] <= target_dolls_prob
    ):
        counter += 1
        prod_array.append(curr_game)
        print(f"Appended 1, Counter currently at:{counter} which was {i} games in")
        print(
            f"The chance of all 3 {np.prod(curr_game)} or 1 in {1/np.prod(curr_game)}"
        )
        # print(prod_array)

    target_guns_array.append(curr_game)

    if i % 1000 == 0:
        t1 = time.time()
        # print(f"Currently at {i/num_runs}%")
        remaining = num_runs - i
        multiple = (remaining / 1000) * (t1 - t0)

        formatted_time = time.strftime(
            "%H:%M:%S", time.localtime(time.time() + multiple)
        )
        print(
            f"{i} Current {round(i/num_runs*100,1)}% completion The script will finish in {int(multiple)} seconds, or at approximately {formatted_time}",
            end="\r",
        )

        t0 = time.time()

    i += 1
    print(f"{i}", end="\r")


print(prod_array)
print(f"Counter:{counter}")

if counter > 0:
    print(f"This means a total chance of {counter/num_runs}")
else:
    print(f"I didnt calculate any games better than this")
