import numpy as np
from utils.utils import run_box_hits_with_inv, prob_this_or_better
import time


box_prob = 0.05

tgun_box_hits = 2367
gersch_box_hits = 687
dolls_box_hits = 1730


guns_info = [
    {
        "name": "gersch",
    },
    {
        "name": "dolls",
    },
    {
        "name": "tgun",
    },
]


def run_box_for_each_gun(
    box_hits: int, chance_succ: float, guns_info: list[dict[str:int]]
) -> list[float]:

    curr_combo = {}

    curr_game_dict = run_box_hits_with_inv(num_box_hits=box_hits)
    for gun in guns_info:
        gun_name = gun["name"]

        luck = prob_this_or_better(
            curr_game_dict[gun_name].observed,
            curr_game_dict[gun_name].trials,
            chance_succ,
        )
        curr_combo[gun_name] = luck

    return curr_combo


def generate_combined_games(
    box_hits: int,
    num_runs: int,
    chance_succ: float,
    guns_info: list[dict],
):
    inc = 0
    success_counter = 0
    t0 = time.time()
    total_guns_dict = {"tgun": [], "gersch": [], "dolls": []}

    try:
        while inc < num_runs:
            curr_combo = run_box_for_each_gun(
                box_hits=box_hits, chance_succ=chance_succ, guns_info=guns_info
            )
            for gun in curr_combo.keys():
                total_guns_dict[gun].append(curr_combo[gun])

            if inc % 1000 == 0:
                t1 = time.time()
                # print(f"Currently at {i/num_runs}%")
                remaining = num_runs - inc
                multiple = (remaining / 1000) * (t1 - t0)

                formatted_time = time.strftime(
                    "%H:%M:%S", time.localtime(time.time() + multiple)
                )
                if inc < 1000:
                    print(f"Estimating duration...")
                else:
                    print(
                        f"Current Game:{inc},  Currently at {round(inc/num_runs*100,1)}% completion,",
                        f" The script will finish in {int(multiple)} seconds, or at approximately {formatted_time}",
                        end="\r",
                    )

                t0 = time.time()

            inc += 1
            print(f"Current Game:{inc}", end="\r")

        print(f"Counter:{success_counter}")

    except KeyboardInterrupt:
        print("\nScript ended early because of Keyboard Intterupt")

    print(
        f"These values are the average probabilities of 'equal to or better' for all games generated out of {inc} games"
    )
    for gun in total_guns_dict.keys():
        current_list = total_guns_dict[gun]
        avg = sum(current_list) / len(current_list)
        print(gun, avg)


if __name__ == "__main__":

    generate_combined_games(
        box_hits=2417, num_runs=150000 * 10, chance_succ=0.05, guns_info=guns_info
    )
