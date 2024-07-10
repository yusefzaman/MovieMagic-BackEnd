from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.db import db


class Users(Resource):
    @jwt_required()
    def get(self):
        users = User.find_all()
        return [u.json() for u in users], 200

    @jwt_required()
    def post(self):
        data = request.get_json()
        user = User(**data)
        user.create()
        return user.json(), 201


class UserDetails(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user, status = User.find_by_id(current_user_id)
        return user.json(), status

    @jwt_required()
    def put(self, id):
        current_user_id = get_jwt_identity()
        if str(current_user_id) != id:
            return {"message": "Unauthorized to update this user"}, 403

        data = request.get_json()
        user, status = User.find_by_id(id)
        if status == 404:
            return user, status
        user, status = User.update_user(id, data)
        return user, status

    @jwt_required()
    def delete(self, id):
        current_user_id = get_jwt_identity()
        if str(current_user_id) != id:
            return {"message": "Unauthorized to delete this user"}, 403

        user, status = User.find_by_id(id)
        if status == 404:
            return user, status
        return User.delete_user(id)
