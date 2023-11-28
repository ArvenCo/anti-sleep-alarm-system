from server.models import User, db

def index():
    user = User.query.all()
    return user

def insert(username:str):
    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    return user

