from utils.utils import run_box_hits, prob_this_or_better
import time


def run_box_for_each_gun(guns_info: list[dict[str:int]]) -> list[bool]:

    curr_combo = []

    for gun in guns_info:
        gun_name = gun["name"]
        box_hits = gun["trials"]
        chance_succ = gun["chance_succ"]
        target_prob_for_gun = gun["target_prob"]

        curr_game_dict = run_box_hits(num_box_hits=box_hits)
        luck = prob_this_or_better(curr_game_dict[gun_name], box_hits, chance_succ)
        # curr_combo[gun_name] = prob_this_or_better(
        #     curr_game_dict[gun_name], box_hits, chance_succ
        # )
        # The following if statement optimises the generation game, as it skips generating the games for the following guns if the first game
        # Does not fit the luck quota for it's target
        if luck <= target_prob_for_gun:
            curr_combo.append(True)
        else:
            curr_combo.append(False)
            break

        # curr_combo.append(
        #     prob_this_or_better(curr_game_dict[gun_name], box_hits, chance_succ)
        # )

    return curr_combo


def generate_seperate_games(num_runs: int, guns_info: list[dict]):
    inc = 0
    success_counter = 0
    t0 = time.time()
    luckier_list = []

    try:
        while inc < num_runs:
            curr_combo = run_box_for_each_gun(guns_info)
            # target_guns_array.append(curr_combo)
            # print("asd")
            # comparison_array = []
            # for item in guns_info:
            #     print(curr_combo[item["name"]] <= item["target_prob"])
            #     comparison_array.append(curr_combo[item["name"]] <= item["target_prob"])
            # print(comparison_array)
            if False not in curr_combo and len(curr_combo) == len(guns_info):

                success_counter += 1
                luckier_list.append(curr_combo)
                print(
                    f"\nAppended 1, So far found: {success_counter} game(s) luckier, which was {inc+1} games in\n"
                )

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
                        f"Current Game:{inc},  Currently at {round(inc/num_runs*100,1)}% completion, The script will finish in {int(multiple)} seconds, or at approximately {formatted_time}",
                        end="\r",
                    )

                t0 = time.time()

            inc += 1
            print(f"Current Game:{inc}", end="\r")

        print(f"Counter:{success_counter}")

    except KeyboardInterrupt:
        print("\nScript ended early because of Keyboard Intterupt")
    if success_counter > 0:
        print("_________Seperate Games__________\n")
        print(
            f"This means a total chance of {success_counter/inc} ({success_counter}/{inc})\nAbout 1 in {round(1/(success_counter/inc),3)} trios of runs had a better luck than all these guns:"
        )
        for item in guns_info:
            print(f"{item['name']}: {item['target_prob']}")
    else:

        print(f"\nI didnt calculate any games better than this ")
        for item in guns_info:
            print(f"{item['name']}: {item['target_prob']}")


if __name__ == "__main__":

    box_prob = 0.05

    tgun_box_hits = 2367
    gersch_box_hits = 687
    dolls_box_hits = 1730

    target_tgun_prob = 0.01308961635
    target_gersch_prob = 0.04200551349
    target_dolls_prob = 0.01216987807

    guns_info = [
        {
            "name": "gersch",
            "trials": gersch_box_hits,
            "chance_succ": box_prob,
            "target_prob": target_gersch_prob,
        },
        {
            "name": "dolls",
            "trials": dolls_box_hits,
            "chance_succ": box_prob,
            "target_prob": target_dolls_prob,
        },
        {
            "name": "tgun",
            "trials": tgun_box_hits,
            "chance_succ": box_prob,
            "target_prob": target_tgun_prob,
        },
    ]

    generate_seperate_games(num_runs=150000 * 100, guns_info=guns_info)
