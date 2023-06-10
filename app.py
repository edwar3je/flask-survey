from flask import Flask, request, render_template, redirect, flash, session
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this-is-secret'

satlen = len(satisfaction_survey.questions)
indlen = (satlen - 1)

@app.route('/home')
def home_display():
    session['start'] = False
    return render_template('home.html', title=satisfaction_survey.title, instructions=satisfaction_survey.instructions)

@app.route('/question/<ind>')
def quest_display(ind):
    if session['start']:
        session['numpath'] = int(request.path.replace('/question/', ''))
        # if responses is empty
        if not session['responses']:
            if session['numpath'] == 0:
                return render_template('question.html', ind=str(session['ind']), ind_n = int(session['ind']), question=satisfaction_survey.questions[int(session['ind'])].question, choices=satisfaction_survey.questions[int(session['ind'])].choices)
            else:
                if session['numpath'] <= indlen:
                    session['ind'] = 0
                    flash('No skipping ahead')
                    return redirect(str(session['ind']))
                else:
                    session['ind'] = 0
                    flash("That question doesn't exist")
                    return redirect(str(session['ind']))
        # if responses is not entirely full
        elif len(session['responses']) < satlen:
            if session['numpath'] <= indlen:
                if session['numpath'] == session['ind']:
                    return render_template('question.html', ind=str(session['ind']), ind_n = int(session['ind']), question=satisfaction_survey.questions[int(session['ind'])].question, choices=satisfaction_survey.questions[int(session['ind'])].choices)
                elif session['numpath'] < session['ind']:
                    session['ind'] = len(session['responses'])
                    flash("No turning back")
                    return redirect(str(session['ind']))
                else:
                    session['ind'] = len(session['responses'])
                    flash("No skipping ahead")
                    return redirect(str(session['ind']))
            else:
                session['ind'] = len(session['responses'])
                flash("That question doesn't exist")
                return redirect(str(session['ind']))
        # if responses is either full or overflowing
        else:
            return redirect('/thanks')
    else:
        flash('Please start the survey')
        return redirect('/home')

@app.route('/handle-process')
def init_sessions():
    session['start'] = True
    session['ind'] = 0
    session['responses'] = []
    print(session['ind'])
    print(session['responses'])
    return redirect('/question/' + str(session['ind']))

@app.route('/thanks', methods=['GET', 'POST'])
def display_and_handle_answers():
    if session['start']:
        if session['ind'] == 0:
            if request.form.get('choosed'):
                session['ind'] += 1
                session['responses'].append(request.form['choosed'])
                print(session['ind'])
                print(session['responses'])
                return redirect('/question/' + str(session['ind']))
            else:
                flash('Select an option')
                return redirect('/question/' + str(session['ind']))
        elif session['ind'] < satlen:
            if request.form.get('choosed'):
                session['ind'] += 1
                session['responses'].append(request.form['choosed'])
                print(session['ind'])
                print(session['responses'])
                return redirect('/question/' + str(session['ind']))
            else:
                flash('Select an option')
                return redirect('/question/' + str(session['ind']))
        elif len(session['responses']) == satlen:
            return render_template('answer.html')
    else:
        flash('Please start the survey')
        return redirect('/home')