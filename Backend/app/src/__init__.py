from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from .extension import db
import os


def create_app():
    from src.views.user_views import users_end
    from src.views.processing_views import process_end
    from src.models.user_models import users
    from src.models.processing_models import user_score

    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

    db.init_app(app)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "matcch"

    migrate = Migrate(app, db)
    migrate.init_app(app, db)

    app.register_blueprint(users_end)
    app.register_blueprint(process_end)

    @app.route("/")
    def get_urls():
        return {"urls": [str(url) for url in app.url_map.iter_rules()]}

    return app
