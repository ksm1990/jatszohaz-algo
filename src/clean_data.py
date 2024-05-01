import datetime
import pandas as pd
import numpy as np


def cleanup_beo_df(
    beo_df: pd.DataFrame,
    max_days_past: int = 100,
    day_of_event: datetime = datetime.datetime.today(),
) -> pd.DataFrame:
    filtered = beo_df.drop(beo_df.columns[[1, 2, -1, -2, -3, -4, -5]], axis=1)
    filtered.drop([0, 1, 2], inplace=True)

    min_date = day_of_event - datetime.timedelta(days=max_days_past)

    filtered["Dátum"] = pd.to_datetime(filtered["Dátum"], format="%Y.%m.%d.")

    filtered = filtered.loc[(filtered["Dátum"] > min_date)]

    filtered["days_before"] = abs((day_of_event - filtered["Dátum"]).dt.days)

    filtered.set_index("Dátum", inplace=True)

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
