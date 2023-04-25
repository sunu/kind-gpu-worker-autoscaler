import logging
import time
from kubernetes import client, config
import redis

logging.basicConfig(level=logging.INFO,)
logger = logging.getLogger(__name__)

# Load the in-cluster Kubernetes configuration
config.load_incluster_config()

# Create an instance of the Kubernetes API client
api_client = client.AppsV1Api()


def scale_deployment(name="gpu-worker", namespace="default"):
    # Get the deployment object
    deployment = api_client.read_namespaced_deployment(name, namespace)

    # Get the number of replicas from the deployment object
    replicas = deployment.spec.replicas

    target_replicas = get_target_replicas()

    if replicas != target_replicas:
        # Update the number of replicas
        deployment.spec.replicas = target_replicas

        # Update the deployment
        api_client.patch_namespaced_deployment(name, namespace, deployment)

        logger.info(f"Deployment {namespace}/{name} scaled to {target_replicas} replicas.")


def get_target_replicas():
    redis_client = redis.Redis(host='redis', port=6379, db=0)
    queue = "gpu"
    queue_length = redis_client.llen(queue)
    return 1 if queue_length > 0 else 0


def main():
    deployment_name = "gpu-worker"
    deployment_namespace = "default"
    logger.info(f"Starting autoscaler. Watching deployment {deployment_namespace}/{deployment_name}...")
    while True:
        try:
            scale_deployment(deployment_name, deployment_namespace)
        except Exception:
            logger.exception("Error while scaling deployment.")
        time.sleep(5)


if __name__ == '__main__':
    main()