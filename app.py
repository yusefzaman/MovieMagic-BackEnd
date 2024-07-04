from flask import Flask
from flask_restful import Api
from models.db import db
from resources.users import Users, UserDetails

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hussain:admin@localhost:5432/'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

api = Api(app)

# Define the API routes
api.add_resource(Users, '/users')
api.add_resource(UserDetails, '/users/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
