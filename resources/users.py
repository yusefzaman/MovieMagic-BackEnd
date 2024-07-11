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

    @jwt_required()
    def put(self, id):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        if not current_user.admin:
            return {"message": "Unauthorized to perform this action"}, 403

        user, status = User.find_by_id(id)
        if status == 404:
            return user, status

        data = request.get_json()
        if "admin" in data:
            user.admin = data["admin"]
            db.session.commit()

        return user.json(), 200


class UserDetails(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user, status = User.find_by_id(current_user_id)
        return user.json(), status

    @jwt_required()
    def put(self, email):
        current_user_id = get_jwt_identity()

        # Find user by email
        user = User.find_by_email(email)
        if not user:
            return {"message": "User not found"}, 404

        # Check if the current user is authorized to update
        if str(current_user_id) != str(user.id):
            return {"message": "Unauthorized to update this user"}, 403

        try:
            # Update admin status to True
            user.admin = True
            user.save()  # Assuming you have a method like save() to commit changes

            return {"message": "Admin status updated successfully"}, 200
        except Exception as e:
            return {"message": f"Failed to update admin status: {str(e)}"}, 500

    @jwt_required()
    def delete(self, id):
        current_user_id = get_jwt_identity()
        if str(current_user_id) != id:
            return {"message": "Unauthorized to delete this user"}, 403

        user, status = User.find_by_id(id)
        if status == 404:
            return user, status
        return User.delete_user(id)


class MakeAdmin(Resource):
    @jwt_required()
    def put(self, email):
        current_user_id = get_jwt_identity()

        # Find user by email
        user = User.query.filter_by(email=email).first()
        if not user:
            return {"message": "User not found"}, 404

        # Check if the current user is authorized to update
        if str(current_user_id) != str(user.id):
            return {"message": "Unauthorized to update this user"}, 403

        try:
            # Update admin status to True
            user.admin = True
            user.save()

            return {"message": "Admin status updated successfully"}, 200
        except Exception as e:
            return {"message": f"Failed to update admin status: {str(e)}"}, 500
