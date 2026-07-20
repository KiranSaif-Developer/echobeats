-- Connect to it before running the rest:
-- \c echobeats

-- ============================================
-- 1. USERS
-- ============================================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    bio VARCHAR(255) DEFAULT '',
    profile_pic VARCHAR(255) DEFAULT 'default.png',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 2. SONGS
-- ============================================
CREATE TABLE songs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    artist VARCHAR(150) NOT NULL,
    album VARCHAR(150) DEFAULT '',
    genre VARCHAR(50) DEFAULT '',
    duration INT DEFAULT 0,          -- duration in seconds
    file_url VARCHAR(255) NOT NULL,  -- path/URL to audio file
    cover_url VARCHAR(255) DEFAULT 'default_cover.png',
    play_count INT DEFAULT 0,
    uploaded_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (uploaded_by) REFERENCES users(id) ON DELETE SET NULL
);

-- ============================================
-- 3. PLAYLISTS
-- ============================================
CREATE TABLE playlists (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255) DEFAULT '',
    is_collaborative BOOLEAN DEFAULT FALSE,
    cover_url VARCHAR(255) DEFAULT 'default_playlist.png',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================
-- 4. PLAYLIST_SONGS (many-to-many: playlists <-> songs)
-- ============================================
CREATE TABLE playlist_songs (
    playlist_id INT NOT NULL,
    song_id INT NOT NULL,
    added_by_user_id INT NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (playlist_id, song_id),
    FOREIGN KEY (playlist_id) REFERENCES playlists(id) ON DELETE CASCADE,
    FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE,
    FOREIGN KEY (added_by_user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================
-- 5. FOLLOWS (many-to-many: users <-> users)
-- ============================================
CREATE TABLE follows (
    follower_id INT NOT NULL,
    following_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (follower_id, following_id),
    FOREIGN KEY (follower_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (following_id) REFERENCES users(id) ON DELETE CASCADE,
    CHECK (follower_id <> following_id)
);

-- ============================================
-- 6. LIKES (users liking songs)
-- ============================================
CREATE TABLE likes (
    user_id INT NOT NULL,
    song_id INT NOT NULL,
    liked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, song_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE
);

-- ============================================
-- 7. COMMENTS (on songs)
-- ============================================
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    song_id INT NOT NULL,
    text VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE
);

-- ============================================
-- 8. LISTENING HISTORY (for recommendations)
-- ============================================
CREATE TABLE listening_history (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    song_id INT NOT NULL,
    played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE
);

-- ============================================
-- HELPFUL INDEXES
-- ============================================
CREATE INDEX idx_songs_title ON songs(title);
CREATE INDEX idx_songs_artist ON songs(artist);
CREATE INDEX idx_history_user ON listening_history(user_id);

-- ============================================
-- SAMPLE DATA
-- ============================================

-- Users (password_hash values here are placeholders — real app will store bcrypt hashes)
INSERT INTO users (username, email, password_hash, bio) VALUES
('ali_khan', 'ali@example.com', 'hashed_pw_1', 'Music lover'),
('sara_ahmed', 'sara@example.com', 'hashed_pw_2', 'Lo-fi and coffee'),
('bilal_r', 'bilal@example.com', 'hashed_pw_3', 'Rock and metal fan');

-- Songs
INSERT INTO songs (title, artist, album, genre, duration, file_url, cover_url) VALUES
('Blinding Lights', 'The Weeknd', 'After Hours', 'Pop', 200, '/audio/blinding_lights.mp3', '/covers/blinding_lights.jpg'),
('Shape of You', 'Ed Sheeran', 'Divide', 'Pop', 233, '/audio/shape_of_you.mp3', '/covers/shape_of_you.jpg'),
('Bohemian Rhapsody', 'Queen', 'A Night at the Opera', 'Rock', 354, '/audio/bohemian_rhapsody.mp3', '/covers/bohemian_rhapsody.jpg'),
('Lo-fi Chill Beat', 'ChillHop', 'Study Sessions', 'Lo-fi', 180, '/audio/lofi_chill.mp3', '/covers/lofi_chill.jpg');

-- Playlists
INSERT INTO playlists (user_id, name, description, is_collaborative) VALUES
(1, 'Workout Mix', 'High energy songs', FALSE),
(2, 'Chill Study Vibes', 'Lo-fi for studying', TRUE);

-- Playlist songs
INSERT INTO playlist_songs (playlist_id, song_id, added_by_user_id) VALUES
(1, 1, 1),
(1, 2, 1),
(2, 4, 2);

-- Follows
INSERT INTO follows (follower_id, following_id) VALUES
(1, 2),
(2, 1),
(3, 1);

-- Likes
INSERT INTO likes (user_id, song_id) VALUES
(1, 1),
(1, 3),
(2, 4);

-- Comments
INSERT INTO comments (user_id, song_id, text) VALUES
(1, 1, 'This song is a banger!'),
(2, 3, 'Timeless classic.');

-- Listening history
INSERT INTO listening_history (user_id, song_id) VALUES
(1, 1),
(1, 2),
(2, 4),
(3, 3);