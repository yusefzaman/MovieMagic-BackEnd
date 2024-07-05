from flask import Blueprint, request, jsonify
from models.ticket import Ticket, db

ticket_bp = Blueprint('ticket_bp', __name__)

@ticket_bp.route('/add_ticket', methods=['POST'])
def add_ticket():
    data = request.json
    id = data.get('id')
    user_id = data.get('user_id')
    movie_id = data.get('movie_id')
    showtime_id = data.get('showtime_id')
    