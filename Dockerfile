# Use the official Python image as base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

 # Install gcc and other build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
 gcc \
 python3-dev \
 libpq-dev \
 libpcap-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the application port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]