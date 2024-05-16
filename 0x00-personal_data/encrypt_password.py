#!/usr/bin/env python3
"""Encrypting passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    hash_password function that expects one string argument
    name password and returns a salted, hashed password, which
    is a byte string.Use the bcrypt package to perform the hashing
    (with hashpw).
    """
    # Generate a salt
    salt = bcrypt.gensalt()

    # Hashing the password with the generated salt
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password
