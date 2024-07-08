from flask_sqlalchemy import SQLAlchemy
from models.db import db


class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    img = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    theatre_id = db.Column(db.PickleType, nullable=True)
    reviews = db.relationship(
        "Review", back_populates="movie", cascade="all, delete-orphan"
    )

    def __init__(self, id, name, img, genre, theatre_id):
        self.id = id
        self.name = name
        self.img = img
        self.genre = genre
        self.theatre_id = theatre_id

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "img": self.img,
            "genre": self.genre,
            "theatre_id": self.theatre_id,
        }
