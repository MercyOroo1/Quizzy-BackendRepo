from flask import Blueprint, jsonify, make_response
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import current_user, jwt_required
from models import db, Response,User

response_bp = Blueprint('response_bp', __name__, url_prefix='/users')
response_api = Api(response_bp)


response_parser = reqparse.RequestParser()
response_parser.add_argument('response', type=str, required=True, help='A response is required')


class ResponseList(Resource):
    
    def post(self):
        data = response_parser.parse_args()
        new_response = Response (
            response = data['response']
        )
        db.session.add(new_response)
        db.session.commit()
        return {'msg': 'user created successfully'}
    
response_api.add_resource(ResponseList, "/responses")
    



















        



       
