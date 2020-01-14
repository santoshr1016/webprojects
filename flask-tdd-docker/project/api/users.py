from flask import Blueprint, request
from flask_restplus import Api, Resource, fields

from project import db
from project.api.models import User

# from sqlalchemy import exc

users_blueprint = Blueprint("users", __name__)
api = Api(users_blueprint)

user = api.model(
    "User",
    {
        "id": fields.Integer(readOnly=True),
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "created_date": fields.DateTime,
    },
)


class UsersList(Resource):
    @api.expect(user, validate=True)
    def post(self):
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")
        response_object = {}
        user = User.query.filter_by(email=email).first()
        if user:
            response_object["message"] = "Sorry. That email already exists."
            return response_object, 400
        db.session.add(User(username=username, email=email))
        db.session.commit()
        response_object = {"message": f"{email} was added!"}

        return response_object, 201

    @api.marshal_with(user, as_list=True)
    def get(self):
        return User.query.all(), 200


class Users(Resource):
    @api.marshal_with(user)
    def get(self, user_id):
        user_got = User.query.filter_by(id=user_id).first()

        if not user_got:
            api.abort(404, f"User {user_id} does not exist")
        return user_got, 200

    def delete(self, user_id):
        response_object = {}
        user_got = User.query.filter_by(id=user_id).first()

        if not user_got:
            api.abort(404, f"User {user_id} does not exist")
        db.session.delete(user_got)
        db.session.commit()
        response_object["message"] = f"{user_got.email} was removed!"
        return response_object, 200

    @api.expect(user, validate=True)
    def put(self, user_id):
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")
        response_object = {}

        user = User.query.filter_by(id=user_id).first()
        if not user:
            api.abort(404, f"User {user_id} does not exist")
        user.username = username
        user.email = email
        db.session.commit()
        response_object["message"] = f"{user.id} was updated!"
        return response_object, 200


api.add_resource(UsersList, "/users")
api.add_resource(Users, "/users/<int:user_id>")
