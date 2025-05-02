# Use an official Python runtime as the base image.
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app inside the container.
WORKDIR /app

# Copy the requirements file into the container.
COPY requirements.txt .

# Install the required packages.
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container.
COPY . .

# Expose the port that the app runs on.
EXPOSE 5000

# Set the environment variable to tell Flask it's in production mode if needed (optional).
ENV FLASK_ENV production

# Set the default command to run the Flask app.
CMD ["flask", "run", "--host=0.0.0.0"]