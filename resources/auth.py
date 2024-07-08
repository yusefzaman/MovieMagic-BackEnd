# resources/auth.py
from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required
from models.user import User
from models.db import db
from werkzeug.security import generate_password_hash, check_password_hash


class Register(Resource):
    def post(self):
        data = request.get_json()
        hashed_password = generate_password_hash(
            data["password"], method="pbkdf2:sha256"
        )
        new_user = User(
            name=data["name"], email=data["email"], password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created successfully"}, 201


class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data["email"]).first()
        if not user or not check_password_hash(user.password_digest, data["password"]):
            return {"message": "Invalid credentials"}, 401

        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}, 200
