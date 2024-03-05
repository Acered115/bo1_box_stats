import numpy as np
import matplotlib.pyplot as plt
from time import time


gun_list = [
    "tgun",
    "gersch",
    "dolls",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
]


def run_box_hits(num_box_hits: int):
    current_hit = 0
    count_dict = {}
    for x in gun_list:
        count_dict[x] = 0

    while current_hit < num_box_hits:
        current_hit += 1
        randint = np.random.randint(0, len(gun_list))
        curr_gun = gun_list[randint]
        count_dict[curr_gun] += 1
    min_gun = min(count_dict, key=lambda k: count_dict[k])
    max_gun = max(count_dict, key=lambda k: count_dict[k])
    least_common = [min_gun, count_dict[min_gun]]
    most_common = [max_gun, count_dict[max_gun]]

    return least_common, most_common, count_dict


def create_list_from_dict(count_dict: dict, sort: bool = True) -> list[dict]:
    _list = []
    for gun_name in gun_list:
        _list.append([gun_name, count_dict[gun_name]])

    if sort == True:
        return sorted(_list, key=lambda x: x[1])
    else:
        return _list


def create_plot(
    target_gun: str,
    num_box_hits: int,
    num_runs: int,
    incr_box_hits=0,
    sort_list: bool = False,
):
    t1 = time()

    target_gun_array = []
    least_common_array = []
    most_common_array = []
    test = 0
    for step in np.arange(0, num_runs):
        num_box_hits += incr_box_hits
        least_common, most_common, count_dict = run_box_hits(num_box_hits)
        target_gun_array.append(num_box_hits / count_dict[target_gun])
        least_common_array.append(num_box_hits / least_common[1])
        most_common_array.append(num_box_hits / most_common[1])
        # counted_list = create_list_from_dict(count_dict)
        # print(counted_list)
        # for index, _ in enumerate(counted_list):
        #     if counted_list[index][0] == target_gun:
        #         avg_array.append(num_box_hits / counted_list[index][1])
        #         break
        # print(least_common)
        # print(type(count_dict[target_gun]))
        if (
            most_common[1] == count_dict[target_gun]
            and num_box_hits / count_dict[target_gun] < 16.5
        ):
            test += 1
            print(
                f"Game {step}, {target_gun} was most common,{test} times, with a trade avg of {num_box_hits/count_dict[target_gun]} out of {num_box_hits} box hits"
            )

        # if num_box_hits / sorted_list[-1][1] < 16:
        #     test += 1
        #     print(test)
        print(step, "\r", end="")

    x_values = range(0, len(target_gun_array))

    # Plot the new_array with each step
    plt.scatter(
        x_values, target_gun_array, color="red", label="Target Gun Trade Ratio", s=1
    )
    # Plot max values as red dots
    plt.scatter(
        x_values,
        most_common_array,
        color="mediumseagreen",
        label="Lowest Trade Ratio",
        s=1,
    )
    # Plot min values as blue dots
    plt.scatter(
        x_values, least_common_array, color="blue", label="Highest Trade Ratio", s=1
    )

    # Fit a line of best fit (polynomial of degree 4) to the "Trade Ratio" data
    z_target = np.polyfit(x_values, target_gun_array, 2)
    p_target = np.poly1d(z_target)
    z_most_comm = np.polyfit(x_values, most_common_array, 2)
    p_most_comm = np.poly1d(z_most_comm)
    z_least_comm = np.polyfit(x_values, least_common_array, 2)
    p_least_comm = np.poly1d(z_least_comm)
    plt.plot(
        x_values,
        p_target(x_values),
        linestyle="--",
        color="darkred",
        label="Best fit of Target Gun",
    )

    # Plot the line of best fit
    plt.plot(
        x_values,
        p_most_comm(x_values),
        linestyle="--",
        color="green",
        label="Best fit of Highest Trade Average",
    )

    # Plot the line of best fit for the max values
    plt.plot(
        x_values,
        p_least_comm(x_values),
        linestyle="--",
        color="purple",
        label="Best fit of Lowest trade Average",
    )
    # Plot the line of best fit for the min values

    plt.xlabel("Step")
    plt.ylabel(f"Frequency of selected gun")
    plt.title(f"Trade Ratio of '{target_gun}' vs. Step")
    plt.grid(True)
    plt.legend()
    print(time() - t1)
    plt.show()


if __name__ == "__main__":
    num_box_hits = 250
    number_of_games = 1000

    create_plot("tgun", num_box_hits, number_of_games, incr_box_hits=10, sort_list=True)
