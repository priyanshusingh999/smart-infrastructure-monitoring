from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import (generate_password_hash, check_password_hash)

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'password':

            session['username'] = username

            flash('Login successful!', 'success')

            return redirect(url_for('dashboard'))

        else:

            flash(
                'Invalid credentials. Please try again.',
                'danger'
            )

    return render_template('auth/login.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        fullname = request.form['fullname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:

            flash('Passwords do not match.', 'danger')

            return redirect(url_for('auth.signup'))


        # Database mein user create karne ka code yahan aayega

        flash('Account created successfully!', 'success')

        return redirect(url_for('auth.login'))


    return render_template('auth/signup.html')


@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():

    if request.method == 'POST':

        email = request.form['email']

        # TODO:
        # MongoDB mein email check karna
        # Password reset token generate karna
        # Reset link email karna

        flash(
            'If an account exists with this email, '
            'a password reset link will be sent.',
            'success'
        )

        return redirect(url_for('auth.forgot_password'))

    return render_template('auth/forgot-password.html')