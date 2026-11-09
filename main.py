from flask import Flask,redirect,url_for
from config import Config
from models import db,Admin
from flask_login import LoginManager

from routes.assignment_routes import assign
from routes.auth_routes import auth
from routes.dashboard_routes import dash
from routes.reader_routes import reader

login_manager = LoginManager()
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Admin,int(user_id))

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth)
    app.register_blueprint(dash)
    app.register_blueprint(reader)
    app.register_blueprint(assign)

    @app.route("/")
    def home():
        return redirect(url_for("auth.login"))

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)