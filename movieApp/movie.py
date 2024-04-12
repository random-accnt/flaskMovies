import os

from flask import (Blueprint, current_app, flash, g, redirect, render_template,
                   request, session, url_for)
from werkzeug.utils import secure_filename

from movieApp import db
from movieApp.db import Image, Movie
from movieApp.util import is_allowed_img, parse_reviews

PREV_URL_KEY = "prev_url"

bp = Blueprint("movie", __name__, url_prefix="/movie")


@bp.route("/")
def index():
    session[PREV_URL_KEY] = url_for("movie.index")
    movies = (
        db.session.execute(db.select(Movie).order_by(Movie.createdAt))
        .scalars()
        .fetchmany(5)
    )

    return render_template("movie/index.html", movies=movies)


@bp.route("/<int:movie_id>")
def single_movie(movie_id):
    movie = get_movie(movie_id)
    positives = parse_reviews(movie.positives if movie.positives else "")
    negatives = parse_reviews(movie.negatives if movie.negatives else "")

    session[PREV_URL_KEY] = url_for("movie.single_movie", movie_id=movie_id )
    return render_template("movie/movie.html", movie=movie, positives=positives, negatives=negatives)


@bp.route("/add", methods=("GET", "POST"))
def add():
    if request.method == "POST":
        title = request.form["title"]
        rating = request.form["option-rating"]
        description = request.form["description"] if request.form["description"] else ""
        positives = request.form["positives"] if request.form["positives"] else ""
        negatives = request.form["negatives"] if request.form["negatives"] else ""
        image = None


        error = None

        if not title:
            error = "Movie title required"

        if not rating.isdigit():
            rating = -1
        else:
            rating = int(rating)

        # make sure value is in range [-1, 5]
        if rating > 5:
            rating = 5
        if rating < -1:
            rating = -1

        if "image" in request.files:
            image = request.files["image"]

        if error is None:
            movie = Movie()
            movie.title = title
            movie.rating = rating
            movie.description = description
            movie.positives = positives
            movie.negatives = negatives


            image_filename = check_image(image, save=True)

            if image_filename != "":
                new_image = Image()
                new_image.filename = image_filename

                db.session.add(new_image)
                db.session.flush()

                movie.id_image = new_image.id

            try:
                db.session.add(movie)
                db.session.commit()
            except db.IntegrityError:
                error = "Some db integrity error? Possibly skill issue"
            else:
                return redirect(session[PREV_URL_KEY])
        flash(error)

    return render_template("movie/add.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
def update(id):
    movie = get_movie(id)
    if request.method == "POST":
        title = request.form["title"]
        rating = request.form["option-rating"]
        description = request.form["description"]
        positives = request.form["positives"] if request.form["positives"] else ""
        negatives = request.form["negatives"] if request.form["negatives"] else ""
        image = None
        error = None

        if not title:
            error = "Movie title required"

        if not rating.isdigit():
            print("ERROR: rating is not a digit: ", rating)
            rating = -1
        else:
            rating = int(rating)

        # make sure value is in range [-1, 5]
        if rating > 5:
            rating = 5
        if rating < -1:
            rating = -1

        if "image" in request.files:
            image = request.files["image"]

        if error is None:
            image_filename = check_image(image, save=True)

            if image_filename != "":
                new_image = Image()
                new_image.filename = image_filename

                db.session.add(new_image)
                db.session.flush()

                movie.id_image = new_image.id

            movie.title = title
            movie.rating = rating
            movie.description = description
            movie.positives = positives
            movie.negatives = negatives
            db.session.commit()

            return redirect(session[PREV_URL_KEY])
        flash(error)

    return render_template("movie/update.html", movie=movie)


@bp.route("/<int:id>/delete", methods=("GET", "POST"))
def delete(id):
    movie = get_movie(id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("movie.index"))

@bp.route("/<int:id>/update_vars/<variable>", methods=['POST',])
def update_vars(id, variable):
    movie = get_movie(id)
    text = request.form.get("new_value")
    if text:
        if variable == "positives":
            movie.positives = f"{movie.positives}\n- {text}" if movie.positives else f"- {text}"
            db.session.commit()
            return render_template('movie/item_list.html', id="pos-and-form", title="Positives", color="border-success", items=parse_reviews(movie.positives), post_url=url_for('movie.update_vars', id=movie.id, variable="positives"))
        elif variable == "negatives":
            movie.negatives = f"{movie.negatives}\n- {text}" if movie.negatives else f"- {text}"
            db.session.commit()
            return render_template('movie/item_list.html', id="neg-and-form", title="Negatives", color="border-danger", items=parse_reviews(movie.negatives), post_url=url_for('movie.update_vars', id=movie.id, variable="negatives"))

    return ""

def get_movie(id):
    movie = db.get_or_404(Movie, id)
    return movie

def check_image(image, save=False) -> str:
    if image is not None and image.filename is not None:
            if image.filename != "" and is_allowed_img(image.filename):
                filename = secure_filename(image.filename)
                
                if save:
                    filepath = os.path.join(current_app.instance_path, current_app.config["IMAGE_DIR"], filename)
                    image.save(filepath)

                return filename
    return ""

