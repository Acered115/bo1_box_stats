import matplotlib.pyplot as plt
from scipy.stats import binom
import os


def plot_binomial_dist(
    trials: int,
    prob: int,
    marked_success: int = 0,
    gun_name: str = "Target Gun",
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

    # Plot a histogram of the PMF values
    plt.bar(range(trials + 1), pmf_values, align="center", alpha=0.7)

    # Create a straight line at the marked success bin
    plt.axvline(
        x=marked_success, color="red", linestyle="--", label=f"x = {marked_success}"
    )

    # Plt labelling stuff
    plt.xlabel(f"Number of Successes, (bin size = 1)")
    plt.ylabel(f"Probability P=x")
    plt.title(
        f"Probability Distribution of {trials} trials with {prob} chance of success "
    )
    plt.xticks(range(0, trials, 5))
    plt.xlim(xlow, xhigh)
    plt.grid(True)

    plt.legend()
    if save_fig:
        if not os.path.exists("plots"):
            os.mkdir("plots")
        plt.savefig(
            f"./plots/{gun_name}_{trials}_{prob}_{marked_success}_binomial_dist.png"
        )
    plt.show()


if __name__ == "__main__":

    plot_binomial_dist(
        gun_name="tgun",
        trials=2367,
        prob=0.05,
        marked_success=143,
        save_fig=False,
    )
