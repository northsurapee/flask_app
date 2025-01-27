from flask import render_template, request, send_file
from . import json_diff_checker_bp
from .logic import get_diff


@json_diff_checker_bp.route('/')
def home():
    return render_template('json_diff_checker/home.html')


@json_diff_checker_bp.route('/compare', methods=['POST'])
def compare():
    # Retrieve expected and actual json string from request
    expected_json_str = request.form['expectedJson']
    actual_json_str = request.form['actualJson']

    # Call compare function
    result = get_diff(expected_json_str, actual_json_str)

    return render_template('json_diff_checker/result.html',
                           result=result)


