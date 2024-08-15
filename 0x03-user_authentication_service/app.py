#!/usr/bin/env python3
"""a simple flask app"""
from flask import Flask, jsonify, request
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/")
def bienvenue():
    """bienvenue"""
    return jsonify({"message": "Bienvenue"}), 200

@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """create a new user using the AUTH module"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
        msg = {"email": f"{email}", "message": "user created"}
        return jsonify(msg), 201
    except Exception:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
