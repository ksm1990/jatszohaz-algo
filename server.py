from flask import Flask
from flask import render_template
from flask import request


names = ['ÁDÁM','ALEX','BALU','BELLA','BORCSA','BORI','DÁVID','DORINA','DORKA','EMMA',
         'FANNI','GERGŐ','JANKA','KATA','KRISTÓF','LILLA','MÁRK','NIKI','PANKA','RÉKA',
         'SANYI','SÁRI','TAKI','VANDA','VERONKA']

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('/partials/name-selector.html', names=names)

@app.route('/names')
def print_names():
    jm_candidates = request.form.getlist('jm')
    carries_to = request.form.getlist('to')
    carries_from = request.form.getlist('from')
    bosses = request.form.getlist('boss')
    return f"jm: {jm_candidates}, to: {carries_to}, from: {carries_from}, boss: {bosses}"