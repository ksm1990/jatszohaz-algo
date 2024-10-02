from itertools import combinations
import pandas as pd
import numpy as np
import math


def create_gm_combinations_df(
    number_of_gamemasters: int,
    list_of_applicants: list[str],
    cleaned_kimittud_df: pd.DataFrame,
    threshhold_percent: int = 57,
    heavy_threshhold_count: int = 2,
    remove_without_boss: bool = True,
    list_of_bosses: list[str] = [],
) -> pd.DataFrame:

    dict_of_results = {}

    min_gm_count_for_game = math.ceil(number_of_gamemasters * threshhold_percent / 100)

    gamemaster_combinations = list(
        combinations(list_of_applicants, number_of_gamemasters)
    )

    if remove_without_boss:
        gamemaster_combinations = [
            comb
            for comb in gamemaster_combinations
            if any(b in comb for b in list_of_bosses)
        ]

    for comb in gamemaster_combinations:
        game_counts = cleaned_kimittud_df[list(comb)].sum(axis=1)
        list_of_games_over_threshhold = (
            cleaned_kimittud_df[game_counts > min_gm_count_for_game].iloc[:, 0].tolist()
        )
        list_of_heavies_over_threshhold = (
            cleaned_kimittud_df[
                (game_counts >= heavy_threshhold_count)
                & (cleaned_kimittud_df["Heavy"] == True)
            ]
            .iloc[:, 0]
            .tolist()
        )

        dict_of_results[comb] = (
            len(list_of_games_over_threshhold) + len(list_of_heavies_over_threshhold),
            list_of_games_over_threshhold,
            list_of_heavies_over_threshhold,
        )

    return pd.DataFrame.from_dict(
        dict_of_results, orient="index", columns=["count", "games", "heavies"]
    )


def calc_beo_weight(days_before: int):
    if days_before == 0:
        return 100
    return 1 - (0.5 * np.log10(days_before))


def calc_beo_weights(cleaned_beo_df: pd.DataFrame):
    weights = pd.Series()

    for name, values in cleaned_beo_df.items():

        if values.dtype != np.dtypes.StrDType:

            continue

        weights[name] = cleaned_beo_df.apply(
            lambda r: calc_beo_weight(r["days_before"]) if "j" in r[name] else 0, axis=1
        ).sum()

    return weights
