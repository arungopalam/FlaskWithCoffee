from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from website import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Invalid password', category='error')
        else:
            flash('User does not exist', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        phone = request.form.get("phone")

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered', category='success')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters', category='error')
        elif password != confirm:
            flash('Passwords dont match', category='error')
        else:
            user = User(email=email, password=generate_password_hash(password), first_name=firstName, last_name=lastName, phone=phone)
            db.session.add(user)
            db.session.commit()
            flash('Account created', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)
