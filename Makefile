create-cluster:
	kind create cluster --config cluster.yaml

build-images:
	docker build -t autoscale-gpu-worker -f services/worker/Dockerfile.gpu services/worker
	docker build -t autoscale-cpu-worker services/worker
	docker build -t autoscale-api services/api
	docker build -t autoscale-autoscaler services/autoscale

load-images:
	kind load docker-image autoscale-gpu-worker autoscale-cpu-worker autoscale-api autoscale-autoscaler -n gpu-test

install-gpu-operator:
	helm install nvidia/gpu-operator --wait --generate-name --create-namespace -n gpu-operator --set driver.enabled=false

deploy-all:
	kubectl apply -f k8s/

delete-cluster:
	kind delete cluster --name gpu-test

port-forward-api:
	kubectl port-forward svc/api-service 9091:9090