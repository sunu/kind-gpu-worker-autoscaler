# base image
FROM python:3.9-slim-buster

# set working directory
WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy app code
COPY . .

# expose port
EXPOSE 9090

# start app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "9090"]
