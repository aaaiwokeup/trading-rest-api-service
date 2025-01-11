from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from db import exist_username, insert_data, get_password_by_username
import bcrypt

auth = Blueprint("auth", __name__)

@auth.route("/")
def home():
    return render_template("login.html")

@auth.route("/signup")
def signup():
    return render_template("register.html")

@auth.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username", None)
    password = data.get("password", None)

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400


    if exist_username(username):
        return jsonify({"error": "Username already exists"}), 409

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    insert_data(username, hashed_password)

    return jsonify({"message": "User registered successfully"}), 201

@auth.route("/login", methods=['POST'])
def log_in():
    data = request.get_json()
    username = data.get("username", None)
    password = data.get("password", None)
    print(data, username, password)
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    result = get_password_by_username(username)

    if not result or not bcrypt.checkpw(password.encode('utf-8'), result.encode('utf-8')):
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)
    return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200

# JWT check
@auth.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Hello, {current_user}"}), 200