#!/usr/bin/env python3
"""app.py modules"""
from flask import Flask, jsonify, request, abort, redirect
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth


AUTH = Auth()

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
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=["POST"])
def login() -> str:
    """a login function to respond to the POST /sessions route"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not (AUTH.valid_login(email, password)):
        abort(401)
    else:
        # creating a new session for the user
        session_id = AUTH.create_session(email)
        # storing the session ID as a cookie with key "session_id" on
        # the response and returning JSON payload of the form
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response


@app.route('/sessions', methods=["DELETE"])
def logout() -> str:
    """function to respond to the DELETE /sessions route."""
    # The request contain the session ID as a cookie with key "session_id".
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)
    try:
        # Find the user with the requested session ID
        user = AUTH._db.find_user_by(session_id=session_id)
    except NoResultFound:
        user = None
    # If the user does not exist, respond with a 403 HTTP status.
    if not user:
        abort(403)
    # If the user exists destroy the session and redirect the user to GET /
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route('/profile', methods=["GET"])
def profile() -> str:
    """profile function to respond to the GET /profile route."""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    else:
        return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=["POST"])
def get_reset_password_token() -> str:
    """you will implement a get_reset_password_token function to respond
    to the POST /reset_password route.
    The request is expected to contain form data with the "email" field.
    If the email is not registered, respond with a 403 status code. Otherwise,
    generate a token and respond with a 200 HTTP status and the following JSON
    payload:"""
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except Exception:
        abort(403)


@app.route("/reset_password", methods=["PUT"])
def reset_password():
    """Route to reset the user's password"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    if not email or not reset_token or not new_password:
        return jsonify({"message": "Email, reset token, \
                        and new password are required"}), 400

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)  # Forbidden if reset token is invalid


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
