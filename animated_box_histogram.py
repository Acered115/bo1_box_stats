import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from box_calc_utils import run_box_hits, default_gun_list
from matplotlib.ticker import MaxNLocator


def update(
    frame,
    num_box_hits: int,
    num_runs: int,
    default_gun_list: list[str],
    target_gun_array: list[int],
    ax,
):

    bin_size = 1
    count_dict = run_box_hits(num_box_hits=num_box_hits, gun_list=default_gun_list)
    target_gun_array.append(count_dict["tgun"])

    # Calculate the bin edges
    min_value = min(target_gun_array)
    max_value = max(target_gun_array)
    num_bins = int((max_value - min_value) / bin_size) + 1
    bin_edges = [min_value + i * bin_size for i in range(num_bins)]

    # Update histogram
    ax.clear()
    ax.hist(target_gun_array, bins=bin_edges, color="skyblue", edgecolor="black")

    # Add labels and title
    plt.xlabel(f"Number of Successes, (bin size = 1)")
    plt.ylabel(f"Occurance")
    ax.set_ylim(0, num_runs * 0.15)
    ax.legend([f"{frame} Simulations"], loc="upper right")

    ax.set_title("Live Histogram plot")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))


def animated_plot_box_histogram(
    num_box_hits: int,
    num_runs: int,
    gun_list: list[str] = default_gun_list,
):

    fig, ax = plt.subplots()
    target_gun_array = []

    # Set up animation
    ani = FuncAnimation(
        fig,
        update,
        frames=range(num_runs),
        fargs=(num_box_hits, num_runs, default_gun_list, target_gun_array, ax),
        interval=0.001,
        repeat=False,
    )
    plt.show()


if __name__ == "__main__":

    animated_plot_box_histogram(num_box_hits=250, num_runs=1000)
