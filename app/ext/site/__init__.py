from app.ext.site.errors import bp as error_bp
from app.ext.site.views import bp


def init_app(app):
    app.register_blueprint(bp)
    app.register_blueprint(error_bp)
