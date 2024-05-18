import numpy as np
from utils.chi_squared_utils import convert_game_to_chi_obs_list
from utils.utils import run_box_hits, run_box_hits_with_inv, text_colors
from utils.example_games_file import *

"""NOTE: Z-scores combining only works properly with non-dependent values, In our case the values are dependent because they come from the same superset.
(Ex: A success in one gun, counts as a failure in all the others.)
However this still creates a measure with some meaning. Allows us to see how
much the z-score of a game skews 
"""


def calc_z_score_from_list(obs_list: list[dict[str:int]]) -> float:
    """Calculate the total z-score of all the guns in a obs_list game.
    (REMEMBER THAT THIS IS NOT PROPER FOR Z-SCORES, just an interesting measure)

    :param obs_list: The Game in question
    :type obs_list: list[dict[str:int]]
    :return: The summed total z-score of all the guns
    :rtype: float
    """
    z_array = []
    z = 0
    for obs in obs_list:
        trials = obs["trials"]
        obs_val = obs["succs"]
        exp_val = trials / 20
        std = np.sqrt(trials * (1 / 20) * (19 / 20))
        z = (obs_val - exp_val) / std
        z_array.append(z)
        if (z) < 0:
            colour = text_colors["red"]
        else:
            colour = text_colors["blue"]
        print(
            f"Individual contributions: {obs}: z-score: {colour}{z}{text_colors['reset']}"
        )
    z_comb = sum(z_array)
    print(f"z_comb: {z_comb}")
    return z_comb
