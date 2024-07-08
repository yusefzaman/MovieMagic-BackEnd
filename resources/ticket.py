from flask import Blueprint, request, jsonify
from models.ticket import Ticket, db
from flask_jwt_extended import jwt_required, get_jwt_identity

ticket_bp = Blueprint("ticket_bp", __name__)


@ticket_bp.route("/add_ticket", methods=["POST"])
@jwt_required()
def add_ticket():
    current_user_id = get_jwt_identity()  # Get the logged-in user's ID
    data = request.json
    id = data.get("id")
    user_id = current_user_id  # Use the logged-in user's ID
    movie_id = data.get("movie_id")
    showtime_id = data.get("showtime_id")

    if not (id and user_id and movie_id and showtime_id):
        return jsonify({"success": False, "message": "All fields are required"}), 400

    ticket = Ticket(id=id, user_id=user_id, movie_id=movie_id, showtime_id=showtime_id)

    db.session.add(ticket)
    db.session.commit()

    return jsonify({"success": True, "message": "Ticket added successfully"})


@ticket_bp.route("/get_tickets", methods=["GET"])
@jwt_required()
def get_tickets():
    current_user_id = get_jwt_identity()  # Get the logged-in user's ID
    tickets = Ticket.query.filter_by(
        user_id=current_user_id
    ).all()  # Get only the logged-in user's tickets
    tickets_data = [ticket.to_dict() for ticket in tickets]
    return jsonify(tickets_data)


@ticket_bp.route("/get_ticket/<ticket_id>", methods=["GET"])
@jwt_required()
def get_ticket(ticket_id):
    current_user_id = get_jwt_identity()  # Get the logged-in user's ID
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return jsonify({"success": False, "message": "Ticket not found"}), 404

    if ticket.user_id != current_user_id:
        return (
            jsonify(
                {"success": False, "message": "Unauthorized access to this ticket"}
            ),
            403,
        )

    return jsonify(ticket.to_dict())
