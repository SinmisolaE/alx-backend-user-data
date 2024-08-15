#!/usr/bin/env python3
""" a basic Flask app"""

from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)
Auth = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def basic():
    """  return a JSON payload of the form:"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def user():
    """ implement the end-point to register a user"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        Auth.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": f"{email}", "message": "user created"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ create a new session for the user
    store it the session ID as a cookie with key "session_id"
    on the response
    return a JSON payload of the form
    else use flask.abort
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not Auth.validate_login(email, password):
        abort(401)
    session_id = Auth.create_session(email)
    response = jsonify({"email": f"{email}", "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
