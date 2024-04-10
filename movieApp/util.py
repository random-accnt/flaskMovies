from movieApp import ALLOWED_IMG_EXTENSIONS


def rowsToDict(rows):
    return [dict(zip(row.keys(), row)) for row in rows]


def rowToDict(row):
    return dict(zip(row.keys(), row))


def is_allowed_img(filename: str):
    return (
        "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMG_EXTENSIONS
    )


def parse_ratings(ratings: str) -> list[str]:
    if ratings is None:
        return []

    result = []
    for val in ratings.rsplit("^-"):
        result.append(val.strip())

    return result
