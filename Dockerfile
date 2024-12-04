# Use a lightweight Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /

# Copy everything from the current directory to the container's /app directory
COPY . /

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Expose port 5000 for the Flask application
EXPOSE 5000

# Run the Flask app using Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:gunicorn_app"]

