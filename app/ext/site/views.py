from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app.ext.auth.form import EditProfileForm, LoginForm, RegistrationForm
from app.ext.db import db, models

bp = Blueprint("site", __name__)


@bp.route("/")
@login_required
def index():
    title = "Home"
    user = {"name": "Felipe"}
    posts = [
        {
            "author": {"username": "Felipe"},
            "body": "Beautiful day in Portland",
        },
        {
            "author": {"username": "Eliza"},
            "body": "Avengers movie was so cool!",
        },
        {
            "author": {"username": "Matteo"},
            "body": "I love mom and daddy",
        },
    ]

    return render_template("index.html", title=title, posts=posts)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("site.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("site.login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("site.index")
        return redirect(next_page)
    return render_template("login.html", title="Sign in", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("site.index"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("site.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = models.User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now registered!")
        return redirect(url_for("site.login"))

    return render_template("register.html", title="Register", form=form)


@bp.route("/login/<username>")
@login_required
def user(username):
    user = models.User.query.filter_by(usernamme=username).first_or_404()
    posts = [
        {"author": user, "body": "Test post #01"},
        {"author": user, "body": "Test post #02"},
    ]
    return render_template("user.html", user=user, posts=posts)


@bp.route("/edit-profile", methods=["GET", "POST"])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your Changes have been saved.")
        return redirect(url_for("site.edit_profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template(
        "edit_profile.html", title="Edit Profile", form=form
    )


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow
        db.session.commit()
