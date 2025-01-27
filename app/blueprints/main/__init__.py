from flask import Blueprint

# Create the blueprint object
main_bp = Blueprint('main', __name__, template_folder='templates', static_folder='static')

# Import routes to associate them with this blueprint
from . import routes




