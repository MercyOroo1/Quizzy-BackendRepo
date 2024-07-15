from flask import Blueprint,jsonify
from flask_jwt_extended import jwt_required, current_user
from models import db, Quiz, Question, Response,Review
from flask_restful import Api, Resource, reqparse
from auth import allow

participant_bp = Blueprint('participant_bp',__name__, url_prefix='/participant')

participant_api = Api(participant_bp)
response_args = reqparse.RequestParser()
response_args.add_argument('response', type=str, required=True, help='A response is required')
response_args.add_argument('question_id', type=str, required=True, help='Question id is required')
# response_args.add_argument('user_id', type=str, required=True, help='User id is required')



class Responses(Resource):
    @jwt_required()
    # user has to be logged in 
    def post(self):
        # participant creates a response to a particular 
        
        data = response_args.parse_args()
        response = data['response']
        question_id = data['question_id']
        user_id = current_user.id

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
             'quiz_id': question.quiz_id,
             'user_id': current_user.id

        



        },201)
    

review_args = reqparse.RequestParser()
review_args.add_argument('rating', type=int, required=True, help='A rating is required')
review_args.add_argument('review_text', type=str, required=True, help='review text is required')
review_args.add_argument('quiz_id', type=str, required=True, help='Quiz id is required')
# review_args.add_argument('user_id', type=str, required=True, help='User id is required')
# will be replaced with current user 
class Reviews(Resource):
    #   participant creates a review of a particular quiz
      @jwt_required()
      def post(self):
           data = review_args.parse_args()
           quiz_id = data['quiz_id']
           quiz = Quiz.query.filter_by(id = quiz_id).first()
           if not quiz:
                return {'msg': "quiz not found"}
           
           new_review = Review(rating = data['rating'],review_text = data['review_text'], quiz_id = quiz_id, user_id = current_user.id)
           
           db.session.add(new_review)
           db.session.commit()

           return jsonify({
                'id': new_review.id,
                "review_text": new_review.review_text,
                "rating": new_review.rating,
                "quiz": quiz.title,
                "user_id": current_user.id,
                "created_at": new_review.created_at
           }, 201)
      
      def get(self):
           reviews = Review.query.all()
           if not reviews:
                return {"msg": "No reviews found"}, 404
           return jsonify ([{
                'id': review.id,
                'rating': review.rating,
                'review_text': review.review_text,
                'quiz_id': review.quiz_id,
                'user_id': review.user_id,
                'created_at': review.created_at,
                'user': {'id': review.user_id, 'username': review.user.username}
                } for review in reviews], 200)
class Quizzes(Resource):  
#  @jwt_required()
 
 def get(self):
        # gets all quizzes with related questions
          quizzes = Quiz.query.all()
          if not quizzes:
               return {"msg": "No quizzes found"}, 404
         
         
          return jsonify ([{
                'id':quiz.id,
                'title':quiz.title,
                'description': quiz.description,
                'created_at': quiz.created_at,
                'updated_at': quiz.updated_at,
                'image-url': quiz.image_url,
                'questions':[{'question_id':q.id,'question_text':q.text, 'choice_1': q.choice_1,'choice_2': q.choice_2,'choice_3': q.choice_3,'choice_4': q.choice_4} for q in quiz.questions],
                'reviews': [{'review_id':r.id,'rating':r.rating, 'review_text': r.review_text,'user_id': r.user_id} for r in quiz.reviews],
          }for quiz in quizzes],200)
 
class QuizzesById(Resource):
     # @jwt_required()
    # gets quiz by id and displays questions 
     def get(self,id):
         quiz = Quiz.query.get(id)
         if not quiz:
             return {"msg": "quiz not found"}
         return jsonify({
                'id':quiz.id,
                'title':quiz.title,
                'description': quiz.description,
                'created_at': quiz.created_at,
                'updated_at': quiz.updated_at,
                'questions':[{'question_id': q.id,'question_text':q.text, 'choice_1': q.choice_1,'choice_2': q.choice_2,'choice_3': q.choice_3,'choice_4': q.choice_4, 'answer':q.answer} for q in quiz.questions],
                'reviews':[{'review_id':r.id,'rating':r.rating, 'review_text': r.review_text,'user_id': r.user_id} for r in quiz.reviews]

         })
class QuizQuestions(Resource):
     @jwt_required()
     def get(self,id):
          quiz = Quiz.query.get(id)
          if not quiz:
               return {'Quiz not found'}
          questions = Question.query.filter_by(quiz_id = quiz.id).all()
          if not questions: 
               return {"Quiz has no questions"}

          return  jsonify ([{
            "question_text": question.text,
            "choice_1": question.choice_1,
            "choice_2": question.choice_2,
            "choice_3":question.choice_3,
            "choice_4":question.choice_4,

          
          }for question in questions])
participant_api.add_resource(Responses,'/responses')
participant_api.add_resource(Reviews,'/reviews')
participant_api.add_resource(Quizzes,'/quizzes')
participant_api.add_resource(QuizzesById,'/quizzes/<int:id>')
participant_api.add_resource(QuizQuestions,'/quizzes/<int:id>/questions')

