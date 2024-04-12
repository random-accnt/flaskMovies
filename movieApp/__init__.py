import os

from flask import (Flask, g, get_flashed_messages, render_template, request,
                   send_from_directory)
from flask_migrate import Migrate
from flask_misaka import Misaka
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

ALLOWED_IMG_EXTENSIONS = {"png", "jpg", "jpeg"}


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///movies.sqlite",
        IMAGE_DIR="uploads/img",
    )

    app.config["DEFAULT_IMAGE"] = "empty.jpg"

    Misaka(app)
    db.init_app(app)
    migrate.init_app(app, db)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/uploads/img/<path:filename>")
    def serve_image(filename):
        filedir = os.path.join(app.instance_path, app.config["IMAGE_DIR"])
        return send_from_directory(filedir, filename)

    from . import movie

    app.register_blueprint(movie.bp)

    return app
