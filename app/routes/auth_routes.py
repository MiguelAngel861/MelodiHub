from flask import Blueprint, render_template

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route('/')
def index():
    return render_template("layout.html")

@auth_bp.route('/profile')
def profile():
    pass

@auth_bp.route("/inicio")
def inicio():
    pass

@auth_bp.route('/repifyWawa')
def repify():
    pass

@auth_bp.route('/gustados')
def liked_tracks():
    pass

@auth_bp.route('/historial')
def historial():
    pass

@auth_bp.route('/gustados')
def gustados():
    pass
