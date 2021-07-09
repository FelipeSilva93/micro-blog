from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()


def init_app(app):
    bootstrap.init_app(app)
