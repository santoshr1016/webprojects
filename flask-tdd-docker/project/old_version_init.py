# from flask import Flask, jsonify
# from flask_restplus import Resource, Api
# import os
# import sys
# from flask_sqlalchemy import SQLAlchemy
#
#
# # instantiate the app
# app = Flask(__name__)
# api = Api(app)
#
# # set config
# app_settings = os.getenv('APP_SETTINGS')
# app.config.from_object(app_settings)
# # print(app.config, file=sys.stderr)
#
# # instantiate db
# db = SQLAlchemy(app)
#
#
# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     username = db.Column(db.String(128), nullable=False)
#     email = db.Column(db.String(123), nullable=False)
#     active = db.Column(db.Boolean(), default=True, nullable=False)
#
#     def __init__(self, un, em):
#         self.username = un
#         self.email = em
#
#
# class Ping(Resource):
#     def get(self):
#         return {
#             'status': 'success',
#             'message': 'pong!'
#         }
#
#
# api.add_resource(Ping, '/ping')
