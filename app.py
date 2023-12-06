from imports import *
from server.routes import *
# from server.models import *

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'secret',
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///anti_sleep.db',
})

app.register_blueprint(sys)
# db.init_app(app)
socketio.init_app(app)

def main():
    # with app.app_context():
    #     db.create_all()
    return socketio.run(app, debug=True, host='0.0.0.0')

if __name__ == '__main__':
    main()