import math
import re

TOTAL_ROUNDS = 7

REGION_COUNTS = {1: "East", 2: "Midwest", 3: "South", 4: "West"}


def get_pos_round(pos):
    return 1 if pos.find("a") > -1 or pos.find("b") > -1 else 2


def get_pos_game_number(pos):
    round = get_pos_round(pos)
    if round == 1:
        return int(re.sub("[^\d\.]", "", pos))
    else:
        return math.ceil(int(pos) / 2)


def get_region(round_number, game_number):
    if TOTAL_ROUNDS - round_number < 2:
        return "Final Four"

    games_in_round = 2 ** (TOTAL_ROUNDS - round_number)
    region_number = math.ceil((game_number / games_in_round) * 4)
    return REGION_COUNTS[region_number]
