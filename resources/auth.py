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
        if not data or "email" not in data or "password" not in data:
            return {"message": "Invalid request, missing email or password"}, 400

        email = data["email"]
        password = data["password"]

        # Step 1: Print received login data
        print(f"Received login data: {data}")

        # Step 2: Query user by email
        user = User.query.filter_by(email=email).first()
        if not user:
            print("User not found.")
            return {"message": "Invalid credentials"}, 401

        # Step 3: Print user details if found
        print(f"User found: {user}")
        print(f"Stored password hash: {user.password_digest}")
        print(f"entered password: {password}")

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        print(f"entered hash password:{hashed_password}")

        # Step 4: Check if password matches
        password_matches = check_password_hash(user.password_digest, password)

        if not password_matches:
            print("Invalid password.")
            return {"message": "Invalid credentials"}, 401

        # Step 5: Password is correct, generate access token
        access_token = create_access_token(identity=user.id)
        print(f"Generated token: {access_token}")

        # Step 6: Return successful login response
        return {"access_token": access_token}, 200
