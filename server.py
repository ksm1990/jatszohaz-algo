from flask import Flask
from flask import render_template
from flask import request
import datetime

from src.constants import NAMES


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

    # try:
    #     gm_count = int(gm_count)
    #     event_date = datetime.datetime.strptime(event_date, "%Y-%m-%d")
    # except ValueError:
    #     return "gm_count must be an integer"

    return f"jm: {jm_candidates}, to: {carries_to}, from: {carries_from}, boss: {bosses}, gm_count: {gm_count}, event_date: {event_date}"
