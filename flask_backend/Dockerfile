# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install the PostgreSQL development libraries
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ./flask_backend/requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Copy the rest of the application code into the container
COPY ./flask_backend ./flask_backend
COPY ./celery_worker ./celery_worker
COPY ./src ./src

# Define environment variable
# ENV FLASK_APP=flask_backend/app.py

# Run flask when the container launches
# CMD ["flask", "run", "--host=0.0.0.0"]
CMD ["python", "-m", "flask", "--app", "flask_backend.app", "run", "--host=0.0.0.0"]
