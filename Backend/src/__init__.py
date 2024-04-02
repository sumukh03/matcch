from flask import Flask
from flask_migrate import Migrate
from .extension import db


def create_app():
    from src.views.user_views import users_end
    from src.models.user_models import users,user_score


    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.db"
    # app.config[
    #     "SQLALCHEMY_DATABASE_URI"
    # ] = "mysql+pymysql://{user}:{password}@{host}/{db_name}".format(user="root",password="palaramukh",host="localhost",db_name="matcch")

    db.init_app(app)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "matcch"

    migrate=Migrate(app, db)
    migrate.init_app(app)

    app.register_blueprint(users_end)

    @app.route("/")
    def get_urls():
        return {"urls": [str(url) for url in app.url_map.iter_rules()]}

    return app