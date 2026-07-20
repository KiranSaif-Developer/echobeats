-- Run this in psql, connected to the echobeats database:
--   psql -U postgres -d echobeats -f 03_add_youtube_support.sql

-- Add a column to store the YouTube video ID for each song
ALTER TABLE songs ADD COLUMN IF NOT EXISTS youtube_video_id VARCHAR(20);

-- Update our 4 sample songs with real YouTube video IDs
UPDATE songs SET youtube_video_id = '4NRXx6U8ABQ' WHERE title = 'Blinding Lights';
UPDATE songs SET youtube_video_id = 'JGwWNGJdvx8' WHERE title = 'Shape of You';
UPDATE songs SET youtube_video_id = 'fJ9rUzIMcZQ' WHERE title = 'Bohemian Rhapsody';
UPDATE songs SET youtube_video_id = 'jfKfPfyJRdk' WHERE title = 'Lo-fi Chill Beat';

-- Confirm it worked
SELECT id, title, artist, youtube_video_id FROM songs;