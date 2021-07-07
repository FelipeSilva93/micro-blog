from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app.ext.auth.form import LoginForm, RegistrationForm
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
