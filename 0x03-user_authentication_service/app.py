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
        else:
            return jsonify({"message": "session does not exist"}), 403
    else:
        return jsonify({"message": "no session id"}), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
