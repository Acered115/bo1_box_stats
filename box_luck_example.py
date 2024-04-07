import numpy as np
import matplotlib.pyplot as plt
from time import time
from box_calc_utils import run_box_hits, create_list_from_dict, default_gun_list


def create_plot(
    target_gun: str,
    num_box_hits: int,
    num_runs: int,
    gun_list: list[str] = default_gun_list,
    incr_box_hits: int = 0,
):
    if target_gun not in gun_list:
        raise ValueError(f"'{target_gun}' not found in the gun_list: {gun_list}")
    t1 = time()

    target_gun_array = []
    least_common_array = []
    most_common_array = []
    special_gun_counter = 0

    for step in np.arange(0, num_runs):
        num_box_hits += incr_box_hits
        count_dict = run_box_hits(num_box_hits=num_box_hits, gun_list=gun_list)

        min_gun = min(count_dict, key=lambda k: count_dict[k])
        max_gun = max(count_dict, key=lambda k: count_dict[k])
        least_common = [min_gun, count_dict[min_gun]]
        most_common = [max_gun, count_dict[max_gun]]

        try:
            target_gun_array.append(num_box_hits / count_dict[target_gun])
        except ZeroDivisionError:
            target_gun_array.append(0)
        try:
            least_common_array.append(num_box_hits / least_common[1])
        except ZeroDivisionError:
            least_common_array.append(0)

        try:
            most_common_array.append(num_box_hits / most_common[1])
        except ZeroDivisionError:
            most_common_array.append(0)

        if (
            most_common[1] == count_dict[target_gun]
            and num_box_hits / count_dict[target_gun] < 16.5524475
        ):
            special_gun_counter += 1
            print(
                f"Game {step}, {target_gun} was most common, {special_gun_counter} times, with a trade avg of {round(num_box_hits/count_dict[target_gun],2)} out of {num_box_hits} box hits,\nCurrent ratio: 1 in {round(step/special_gun_counter,2)}."
            )

        print(f"Current Game: {step}", "\r", end="")

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

    if num_runs < 1000:
        poly_degree = 2
    else:
        poly_degree = 3

    # Fit a line of best fit (polynomial of degree 4) to the "Trade Ratio" data
    z_target = np.polyfit(x_values, target_gun_array, poly_degree)
    p_target = np.poly1d(z_target)
    z_most_comm = np.polyfit(x_values, most_common_array, poly_degree)
    p_most_comm = np.poly1d(z_most_comm)
    z_least_comm = np.polyfit(x_values, least_common_array, poly_degree)
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

    plt.xlabel("Steps")
    plt.ylabel(f"Frequency of selected gun")
    plt.title(f"Trade Ratio of '{target_gun}' vs. Step")
    plt.grid(True)
    plt.legend()
    print(time() - t1)
    plt.show()


if __name__ == "__main__":

    create_plot(
        target_gun="tgun",
        num_box_hits=236,
        num_runs=7000,
        incr_box_hits=1,
    )
