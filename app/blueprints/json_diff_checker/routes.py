from flask import render_template, request, send_file, Blueprint
from .logic import get_diff

# Create the blueprint object
json_diff_checker_bp = Blueprint('json_diff_checker',
                                 __name__,
                                 template_folder='templates',
                                 static_folder='static')


@json_diff_checker_bp.route('/')
def fill_json():
    return render_template('json_diff_checker/fill_json.html')


@json_diff_checker_bp.route('/compare', methods=['POST'])
def compare():
    # Retrieve expected and actual json string from request
    expected_json_str = request.form['expectedJson']
    actual_json_str = request.form['actualJson']

    # Call compare function
    result = get_diff(expected_json_str, actual_json_str)

    return render_template('json_diff_checker/result.html',
                           result=result)
