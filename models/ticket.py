from app import db

class Ticket(db.Model):
    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.String, db.ForeignKey('movie.id'), nullable=False)
    showtime_id = db.Column(db.String, db.ForeignKey('showtime.id'), nullable=False)

    def __init__(self, id, user_id, movie_id, showtime_id):
        self.id = id
        self.user_id = user_id
        self.movie_id = movie_id
        self.showtime_id = showtime_id

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'movie_id': self.movie_id,
            'showtime_id': self.showtime_id
        }
