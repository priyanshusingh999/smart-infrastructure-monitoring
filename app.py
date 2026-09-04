from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.config.from_object('config.Config')

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Here you would typically check the username and password against a database
        if username == 'admin' and password == 'password':  # Example credentials
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('auth/login.html')


@app.route('/dashboard')
def dashboard():
    return render_template('pages/dashboard.html')

@app.route('/documents')
def documents():
    return render_template('pages/document.html')

@app.route('/schedule')
def schedule():
    return render_template('pages/schedule.html')

@app.route('/progress')
def progress():
    return render_template('pages/progress.html')

@app.route('/risks')
def risks():
    return render_template('pages/risk&delays.html')

@app.route('/assistant')
def assistant():
    return render_template('pages/assistant.html')

if __name__ == '__main__':
    app.run(debug=True)