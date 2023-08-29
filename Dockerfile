# syntax=docker/dockerfile:1.2
FROM python:3.11.3
ENV PYTHONUNBUFFERED True

# Set the working directory
WORKDIR /app

# Copy the local code to the container image.
COPY ./challenge /app

# Copy the requirements.txt to the container image.
COPY requirements.txt /app

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variables
ENV PORT=8080
EXPOSE 8080

# Run the application
CMD uvicorn api:app --host 0.0.0.0 --port $PORT
