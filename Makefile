.PHONY: setup-cluster delete-cluster dev prod token-admin clean

setup-cluster:
	minikube start --profile local

delete-cluster:
	minikube delete --profile local

dev:
	sudo skaffold dev --port-forward -p truenas-storage-classes;

prod:
	sudo skaffold deploy --port-forward -p truenas-storage-classes,ddns;

token-admin:
	kubectl -n kubernetes-dashboard create token admin-user

clean:
	make delete-cluster
	make setup-cluster
