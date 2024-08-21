from flask import Flask
from flask import render_template
from flask import request
import datetime

import pandas as pd

from src.clean_data import clean_kimittud_df, cleanup_beo_df
from src.gsheet_download import download_data
from src.constants import NAMES
from src.utils import calc_beo_weights, create_gm_combinations_df


app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("/partials/name-selector.html", names=NAMES)


@app.route("/names", methods=["POST"])
def print_names():
    jm_candidates = request.form.getlist("jm")
    carries_to = request.form.getlist("to")
    carries_from = request.form.getlist("from")
    bosses = request.form.getlist("boss")
    gm_count = request.form.get("gm-count")
    event_date = request.form.get("event-date")
    must_have_boss = request.form.get("must-have-boss") == "on"
    threshhold_percent = request.form.get("threshhold-percent", type=int)
    game_min_count = request.form.get("game-min-count", type=int, default=85)

    beo_raw, kimittud_raw = download_data()
    beo = cleanup_beo_df(
        beo_raw, day_of_event=datetime.datetime.fromisoformat(event_date)
    )
    kimittud = clean_kimittud_df(kimittud_raw)

    try:
        gm_combinations: pd.DataFrame = create_gm_combinations_df(
            int(gm_count),
            jm_candidates,
            kimittud,
            remove_without_boss=must_have_boss,
            list_of_bosses=bosses,
            threshhold_percent=threshhold_percent,
        )
    except Exception as e:
        return f"Error: {e.with_traceback(None)}"

    weights = calc_beo_weights(beo)

    gm_combinations["beo_weights"] = gm_combinations.apply(
        lambda r: weights[list(r.name)].sum(), axis=1
    )

    gm_combinations = gm_combinations[gm_combinations["count"] > game_min_count]

    return (
        weights.to_frame().to_html()
        + gm_combinations.sort_values(by=["beo_weights"], ascending=True).to_html()
    )
