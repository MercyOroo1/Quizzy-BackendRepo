from flask import Blueprint,jsonify
from flask_jwt_extended import jwt_required, current_user
from models import db, Quiz, Question, Response,Review
from flask_restful import Api, Resource, reqparse
# from auth import allow

participant_bp = Blueprint('participant_bp',__name__, url_prefix='/participant')

participant_api = Api(participant_bp)
response_args = reqparse.RequestParser()
response_args.add_argument('response', type=str, required=True, help='A response is required')
response_args.add_argument('question_id', type=str, required=True, help='Question id is required')
response_args.add_argument('user_id', type=str, required=True, help='User id is required')



class Responses(Resource):
    def post(self):
        # participant creates a response to a particular question
        data = response_args.parse_args()
        response = data['response']
        question_id = data['question_id']
        user_id = data['user_id']

        # (will be replaced with current_user)

        question = Question.query.filter_by(id = question_id).first()
        if not question: 
            return {'msg': 'question not found'}
        quiz_id = question.quiz_id
        
        new_response = Response(response= response,question_id = question_id,user_id = user_id, quiz_id = quiz_id )

        db.session.add(new_response)
        db.session.commit()
        # checks whether the response provided matches the answer in the questions table
        is_correct = (new_response.response.strip().lower() == question.answer.strip().lower())  
        return jsonify({
            'id': new_response.id,
            'response': new_response.response,
            'question_id':new_response.question_id,
            # (question id should be equal to id of the question that is fetched)
             'question': question.text,
             'is_correct': is_correct,
             'quiz_id': question.quiz_id

        



        },201)
    

review_args = reqparse.RequestParser()
review_args.add_argument('rating', type=int, required=True, help='A rating is required')
review_args.add_argument('review_text', type=str, required=True, help='review text is required')
review_args.add_argument('quiz_id', type=str, required=True, help='Quiz id is required')
review_args.add_argument('user_id', type=str, required=True, help='User id is required')
# will be replaced with current user 
class Reviews(Resource):
    #   participant creates a review of a particular quiz
      def post(self):
           data = review_args.parse_args()
           quiz_id = data['quiz_id']
           quiz = Quiz.query.filter_by(id = quiz_id).first()
           if not quiz:
                return {'msg': "quiz not found"}
           
           new_review = Review(rating = data['rating'],review_text = data['review_text'], quiz_id = quiz_id, user_id = data['user_id'])
           
           db.session.add(new_review)
           db.session.commit()

           return jsonify({
                'id': new_review.id,
                "review_text": new_review.review_text,
                "rating": new_review.rating,
                "quiz": quiz.title,
                "user_id": new_review.user_id
           }, 201)
participant_api.add_resource(Responses,'/responses')
participant_api.add_resource(Reviews,'/reviews')
