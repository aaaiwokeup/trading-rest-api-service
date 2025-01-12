from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import get_jwt_identity, jwt_required

from services import AuthService
from db import engine

auth = Blueprint("auth", __name__)
auth_service = AuthService(engine)

@auth.route("/")
def home():
    return render_template("login.html")

@auth.route("/signup")
def signup():
    return render_template("register.html")

@auth.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    return auth_service.register(data)

@auth.route("/login", methods=['POST'])
def log_in():
    data = request.get_json()
    return auth_service.log_in(data)

# JWT check
@auth.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Hello, {current_user}"}), 200