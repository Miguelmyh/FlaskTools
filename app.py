from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "123"
app.debug= True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"

@app.route('/')
def index():
    title = survey.title
    instructions = survey.instructions
    questions = survey.questions
        
    return render_template('index.html', title = title, instructions = instructions, questions = questions)

@app.route('/begin', methods=['POST'])
def begin():
    session[RESPONSES_KEY] = []
    return redirect('questions/0')

@app.route('/answer', methods=['POST'])
def handleAnswer():
    choice = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if(len(responses) == len(survey.questions)):
        flash("thanks for completion")
        return redirect('/')

    return redirect(f"/questions/{len(responses)}")

@app.route('/questions/<int:qid>')
def show_question(qid):
    responses = session.get(RESPONSES_KEY)
    
    if ( responses is None):
        return redirect('/')
    
    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != qid):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[qid]
    return render_template("question.html", question_num=qid, question=question)
    
    
