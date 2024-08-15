#!/usr/bin/env python3
"""a simple flask app"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def bienvenue():
    """bienvenue"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """create a new user using the AUTH module"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        msg = {"email": f"{email}", "message": "user created"}
        return jsonify(msg)
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """
    function to responde to the sessions route
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        resp = jsonify({"email": f"{email}", "message": "logged in"})
        resp.set_cookie("session_id", session_id)
        return resp
    else:
        abort(401)
    return None


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """
    In this task, you will implement a logout
    function to respond to the DELETE /sessions route.
    """
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(session_id)
            return redirect("/")
    return jsonify({"message": "no session or invalid id"}), 403


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """
    function to responde to the profile route
    """
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email}), 200
    return jsonify({"message": "no session or invalid id"}), 403


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    function to responde to the reset_password route
    Return:
    {"email": "<user email>", "reset_token": "<reset token>"}
    """
    try:
        email = request.form.get("email")
        reset_token = AUTH.get_reset_password_token(email)
        msg = {"email": f"{email}", "reset_token": f"{reset_token}"}
        return jsonify(msg)
    except ValueError:
        return jsonify({"message": "invalid email"}), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
