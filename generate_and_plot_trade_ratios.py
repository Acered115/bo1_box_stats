import numpy as np
import matplotlib.pyplot as plt
from time import time
from utils.utils import run_box_hits, default_gun_list


def create_plot(
    target_gun: str,
    num_box_hits: int,
    num_runs: int,
    gun_list: list[str] = default_gun_list,
    incr_box_hits: int = 0,
    marked_trade_ratio: float | None = None,
):
    if target_gun not in gun_list:
        raise ValueError(f"'{target_gun}' not found in the gun_list: {gun_list}")
    t1 = time()

    target_gun_array = []
    least_common_array = []
    most_common_array = []
    marked_trade_ratio_counter = 0

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
            marked_trade_ratio != None
            and num_box_hits / count_dict[target_gun] <= marked_trade_ratio
        ):
            marked_trade_ratio_counter += 1
            print(
                f"Game {step}, {target_gun} trade ratio <= {marked_trade_ratio}, {marked_trade_ratio_counter} times, trade avg of {round(num_box_hits/count_dict[target_gun],2)} out of {num_box_hits} box hits,\nCurrent ratio: 1 in {round(step/marked_trade_ratio_counter,2)}, ({marked_trade_ratio_counter}/{step})."
            )

        print(f"Current Game: {step}", "\r", end="")

    print(
        f"Script finished, the {target_gun} had a trade ratio <= {marked_trade_ratio} {marked_trade_ratio_counter} times,\nRatio: 1 in {round(step/marked_trade_ratio_counter,2)}, ({marked_trade_ratio_counter}/{num_runs})."
    )
    plt.axhline(
        y=marked_trade_ratio,
        color="black",
        linestyle="--",
        label=f"x = {marked_trade_ratio}",
    )

    x_values = range(0, len(target_gun_array))

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

    # Plot the new_array with each step
    plt.scatter(
        x_values, target_gun_array, color="red", label="Target Gun Trade Ratio", s=1
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
        label="Best fit of Lowest Trade Ratio",
    )

    # Plot the line of best fit for the max values
    plt.plot(
        x_values,
        p_least_comm(x_values),
        linestyle="--",
        color="purple",
        label="Best fit of Highest Trade Ratio",
    )
    # Plot the line of best fit for the min values

    plt.xlabel("Steps")
    plt.ylabel(f"Trade Ratios")
    plt.title(f"Trade Ratio of '{target_gun}' vs. Step")
    plt.grid(True)
    plt.ylim(top=45)
    plt.legend()
    print(time() - t1)
    plt.show()


if __name__ == "__main__":

    create_plot(
        target_gun="tgun",
        num_box_hits=600,
        num_runs=5000,
        incr_box_hits=0,
        marked_trade_ratio=15.26666667,
    )
