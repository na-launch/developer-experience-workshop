# Use an official Python runtime as a parent image (we won't use the Red Hat UBI as this is a very fast test)
FROM python:3.9-slim

# Set the working directory to /projects
WORKDIR /projects

# Copy requirements.txt into the container
COPY requirements.txt /projects/requirements.txt

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . /projects

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable (optional, you can override this at runtime)
ENV countryCode=EN

# Run the app using uvicorn when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
