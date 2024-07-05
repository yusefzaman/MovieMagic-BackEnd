from db import db
from datetime import datetime
from models.user import User
from models.movie import Movie


class Review(db.Model):
    id = db.Column(db.String, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="reviews")

    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"), nullable=False)
    movie = db.relationship("Movie", back_populates="reviews")

    def __init__(self, content, rating, user_id, movie_id):
        self.content = content
        self.rating = rating
        self.user_id = user_id
        self.movie_id = movie_id
