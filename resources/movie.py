import requests
from flask import Blueprint, request, jsonify
from models.movie import Movie, db
from models.theatre import Theatre

movie_bp = Blueprint("movie_bp", __name__)

API_URL = "https://api.themoviedb.org/3/discover/movie"
API_KEY = "abbef35f11cad16e5640f14b9057e4d1"

@movie_bp.route("/add_movie", methods=["POST"])  # for adding movies manualy
def add_movie():
    data = request.json
    id = data.get("id")
    name = data.get("name")
    img = data.get("img")
    genre = data.get("genre")
    theatre_id = data.get("theatre_id")

    if not (id and name and img and genre and theatre_id):
        return jsonify({"success": False, "message": "All fields are required"}), 400

    theatre = Theatre.query.get(theatre_id)
    if not theatre:
        return jsonify({"success": False, "message": "Invalid theatre ID"}), 400

    movie = Movie(id=id, name=name, img=img, genre=genre, theatre_id=theatre_id)

    db.session.add(movie)
    db.session.commit()

    return jsonify({"success": True, "message": "Movie added successfully"})


@movie_bp.route(
    "/fetch_movies", methods=["POST"]
)  # for adding movies from the api to the database
def fetch_and_add_movies():
    data = request.json
    page_number = data.get("page_number", 1)  # Default to page 1 if not provided

    response = requests.get(API_URL, params={"api_key": API_KEY, "page": page_number})

    if response.status_code != 200:
        return (
            jsonify(
                {"success": False, "message": "Failed to fetch data from external API"}
            ),
            response.status_code,
        )

    movies_data = response.json().get("results", [])

    for movie_data in movies_data:
        id = str(movie_data.get("id"))
        name = movie_data.get("title")
        img = f"https://image.tmdb.org/t/p/w500{movie_data.get('poster_path')}"
        # genre = ", ".join([genre["name"] for genre in movie_data.get("genre_ids", [])])
        theatre_id = None

        existing_movie = Movie.query.filter_by(id=id).first()
        if existing_movie:
            continue

        # Create a new Movie object and add it to the database
        movie = Movie(id=id, name=name, img=img, genre="Comedy", theatre_id=theatre_id)
        db.session.add(movie)

    db.session.commit()  # to prevent unexcepted behaviour

    return jsonify(
        {
            "success": True,
            "message": "Movies fetched from TMDb API and added successfully",
        }
    )


@movie_bp.route("/movies", methods=["GET"])
def get_movies():
    movies = Movie.query.all()
    movies_data = [movie.to_dict() for movie in movies]
    return jsonify(movies_data)


@movie_bp.route("/movies_by_theatre/<string:theatre_id>", methods=["GET"])
def get_movies_by_theatre(theatre_id):
    movies = Movie.query.filter_by(theatre_id=theatre_id).all()
    movies_data = [movie.to_dict() for movie in movies]
    return jsonify(movies_data)
