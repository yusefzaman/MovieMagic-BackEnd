from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Movie(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    img = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    theatre_ids = db.Column(db.PickleType, nullable=False)

    def __init__(self, id, name, img, genre, theatre_ids):
        self.id = id
        self.name = name
        self.img = img
        self.genre = genre
        self.theatre_ids = theatre_ids

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'img': self.img,
            'genre': self.genre,
            'theatre_ids': self.theatre_ids
        }
