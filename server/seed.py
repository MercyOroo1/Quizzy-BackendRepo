from app import app
from models import User, Role, Quiz, Question, Response, Review, db
from app import bcrypt

def delete_tables():
    db.session.query(Response).delete()
    db.session.query(Review).delete()
    db.session.query(Question).delete()
    db.session.query(Quiz).delete()
    db.session.query(User).delete()
    db.session.query(Role).delete()
    db.session.commit()

def create_roles():
    roles = ['Admin', 'User']
    for role in roles:
        db.session.add(Role(name=role))
    db.session.commit()

def create_users():
    users = [
        {'email': 'admin@example.com', 'username': 'admin', 'password_hash': '123456789', 'role': 'Admin'},
        {'email': 'user1@example.com', 'username': 'user1', 'password_hash': 'hashed_user1_password', 'role': 'User'},
        {'email': 'user2@example.com', 'username': 'user2', 'password_hash': 'hashed_user2_password', 'role': 'User'}
    ]
    for user_data in users:
        hashed_password = bcrypt.generate_password_hash(user_data['password_hash']).decode('utf-8')
        user = User(
            email=user_data['email'],
            username=user_data['username'],
            password_hash=hashed_password,
        )
        user.roles.append(Role.query.filter_by(name=user_data['role']).first())
        db.session.add(user)
    db.session.commit()

def create_quizzes():
    quizzes = [
        {'title': 'Geography', 'description': 'Extend you geographical knowledge', 'image_url': 'https://www.google.com/imgres?q=Globe%20png%20Image&imgurl=http%3A%2F%2Fatlas-content-cdn.pixelsquid.com%2Fstock-images%2Fearth-k1kYV36-600.jpg&imgrefurl=https%3A%2F%2Fwww.pixelsquid.com%2Fpng%2Fearth-2045628189572601703&docid=FLHLpVNHrrYj5M&tbnid=gHbwitgw8QJYzM&vet=12ahUKEwiNz7i0iKeHAxV9VaQEHVwsDoUQM3oFCIcBEAA..i&w=600&h=600&hcb=2&ved=2ahUKEwiNz7i0iKeHAxV9VaQEHVwsDoUQM3oFCIcBEAA'},
        {'title': 'History', 'description': 'Make your ', 'image_url':'https://www.google.com/imgres?q=Globe%20png%20Image&imgurl=https%3A%2F%2Fpurepng.com%2Fpublic%2Fuploads%2Flarge%2Fglobe-br7.png&imgrefurl=https%3A%2F%2Fpnghunter.com%2Fpng%2Fglobe-8%2F&docid=WYn2V0xgpuBEXM&tbnid=cKdBzhnApMSNbM&vet=12ahUKEwiNz7i0iKeHAxV9VaQEHVwsDoUQM3oECDoQAA..i&w=2246&h=2273&hcb=2&ved=2ahUKEwiNz7i0iKeHAxV9VaQEHVwsDoUQM3oECDoQAA'}
    ]
    for quiz_data in quizzes:
        quiz = Quiz(
            title=quiz_data['title'],
            description=quiz_data['description'],
            image_url=quiz_data['image_url'],
        )
        db.session.add(quiz)
    db.session.commit()

def create_questions():
    quizzes = Quiz.query.all()
    questions = [
        {'text': 'What is the capital of France?', 'choice_1': 'Paris', 'choice_2': 'London', 'choice_3': 'Berlin', 'choice_4': 'Madrid', 'answer': 'A'},
        {'text': 'What is 2 + 2?', 'choice_1': '3', 'choice_2': '4', 'choice_3': '5', 'choice_4': '6', 'answer': 'B'}
    ]
    for quiz in quizzes:
        for question_data in questions:
            question = Question(
                text=question_data['text'],
                choice_1=question_data['choice_1'],
                choice_2=question_data['choice_2'],
                choice_3=question_data['choice_3'],
                choice_4=question_data['choice_4'],
                answer=question_data['answer'],
                quiz_id=quiz.id
            )
            db.session.add(question)
    db.session.commit()

def create_responses():
    users = User.query.all()
    questions = Question.query.all()
    responses = [
        {'response': 'A'},
        {'response': 'B'}
    ]
    for user in users:
        for question, response_data in zip(questions, responses):
            response = Response(
                response=response_data['response'],
                quiz_id=question.quiz_id,
                question_id=question.id,
                user_id=user.id
            )
            db.session.add(response)
    db.session.commit()

def create_reviews():
    users = User.query.all()
    quizzes = Quiz.query.all()
    reviews = [
        {'rating': 5, 'review_text': 'Great quiz!'},
        {'rating': 4, 'review_text': 'Good quiz!'}
    ]
    for user in users:
        for quiz, review_data in zip(quizzes, reviews):
            review = Review(
                rating=review_data['rating'],
                review_text=review_data['review_text'],
                quiz_id=quiz.id,
                user_id=user.id
            )
            db.session.add(review)
    db.session.commit()

def seed():
    delete_tables()
    create_roles()
    create_users()
    create_quizzes()
    create_questions()
    create_responses()
    create_reviews()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Make sure all tables are created
        seed()
