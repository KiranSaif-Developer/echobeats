"""
Playlist creation and management.
GET  /api/playlists                      - all playlists for logged-in user
POST /api/playlists                      - create a new playlist
GET  /api/playlists/<id>                 - one playlist with its songs
POST /api/playlists/<id>/songs           - add a song to a playlist
DELETE /api/playlists/<id>/songs/<sid>   - remove a song from a playlist
"""

from flask import Blueprint, request, jsonify
from db import get_connection, fetch_all, fetch_one, execute
from auth_utils import login_required

playlists_bp = Blueprint("playlists", __name__, url_prefix="/api/playlists")


@playlists_bp.route("", methods=["GET"])
@login_required
def get_my_playlists():
    conn = get_connection()
    playlists = fetch_all(
        conn,
        "SELECT * FROM playlists WHERE user_id = :user_id ORDER BY created_at DESC",
        user_id=request.user_id,
    )
    conn.close()
    return jsonify(playlists), 200


@playlists_bp.route("", methods=["POST"])
@login_required
def create_playlist():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    description = data.get("description", "")
    is_collaborative = data.get("is_collaborative", False)

    if not name:
        return jsonify({"error": "Playlist name is required"}), 400

    conn = get_connection()
    playlist = fetch_one(
        conn,
        """
        INSERT INTO playlists (user_id, name, description, is_collaborative)
        VALUES (:user_id, :name, :description, :is_collaborative)
        RETURNING *
        """,
        user_id=request.user_id,
        name=name,
        description=description,
        is_collaborative=is_collaborative,
    )
    conn.close()
    return jsonify(playlist), 201


@playlists_bp.route("/<int:playlist_id>", methods=["GET"])
def get_playlist(playlist_id):
    conn = get_connection()
    playlist = fetch_one(conn, "SELECT * FROM playlists WHERE id = :playlist_id", playlist_id=playlist_id)

    if playlist is None:
        conn.close()
        return jsonify({"error": "Playlist not found"}), 404

    songs = fetch_all(
        conn,
        """
        SELECT s.* FROM songs s
        JOIN playlist_songs ps ON ps.song_id = s.id
        WHERE ps.playlist_id = :playlist_id
        ORDER BY ps.added_at
        """,
        playlist_id=playlist_id,
    )
    conn.close()

    playlist["songs"] = songs
    return jsonify(playlist), 200


@playlists_bp.route("/<int:playlist_id>/songs", methods=["POST"])
@login_required
def add_song_to_playlist(playlist_id):
    data = request.get_json() or {}
    song_id = data.get("song_id")

    if not song_id:
        return jsonify({"error": "song_id is required"}), 400

    conn = get_connection()
    execute(
        conn,
        """
        INSERT INTO playlist_songs (playlist_id, song_id, added_by_user_id)
        VALUES (:playlist_id, :song_id, :user_id)
        ON CONFLICT (playlist_id, song_id) DO NOTHING
        """,
        playlist_id=playlist_id,
        song_id=song_id,
        user_id=request.user_id,
    )
    conn.close()
    return jsonify({"message": "Song added to playlist"}), 200


@playlists_bp.route("/<int:playlist_id>/songs/<int:song_id>", methods=["DELETE"])
@login_required
def remove_song_from_playlist(playlist_id, song_id):
    conn = get_connection()
    execute(
        conn,
        "DELETE FROM playlist_songs WHERE playlist_id = :playlist_id AND song_id = :song_id",
        playlist_id=playlist_id,
        song_id=song_id,
    )
    conn.close()
    return jsonify({"message": "Song removed from playlist"}), 200