from flask import Blueprint, render_template

# Create the blueprint object
main_bp = Blueprint('main', __name__, template_folder='templates', static_folder='static')


@main_bp.route('/')
def home():
    return render_template('main/home.html')