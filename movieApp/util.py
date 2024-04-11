from sqlalchemy.event import contains

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
    current = []
    for line in ratings.splitlines():
        if len(line.strip()) == 0:
            continue

        if line.startswith("-"):
            if len(current) == 0:
                current.append(line[1:].strip())
            else:
                result.append("\n".join(current))
                current = [
                    line[1:].strip(),
                ]
        else:
            # skip wrong format
            if len(current) > 0:
                current.append(line.strip())

    if len(current) > 0:
        result.append("\n".join(current))

    return result
