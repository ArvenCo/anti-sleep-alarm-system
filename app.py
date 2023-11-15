from imports import *
from server.routes import *
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

app.register_blueprint(sys)

socketio.init_app(app)



def main():
    return socketio.run(app, debug=True)

if __name__ == '__main__':
    main()