#!/usr/bin/env python3
"""Basic Flask app"""

from flask import Flask, jsonify, request, abort, session, redirect, url_for
from auth import Auth
import os

AUTH = Auth()

app = Flask(__name__)
# Generate random bytes
random_bytes = os.urandom(98)
# Encode the random bytes as a hexadecimal string
secret_key = random_bytes.hex()
app.config['SECRET_KEY'] = secret_key


@app.route("/", methods=['GET'])
def index():
    """Root route"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """Users route"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """Sessions route"""
    email = request.form.get("email")
    password = request.form.get("password")
    user = AUTH.valid_login(email, password)
    if not user:
        abort(401)
    else:
        session_id = AUTH.create_session(email)
        session = jsonify({"email": email, "message": "logged in"})
        session.set_cookie('session_id', session_id)
        return session


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """DELETE session"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """Profile function"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        user_email = user.email
        return jsonify({"email": user_email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> str:
    """Get reset password token"""
    email = request.form.get("email")
    try:
        user_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": user_token}), 200
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """Update password end-point"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        user = AUTH.update_password(reset_token, new_password)
        return jsonify({"email": {email}, "message": "Password updated"})
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
