import logging

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import (generate_password_hash, check_password_hash)
from pymongo.errors import DuplicateKeyError, PyMongoError
from routes.database import (create_user, get_user_by_email, get_user_by_username, password_reset_collection, users_collection, ensure_indexes,)
from datetime import datetime, timedelta
from routes.email import send_otp_email
import secrets
import smtplib

MIN_PASSWORD_LENGTH = 8
logger = logging.getLogger(__name__)
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        try:
            user = get_user_by_username(username)
        except PyMongoError:
            flash('Database is unavailable. Please try again later.', 'danger')
            return render_template('auth/login.html'), 503

        password_matches = (
            user is not None
            and check_password_hash(user.get('password', ''), password)
        )

        if password_matches:

            session['username'] = username

            if user:
                session['user_id'] = str(user['_id'])

            flash('Login successful!', 'success')

            return redirect(url_for('dashboard'))
        else:

            flash(
                'Invalid credentials. Please try again.',
                'danger'
            )

    return render_template('auth/login.html')


@auth.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        fullname = request.form.get('fullname', '').strip()
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not fullname or not username or not email or not password:

            flash('All fields are required.', 'danger')

            return redirect(url_for('auth.signup'))

        if len(password) < MIN_PASSWORD_LENGTH:
            flash(f'Password must be at least {MIN_PASSWORD_LENGTH} characters.', 'danger')
            return redirect(url_for('auth.signup'))

        if password != confirm_password:

            flash('Passwords do not match.', 'danger')

            return redirect(url_for('auth.signup'))

        try:
            username_exists = get_user_by_username(username)
            email_exists = get_user_by_email(email)
        except PyMongoError:
            flash('Database is unavailable. Please try again later.', 'danger')
            return render_template('auth/signup.html'), 503

        if username_exists:

            flash('Username is already in use.', 'danger')

            return redirect(url_for('auth.signup'))

        if email_exists:

            flash('Email is already registered.', 'danger')

            return redirect(url_for('auth.signup'))

        try:
            create_user(
                fullname,
                username,
                email,
                generate_password_hash(password),
            )
        except DuplicateKeyError:

            flash('Username or email is already registered.', 'danger')

            return redirect(url_for('auth.signup'))
        except PyMongoError:
            flash('Database is unavailable. Please try again later.', 'danger')
            return render_template('auth/signup.html'), 503

        flash('Account created successfully!', 'success')

        return redirect(url_for('auth.login'))


    return render_template('auth/signup.html')


@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():

    if request.method == 'POST':

        email = request.form.get(
            'email',
            ''
        ).strip().lower()

        try:
            user = get_user_by_email(email)
        except PyMongoError:
            flash('Database is unavailable. Please try again later.', 'danger')
            return render_template('auth/forgot-password.html'), 503

        if not user:
            flash('No account was found for that email address.', 'danger')
            return redirect(url_for('auth.forgot_password'))

        otp = f"{secrets.randbelow(1000000):06d}"

        otp_hash = generate_password_hash(otp)

        now = datetime.utcnow()

        try:
            ensure_indexes()
            password_reset_collection.delete_many({
                "email": email
            })

            password_reset_collection.insert_one({
                "email": email,
                "otp_hash": otp_hash,
                "attempts": 0,
                "created_at": now,
                "expires_at": now + timedelta(minutes=10)
            })
        except PyMongoError:
            flash('Database is unavailable. Please try again later.', 'danger')
            return render_template('auth/forgot-password.html'), 503

        try:
            send_otp_email(email, otp)
        except (OSError, RuntimeError, smtplib.SMTPException):
            logger.exception('Could not send password reset email')
            password_reset_collection.delete_many({'email': email})
            session.pop('reset_email', None)
            flash('Password reset email could not be sent. Please try again later.', 'danger')
            return redirect(url_for('auth.forgot_password'))

        session["reset_email"] = email
        session.pop("otp_verified", None)

        flash(
            "If an account exists with this email, "
            "a reset OTP has been sent.",
            "success"
        )

        return redirect(
            url_for('auth.verify_otp')
        )

    return render_template('auth/forgot-password.html')


# @auth.route('/forgot-password', methods=['GET', 'POST'])
# def forgot_password():

#     if request.method == 'POST':

#         email = request.form['email']

#         # TODO:
#         # MongoDB mein email check karna
#         # Password reset token generate karna
#         # Reset link email karna

#         flash(
#             'If an account exists with this email, '
#             'a password reset link will be sent.',
#             'success'
#         )

#         return redirect(url_for('auth.forgot_password'))

#     return render_template('auth/forgot-password.html')


@auth.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():

    email = session.get("reset_email")

    if not email:

        flash(
            "Please request a new password reset.",
            "danger"
        )

        return redirect(
            url_for('auth.forgot_password')
        )


    if request.method == 'POST':

        otp = request.form.get(
            'otp',
            ''
        ).strip()


        reset_data = password_reset_collection.find_one({
            "email": email
        })


        if not reset_data:

            flash(
                "Invalid or expired OTP.",
                "danger"
            )

            return redirect(
                url_for('auth.forgot_password')
            )


        # Expiry check

        if datetime.utcnow() > reset_data["expires_at"]:

            password_reset_collection.delete_one({
                "_id": reset_data["_id"]
            })

            flash(
                "OTP has expired. Please request a new one.",
                "danger"
            )

            return redirect(
                url_for('auth.forgot_password')
            )


        # Attempt limit

        if reset_data["attempts"] >= 5:

            password_reset_collection.delete_one({
                "_id": reset_data["_id"]
            })

            flash(
                "Too many incorrect attempts.",
                "danger"
            )

            return redirect(
                url_for('auth.forgot_password')
            )


        # Verify OTP

        if not check_password_hash(reset_data["otp_hash"], otp):

            password_reset_collection.update_one(
                {"_id": reset_data["_id"]},
                {
                    "$inc": {
                        "attempts": 1
                    }
                }
            )

            flash(
                "Invalid OTP.",
                "danger"
            )

            return redirect(
                url_for('auth.verify_otp')
            )


        # OTP verified

        session["otp_verified"] = True

        return redirect(
            url_for('auth.reset_password')
        )


    return render_template(
        'auth/verify_otp.html'
    )


@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password():

    email = session.get('reset_email')

    if not email or not session.get('otp_verified'):

        flash(
            'Please verify the OTP before resetting your password.',
            'danger'
        )

        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':

        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if len(password) < MIN_PASSWORD_LENGTH:

            flash(
                f'Password must be at least {MIN_PASSWORD_LENGTH} characters.',
                'danger'
            )

            return redirect(url_for('auth.reset_password'))

        if password != confirm_password:

            flash('Passwords do not match.', 'danger')

            return redirect(url_for('auth.reset_password'))

        result = users_collection.update_one(
            {'email': email},
            {'$set': {'password': generate_password_hash(password)}}
        )

        if result.matched_count == 0:

            session.pop('reset_email', None)
            session.pop('otp_verified', None)

            flash('Account not found. Please try again.', 'danger')

            return redirect(url_for('auth.forgot_password'))

        session.pop('reset_email', None)
        session.pop('otp_verified', None)

        password_reset_collection.delete_one({'email': email})

        flash('Password updated successfully. Please sign in.', 'success')

        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html')