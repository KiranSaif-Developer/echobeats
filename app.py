"""
EchoBeats Backend - Main entry point.
Run with: python app.py
Server starts at http://localhost:5000
"""

from flask import Flask, jsonify
from flask_cors import CORS

from routes.auth import auth_bp
from routes.songs import songs_bp
from routes.playlists import playlists_bp

app = Flask(__name__)
CORS(app)  # allows your HTML/JS frontend (running on a different port) to call this API

# Register all route groups
app.register_blueprint(auth_bp)
app.register_blueprint(songs_bp)
app.register_blueprint(playlists_bp)


@app.route("/")
def health_check():
    return jsonify({"status": "EchoBeats API is running"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)