from flask import Blueprint, request, jsonify
from models.movie import Movie, db
from models.theatre import Theatre


movie_bp = Blueprint('movie_bp', __name__)

API_URL = ""  

@movie_bp.route('/add_movie', methods=['POST'])
def add_movie():
    data = request.json
    id = data.get('id')
    name = data.get('name')
    img = data.get('img')
    genre = data.get('genre')
    theatre_id = data.get('theatre_id')

    if not (id and name and img and genre and theatre_id):
        return jsonify({'success': False, 'message': 'All fields are required'}), 400

    theatre = Theatre.query.get(theatre_id)
    if not theatre:
        return jsonify({'success': False, 'message': 'Invalid theatre ID'}), 400

    movie = Movie(id=id, name=name, img=img, genre=genre, theatre_id=theatre_id)
    
    db.session.add(movie)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Movie added successfully'})

@movie_bp.route('', methods=['POST'])
def fetch_and_add_movie(external_movie_id):
    
    response = request.get(f"{API_URL}/{external_movie_id}")
    
    if response.status_code != 200:
        return jsonify({'success': False, 'message': 'Failed to fetch data from external API'}), response.status_code

    movie_data = response.json()
    
    id = movie_data.get('id')
    name = movie_data.get('name')
    img = movie_data.get('img')
    genre = movie_data.get('genre')
    theatre_id = request.json.get('theatre_id')

    if not theatre_id:
        return jsonify({'success': False, 'message': 'Theatre ID is required'}), 400

    theatre = Theatre.query.get(theatre_id)
    if not theatre:
        return jsonify({'success': False, 'message': 'Invalid theatre ID'}), 400

    movie = Movie(id=id, name=name, img=img, genre=genre, theatre_id=theatre_id)
    
    db.session.add(movie)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Movie fetched from external API and added successfully'})

@movie_bp.route('', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    movies_data = [movie.to_dict() for movie in movies]
    return jsonify(movies_data)

@movie_bp.route('', methods=['GET'])
def get_movies_by_theatre(theatre_id):
    movies = Movie.query.filter_by(theatre_id=theatre_id).all()
    movies_data = [movie.to_dict() for movie in movies]
    return jsonify(movies_data)






