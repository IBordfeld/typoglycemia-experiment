from flask import Flask, render_template, url_for, request, redirect
from forms import StartScreen, ExperimentScreen
from main import Subject
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'caed3c9aed312205beb3578aad5d6be2'
subject = Subject()

@app.route("/", methods=['GET', 'POST'])
def start():
    form = StartScreen()
    first, last, age, sex = form.get_info()
    if form.validate_on_submit():
        subject.updateInformation(first, last, age, sex)
        return redirect(url_for('experiment'))
    return render_template("start.html", title="Start", form=form)

@app.route("/experiment", methods=['GET', 'POST'])
def experiment():
    user = ExperimentScreen()

    if not subject.pickedSentence:
        subject.pickedSentence = True
        subject.sentence = subject.runExperiment()
        subject.timeStart = time.time()
    
    if user.validate_on_submit():
        subject.timeEnd = time.time()
        subject.responseTime = int((subject.timeEnd - subject.timeStart) * 1000)
        subject.answer = user.getAnswer().data
        subject.isCorrect = subject.checkAnswer(subject.sentence[1], subject.answer)
        subject.showData()
        subject.reset()
        if subject.done():
            return redirect(url_for('complete'))
        return redirect(url_for('experiment'))
   
    return render_template("experiment.html", title="Experiment", form=user, sentence = subject.sentence[0])

@app.route("/complete", methods=['GET', 'POST'])
def complete():
    rt = subject.results()
    return render_template("complete.html", title="Complete", totalCorrect = subject.totalRight, responseTime = rt)

if __name__ == "__main__":
    app.run(debug = True)
