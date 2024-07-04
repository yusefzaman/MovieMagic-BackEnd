from flask import request
from flask_restful import Resource
from models.user import User
from models.db import db

class Users(Resource):
    def get(self):
        users = User.find_all()
        return [u.json() for u in users], 200

    def post(self):
        data = request.get_json()
        user = User(**data)
        user.create()
        return user.json(), 201

class UserDetails(Resource):
    def get(self, id):
        user, status = User.find_by_id(id)
        return user, status

    def put(self, id):
        data = request.get_json()
        user, status = User.find_by_id(id)
        if status == 404:
            return user, status
        user, status = User.update_user(id, data)
        return user, status

    def delete(self, id):
        user, status = User.find_by_id(id)
        if status == 404:
            return user, status
        return User.delete_user(id)
