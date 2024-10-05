from itertools import combinations
import pandas as pd
import numpy as np
import math
import datetime


def calc_event_weight(days_before: int):
    if days_before == 0:
        return 100
    return 1 - (0.5 * np.log10(days_before))


def cleanup_beo_df(
    beo_df: pd.DataFrame,
    day_of_event: datetime,
    non_monday_event_weight: float,
    max_days_past: int = 100,
) -> pd.DataFrame:
    # filtered = beo_df.drop(beo_df.columns[[1, 2, -1, -2, -3, -4, -5]], axis=1)
    filtered = beo_df.copy()  # Create a copy to avoid modifying the original DataFrame
    filtered = filtered.iloc[3:]  # Remove first 3 rows more efficiently

    min_date = day_of_event - datetime.timedelta(days=max_days_past)

    filtered["Dátum"] = pd.to_datetime(filtered["Dátum"], format="%Y.%m.%d.")

    filtered = filtered[filtered["Dátum"] > min_date]

    filtered["days_before"] = (day_of_event - filtered["Dátum"]).dt.days.abs()

    filtered["event_type_weight"] = np.where(
        filtered["Hétfői esemény? (algoritmus miatt)"] == "TRUE",
        1,
        non_monday_event_weight,
    )

    filtered["event_weight"] = filtered["days_before"].apply(calc_event_weight)

    filtered["complete_weight"] = (
        filtered["event_type_weight"] * filtered["event_weight"]
    )

    filtered.set_index("Dátum", inplace=True)

    print(filtered)

    return filtered


def clean_kimittud_df(kimittud_df: pd.DataFrame, count_of_retired_gms: int = 4):
    df = kimittud_df.copy()
    df.drop(
        [
            "Hot shit?",
            "HIÁNY",
            "Co-op",
            "Gyerek",
            "Kétfős",
            "Nyelvfüggetlen",
            "Party",
            "Szélproof",
            "!!!",
        ],
        axis=1,
        inplace=True,
    )
    # delete empty rows based on the last value of column 'ÁDÁM':

    column_to_check = "ÁDÁM"
    df.replace("", np.nan, inplace=True)
    df.dropna(subset=column_to_check, inplace=True)

    df.drop(df.columns[-count_of_retired_gms:], axis=1, inplace=True)

    df.drop([0, 1], inplace=True)

    df.iloc[:, 2:] = df.iloc[:, 2:].apply(lambda x: x == "2")
    df.iloc[:, 1] = df.iloc[:, 1].apply(lambda x: x == "TRUE")

    df[df.columns[1:]] = df[df.columns[1:]].astype("bool")

    return df


def create_gm_combinations_df(
    number_of_gamemasters: int,
    list_of_applicants: list[str],
    cleaned_kimittud_df: pd.DataFrame,
    threshhold_percent: int,
    heavy_threshhold_count: int,
    remove_without_boss: bool,
    list_of_bosses: list[str],
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


def calc_beo_weights(cleaned_beo_df: pd.DataFrame):

    weights = pd.Series()

    for name, values in cleaned_beo_df.items():

        if values.dtype != np.dtypes.StrDType:
            continue

        if str(name).upper() != str(name):
            # if it's not an uppercase name, skip
            continue

        try:
            weights[name] = cleaned_beo_df.apply(
                lambda r: (
                    r["complete_weight"]
                    if type(r[name]) == str and "j" in r[name]
                    else 0
                ),
                axis=1,
            ).sum()
        except KeyError:
            continue

    return weights
