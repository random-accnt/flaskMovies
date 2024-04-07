import sqlite3
from datetime import datetime
from typing import Optional

from flask import current_app, g
from sqlalchemy import ForeignKey, func, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from movieApp import db


class Movie(db.Model):
    __tablename__ = "movie_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str]
    rating: Mapped[Optional[int]]
    createdAt: Mapped[datetime] = mapped_column(default=func.current_timestamp())
    id_image: Mapped[int] = mapped_column(ForeignKey("image_table.id"))
    image: Mapped["Image"] = relationship()


class Image(db.Model):
    __tablename__ = "image_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(nullable=False)


def get_default_image_id():
    if "default_image" not in g:
        result = db.session.execute(
            select(Image.id).where(
                Image.filename == current_app.config["DEFAULT_IMAGE"]
            )
        ).one_or_none()
        if result is None:
            # WARNING: less than ideal "solution"
            print("NO DEFAULT IMAGE IN DB")
        else:
            g.default_image = result[0]

    return g.default_image
