#!/usr/bin/env python3
""" a basic Flask app"""

from flask import Flask, jsonify
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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
