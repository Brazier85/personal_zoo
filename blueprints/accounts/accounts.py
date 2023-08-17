from flask import current_app, render_template, request, redirect, url_for, flash, Blueprint
from flask_login import current_user, login_required, login_user, logout_user
from flask_bcrypt import check_password_hash, generate_password_hash

from functions import *

from .forms import RegisterForm, LoginForm, PasswordForm

accounts_bp = Blueprint("accounts", __name__, template_folder="templates")

@accounts_bp.route("/", methods=["GET", "POST"])
@login_required
def profile():
    print(current_user.id)
    user = User.query.filter(User.id==current_user.id).first()
    return render_template("profile.html", user=user, location="profile")
    
@accounts_bp.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    users = User.query.all()
    if current_user.is_admin:
        return render_template("admin.html", users=users, location="account")
    else:
        flash("You need to be an Administrator to view this page!", "warning")
        return redirect("/")

@accounts_bp.route("/change_password/<int:id>", methods=["GET", "POST"])
@login_required
def update_password(id):

    target_user = User.query.get_or_404(id)

    if current_user == target_user:
        form = PasswordForm(request.form)

        if form.validate_on_submit():
            if check_password_hash(target_user.password, form.old_password.data):
                target_user.password = generate_password_hash(form.new_password.data)
                db.session.add(target_user)
                db.session.commit()
                flash("Password changed!", "success")
                return redirect(url_for("accounts.profile"))
            else:
                flash("Wrong current password entered!", "danger")
                return redirect(url_for("accounts.profile"))
        
        return render_template("password_form.html", form=form, location="profile", id=id)

@accounts_bp.route("/change/<string:mode>/<int:id>", methods=["GET", "POST"])
@login_required
def change(mode, id):

    target_user = User.query.get_or_404(id)

    if current_user.is_admin:
        if current_user == target_user:
            flash("You can not change your own account!", "warning")
            return "", 200
        else:
            if mode == "admin":
                if target_user.is_admin:
                    target_user.is_admin = False
                else:
                    target_user.is_admin = True

                db.session.add(target_user)
                db.session.commit()

                return "", 200
            if mode == "active":
                if target_user.is_active:
                    target_user.is_active = False
                else:
                    target_user.is_active = True

                db.session.add(target_user)
                db.session.commit()

            if mode == "delete":
                db.session.delete(target_user)
                db.session.commit()

            return "", 200
    else:
        flash("You need to be an Administrator to view this page!", "warning")
        return redirect("/")

@accounts_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You are already registered.", "info")
        return redirect("/")
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        # Check for existing users
        admins = User.query.filter(User.is_admin==True).count()
        if admins == 0:
            user = User(email=form.email.data, password=form.password.data, is_admin=True, is_active=True)
            flash("Registration successful. You are an administrator!", "success")
        else:
            user = User(email=form.email.data, password=form.password.data)
            flash("Registration successful. Ask an administrator to activate your account!", "success")
        db.session.add(user)
        db.session.commit()

        login_user(user, True)

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
            login_user(user, True)
            if current_user.is_active:
                flash("Login successful!", "success")
                return redirect("/")
            else:
                flash("Your user is not activated!", "warning")
                return render_template("login.html", form=form)            
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