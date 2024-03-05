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
    target_gun: str, num_box_hits: int, num_runs: int, sort_list: bool = False
):
    t1 = time()

    avg_array = []
    min_array = []
    max_array = []
    test = 0
    for step in np.arange(0, num_runs):
        num_box_hits += 5
        least_common, most_common, count_dict = run_box_hits(num_box_hits)
        # new_array.append(num_box_hits / count_dict["tgun"])
        min_array.append(num_box_hits / least_common[1])
        max_array.append(num_box_hits / most_common[1])
        counted_list = create_list_from_dict(count_dict)
        # print(counted_list)
        for index, _ in enumerate(counted_list):
            if counted_list[index][0] == target_gun:
                avg_array.append(num_box_hits / counted_list[index][1])
                break

        # if num_box_hits / sorted_list[-1][1] < 16:
        #     test += 1
        #     print(test)
        print(step, "\r", end="")
    x_values = range(0, len(avg_array))

    # Plot the new_array with each step
    plt.plot(
        x_values, avg_array, marker="o", linestyle="-", linewidth=0.5, markersize=0.3
    )
    # Plot max values as red dots
    plt.plot(
        x_values,
        max_array,
        color="red",
        label="Max Values",
        marker="o",
        markersize=0.3,
        linewidth=0.5,
    )

    # Plot min values as blue dots
    plt.plot(
        x_values,
        min_array,
        color="blue",
        label="Min Values",
        marker="o",
        markersize=0.3,
        linewidth=0.5,
    )
    # Fit a line of best fit (polynomial of degree 1) to the "Trade Ratio" data
    z_max = np.polyfit(x_values, max_array, 5)
    p_max = np.poly1d(z_max)

    # Plot the line of best fit
    plt.plot(
        x_values,
        p_max(x_values),
        linestyle="--",
        color="green",
        label="Line of Best Fit",
    )
    z_min = np.polyfit(x_values, min_array, 5)
    p_min = np.poly1d(z_min)

    # Plot the line of best fit
    plt.plot(
        x_values,
        p_max(x_values),
        linestyle="--",
        color="green",
        label="Line of Best Fit",
    )
    # Plot the line of best fit
    plt.plot(
        x_values,
        p_min(x_values),
        linestyle="--",
        color="pink",
        label="Line of Best Fit",
    )
    plt.xlabel("Step")
    plt.ylabel(f"Frequency of selected gun")
    plt.title(f"Trade Ratio of '{target_gun}' vs. Step")
    plt.grid(True)
    print(time() - t1)
    plt.show()


if __name__ == "__main__":
    num_box_hits = 1000
    number_of_games = 1000

    create_plot("tgun", num_box_hits, number_of_games, sort_list=True)
