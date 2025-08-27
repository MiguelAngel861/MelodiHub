from flask import Blueprint, render_template


auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route('/')
def index():
    return "hola"