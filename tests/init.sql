-- Create the audios table
CREATE TABLE audios (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL
);

-- Create the audio_fingerprints table
CREATE TABLE audio_fingerprints (
    id SERIAL PRIMARY KEY,
    audio_id INT REFERENCES audios(id) ON DELETE CASCADE,
    fingerprint BYTEA NOT NULL,
    time_offset INTEGER NOT NULL
);


-- Insert data into the audios table
INSERT INTO audios (title) VALUES ('Test Audio Init');