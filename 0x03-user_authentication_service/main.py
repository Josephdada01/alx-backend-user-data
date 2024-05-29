#!/usr/bin/env python3
"""Main module that test if all functions work"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """Testing the registering function"""
    res = requests.post(f"{BASE_URL}/users", data={'email': email,
                                                   'password': password})
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    payload = res.json()
    assert payload == {"email": email, "message":
                       "user created"}, f"Unexpected payload: {payload}"


def log_in_wrong_password(email: str, password: str) -> None:
    """Testing the logging function"""
    res = requests.post(f"{BASE_URL}/sessions", data={'email': email,
                                                      'password': password})
    assert res.status_code == 401, f"Expected 401, got {res.status_code}"


def log_in(email: str, password: str) -> str:
    """Testing the logging function"""
    res = requests.post(f"{BASE_URL}/sessions", data={'email': email,
                                                      'password': password})
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    payload = res.json()
    assert payload == {"email": email,
                       "message":
                       "logged in"}, f"Unexpected payload: {payload}"
    session_id = res.cookies.get("session_id")
    assert session_id is not None, "No session_id found in cookies"
    return session_id


def profile_unlogged() -> None:
    """Testing the profile function"""
    res = requests.get(f"{BASE_URL}/profile")
    assert res.status_code == 403, f"Expected 403, got {res.status_code}"


def profile_logged(session_id: str) -> None:
    """Testing the profile function"""
    cookies = {'session_id': session_id}
    res = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    payload = res.json()
    assert "email" in payload, f"Email not in payload: {payload}"


def log_out(session_id: str) -> None:
    """Testing the logout function"""
    cookies = {'session_id': session_id}
    res = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"


def reset_password_token(email: str) -> str:
    """Testing the reset password function"""
    res = requests.post(f"{BASE_URL}/reset_password", data={'email': email})
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    payload = res.json()
    assert "reset_token" in payload, f"Reset token not in payload: {payload}"
    return payload['reset_token']


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Testing the update passwrd function"""
    res = requests.put(f"{BASE_URL}/reset_password", data={'email': email,
                                                           'reset_token':
                                                           reset_token,
                                                           'new_password':
                                                           new_password})
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    payload = res.json()
    assert payload == {"email": email, "message":
                       "Password updated"}, f"Unexpected payload: {payload}"


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
