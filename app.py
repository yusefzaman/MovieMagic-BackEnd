from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate  # Import Flask-Migrate

from models.db import db  # Import database configuration
from resources.users import Users, UserDetails
from resources.auth import Register, Login
from resources.movie import movie_bp
from resources.reviews import Reviews, ReviewDetails
from resources.theatre import theatre_bp

app = Flask(__name__)
CORS(app)

# Configuration
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://hussain:admin@localhost:5432/magicinspector"
)

app.config["SQLALCHEMY_ECHO"] = True
app.config["JWT_SECRET_KEY"] = "your_jwt_secret_key"  # Change this in production

# Initialize Flask extensions
db.init_app(app)
jwt = JWTManager(app)

# Create Migrate instance
migrate = Migrate(app, db)  # Create the Migrate instance

# Initialize API
api = Api(app)

# API Routes
api.add_resource(Users, "/users")
api.add_resource(UserDetails, "/users/<uuid:id>")
api.add_resource(Register, "/register")
api.add_resource(Login, "/signin")
app.register_blueprint(theatre_bp, url_pref="")
app.register_blueprint(movie_bp, url_prefix="")
api.add_resource(Reviews, "/reviews")
api.add_resource(ReviewDetails, "/reviews/<string:review_id>")

if __name__ == "__main__":
    app.run(debug=True)
