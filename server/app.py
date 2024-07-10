from flask import  Flask, render_template, url_for, request, redirect, session
from flask_migrate import Migrate
from flask_restful import Resource, Api

from datetime import timedelta

from models import User, db
from creator import creator_bp
from participant import participant_bp
# from response import response_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///quiz.db'
app.config['SECRET_KEY'] ='ab1479e159f8b60fc6ade3e987a306'
api = Api(app)

app.register_blueprint(creator_bp)
app.register_blueprint(participant_bp)



db.init_app(app)




migrate = Migrate(app=app, db=db)

class Login(Resource):
    def post(self):
        all_requests = request.get_json()

        username = all_requests['username']
        password = all_requests['password']

        user = User.query.filter_by(username=username).first()

        if user and user.authenticate(password):
            session['user_id'] = user.id
            return user.to_dict(), 200
        else:
            return {'message': 'Invalid username or password'}, 401
        
class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        return {}, 204
    pass

class CheckSession(Resource):
    def get(self):
        if session.get('user_id'):
            user = User.query.filter(User.id == session['user_id']).first()
            return user.to_dict(), 200
        return {}, 204
    
class Signup(Resource):
    def post(self):

        username = request.get_json()['username']
        password = request.get_json()['password']
        
        if username and password:
            user = User(username=username)
            user.password_hash = password
            db.session.add(user)
            db.session.commit()

            session['user_id'] = user.id

            return user.to_dict(), 201
        
        return {'message': 'Username or password missing'}, 422
    
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')


if __name__ == '__main__':
    app.run(port=5555, debug=True)












