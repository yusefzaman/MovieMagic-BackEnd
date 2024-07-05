from flask import request, jsonify
from flask_restful import Resource
from models.review import Review
from models.db import db


class Reviews(Resource):
    def post(self):
        data = request.get_json()
        content = data.get("content")
        rating = data.get("rating")
        user_id = data.get("user_id")
        movie_id = data.get("movie_id")

        if not all([content, rating, user_id, movie_id]):
            return (
                jsonify({"message": "All fields are required for review creation"}),
                400,
            )

        new_review = Review(content, rating, user_id, movie_id)
        db.session.add(new_review)
        db.session.commit()

        return jsonify({"message": "Review created successfully"}), 201
