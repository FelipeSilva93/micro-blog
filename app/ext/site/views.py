from flask import Blueprint, render_template

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
