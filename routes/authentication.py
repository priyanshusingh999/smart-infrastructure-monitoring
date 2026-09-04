from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import (generate_password_hash, check_password_hash)
from routes.database import password_reset_collection, users_collection
from datetime import datetime, timedelta
from routes.email import send_otp_email
import secrets

otp = f"{secrets.randbelow(1000000):06d}"

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

        email = request.form.get(
            'email',
            ''
        ).strip().lower()

        user = users_collection.find_one({
            "email": email
        })

        if user:

            otp = f"{secrets.randbelow(1000000):06d}"

            otp_hash = generate_password_hash(otp)

            now = datetime.utcnow()

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

            send_otp_email(
                email,
                otp
            )

            session["reset_email"] = email

        flash(
            "If an account exists with this email, "
            "a reset OTP has been sent.",
            "success"
        )

        return redirect(
            url_for('auth/verify_otp')
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
            url_for('forgot-password')
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
                url_for('forgot_password')
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
                url_for('forgot_password')
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
                url_for('forgot_password')
            )


        # Verify OTP

        if not check_password_hash(
            reset_data["otp_hash"],
            otp
        ):

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
                url_for('verify_otp')
            )


        # OTP verified

        session["otp_verified"] = True

        password_reset_collection.delete_one({
            "_id": reset_data["_id"]
        })

        return redirect(
            url_for('reset_password')
        )


    return render_template(
        'verify_otp.html'
    )