import click

from app.ext.db import db


def init_app(app):
    @app.cli.command()
    def create_db():
        """This command inicializate the database"""
        db.create_all()
