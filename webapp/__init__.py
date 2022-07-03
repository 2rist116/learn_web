from flask import Flask

from webapp.db import db
from webapp.user.models import User
from flask_login import LoginManager
from webapp.user.views import blueprint as user_blueprint
from webapp.admin.views import blueprint as admin_blueprint


# set FLASK_APP=webapp && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    return app
