import requests
from flask import Blueprint, request, jsonify
from models.theatre import Theatre, db
import json

theatre_bp = Blueprint("theatre_bp", __name__)
API_URL = "https://serpapi.com/search.json"
API_KEY = "3327939e08bff45a40f8eb2b50929cb5e52bdb33f459ec166f552f6bf9f62705"
payload={"api_key":API_KEY,"q":"bad+boys+theater","location":"Austin,+Texas,+United+States","hl":"en","gl":"us"}

@theatre_bp.route("/add_theatre", methods=["POST"])
def add_theatre():
    data = request.json
    name = data.get("name")
    location = data.get("location")
    day = data.get("day")
    time = data.get("time")
    if not (id and name):
        return jsonify({"success": False, "message": "ID and Name are required"}), 400

    theatre = Theatre(name=name, location=location, time=time, day=day)

    db.session.add(theatre)
    db.session.commit()

    return jsonify({"success": True, "message": "Theatre added successfully", "id": theatre.id})

@theatre_bp.route(
    "/fetch_theatres", methods=["GET"]
)  # for adding theatres from the api to the database
def fetch_and_add_theatres():
    # data = request.json
    response = requests.get(API_URL, params=payload)
    if response.status_code != 200:
        return (
            jsonify(
                {"success": False, "message": "Failed to fetch data from external API"}
            ),
            response.status_code,
        )

    print(response.json())
    print("=======================================")
    theatres_data = response.json().get("showtimes", [])[0].get("theaters", [])
    print( json.dumps(theatres_data, indent=4) )
    for theatre_data in theatres_data:
        name = theatre_data.get("name")
        location = theatre_data.get("address")
        time = theatre_data.get("showing")[0].get("time", [])
        existing_theatre = Theatre.query.filter_by(name=name).first()
       
        if existing_theatre:
            print("Theatre exists!")
            continue

        # Create a new theatre object and add it to the database
        print("Creating theatre...")
        theatre = Theatre(name=name, location=location, time=time)
        db.session.add(theatre)
        db.session.commit()
        # to prevent unexcepted behaviour

    return jsonify(
        {
            "success": True,
            "message": "theatres fetched from TMDb API and added successfully",
        }
    )


@theatre_bp.route("/theatres", methods=["GET"])
def get_theatres():
    theatres = Theatre.query.all()
    theatres_data = [theatre.to_dict() for theatre in theatres]
    return jsonify(theatres_data)


@theatre_bp.route("/theatr", methods=["GET"])
def get_theatre(theatre_id):
    theatre = Theatre.query.get(theatre_id)
    if not theatre:
        return jsonify({"success": False, "message": "Theatre not found"}), 404

    return jsonify(theatre.to_dict())
