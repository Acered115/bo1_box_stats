import matplotlib.pyplot as plt
from box_calc_utils import run_box_hits, default_gun_list
import time


def plot_box_histogram(
    num_box_hits: int,
    num_runs: int,
    marked_success: int = None,
    gun_list: list[str] = default_gun_list,
):
    bin_size = 1
    target_gun_array = []
    i = 0
    t0 = time.time()
    while i < num_runs:
        count_dict = run_box_hits(
            num_box_hits=num_box_hits,
            gun_list=gun_list,
        )
        target_gun_array.append(count_dict["tgun"])

        i += 1

        if i % 500 == 0:
            t1 = time.time()
            # print(f"Currently at {i/num_runs}%")
            remaining = num_runs - i
            multiple = (remaining / 500) * (t1 - t0)

            time.localtime(time.time() + multiple)
            formatted_time = time.strftime(
                "%H:%M:%S", time.localtime(time.time() + multiple)
            )
            print(
                f"Currently at {i/num_runs*100}% completion. The script will finish in {int(multiple)} seconds, or at approximately {formatted_time}",
                end="\r",
            )

            t0 = time.time()

    print()
    # Calculate the bin edges
    min_value = min(target_gun_array)
    max_value = max(target_gun_array)
    num_bins = int((max_value - min_value) / bin_size) + 1
    bin_edges = [min_value + i * bin_size for i in range(num_bins)]

    # Create histogram
    plt.hist(target_gun_array, bins=bin_edges, color="skyblue", edgecolor="black")
    if marked_success:

        plt.axvline(
            x=marked_success, color="red", linestyle="--", label=f"x = {marked_success}"
        )

    plt.grid(True)
    # Add labels and title
    plt.xlabel(f"Number of Successes, (bin size = 1)")
    plt.ylabel(f"Occurance")
    plt.title(
        f"Histogram plot of {num_runs} runs of {num_box_hits} box hits with {round(1/len(count_dict),2)} chance of success ",
        wrap=True,
    )

    # Show plot
    plt.show()


if __name__ == "__main__":
    plot_box_histogram(
        num_box_hits=2360,
        num_runs=10000,
        marked_success=143,
    )
