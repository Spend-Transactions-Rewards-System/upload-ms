# Base image
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the default port for the Flask app
EXPOSE 8080

# Start Gunicorn
CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:8080", "wsgi:app"]