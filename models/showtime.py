from flask import Blueprint, request, jsonify
from models.showtime import Showtime, db


showtime_bp = Blueprint('showtime_bp', __name__)