from flask import Flask, render_template, request, redirect, url_for, flash, session
from routes.authentication import auth, login_required

app = Flask(__name__)
app.config.from_object('config.Config')
app.register_blueprint(auth)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('pages/dashboard.html')


@app.route('/documents')
@login_required
def documents():
    return render_template('pages/document.html')


@app.route('/schedule')
@login_required
def schedule():
    return render_template('pages/schedule.html')


@app.route('/progress')
@login_required
def progress():
    return render_template('pages/progress.html')


@app.route('/risks')
@login_required
def risks():
    return render_template('pages/risk&delays.html')


@app.route('/assistant')
@login_required
def assistant():
    return render_template('pages/assistant.html')


if __name__ == '__main__':
    app.run(debug=True)