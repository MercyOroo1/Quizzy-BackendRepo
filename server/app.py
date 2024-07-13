from flask import Flask, render_template, url_for, request, redirect, session, jsonify
from flask_migrate import Migrate
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt, create_access_token, get_jwt_identity, jwt_required, create_refresh_token
from datetime import timedelta
from models import User, db
from creator import creator_bp
from participant import participant_bp
from flask_bcrypt import Bcrypt
from flask_cors import CORS
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SECRET_KEY'] = 'ab1479e159f8b60fc6ade3e987a306'
api = Api(app)

app.register_blueprint(creator_bp)
app.register_blueprint(participant_bp)

jwt = JWTManager(app)
db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

CORS(app)

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).first()

# login

login_args = reqparse.RequestParser()
login_args.add_argument('email', required=True, help='Email cannot be blank')
login_args.add_argument('password', required=True, help='Password cannot be blank')

class Login(Resource):
    def post(self):
        data = login_args.parse_args()
        # check if the user exists
        user = User.query.filter_by(email=data.get('email')).first()
        if not user:
            return {"msg": "User does not exist"}, 404
        if not bcrypt.check_password_hash(user.password_hash, data.get('password')):
            return {"msg": "Password is incorrect!"}, 401
        # login
        token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return {"token": token, "refresh_token": refresh_token}, 200

    @jwt_required(refresh=True)
    def get(self):
        current_user_id = get_jwt_identity()
        token = create_access_token(identity=current_user_id)
        return {"token": token}, 200

class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        return {}, 204

class CheckSession(Resource):
    def get(self):
        if session.get('user_id'):
            user = User.query.filter(User.id == session['user_id']).first()
            return user.to_dict(), 200
        return {}, 204

# signup

signup_args = reqparse.RequestParser()
signup_args.add_argument('email', required=True, help='Email cannot be blank')
signup_args.add_argument('password', required=True, help='Password cannot be blank')
signup_args.add_argument('username', required=True, help='Username cannot be blank')

class Signup(Resource):
    def post(self):
        data = signup_args.parse_args()
        if User.query.filter_by(username=data.get('username')).first():
            return {'error': 'Username already exists'}, 422

        hashed_password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')
        new_user = User(email=data.get('email'), username=data.get('username'), password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return {"msg": 'User created successfully'}, 201
    
class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user_id)
        return {"token": new_access_token}, 200

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(TokenRefresh, '/token/refresh')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
