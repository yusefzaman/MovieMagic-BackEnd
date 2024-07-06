from flask import Blueprint, request, jsonify
from models.showtime import Showtime, db
from datetime import datetime

showtime_bp = Blueprint('showtime_bp', __name__)

@showtime_bp.route('/add_showtime', methods=['POST'])
def add_showtime():
    data = request.json
    id = data.get('id')
    theatre_id = data.get('theatre_id')
    seats = data.get('seats')
    time = data.get('time')
    price = data.get('price')

    if not (id and theatre_id and time and price):
        return jsonify({'success': False, 'message': 'All fields are required'}), 400
    
    
    time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')
    
    
    showtime = Showtime(id=id, theatre_id=theatre_id, time=time, price=price)

    db.session.add(showtime)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Showtime added successfully'})

@showtime_bp.route('/get_showtimes', methods=['GET'])
def get_showtimes():
    showtimes = Showtime.query.all()
    showtimes_data = [showtime.to_dict() for showtime in showtimes]
    return jsonify(showtimes_data)

@showtime_bp.route('/get_showtime/<showtime_id>', methods=['GET'])
def get_showtime(showtime_id):
    showtime = Showtime.query.get(showtime_id)
    if not showtime:
        return jsonify({'success': False, 'message': 'Showtime not found'}), 404

    return jsonify(showtime.to_dict())

@showtime_bp.route('/reserve_seats/<showtime_id>', methods=['POST'])
def reserve_seats(showtime_id):
    showtime = Showtime.query.get(showtime_id)
    if not showtime:
        return jsonify({'success': False, 'message': 'Showtime not found'}), 404
    
    data = request.json
    seats_to_reserve = data.get('seats')

    if not seats_to_reserve:
        return jsonify({'success': False, 'message': 'No seats to reserve provided'}), 400
    

    if any(seat < 0 or seat >= 60 for seat in seats_to_reserve):
        return jsonify({'success': False, 'message': 'Seat index out of range'}), 400
    
    available_seats = showtime.seats


    for seat in seats_to_reserve:
        if available_seats[seat]:
            return jsonify({'success': False, 'message': f'Seat {seat} is already reserved'}), 400
        
    for seat in seats_to_reserve:
        available_seats[seat] = True

    return jsonify({'success': True, 'message': 'Seats reserved successfully'})    