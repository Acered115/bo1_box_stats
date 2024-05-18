import numpy as np
from scipy.stats import chi2, binom
import matplotlib.pyplot as plt


text_colors = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "reset": "\033[0m",  # Resets the color to default
}
default_gun_list = [
    "tgun",
    "gersch",
    "dolls",
    "a",
    "b",
    "c",
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
]


class Inventory:
    """Class which creates the inventory object"""

    def __init__(self):
        self.tgun_slot: str = ""
        self.tac_slot: str = ""

    def __repr__(self):
        return f"Tgun_slot: {self.tgun_slot}, Tac Slot: {self.tac_slot}"


class WeaponStat:
    """Class which holds information about the weapon from a game"""

    def __init__(self, name: str):
        self.name: str = name
        self.trials: int = 0
        self.observed: int = 0
        self.z_score: float = 0.0

    def __repr__(self):
        if self.z_score < 0:
            colour = text_colors["red"]
        else:
            colour = text_colors["blue"]
        return f"Gun: {self.name}, trials: {self.trials}, observed: {self.observed}, z-score: {colour}{self.z_score}{text_colors['reset']}\n"


def calc_z_score(obs: dict[str:WeaponStat]) -> float:
    """Function used to calculate the z_score of a weapon

    :param obs: The weapon observation
    :type obs: dict[str:WeaponStat]
    :return: The z-score
    :rtype: float
    """
    # print(obs)
    prob = 1 / 20
    trials = obs.trials
    obs_val = obs.observed
    exp_val = trials / 20
    std = np.sqrt(trials * (prob) * (1 - prob))
    z = (obs_val - exp_val) / std
    return z


def roll_box(current_local_list: list[str]) -> str:
    """Just rolls the box for you using the currently available
    box weapons

    :param current_local_list: The currently available box weapons
    :type current_local_list: list[str]
    :return: The weapon resulting from the roll
    :rtype: str
    """
    # As far as I am aware this randomess is the
    # same type as the game and is uniformly distributed

    randint = np.random.randint(0, len(current_local_list))
    curr_gun = current_local_list[randint]
    return curr_gun


def swap_gun(
    wep_type: str, inv: Inventory, curr_gun: str, local_gun_list: list[str]
) -> None:
    """Swaps the gun currently in the targetted inventory slot

    :param wep_type: The type of weapon it is (either tac or gun)
    :type wep_type: str
    :param inv: The inventory object passed through
    :type inv: Inventory
    :param curr_gun: The gun currently rolled from the box
    :type curr_gun: str
    :param local_gun_list: The list which holds the currently available guns in the box
    :type local_gun_list: list[str]
    """
    if wep_type == "tac":
        local_gun_list.append(inv.tac_slot)
        inv.tac_slot = curr_gun
        local_gun_list.remove(curr_gun)
    else:
        local_gun_list.append(inv.tgun_slot)
        inv.tgun_slot = curr_gun
        local_gun_list.remove(curr_gun)


def run_box_hits_with_inv(
    num_box_hits: int, gun_list: list[str] = default_gun_list
) -> dict[str:WeaponStat]:
    """Runs the box for num_box_hits amount of times.
    -> Has inventory and state, meaning that tacticals are treated appropriately
    -> Assumes the Tgun is always available in the box with every hit (aka traded out before hitting the box)

    :return: The game object of a dictionary with str:WeaponStat
    :rtype: dict[str:WeaponStat]
    """
    curr_gun = ""
    local_gun_list = gun_list[:]
    # local_gun_list.remove("tgun")
    local_gun_list.remove("dolls")
    local_gun_list.append("r")
    # local_gun_list.append("z")
    current_hit = 0
    count_dict: dict[str:WeaponStat] = {}
    inv = Inventory()
    inv.tac_slot = "dolls"
    # Currently the tgun slot isnt used
    inv.tgun_slot = "tgun"

    for x in local_gun_list:
        count_dict[x] = WeaponStat(name=x)

    for wep in ["gersch", "dolls", "tgun"]:
        if wep not in count_dict.keys():
            count_dict[wep] = WeaponStat(name=wep)

    while current_hit < num_box_hits:
        current_hit += 1
        for x in count_dict.keys():
            if x != inv.tac_slot:
                count_dict[x].trials += 1
        curr_gun = roll_box(current_local_list=local_gun_list)

        # print(local_gun_list, len(local_gun_list))
        # if inv.tgun_slot == "tgun" and curr_gun != "gersch":
        #     r2 = np.random.randint(0, 100)
        #     if r2 < 10:
        #         count_dict[curr_gun].observed += 1
        #         continue

        if curr_gun == "gersch" or curr_gun == "dolls":
            # r2 = np.random.randint(0, 100)
            if curr_gun == "dolls":
                r2 = np.random.randint(0, 100)
                if r2 < 61:
                    count_dict[curr_gun].observed += 1
                    continue
                # if inv.tgun_slot == "tgun":
                #     if r2 < 10:
                #         count_dict[curr_gun].observed += 1
                #         continue
                # else:
                #     if r2 < 75:
                #         count_dict[curr_gun].observed += 1
                #         continue
            swap_gun("tac", inv=inv, curr_gun=curr_gun, local_gun_list=local_gun_list)
        # elif curr_gun == "tgun":
        #     # print(curr_gun)
        #     swap_gun("gun", inv=inv, curr_gun=curr_gun, local_gun_list=local_gun_list)
        # else:
        #     swap_gun("gun", inv=inv, curr_gun=curr_gun, local_gun_list=local_gun_list)

        # break
        # if curr_gun

        count_dict[curr_gun].observed += 1
    for x in count_dict.keys():
        # print(count_dict[x])
        count_dict[x].z_score = calc_z_score(count_dict[x])
    return count_dict


def run_box_hits(
    num_box_hits: int, gun_list: list[str] = default_gun_list
) -> dict[str:int]:
    """Creates a game with num_box_hits
    -> All guns have the same sample size
    -> Does not have inventory logic
    -> All guns in the list are available every hit

    :return: Dictionary containing the occurance of every gun
    :rtype: dict[str:int]
    """
    current_hit = 0
    count_dict = {}
    for x in gun_list:
        count_dict[x] = 0

    while current_hit < num_box_hits:
        current_hit += 1
        randint = np.random.randint(0, len(gun_list))
        curr_gun = gun_list[randint]
        count_dict[curr_gun] += 1

    return count_dict


def create_list_from_dict(count_dict: dict, sort: bool = True) -> list[dict]:
    """If you want to create a list from the output dict of run_box_hits

    :param count_dict: The output of run_box_hits
    :type count_dict: dict
    :param sort: Sort the list?, defaults to True
    :type sort: bool, optional
    :return: A list representing the same information as the inputted dict
    :rtype: list[dict]
    """
    _list = []

    for gun_name in count_dict.keys():
        _list.append([gun_name, count_dict[gun_name]])

    if sort == True:
        return sorted(_list, key=lambda x: x[1])
    else:
        return _list


def prob_this_or_better(value: int, trials: int, prob: float) -> float:
    """Calculate the probabiliy of the value or better out of the
    number of trials

    :param value: The target value for "equal or better"
    :type value: int
    :param trials: The number of trails that the target value occured from
    :type trials: int
    :param prob: The chance of success
    :type prob: float
    :return: Returns the probability of this or better out of 1
    :rtype: float
    """
    return 1 - binom.cdf(value - 1, trials, prob)


if __name__ == "__main__":
    from pprint import pprint

    print(run_box_hits_with_inv(2417))
