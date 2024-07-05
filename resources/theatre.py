from flask import Blueprint, request, jsonify
from models.theatre import Theatre, db

theatre_bp = Blueprint("theatre_bp", __name__)


@theatre_bp.route("/add_theatre", methods=["POST"])
def add_theatre():
    data = request.json
    id = data.get("id")
    name = data.get("name")

    if not (id and name):
        return jsonify({"success": False, "message": "ID and Name are required"}), 400

    theatre = Theatre(id=id, name=name)

    db.session.add(theatre)
    db.session.commit()

    return jsonify({"success": True, "message": "Theatre added successfully"})


@theatre_bp.route("", methods=["GET"])
def get_theatres():
    theatres = Theatre.query.all()
    theatres_data = [theatre.to_dict() for theatre in theatres]
    return jsonify(theatres_data)


@theatre_bp.route("", methods=["GET"])
def get_theatre(theatre_id):
    theatre = Theatre.query.get(theatre_id)
    if not theatre:
        return jsonify({"success": False, "message": "Theatre not found"}), 404

    return jsonify(theatre.to_dict())
