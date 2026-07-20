"""
Song browsing, searching, and liking.
GET  /api/songs               - list all songs
GET  /api/songs/<id>          - get one song's details
GET  /api/songs/search?q=...  - search by title/artist
POST /api/songs/<id>/like     - like a song (requires login)
POST /api/songs/<id>/play     - log a play (increments play_count, adds history)
"""

from flask import Blueprint, request, jsonify
from db import get_connection, fetch_all, fetch_one, execute
from auth_utils import login_required

songs_bp = Blueprint("songs", __name__, url_prefix="/api/songs")


@songs_bp.route("", methods=["GET"])
def list_songs():
    conn = get_connection()
    songs = fetch_all(conn, "SELECT * FROM songs ORDER BY play_count DESC")
    conn.close()
    return jsonify(songs), 200


@songs_bp.route("/search", methods=["GET"])
def search_songs():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"error": "Provide a search query with ?q="}), 400

    conn = get_connection()
    results = fetch_all(
        conn,
        """
        SELECT * FROM songs
        WHERE title ILIKE :pattern OR artist ILIKE :pattern
        ORDER BY play_count DESC
        """,
        pattern=f"%{query}%",
    )
    conn.close()
    return jsonify(results), 200


@songs_bp.route("", methods=["POST"])
@login_required
def create_song():
    data = request.get_json() or {}
    title = data.get("title", "").strip()
    artist = data.get("artist", "").strip()
    album = data.get("album", "").strip()
    genre = data.get("genre", "").strip()
    duration = data.get("duration", 0)
    youtube_video_id = data.get("youtube_video_id", "").strip()
    cover_url = data.get("cover_url", "").strip() or "default_cover.png"

    if not title or not artist or not youtube_video_id:
        return jsonify({"error": "title, artist, and youtube_video_id are required"}), 400

    conn = get_connection()
    song = fetch_one(
        conn,
        """
        INSERT INTO songs (title, artist, album, genre, duration, file_url, cover_url, youtube_video_id, uploaded_by)
        VALUES (:title, :artist, :album, :genre, :duration, :file_url, :cover_url, :youtube_video_id, :uploaded_by)
        RETURNING *
        """,
        title=title,
        artist=artist,
        album=album,
        genre=genre,
        duration=duration,
        file_url=f"https://youtube.com/watch?v={youtube_video_id}",
        cover_url=cover_url,
        youtube_video_id=youtube_video_id,
        uploaded_by=request.user_id,
    )
    conn.close()
    return jsonify(song), 201


@songs_bp.route("/<int:song_id>", methods=["GET"])
def get_song(song_id):
    conn = get_connection()
    song = fetch_one(conn, "SELECT * FROM songs WHERE id = :song_id", song_id=song_id)
    conn.close()

    if song is None:
        return jsonify({"error": "Song not found"}), 404
    return jsonify(song), 200


@songs_bp.route("/<int:song_id>/like", methods=["POST"])
@login_required
def like_song(song_id):
    conn = get_connection()
    execute(
        conn,
        """
        INSERT INTO likes (user_id, song_id)
        VALUES (:user_id, :song_id)
        ON CONFLICT (user_id, song_id) DO NOTHING
        """,
        user_id=request.user_id,
        song_id=song_id,
    )
    conn.close()
    return jsonify({"message": "Song liked"}), 200


@songs_bp.route("/<int:song_id>/play", methods=["POST"])
@login_required
def play_song(song_id):
    conn = get_connection()
    execute(
        conn,
        "UPDATE songs SET play_count = play_count + 1 WHERE id = :song_id",
        song_id=song_id,
    )
    execute(
        conn,
        "INSERT INTO listening_history (user_id, song_id) VALUES (:user_id, :song_id)",
        user_id=request.user_id,
        song_id=song_id,
    )
    conn.close()
    return jsonify({"message": "Play recorded"}), 200