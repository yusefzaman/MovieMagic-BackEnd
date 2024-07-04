from flask import Blueprint, request, jsonify
from models.movie import Movie, db
# from models.theatre import Theatre

movie_bp = Blueprint('movie_bp', __name__)

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

    theatre = theatre.query.get(theatre_id)
    if not theatre:
        return jsonify({'success': False, 'message': 'Invalid theatre ID'}), 400
    
    movie = Movie(id=id, name=name, img=img, genre=genre, theatre_id=theatre_id)
    
    db.session.add(movie)
    db.session.commit()


    return jsonify({'success': True, 'message': 'Movie added successfully'})

# @movie_bp.route('/fetch_and_add_movie/<external_movie_id>', methods=['POST'])
# def fetch_and_add_movie(external_movie_id):
#     response = requests.get(f"{###}/{external_movie_id}")





