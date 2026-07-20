"""
Signup and login endpoints.
POST /api/auth/signup
POST /api/auth/login
"""

from flask import Blueprint, request, jsonify
from db import get_connection, fetch_one, is_unique_violation
from auth_utils import hash_password, check_password, generate_token

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not username or not email or not password:
        return jsonify({"error": "username, email, and password are required"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    password_hash = hash_password(password)

    conn = get_connection()
    try:
        new_user = fetch_one(
            conn,
            """
            INSERT INTO users (username, email, password_hash)
            VALUES (:username, :email, :password_hash)
            RETURNING id, username, email
            """,
            username=username,
            email=email,
            password_hash=password_hash,
        )
    except Exception as e:
        if is_unique_violation(e):
            return jsonify({"error": "Username or email already exists"}), 409
        raise
    finally:
        conn.close()

    token = generate_token(new_user["id"], new_user["username"])
    return jsonify({"user": new_user, "token": token}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    conn = get_connection()
    user = fetch_one(
        conn,
        "SELECT id, username, email, password_hash FROM users WHERE email = :email",
        email=email,
    )
    conn.close()

    if user is None or not check_password(password, user["password_hash"]):
        return jsonify({"error": "Invalid email or password"}), 401

    token = generate_token(user["id"], user["username"])
    return jsonify(
        {
            "user": {"id": user["id"], "username": user["username"], "email": user["email"]},
            "token": token,
        }
    ), 200