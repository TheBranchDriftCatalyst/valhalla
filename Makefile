.PHONY: lint setup-cluster delete-cluster dev clean

lint:
	@kube-score score
	@kubescan scan

setup-cluster:
	@minikube start
	@minikube addons enable metrics-server

delete-cluster:
	@minikube delete

dev:
	@sudo skaffold dev

clean:
	@$(MAKE) delete-cluster
	@$(MAKE) setup-cluster
