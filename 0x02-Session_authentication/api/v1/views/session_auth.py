#!/usr/bin/env python3
"""
module for session auth
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=["POST"], strict_slashes=False)
def login():
    """
    authenticates a user"""
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == '':
        return jsonify({ "error": "email missing" }), 400
    if password is None or password == '':
        return jsonify({ "error": "password missing" }), 400
    try:
        users = User.search({'email': user_email})
        if len(users) == 0:
            return jsonify({ "error": "no user found for this email" }), 404
        valid_pwd = False
        user = None
        for u in users:
            if u.is_valid_password(password):
                valid_pwd = True
                user = u
                break
        if valid_pwd == False:
            return jsonify({ "error": "wrong password" }), 401
        from api.v1.app import auth
        session_id = auth.create_session(user.id)
        response = jsonify(user.to_json())
        response.set_cookie(os.getenv("SESSION_NAME"), sessiond_id)
        return response, 200
    except Exception:
        return jsonify({ "error": "no user found for this email" }), 404

@app_views.route('/auth_session/logout', methods=["DELETE"], strict_slashes=False)
def logout():
    """
    delete session id from cookie"""
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
