from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Movie(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    img = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    theatre_ids = db.Column(db.PickleType, nullable=False)


