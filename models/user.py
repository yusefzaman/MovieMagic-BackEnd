from datetime import datetime
from flask import request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_digest = db.Column(db.String(255), nullable=False)  # Store the hashed password
    image = db.Column(db.String(255), nullable=True)  # URL or path to the user's image
    admin = db.Column(db.Boolean, default=False, nullable=False)  # boolean to track the type of the user
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

    def __init__(self, name, email, password, image=None, admin=False):
        self.name = name
        self.email = email
        self.password_digest = generate_password_hash(password)#hash the password
        self.image = image
        self.admin = admin

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "image": self.image,
            "admin": self.admin,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    @classmethod
    def find_all(cls):
        return User.query.all()

    @classmethod
    def find_by_id(cls, id):
        user = User.query.get(id)
        if user is None:
            return {"message":"there is no user with such ID"}, 404
        return user

    @classmethod
    def update_user(cls, id):
        user = User.query.get(id)
        if user is None:
            return {"message":"cannot update user with such ID, becuase its undefiend."}, 404
        data = request.get_json()
        user.email = data.get('email', user.email)
        user.name = data.get('name', user.name)
        if 'password' in data:
            user.password_digest = generate_password_hash(data['password'])
        user.image = data.get('image', user.image)
        user.admin = data.get('admin', user.admin)
        db.session.commit()
        return user.json()

    @classmethod
    def delete_user(cls, id):
        user = User.query.get(id)
        if user is None:
            return {"message": f"User with id {id} not found"}, 404
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User Deleted'}, 204
    
    def verify_password(self, password):
        return check_password_hash(self.password_digest, password)

  