from flask import Blueprint,jsonify
from flask_jwt_extended import jwt_required, current_user
from models import db, Quiz, Question,Response,Review
from flask_restful import Api, Resource, reqparse
from auth import allow

creator_bp = Blueprint('creator_bp',__name__, url_prefix='/creator')

creator_api = Api(creator_bp)

quiz_args = reqparse.RequestParser()
quiz_args.add_argument('title', type=str, required=True, help='quiz name is required')
quiz_args.add_argument('description', type=str, required=True, help='quiz description is required')


class Quizzes(Resource):
    # creates a quiz with no questions
    @jwt_required()
    @allow('Admin')
    def post(self):
        data = quiz_args.parse_args()
        new_quiz = Quiz(
            title=data['title'],
            description=data['description']
        )
        db.session.add(new_quiz)
        db.session.commit()

        return jsonify({
        'id':new_quiz.id,
        'title': new_quiz.title,
        'description': new_quiz.description,
        'created_at': new_quiz.created_at,
        'updated_at': new_quiz.updated_at
    })
    @jwt_required()
    @allow('Admin')    
    def get(self):
          
        # gets all quizzes with related questions and answers
          quizzes = Quiz.query.all()
          if not quizzes:
               return {"msg": "No quizzes found"}
         
         
          return jsonify ([{
                'id':quiz.id,
                'title':quiz.title,
                'description': quiz.description,
                'created_at': quiz.created_at,
                'updated_at': quiz.updated_at,
                'questions':[{'question_id':q.id,'question_text':q.text, 'choice_1': q.choice_1,'choice_2': q.choice_2,'choice_3': q.choice_3,'choice_4': q.choice_4,'answer': q.answer } for q in quiz.questions],
                'reviews': [{'review_id':r.id,'rating':r.rating, 'review_text': r.review_text,'user_id': r.user_id} for r in quiz.reviews],
          }for quiz in quizzes])
    
class QuizzesById(Resource):
    #  a creator can see the answers but the participants cannot
    # gets quiz by id and displays questions and answers
     @jwt_required()
     @allow('Admin')
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
                'questions':[{'question_id': q.id,'question_text':q.text, 'choice_1': q.choice_1,'choice_2': q.choice_2,'choice_3': q.choice_3,'choice_4': q.choice_4, 'answer': q.answer} for q in quiz.questions],
                'reviews':[{'review_id':r.id,'rating':r.rating, 'review_text': r.review_text,'user_id': r.user_id} for r in quiz.reviews]

         })
    #  changes quiz description or title
     @jwt_required()
     @allow('Admin')
     def patch(self,id):
          data = quiz_args.parse_args()
          quiz = Quiz.query.get(id)
          if not quiz:
               return {'msg': 'quiz not found'}
          
          if 'title' in data:
            quiz.title = data['title']
          if 'description' in data:
            quiz.description = data['description']
        
          db.session.commit()
          return jsonify({
         'id':quiz.id,
        'title': quiz.title,
        'description': quiz.description,
        'created_at': quiz.created_at,
        'updated_at': quiz.updated_at
    },{"msg": "Quiz updated successfully"},201)
     @jwt_required()
     @allow('Admin')
     def delete(self, id):
      quiz = Quiz.query.get(id)

      if not quiz:
        return {"msg": "Quiz not found"}, 404 

      db.session.delete(quiz)
      db.session.commit()

      return jsonify({'msg': "Quiz deleted successfully"}, 204 ) 
     
questions_args = reqparse.RequestParser()
questions_args.add_argument('text', type=str, required=True, help='question is required')
questions_args.add_argument('choice_1', type=str, required=True, help='choice_1 is required')
questions_args.add_argument('choice_2', type=str, required=True, help='choice_2 is required')
questions_args.add_argument('choice_3', type=str, required=True, help='choice_3 is required')
questions_args.add_argument('choice_4', type=str, required=True, help='choice_4 is required')
questions_args.add_argument('answer', type=str, required=True, help='question answer is required')
questions_args.add_argument('quiz_id', type=int, required=True, help='quiz id is required')


class Questions(Resource):
    # creates questions and assigns them to a specific quiz
    @jwt_required()
    @allow('Admin')
    def post(self):
      data = questions_args.parse_args()
      
      new_question = Question(
            text = data['text'],
            choice_1 =data['choice_1'],
            choice_2 =data['choice_2'],
            choice_3 =data['choice_3'],
            choice_4 =data['choice_4'],
            answer =data['answer'],
            quiz_id = data['quiz_id']
        )
      db.session.add(new_question)
      db.session.commit()

      return jsonify({
        'id':new_question.id,
        'text': new_question.text,
        'choice_1': new_question.choice_1,
        'choice_2': new_question.choice_2,
        'choice_3': new_question.choice_3,
        'choice_4': new_question.choice_4,
        'answer': new_question.answer,
        "quiz_id": new_question.quiz_id
    },201)
#  creator can update questions 
class QuestionsById(Resource):
    @jwt_required()
    @allow('Admin')
    def patch(self,id):
        data = questions_args.parse_args()
        question = Question.query.get(id)
        if not question:
               return {'msg': 'question not found'}
          
        if 'text' in data:
            question.text = data['text']
        if 'choice_1' in data:
            question.choice_1 = data['choice_1']
        if 'choice_2' in data:
            question.choice_2 = data['choice_2']
        if 'choice_3' in data:
            question.choice_3 = data['choice_3']
        if 'choice_4' in data:
            question.choice_4 = data['choice_4']
        if 'answer' in data:
            question.answer = data['answer']


        
        
        db.session.commit()
        return jsonify({
         'id':question.id,
         'question_text': question.text,
        'choice_1': question.choice_1,
        'choice_2': question.choice_2,
        'choice_3': question.choice_3,
        'choice_4': question.choice_4,
        'answer': question.answer,
    },{"msg": "Question updated successfully"},201)
     

class QuestionResponses(Resource):
    # creator gets all responses of a particular question
    @jwt_required()
    @allow('Admin')
    def get(self, id):
        question = Question.query.get(id)
        if not question:
            return {"msg": "Question not found"}, 404
        
        responses = Response.query.filter_by(question_id=question.id).all()
        
        return jsonify([{
            "id": response.id,
            "response": response.response,
            "user_id": response.user_id,
        } for response in responses],200)


class QuizReviews(Resource):
    # gets all reviews of a specific quiz
    @jwt_required()
    # @allow('Admin')
    def get(self,id):
        quiz = Quiz.query.get(id)
        if not quiz:
            return{"msg":"quiz not found"},404
        reviews = Review.query.filter_by(quiz_id = quiz.id).all()

        return jsonify ([{
            "id": review.id,
            "rating": review.rating,
            "review_text": review.review_text,
            "user_id":review.user_id,
            "quiz_id": review.quiz_id
                                                                    }for review in reviews])


creator_api.add_resource(Quizzes,"/quizzes")
creator_api.add_resource(QuizzesById,"/quizzes/<int:id>")
creator_api.add_resource(Questions,"/questions")
creator_api.add_resource(QuestionsById,"/questions/<int:id>")
creator_api.add_resource(QuestionResponses,"/questions/<int:id>/responses")
creator_api.add_resource(QuizReviews,"/quizzes/<int:id>/reviews")


