# Set the base image to use
FROM python:3.9-slim-buster

# set working directory
WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the script into the container
COPY autoscaler.py .

# Start the script when the container starts
CMD ["python", "-m", "autoscaler"]