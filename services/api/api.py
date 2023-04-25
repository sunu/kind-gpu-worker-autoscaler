import json
import redis
from fastapi import FastAPI

app = FastAPI()

# create a Redis client and get the queue
r = redis.Redis(host='redis', port=6379, db=0)

@app.post('/job')
async def create_job(platform: str, length: int):
    if platform not in ['cpu', 'gpu']:
        return {'message': 'Invalid platform'}

    # create the job payload as a dictionary
    job_data = {'matrix_length': length}

    # add the job to the Redis queue
    r.rpush(platform, json.dumps(job_data))

    return {'message': 'Job created successfully'}
