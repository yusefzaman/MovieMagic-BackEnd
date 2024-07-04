from flask import request
from flask_restful import Resource
from models.user import User
from models.db import db

#Class and def
class Users(Resource):
    def get(self):
        users=User.find_all() #get all the information from the user table
        return [u.json() for u in users]# return the user as json
    def post(self):
        data=request.get_json()#return thre requested data as json
        user=User(**data)#like the spreed operator since we will increase the number of elments
        user.create()#create the user instance in the database
        return user.json(),201
class UserDetails(Resource):
    def get(self,user_id):
        pass
  
        