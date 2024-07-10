from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import MetaData
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)



user_roles = db.Table(
    "user_roles",
    metadata,
    db.Column("role_id",db.ForeignKey("roles.id")),
    db.Column("user_id", db.ForeignKey("users.id")),
)

class Role(db.Model):
    __tablename__='roles'
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(255))
    user = db.relationship('User',back_populates='roles', secondary=user_roles)


# class TokenBlocklist(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     jti = db.Column(db.String(36), nullable=False, index=True)
#     created_at = db.Column(db.DateTime, nullable=False)
  
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    reviews = db.relationship('Review', back_populates='user', cascade="all, delete-orphan")
    responses = db.relationship('Response', back_populates='user', cascade="all, delete-orphan")
    serialize_rules = ('-user.reviews',)
    roles = db.relationship('Role',back_populates='user', secondary=user_roles)

class Quiz(db.Model, SerializerMixin):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    reviews = db.relationship('Review', back_populates='quiz')
    questions = db.relationship('Question', back_populates='quiz', cascade="all, delete-orphan")
    serialize_rules = ('-quiz.questions',)

class Question(db.Model, SerializerMixin):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    choice_1 = db.Column(db.String(255))
    choice_2 = db.Column(db.String(255))
    choice_3 = db.Column(db.String(255))
    choice_4 = db.Column(db.String(255))
    answer = db.Column (db.String(1))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))
    quiz = db.relationship('Quiz', back_populates='questions')

class Response(db.Model, SerializerMixin):
    __tablename__ = 'responses'

    id = db.Column(db.Integer, primary_key=True)
    response = db.Column(db.String(255))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    user = db.relationship('User', back_populates='responses')
    question = db.relationship('Question', back_populates = "responses")
    quiz = db.relationship('Quiz', back_populates = "responses")

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    review_text = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    quiz = db.relationship('Quiz', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')