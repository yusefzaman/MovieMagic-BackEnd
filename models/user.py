import uuid
from datetime import datetime
from models.db import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_digest = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow
    )
    reviews = db.relationship("Review", back_populates="user")

    def __init__(self, name, email, password, image=None, admin=False):
        self.name = name
        self.email = email
        self.password_digest = password
        self.image = image
        self.admin = admin

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "image": self.image,
            "admin": self.admin,
            "password_digest": self.password_digest,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id):
        user = cls.query.get(id)
        if user is None:
            return {"message": "no such user with this ID"}, 404
        return user, 200

    @classmethod
    def update_user(cls, id, data):
        user = cls.query.get(id)
        if user is None:
            return {
                "message": "there is no such user with such ID, so you can't update"
            }, 404
        for key in data.keys():
            setattr(user, key, data[key])
        db.session.commit()
        return user.json(), 200

    @classmethod
    def delete_user(cls, id):
        user = cls.query.get(id)
        if user is None:
            return {"message": "user with such ID is not found."}, 404
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 204

    def verify_password(self, password):
        return check_password_hash(self.password_digest, password)
