from flask import Flask, render_template

from blueprints.excel_diff_checker import excel_diff_checker_bp

app = Flask(__name__)
app.register_blueprint(excel_diff_checker_bp, url_prefix='/excel-diff-checker')

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
