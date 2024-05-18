from scipy.stats import chi2
from utils.utils import (
    WeaponStat,
    text_colors,
)
import numpy as np
import matplotlib.pyplot as plt


def extract_target_guns(
    count_dict: dict[str:int], target_guns: str
) -> list[dict[str:int]]:

    temp_dict = {}
    for gun in target_guns:
        temp_dict[gun] = count_dict[gun]

    return temp_dict


def plot_chi_squared_curve(
    title: str, chi_val: float, deg_freedom: int, null_pval: float
):
    """Does what it says on the tin

    :param title: The title of the plot
    :type title: str
    :param chi_val: The target chi_value you wanna plot for
    :type chi_val: float
    :param deg_freedom: Degrees of freedom (usually num_categories -1)
    :type deg_freedom: int
    :param null_pval: The Null Hypothesis p_value, the critical chi-squared val is calculated from this
    :type null_pval: float
    """
    p_value = 1 - chi2.cdf(chi_val, deg_freedom)
    # x range

    x = np.linspace(0, 100, 10000)

    null_hyp = chi2.ppf(1 - null_pval, deg_freedom)

    # Get chi-squared probability density function for the specified degrees of freedom
    y = chi2.pdf(x, deg_freedom)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(
        x,
        y,
        label=f"χ2 Dist ({deg_freedom} DOF)",
        color="b",
    )
    plt.title(title)
    plt.xlabel("χ2 Value")
    plt.ylabel("Probability Density")

    colour = "green"
    plt.fill_between(
        x,
        y,
        where=(x >= chi_val) & (x <= null_hyp),
        color=colour,
        alpha=0.5,
        label=f"P-Value ({p_value:.5f})",
    )
    plt.fill_between(
        x,
        y,
        where=(x >= null_hyp),
        color="red",
        alpha=0.5,
        label=f"rejection region x <= ({null_pval:.5f})",
    )

    plt.axvline(x=chi_val, color="green", linestyle="--", label="χ2 GOF Val")
    plt.axvline(x=null_hyp, color="red", linestyle="--", label="Null Hyp p-value")

    # Set y-axis to start at zero
    plt.ylim(bottom=0)

    # Set x-axis to start at zero
    plt.xlim(left=0, right=null_hyp * 3)
    plt.legend()
    plt.show()  # Display the plot


def convert_game_to_chi_obs_list(
    count_dict: dict[str:WeaponStat] | dict[str:int],
) -> list[dict[str:int]]:
    """Used to convert a generated game of either both types time chi-squared calculation.

    :return: Returns the "obs_list" type needed for the chi-squared function
    :rtype: list[dict[str:int]]
    """
    obs_list = []
    tgun = count_dict["tgun"]
    if isinstance(tgun, WeaponStat):
        for key in count_dict.keys():
            obs_list.append(
                {
                    "name": key,
                    "trials": count_dict[key].trials,
                    "succs": count_dict[key].observed,
                }
            )
    else:
        for key in count_dict.keys():
            obs_list.append(
                {
                    "name": key,
                    "trials": sum(count_dict.values()),
                    "succs": count_dict[key],
                }
            )

    return obs_list


def remove_unlucky(
    observed_guns: list[dict[str, str | int]], chance_succ: float
) -> list[dict[str, str | int]]:
    """Removes the unlucky games from an obs_list

    :param observed_guns: obs_list you wanna pass in
    :type observed_guns: list[dict[str, str  |  int]]
    :param chance_succ: The chance of success
    :type chance_succ: float
    :return: The new obs_list without the unlucky guns
    :rtype: list[dict[str, str  |  int]]
    """
    # Make a copy to iterate over
    observed_guns_copy = observed_guns[:]

    # Iterate over the copy and remove elements from the original
    for obs in observed_guns_copy:
        obs_trials = obs["trials"]
        exp_val = obs_trials * chance_succ
        obs_succs = obs["succs"]

        # Remove from the original list if expected value is greater than observed successes
        if exp_val > obs_succs:
            observed_guns.remove(obs)  # Modify the original list
    return observed_guns


def chi_squared(
    observed_guns: list[dict[str, str | int]],
    chance_succ: float = 0.05,
    null_hyp_pval: float = 0.025,
) -> float:
    """Iterates through the obs_list object and calculates the
    Chi-squared total for the number of categories.

    :param observed_guns: The obs_list you wanna pass in
    :type observed_guns: list[dict[str, str  |  int]]
    :param chance_succ: The chance of success, defaults to 0.05
    :type chance_succ: float, optional
    :param null_hyp_pval: The critical null hypothesis value, defaults to 0.025
    :type null_hyp_pval: float, optional
    :return: Returns the chi-squared total
    :rtype: float
    """
    chi_squared_dict: dict[str:int] = {}

    for obs in observed_guns:

        obs_trials = obs["trials"]
        obs_succs = obs["succs"]
        obs_name = obs["name"]
        exp_val = obs_trials * chance_succ

        chi_squared_i = ((obs_succs - exp_val) ** 2) / exp_val
        chi_squared_dict[obs_name] = chi_squared_i
        chi_squared_total = sum(chi_squared_dict.values())
        print(
            f"exp:{round(exp_val,2)}, {text_colors['green']}obs:{obs}{text_colors['reset']},",
            f"chi_squared: {text_colors['blue']}{round(chi_squared_i,2) } ({text_colors['yellow']}{round(chi_squared_total,2)}",
            f"cumulative{text_colors['reset']})",
        )
    deg_freedom = len(observed_guns) - 1
    print(
        f"Finding Chi squared (weighted) for {len(observed_guns)} guns, DOF = {deg_freedom}"
    )

    critical_val = chi2.ppf(1 - null_hyp_pval, deg_freedom)
    if chi_squared_total > critical_val:
        print(
            f"{round(chi_squared_total,2)} > {round(critical_val,2)}chi_squared is greater than the critical value ({round(critical_val,2)}  for null_hyp_pval of {null_hyp_pval})"
        )

    else:
        print(f"{chi_squared_total} < {critical_val} Seems plausible ngl")

    for gun in chi_squared_dict.keys():
        if chi_squared_dict[gun] > 3:
            print(
                f"{text_colors['red']} The {gun} has quite a significant chi-val: {round(chi_squared_dict[gun],2)}{text_colors['reset']}"
            )
    return chi_squared_total


def chi_squared_weighted(
    observed_guns: list[dict[str, str | int]],
    chance_succ: float = 0.05,
    null_hyp_pval: float = 0,
) -> float:
    """Iterates through the obs_list object and calculates the
    Weighted Chi-squared total for the number of categories.

    :param observed_guns: The obs_list you wanna pass in
    :type observed_guns: list[dict[str, str  |  int]]
    :param chance_succ: The chance of success, defaults to 0.05
    :type chance_succ: float, optional
    :param null_hyp_pval: The critical null hypothesis value, defaults to 0.025
    :type null_hyp_pval: float, optional
    :return: Returns the chi-squared total
    :rtype: float
    """
    weighted_chi_stat_dict: dict[str:int] = {}
    highest_trials = max(observed_guns, key=lambda x: x["trials"])["trials"]

    for obs in observed_guns:
        obs_trials = obs["trials"]
        obs_succs = obs["succs"]
        obs_name = obs["name"]
        exp_val = obs_trials * chance_succ
        weight = obs_trials / highest_trials
        chi_squared_i = ((obs_succs - exp_val) ** 2) / exp_val
        weighted_chi_squared_i = chi_squared_i * weight
        weighted_chi_stat_dict[obs_name] = weighted_chi_squared_i
        weighted_chi_squared_total = sum(weighted_chi_stat_dict.values())
        print(
            f"exp:{round(exp_val,2)}, {text_colors['green']}obs:{obs}{text_colors['reset']},",
            f"{text_colors['cyan']}weight: {obs_trials}/{highest_trials} or {round(weight,2)}{text_colors['reset']},",
            f"weighted chi_squared: {text_colors['blue']}{round(weighted_chi_squared_i,2) } ({text_colors['yellow']}{round(weighted_chi_squared_total,2)}",
            f"cumulative{text_colors['reset']})",
        )

    deg_freedom = len(observed_guns) - 1
    print(
        f"Finding Chi squared (weighted) for {len(observed_guns)} guns, DOF = {deg_freedom}"
    )
    critical_val = chi2.ppf(1 - null_hyp_pval, deg_freedom)
    if weighted_chi_squared_total > critical_val:
        print(
            f"{round(weighted_chi_squared_total,2)} > {round(critical_val,2)} chi_squared is greater than the critical value ({round(critical_val,2)}  for null_hyp_pval of {null_hyp_pval})"
        )

    else:
        print(f"{weighted_chi_squared_total} < {critical_val} Seems plausible ngl")

    for gun in weighted_chi_stat_dict.keys():
        if weighted_chi_stat_dict[gun] > 3:
            print(
                f"{text_colors['red']} The {gun} has quite a significant weighted chi-stat: {round(weighted_chi_stat_dict[gun],2)}{text_colors['reset']}"
            )
    return weighted_chi_squared_total
