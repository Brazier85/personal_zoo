from flask import current_app, render_template, request, redirect, url_for, flash, Blueprint
from flask_login import current_user, login_required, login_user, logout_user
from flask_bcrypt import check_password_hash

from functions import *

from .forms import RegisterForm, LoginForm

accounts_bp = Blueprint("accounts", __name__, template_folder="templates")

@accounts_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You are already registered.", "info")
        return redirect("/")
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("You registered and are now logged in. Welcome!", "success")

        return redirect("/")

    return render_template("register.html", form=form, location="register")

@accounts_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect("/")
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect("/")
        else:
            flash("Invalid email and/or password.", "warning")
            return render_template("login.html", form=form)
    return render_template("login.html", form=form, location="login")

@accounts_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")
    return redirect("/")