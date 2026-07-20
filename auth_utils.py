"""
Helper functions for password hashing and JWT tokens.
Used by routes/auth.py, and by any route that needs to check
"is this user logged in?" (via the @login_required decorator).
"""

import os
import jwt
import bcrypt
from functools import wraps
from flask import request, jsonify
from datetime import datetime, timedelta, timezone

JWT_SECRET = os.getenv("JWT_SECRET", "dev_secret_change_me")
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRY_HOURS = 24


def hash_password(plain_password: str) -> str:
    """Turns a plain text password into a secure bcrypt hash for storing in DB."""
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def check_password(plain_password: str, hashed_password: str) -> bool:
    """Compares a login attempt's password against the stored hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def generate_token(user_id: int, username: str) -> str:
    """Creates a JWT token after successful login/signup."""
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRY_HOURS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str):
    """Verifies a token and returns its payload, or None if invalid/expired."""
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def login_required(f):
    """
    Decorator to protect routes that need a logged-in user.
    Expects header: Authorization: Bearer <token>

    Usage:
        @app.route("/playlists")
        @login_required
        def my_playlists():
            user_id = request.user_id   # set by this decorator
            ...
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        token = auth_header.split(" ")[1]
        payload = decode_token(token)
        if payload is None:
            return jsonify({"error": "Invalid or expired token"}), 401

        request.user_id = payload["user_id"]
        request.username = payload["username"]
        return f(*args, **kwargs)

    return wrapper
