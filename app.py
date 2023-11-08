from server.requirements import *

app = Flask(__name__)



def main():
    return app.run(debug=True)

if __name__ == '__main__':
    main()