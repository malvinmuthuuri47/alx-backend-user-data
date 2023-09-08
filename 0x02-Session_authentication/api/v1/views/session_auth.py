#!/usr/bin/env python3
""" Module for Session views """

from flask import request, jsonify, abort, make_response
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ POST /api/v1/auth_session/login
    Return:
        - The User instance based on the email
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    elif password is None or password == '':
        return jsonify({"error": "password missing"}), 400

    # Retrieve the User instance based on the Email
    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    else:
        for user in users:
            if user.is_valid_password(password):
                from api.v1.app import auth
                session_id = auth.create_session(user.id)
                dict_repr_user = jsonify(user.to_json())
                session_name = os.getenv('SESSION_NAME')
                dict_repr_user.set_cookie(session_name, session_id)
                return dict_repr_user
        return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """This function logs out the user and deletes their session cookie"""
    from api.v1.app import auth
    session = auth.destroy_session(request)
    if session is False:
        abort(404)
    else:
        return jsonify({}), 200
