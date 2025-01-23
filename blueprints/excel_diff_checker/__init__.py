from flask import Blueprint

excel_diff_checker_bp = Blueprint('excel_diff_checker', __name__,
                                  template_folder='templates',
                                  static_folder='static')

from . import routes
