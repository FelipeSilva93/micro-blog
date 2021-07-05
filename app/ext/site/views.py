from flask import Blueprint, flash, redirect, render_template, url_for

from app.ext.auth.form import LoginForm

bp = Blueprint("site", __name__)


@bp.route("/")
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

    return render_template("index.html", title=title, user=user, posts=posts)


@bp.route("/login", methods=["get", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash(
            f"Login requested for user {form.username.data}, remember_me={form.remember_me.data}"
        )
        return redirect(url_for("site.index"))
    return render_template("login.html", title="Sign In", form=form)
