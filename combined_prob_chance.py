import matplotlib.pyplot as plt
import numpy as np
from box_calc_utils import run_box_hits
import time
from scipy.stats import binom
from pprint import pprint


def prob_this_or_better(value, trials, prob):

    return 1 - binom.cdf(value - 1, trials, prob)


num_runs = 150000
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


def run_box_hits_for_guns(guns_info: list[dict[str:int]]) -> list[float]:
    curr_combo = []

    for gun in guns_info:
        gun_name = gun["gun_name"]
        box_hits = gun["num_hits"]
        chance_succ = gun["chance_succ"]
        curr_game_dict = run_box_hits(num_box_hits=box_hits)

        curr_combo.append(
            prob_this_or_better(curr_game_dict[gun_name], box_hits, chance_succ)
        )

    return curr_combo


guns_info = [
    {
        "gun_name": "tgun",
        "num_hits": tgun_box_hits,
        "chance_succ": prob,
    },
    {
        "gun_name": "gersch",
        "num_hits": gersch_box_hits,
        "chance_succ": prob,
    },
    {
        "gun_name": "dolls",
        "num_hits": dolls_box_hits,
        "chance_succ": prob,
    },
]
try:
    while i < num_runs:
        curr_combo = run_box_hits_for_guns(guns_info)
        target_guns_array.append(curr_combo)

        if (
            curr_combo[0] <= target_tgun_prob
            and curr_combo[1] <= target_gersch_prob
            and curr_combo[2] <= target_dolls_prob
        ):
            counter += 1
            prod_array.append(curr_combo)
            print(
                f"\nAppended 1, So far found: {counter} game(s) luckier, which was {i+1} games in\n"
            )
            print(
                f"The chance of all 3 {np.prod(curr_combo)} or 1 in {1/np.prod(curr_combo)} (This one is their probabilities multiplied together)"
            )
            # print(prod_array)

        if i % 1000 == 0:
            t1 = time.time()
            # print(f"Currently at {i/num_runs}%")
            remaining = num_runs - i
            multiple = (remaining / 1000) * (t1 - t0)

            formatted_time = time.strftime(
                "%H:%M:%S", time.localtime(time.time() + multiple)
            )
            if i < 1000:
                print(f"Estimating duration...")
            else:
                print(
                    f"Current Game:{i},  Currently at {round(i/num_runs*100,1)}% completion, The script will finish in {int(multiple)} seconds, or at approximately {formatted_time}",
                    end="\r",
                )

            t0 = time.time()

        i += 1
        print(f"Current Game:{i}", end="\r")

    # print(target_guns_array)
    # print(prod_array)
    print(f"Counter:{counter}")
    print("__________________\n")

    if counter > 0:
        print(
            f"This means a total chance of {counter/i} ({counter}/{i})\nAbout 1 in {round(1/(counter/i),3)} trios of runs had a better luck than:\ntgun: {target_tgun_prob},\ngesrch: {target_gersch_prob}\ndolls: {target_dolls_prob} "
        )
    else:
        print(
            f"I didnt calculate any games better than this \ntgun: {target_tgun_prob},\ngesrch: {target_gersch_prob}\ndolls: {target_dolls_prob} "
        )
except KeyboardInterrupt:
    print("Script ended early because of Keyboard Intterupt")
    if counter > 0:
        print("__________________\n")
        print(
            f"This means a total chance of {counter/i} ({counter}/{i})\nAbout 1 in {round(1/(counter/i),3)} trios of runs had a better luck than:\ntgun: {target_tgun_prob},\ngesrch: {target_gersch_prob}\ndolls: {target_dolls_prob} "
        )
    else:
        print()
        print(
            f"I didnt calculate any games better than this \ntgun: {target_tgun_prob},\ngesrch: {target_gersch_prob}\ndolls: {target_dolls_prob} "
        )
