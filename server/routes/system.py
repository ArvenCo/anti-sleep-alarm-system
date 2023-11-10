from imports import *

sys = Blueprint('sys', __name__)

@sys.route('/')
def index():
    return 