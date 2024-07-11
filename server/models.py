from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



user_roles = db.Table(
    "user_roles",
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"))
)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))
    reviews = db.relationship('Review', back_populates='user', cascade="all, delete-orphan")
    responses = db.relationship('Response', back_populates='user', cascade="all, delete-orphan")
    

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class Quiz(db.Model):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    questions = db.relationship('Question', back_populates='quiz', cascade="all, delete-orphan")
    reviews = db.relationship('Review', back_populates='quiz', cascade="all, delete-orphan")
    responses = db.relationship('Response', back_populates='quiz', cascade="all, delete-orphan")  # Added this line
    

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    choice_1 = db.Column(db.String(255))
    choice_2 = db.Column(db.String(255))
    choice_3 = db.Column(db.String(255))
    choice_4 = db.Column(db.String(255))
    answer = db.Column(db.String(1))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))
    responses = db.relationship('Response', back_populates='question')
    quiz = db.relationship('Quiz', back_populates='questions')

class Response(db.Model):
    __tablename__ = 'responses'

    id = db.Column(db.Integer, primary_key=True)
    response = db.Column(db.String(255))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    user = db.relationship('User', back_populates='responses')
    question = db.relationship('Question', back_populates='responses')
    quiz = db.relationship('Quiz', back_populates='responses')

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    review_text = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    quiz = db.relationship('Quiz', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')
