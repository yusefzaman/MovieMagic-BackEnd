from flask import request
from flask_restful import Resource
from models.user import User
from models.db import db

# Class and def
class Users(Resource):
    def get(self):
        users = User.find_all()  # Get all the information from the user table
        return [u.json() for u in users], 200  # Return the users as JSON

    def post(self):
        data = request.get_json()  # Return the requested data as JSON
        user = User(**data)  # Create a user instance using the provided data
        user.create()  # save class instance of user in the database
        return user.json(), 201

class UserDetails(Resource):
    def get(self, id):
        user, status = User.find_by_id(id)  # Find the user by ID
        if status == 404:
            return user, status
        return user.json(), 200

    def put(self, id):
        user, status = User.find_by_id(id)  # Find the user by ID
        if status == 404:
            return user, status
        data = request.get_json()  # Get the data as JSON
        for key in data.keys():
            setattr(user, key, data[key])
        db.session.commit()  # Save the updated user
        return user.json(), 200

    def delete(self, id):
        user, status = User.find_by_id(id)  # Find the user by ID
        if status == 404:
            return user, status
        db.session.delete(user)  # Delete the user from the database
        db.session.commit()  # Commit the changes
        return {"message": "User deleted"}, 204
