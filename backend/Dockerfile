# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY app/requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY app/ /app/

# Expose the port the app runs on
EXPOSE 5000

ENV FLASK_APP=/app/main.py

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]