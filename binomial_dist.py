import matplotlib.pyplot as plt
from scipy.stats import binom
import os


def plot_binomial_dist(
    trials: int,
    prob: int,
    marked_success: int,
    gun_name: str | None = None,
    save_fig: bool = False,
):
    # Creating a binomial pmf calculation for every possible success between 0 and trials and storing it into a list
    pmf_values = [binom.pmf(i, trials, prob) for i in range(trials + 1)]

    ############################################################################################
    # All below is all for displaying the graph, the math is done above ^

    xlow = 0
    xhigh = 0
    # Find an appropriate lower and upper cutoff for the graph
    xlow = next(i for i, value in enumerate(pmf_values) if value > 10e-05) - 10
    xhigh = (
        len(pmf_values)
        - next(i for i, value in enumerate(pmf_values[::-1]) if value > 10e-05)
        + 10
    )

    # Plot a bar graph of the PMF values
    bars = plt.bar(
        range(trials + 1), pmf_values, align="center", alpha=0.7, color="grey"
    )

    # Create a straight line at the marked success bin
    plt.axvline(
        x=marked_success, color="red", linestyle="--", label=f"x = {marked_success}"
    )

    # Color bars above marked success differently
    for i, bar in enumerate(bars):
        if i > marked_success:
            bar.set_color("purple")  # Set color to green for bars above marked success
        if i == marked_success:
            bar.set_color("blue")

    # Calculate the CDF
    cdf = sum(pmf_values[: marked_success + 1])
    # Calculate total area of the marked region
    complement_of_cdf = sum(pmf_values[marked_success:])

    # Plt labelling stuff
    plt.xlabel(f"Number of Successes, (bin size = 1)")
    plt.ylabel(f"Probability Mass Function (PMF)")
    plt.title(
        f"PMF Distribution of {trials} trials with {prob} chance of success,\nTag: {gun_name} "
    )

    plt.xticks(range(0, trials, 5))
    plt.xlim(xlow, xhigh)
    plt.grid(True)

    # Create legend for the dashed line and coloured bars
    legend_entries = [
        f"x = {marked_success}",
        f"Compli area (purple):\n {complement_of_cdf:.4f}",
        f"CDF area (grey):\n{cdf:.4f}",
    ]
    plt.legend(
        handles=[
            plt.axvline(x=0, color="red", linestyle="--"),
            bars[marked_success + 1],
            bars,
        ],
        labels=legend_entries,
        loc="upper left",
    )

    if save_fig:
        if not os.path.exists("plots"):
            os.mkdir("plots")
        plt.savefig(
            f"./plots/{gun_name}_{trials}_{prob}_{marked_success}_binomial_dist.png"
        )

    plt.show()


if __name__ == "__main__":

    plot_binomial_dist(
        gun_name="Dolls",
        trials=1730,
        prob=0.05,
        marked_success=108,
        save_fig=True,
    )
