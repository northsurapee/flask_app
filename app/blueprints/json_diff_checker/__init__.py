from flask import Blueprint

# Create the blueprint object
json_diff_checker_bp = Blueprint('json_diff_checker',
                                 __name__,
                                 template_folder='templates',
                                 static_folder='static')

# Import routes to associate them with this blueprint
from . import routes
