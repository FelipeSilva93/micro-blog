import click

from app.ext.db import db, models


def init_app(app):
    @app.cli.command()
    def create_db():
        """This command inicializate the database"""
        db.create_all()

    @app.cli.command()
    @click.option("--username", "-u")
    @click.option("--email", "-e")
    @click.option("--password", "-p")
    def add_user(username, email, password):
        """This command add a new user do database"""
        user = models.User(
            username=username,
            email=email,
        )
        password = user.set_password(password)

        db.session.add(user)
        db.session.commit()
