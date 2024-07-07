from models.db import db
from datetime import datetime
from uuid import uuid4


class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.String(50), primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="reviews")

    movie_id = db.Column(db.String, db.ForeignKey("movies.id"), nullable=False)
    movie = db.relationship("Movie", back_populates="reviews")

    def __init__(self, content, rating, user_id, movie_id):
        self.content = content
        self.rating = rating
        self.user_id = user_id
        self.movie_id = movie_id

    def to_dict(self):
        return {
            "id": str(uuid.uuid4().hex),
            "content": self.content,
            "rating": self.rating,
            "created_at": str(self.created_at),
            "user": self.user.to_dict() if self.user else None,
            "movie": self.movie.to_dict() if self.movie else None,
        }
