# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app code to the container
COPY . .

# Set the environment variable for Flask
ENV PORT=8080

# Expose the port the app runs on
EXPOSE 8080

# Run the Flask app on container startup
CMD ["python", "server.py"]
