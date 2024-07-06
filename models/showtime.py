from flask import Blueprint, request, jsonify
from models.showtime import Showtime, db


showtime_bp = Blueprint('showtime_bp', __name__)

@showtime_bp.route('/add_showtime', methods=['POST'])
def add_showtime():
    data = request.json
    id = data.get('id')
    theatre_id = data.get('theatre_id')
    seats = data.get('seats')
    time = data.get('time')
    price = data.get('price')

    if not (id and theatre_id and seats and time and price):
        return jsonify({'success': False, 'message': 'All fields are required'}), 400
    showtime = Showtime(id=id, theatre_id=theatre_id, seats=seats, time=time, price=price)

    db.session.add(showtime)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Showtime added successfully'})
