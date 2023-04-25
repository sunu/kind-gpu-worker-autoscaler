# Use the official TensorFlow 2.12.0 Docker image
FROM tensorflow/tensorflow:2.12.0

# set working directory
WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the script into the container
COPY worker.py .

# Start the script when the container starts
CMD ["python", "-m", "worker"]
