from flask import Flask, request, render_template, redirect, flash
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this-is-secret'

responses = []
reslen = len(responses)
ind = -1
indlen = (len(satisfaction_survey.questions)) - 1

@app.route('/home')
def home_display():
    return render_template('home.html', title=satisfaction_survey.title, instructions=satisfaction_survey.instructions)

@app.route('/question/<ind>')
def quest_display(ind):
    path = request.path.replace('/question/', '')
    num_path = int(path)
    if not responses:
        if num_path == 0:
            return render_template('question.html', ind=ind, ind_n = int(ind), question=satisfaction_survey.questions[int(ind)].question, choices=satisfaction_survey.questions[int(ind)].choices)
        elif num_path > indlen:
            ind = 0
            flash("That question doesn't exist.")
            return redirect(str(ind))
        else:
            ind = 0
            flash("No peeking.")
            return redirect(str(ind))
    else:
        if num_path < len(responses):
            ind = len(responses)
            flash("Can't access previously answered questions.")
            return redirect('/question/' + str(ind))
        elif num_path > len(responses):
            if num_path > indlen:
                ind = len(responses)
                flash("That question doesn't exist.")
                return redirect('question/' + str(ind))
            else:
                ind = len(responses)
                flash("No peeking.")
                return redirect('question/' + str(ind))
        else:
            return render_template('question.html', ind=ind, ind_n = int(ind), question=satisfaction_survey.questions[int(ind)].question, choices=satisfaction_survey.questions[int(ind)].choices)

@app.route('/question/<ran>')

@app.route('/thanks', methods=['GET', 'POST'])
def display_answer():
    global ind
    if ind != indlen:
        if ind == -1:
            ind += 1
            return redirect('/question/' + str(ind))
        else:
            data = request.form['choosed']
            responses.append(data)
            print(ind)
            print(len(responses))
            ind += 1
            return redirect('/question/' + str(ind))
    else:
        data = request.form['choosed']
        responses.append(data)
        print(ind)
        print(len(responses))
        return render_template('answer.html')