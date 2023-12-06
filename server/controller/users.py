# from server.models import User, db

# def index():
#     user = User.query.all()
#     return user

# def insert(username:str):
#     user = User.query.filter(User.username == username).first()
#     if user is None:
#         new_user = User(username=username)
#         db.session.add(new_user)
#         db.session.commit()
#         return new_user
#     return user

