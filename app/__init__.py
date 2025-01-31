from flask import Flask

# Import Blueprints
from app.blueprints.excel_diff_checker.routes import excel_diff_checker_bp
from app.blueprints.main.routes import main_bp


def create_app():
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(excel_diff_checker_bp, url_prefix='/excel-diff-checker')
    app.register_blueprint(main_bp)

    return app
