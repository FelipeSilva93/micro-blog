from app.ext.site.views import bp


def init_app(app):
    app.register_blueprint(bp)
