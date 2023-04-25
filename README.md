# Kind GPU Worker Autoscaler Example

This example shows how to scale a GPU worker deployment to zero when there are no pending jobs and scale it back up when there are pending jobs.

## Prerequisites

* [Kind fork with GPU support](https://jacobtomlinson.dev/posts/2022/quick-hack-adding-gpu-support-to-kind/)
* Make sure you have a working `kubectl` installation
* Make sure the host machine has a GPU and the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker) installed
* There might be some other things I've forgotten

## Running

1. Create a Kind cluster with GPU support
    ```bash
    make create-cluster
    ```
2. Build the docker images
    ```bash
    make build-images
    ```
3. Load the docker images into the Kind cluster
    ```bash
    make load-images
    ```
4. Install NVIDIA GPU operator in the cluster
    ```bash
    make install-nvidia-operator
    ```
5. Deploy the api, worker and autoscaler
    ```bash
    make deploy-all
    ```
6. Port forward the api to localhost
    ```bash
    make port-forward-api
    ```
7. Submit a job to the api on localhost:9091. Watch the pods and logs to see the autoscaler in action.
8. Delete the cluster when you're done
    ```bash
    make delete-cluster
    ```

## Notes

* The api is a simple fastapi app that queues a matrix length into either the `cpu` or `gpu` redis queue.
* `cpu-worker` listens to the `cpu` queue and multiplies two random matrices of dimension `length x length` together on the CPU.
* Similarly `gpu-worker` listens to the `gpu` queue and multiplies two random matrices of dimension `length x length` together on the GPU.
* The `autoscaler` is a simple python script that uses the Kubernetes API to scale the `gpu-worker` deployment to zero when there are no pending jobs in the `gpu` redis queue and scales `gpu-worker` back up when there are jobs available again in the `gpu` redis queue.
