# Use the official Python image
FROM python:3.11

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY ./celery_worker/requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY ./celery_worker ./celery_worker
COPY ./src ./src

# Command to run the Celery worker
CMD ["celery", "-A", "celery_worker.celery_worker", "worker", "--loglevel=info"]
