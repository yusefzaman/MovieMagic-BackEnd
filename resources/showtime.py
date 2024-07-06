from app import db

class Showtime(db.Model):
    id = db.Column(db.String, primary_key=True)
    theatre_id = db.Column(db.String, db.ForeignKey('theatre.id'), nullable=False)
    seats = db.Column(db.PickleType, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, id, theatre_id, seats, time, price):
        self.id = id
        self.theatre_id = theatre_id
        self.seats = seats
        self.time = time
        self.price = price

    def to_dict(self):
        return {
            'id': self.id,
            'theatre_id': self.theatre_id,
            'seats': self.seats,
            'time': self.time,
            'price': self.price
        }    