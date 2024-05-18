from utils.chi_squared_utils import *
from utils.utils import run_box_hits, run_box_hits_with_inv
from utils.example_games_file import *


if __name__ == "__main__":
    trials = 2417
    chance_succ = 0.05
    null_hyp_pval = 0.025
    num_runs = 5000
    count = 0
    for inc in range(0, num_runs):
        target_guns = extract_target_guns(
            run_box_hits_with_inv(trials), target_guns=["tgun", "gersch", "dolls"]
        )
        obs_list = convert_game_to_chi_obs_list(target_guns)

        # obs_list = furret_asc224
        # If you wish to remove the "unlucky" contributions from the distribution, uncomment this
        obs_list = remove_unlucky(obs_list, chance_succ)
        if len(obs_list) == 0:
            continue
        deg_freedom = len(obs_list) - 1
        chi_val = chi_squared(
            observed_guns=obs_list, chance_succ=chance_succ, null_hyp_pval=null_hyp_pval
        )
        p_value = chi2.sf(chi_val, deg_freedom)
        print(f"P-Value: {p_value:.6f}")
        weighted = " "
        if chi_val >= 14.00:
            count += 1

        title = f"x2 GOF Value{weighted}vs Critical value  "
        # plot_chi_squared_curve(
        #     title=title, chi_val=chi_val, deg_freedom=deg_freedom, null_pval=0.025
        # )
        print(f"Current Iteration {inc}, current count: {count}")
    print(f"There were {count} games luckier than 13 chi squared")
