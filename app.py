# app.py
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from models.db import db
from resources.users import Users, UserDetails
from resources.auth import Register, Login
from resources.movie import movie_bp

app = Flask(__name__)

# Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://hussain:admin@localhost:5432/magicinspector"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "your_jwt_secret_key"  # Change this in production

# Initialize Flask extensions
db.init_app(app)
jwt = JWTManager(app)

# Create database tables
with app.app_context():
    db.create_all()

# Initialize API
api = Api(app)

# API Routes
api.add_resource(Users, "/users")
api.add_resource(UserDetails, "/users/<uuid:id>")
api.add_resource(Register, "/register")
api.add_resource(Login, "/login")
app.register_blueprint(movie_bp, url_prefix="/movies")

if __name__ == "__main__":
    app.run(debug=True)
