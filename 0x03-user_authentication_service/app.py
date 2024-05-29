#!/usr/bin/env python3
"""app.py modules"""
from flask import Flask, jsonify, request, abort, make_response
from auth import Auth


Auth = Auth()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """defining the home route"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=["POST"])
def users() -> str:
    """users functio that implement the route for the users"""
    # get the data the user pass from the form
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        # register the user
        user = Auth.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login() -> str:
    """a login function to respond to the POST /sessions route"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not (Auth.valid_login(email, password)):
        abort(404)
    else:
        # creating a new session for the user
        session_id = Auth.create_session(email)
        # storing the session ID as a cookie with key "session_id" on
        # the response and returning JSON payload of the form
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
