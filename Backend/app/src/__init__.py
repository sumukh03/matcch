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
    DATABASE_URI = os.environ.get('DATABASE_URI')

    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://username:password@db:3306/dbname"
    # app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:palaramukh@localhost/matcch"
    # app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@mysql:3307/matcch"
    # app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@db:3307/postgres"
    # app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.environ['MYSQL_USER']}:{os.environ['MYSQL_PASSWORD']}@{os.environ['MYSQL_HOST']}/{os.environ['MYSQL_DATABASE']}"
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'mysql+pymysql://root:root@db:3306/matcch')
    db.init_app(app)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "matcch"

    migrate = Migrate(app, db)
    migrate.init_app(app)

    app.register_blueprint(users_end)
    app.register_blueprint(process_end)

    @app.route("/")
    def get_urls():
        return {"urls": [str(url) for url in app.url_map.iter_rules()]}

    return app
