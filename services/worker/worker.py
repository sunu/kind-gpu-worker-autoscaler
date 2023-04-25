import tensorflow as tf
import time
import json
import redis
import logging
import sys


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def worker(platform="cpu"):
    # Connect to Redis
    redis_client = redis.Redis(host='redis', port=6379, db=0)
    is_gpu = tf.test.is_gpu_available()
    queue = platform

    logger.info(f"Starting worker. Listening to queue {queue}...")


    while True:
        # get task from redis queue
        logger.debug("Waiting for task...")
        task = redis_client.blpop(queue, timeout=5)
        if task:
            task = json.loads(task[1].decode('utf-8'))
            logger.info(f"Task: {task}")

            # Set up TensorFlow to use GPU
            if is_gpu:
                physical_devices = tf.config.list_physical_devices('GPU')
                tf.config.experimental.set_memory_growth(physical_devices[0], True)

            # Generate random matrices
            matrix_size = int(task['matrix_length'])
            matrix_a = tf.random.normal([matrix_size, matrix_size])
            matrix_b = tf.random.normal([matrix_size, matrix_size])
            logger.info(f"Matrix size: {matrix_size} x {matrix_size}")

            if is_gpu:
                # Perform matrix multiplication on GPU
                start_time = time.time()
                with tf.device('/GPU:0'):
                    result_gpu = tf.matmul(matrix_a, matrix_b)
                gpu_time = time.time() - start_time

                # Print results and timing information
                logger.info(f"GPU time: {gpu_time:.4f} seconds")
            else:
                # Perform matrix multiplication on CPU
                start_time = time.time()
                result_cpu = tf.matmul(matrix_a, matrix_b)
                cpu_time = time.time() - start_time

                # Print results and timing information
                logger.info(f"CPU time: {cpu_time:.4f} seconds")
        else:
            logger.debug("No task available. Sleeping...")
            time.sleep(5)


if __name__ == '__main__':
    platform = sys.argv[1] if len(sys.argv) > 1 else "cpu"
    worker(platform=platform)