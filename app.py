from flask import Flask, request, render_template, redirect, flash, session
from surveys import satisfaction_survey
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'oh-so-secret'

debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.route('/')
def index():
    """ Homepage """
    return render_template('start.html', survey=satisfaction_survey)

@app.route('/setsession', methods=["POST"])
def set_session():
    session['responses'] = []
    return redirect('/questions/0')

@app.route('/questions/<int:qindex>')
def show_question(qindex):
    """ Shows each question page """
    
    pindex = len(session['responses'])
    if qindex is pindex and pindex is not 4:
        return render_template('question.html', survey=satisfaction_survey, qindex=qindex)
    elif pindex is 4:
        return redirect(f'/thanks')
    else:
        flash(f"Redirect to question {pindex}: you tried to access an invalid question out of order")
        return redirect(f'/questions/{pindex}')

@app.route('/answer')
def handle_thanks():
    """ Handles GET to answer e.g. renders thank you if survey is finished"""

    return redirect(f'/thanks')

@app.route('/answer/<int:aindex>', methods=["POST"])
def handle_answer(aindex):
    """ Handles answer """

    responses = session['responses']
    responses.append(request.form['choice'])
    session['responses'] = responses
    if aindex < len(satisfaction_survey.questions) - 1:
        aindex = aindex + 1
        return redirect(f'/questions/{aindex}')
    else:
        return redirect(f'/thanks')
    
@app.route('/thanks')
def thanks():
    return render_template('thanks.html', survey=satisfaction_survey)