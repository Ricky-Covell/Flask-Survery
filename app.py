from flask import Flask, request, render_template, session, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

RESPONSES_KEY = "responses"

DEBUG = True
app = Flask(__name__)

app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)



@app.route("/")
def display_survey():
    '''Shows Satisfaction Survery'''

    return render_template('home_page.html', survey=satisfaction_survey)

@app.route('/init', methods=["POST"])
def make_response_list():
    '''Makes Empty Response List In Session Before Questions Page'''

    session[RESPONSES_KEY] = []

    return redirect('/questions/0')


@app.route("/questions/<int:qid>")
def display_question(qid):
    '''Shows Current Question'''

    responses = session[RESPONSES_KEY]

    if (responses is None):
        return redirect('/')
    
    if (len(responses) != qid):
        flash("Invalid question.")
        return redirect(f"/questions/{len(responses)}")

    
    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect('/thanks')

    question = satisfaction_survey.questions[qid]
    return render_template('questions.html', question=question, question_number=qid)


@app.route("/answer", methods=["POST"])
def handle_answer():
    '''Saves Response and Redirects to Next Question'''

    answer = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(answer)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect('/thanks')
    
    else:
        return redirect(f'/questions/{len(responses)}') 
    
@app.route("/thanks")
def thank_user():
    '''Thanks User After Survey Is Complete'''

    return render_template('thanks.html')
