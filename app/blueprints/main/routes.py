from flask import Blueprint, render_template

from . import main_bp

@main_bp.route('/')
def home():
    return render_template('main/home.html')



    