import numpy as np

default_gun_list = [
    "tgun",
    "gersch",
    "dolls",
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
    "r",
    "s",
    "t",
]


def run_box_hits(
    num_box_hits: int, gun_list: list[str] = default_gun_list
) -> dict[str:int]:
    current_hit = 0
    count_dict = {}
    for x in gun_list:
        count_dict[x] = 0

    while current_hit <= num_box_hits:
        current_hit += 1
        randint = np.random.randint(0, len(gun_list))
        curr_gun = gun_list[randint]
        count_dict[curr_gun] += 1

    return count_dict


def create_list_from_dict(count_dict: dict, sort: bool = True) -> list[dict]:
    _list = []

    for gun_name in count_dict.keys():
        _list.append([gun_name, count_dict[gun_name]])

    if sort == True:
        return sorted(_list, key=lambda x: x[1])
    else:
        return _list


if __name__ == "__main__":
    from pprint import pprint

    count_dict = run_box_hits(2367)
    pprint(create_list_from_dict(count_dict))
