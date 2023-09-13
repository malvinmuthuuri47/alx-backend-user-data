#!/usr/bin/env python3
"""Basic Flask app"""

from flask import Flask, jsonify, request, abort, session
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
def sessions():
    """Sessions route"""
    email = request.form.get("email")
    password = request.form.get("password")
    user = AUTH.valid_login(email, password)
    if not user:
        abort(401)
    else:
        session['session_id'] = AUTH.create_session(email)
        response_data = {"email": email, "message": "logged in"}
        return jsonify(response_data), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
