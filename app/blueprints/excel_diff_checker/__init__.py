from flask import Blueprint

# Create the blueprint object
excel_diff_checker_bp = Blueprint('excel_diff_checker', __name__,
                                  template_folder='templates',
                                  static_folder='static')

# Import routes to associate them with this blueprint
from . import routes
