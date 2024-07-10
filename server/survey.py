# from flask import Blueprint, jsonify, make_response
# from flask_restful import Api, Resource, reqparse
# from models import db, Survey

# survey_bp = Blueprint('survey_bp', __name__, url_prefix='/surveys')
# survey_api = Api(survey_bp)

# survey_parser = reqparse.RequestParser()
# survey_parser.add_argument('title', type=str, required=True, help='survey name is required')
# survey_parser.add_argument('description', type=str, required=True, help='survey description is required')

# class SurveyListResource(Resource):
#     def get(self):
#         surveys = Survey.query.all()
#         return jsonify([survey.to_dict() for survey in surveys])
#     # admins only
#     def post(self):
#         data = survey_parser.parse_args()
#         new_survey = Survey(
#             title=data['title'],
#             description=data['description']
#         )
#         db.session.add(new_survey)
#         db.session.commit()
#         return {"msg": "Survey created successfully", "survey": new_survey.to_dict()}, 201

# class SurveyResource(Resource):
#     def get(self, id):
#         survey = Survey.query.get(id)
#         if not survey:
#             return {'message': 'Survey not found'}, 404
#         return survey.to_dict(), 200
#     # admins only 
#     def patch(self, id):
#         data = survey_parser.parse_args()
#         survey = Survey.query.get(id)
#         if not survey:
#             return {'msg': "Survey not found"}, 404
        
#         if 'title' in data:
#             survey.title = data['title']
#         if 'description' in data:
#             survey.description = data['description']
        
#         db.session.commit()
#         return {'msg': 'Survey updated successfully', "survey": survey.to_dict()}, 200
#     # admin
#     def delete(self, id):
#         survey = Survey.query.get(id)
#         if not survey:
#             return {"msg": "Survey not found"}, 404
#         db.session.delete(survey)
#         db.session.commit()
#         return {'msg': 'Survey deleted successfully'}, 204


# survey_api.add_resource(SurveyListResource, '/')
# survey_api.add_resource(SurveyResource, '/<int:id>')
