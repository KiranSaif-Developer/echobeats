"""
Handles the connection to our PostgreSQL database using pg8000.

We use pg8000 instead of psycopg2 because psycopg2-binary doesn't ship
prebuilt wheels for newer Python versions (it needs Microsoft C++ Build
Tools to compile from source). pg8000 is pure Python, so no compiler
needed, regardless of Python version.

Important difference from psycopg2:
- pg8000 uses ":name" style placeholders, not "%s"
  e.g. conn.run("SELECT * FROM users WHERE email = :email", email=email)
- pg8000 doesn't return dictionaries by default (just plain rows), so the
  helper functions below (fetch_all, fetch_one, execute) convert results
  into dictionaries for you, the same way RealDictCursor did in psycopg2.
"""

import os
import pg8000.native as pg8000
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """Opens a new connection to the echobeats Postgres database."""
    return pg8000.Connection(
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.getenv("DB_NAME", "echobeats"),
    )


def fetch_all(conn, sql, **params):
    """
    Runs a SELECT (or INSERT/UPDATE ... RETURNING) and returns
    a list of dictionaries, one per row.
    Usage: fetch_all(conn, "SELECT * FROM songs WHERE genre = :genre", genre="Pop")
    """
    rows = conn.run(sql, **params)
    columns = [col["name"] for col in conn.columns] if conn.columns else []
    return [dict(zip(columns, row)) for row in rows]


def fetch_one(conn, sql, **params):
    """Same as fetch_all, but returns just the first row (or None)."""
    results = fetch_all(conn, sql, **params)
    return results[0] if results else None


def execute(conn, sql, **params):
    """For INSERT/UPDATE/DELETE statements that don't need to return rows."""
    conn.run(sql, **params)


def is_unique_violation(error: Exception) -> bool:
    """
    Checks if an exception was caused by a duplicate value
    (e.g. signing up with an email that's already taken).
    Postgres error code 23505 = unique_violation.
    """
    return "23505" in str(error) or "duplicate key" in str(error).lower()
