from models.db import db

class Theatre(db.Model):
    __tablename__ = 'theatres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    time = db.Column(db.String(80), nullable=False)

    def __init__(self, name, location, time):
        self.name = name
        self.location = location
        self.time = time

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "time": self.time
        }
