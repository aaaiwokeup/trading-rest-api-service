from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy import insert, select
import bcrypt

from db import users_table

class AuthService:
    def __init__(self, engine):
        self.engine = engine

    def insert_data(self, username, password):
        with self.engine.connect() as conn:
            query = insert(users_table).values([{"username": username, "password": password}])
            conn.execute(query)
            conn.commit()

    def exist_username(self, username):
        with self.engine.connect() as conn:
            query = select(users_table.c.username).where(users_table.c.username == username)
            result = conn.execute(query)
            exists = result.fetchone() is not None
            return exists

    def get_password_by_username(self, username):
        with self.engine.connect() as conn:
            query = select(users_table.c.password).where(users_table.c.username == username)
            result = conn.execute(query)
            try:
                password = result.fetchone()[0]
                return password
            except TypeError:
                return None

    def register(self, data):
        username = data.get("username", None)
        password = data.get("password", None)

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        if self.exist_username(username):
            return jsonify({"error": "Username already exists"}), 409

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        self.insert_data(username, hashed_password)

        return jsonify({"message": "User registered successfully"}), 201

    def log_in(self, data):
        username = data.get("username", None)
        password = data.get("password", None)

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        result = self.get_password_by_username(username)

        if not result or not bcrypt.checkpw(password.encode('utf-8'), result.encode('utf-8')):
            return jsonify({"error": "Invalid username or password"}), 401

        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200