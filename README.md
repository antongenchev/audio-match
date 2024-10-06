# audio-match
A full stack web app for audio recognition

-Redis container for the task queue
-Celery for the task workers. which will process audio and handle more
time consuming audio matching
-Flask app for the backend. Initially flask will render templates but
later a separate frontend app can be created
-Postgres database for storing the users, the acoustic fingerprints,
etc.
-PgAdmin for having an easy to use interface to the database
-Flower for having an easy view of the celery tasks while developing

For now the audio files will be stored on a docker volume. The plan is
to move them to an S3 bucket later on