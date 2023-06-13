kubectl -n kubernetes-dashboard create token admin-user
# Status

Currently a refactor of my drogon home lab to utilzie kubernetes and skaffold.

> This is only partially functional and until V1 is reached will continue to use the old repository drogon (private).

This is a monorepo that does a few things.

It runs drogon server (my home server)
It runs my ephemeral staging enviroment
It runs my private tools cluster

## TODO

- [ ] Add traefik and prometheus metrics scraping to prom:

```yaml
- job_name: 'prometheus'
    scrape_interval: 5s
    static_configs:
      - targets: ['localhost:9090']

- job_name: 'traefik'
scrape_interval: 5s
static_configs:
    - targets: ['infra_traefik:8080']
```

- [ ] create deployment for brainz
- [ ] create deployment for chain

## Persistent Volumes using [Democratic-CSI](https://github.com/democratic-csi/democratic-csi)

**Storage Class Names**
- reclaimPolicy: DESTROY
    - iscsi-ephemeral
    - nfs-ephemeral
-  reclaimPolocy: 
- nfs-persistent
- iscsi-persistent

> The values is kinda a pita to get and can be generated via the following snippet
```shell
wget https://raw.githubusercontent.com/democratic-csi/charts/master/stable/democratic-csi/examples/freenas-nfs.yaml -O - | sed '/INLINE/,$d' > nfs.yaml
wget https://raw.githubusercontent.com/democratic-csi/democratic-csi/master/examples/freenas-api-nfs.yaml -O - | sed -e 's/^/    /g' >> nfs.yaml
wget https://raw.githubusercontent.com/democratic-csi/charts/master/stable/democratic-csi/examples/freenas-iscsi.yaml -O - | sed '/INLINE/,$d' > iscsi.yaml
wget https://raw.githubusercontent.com/democratic-csi/democratic-csi/master/examples/freenas-api-iscsi.yaml -O - | sed -e 's/^/    /g' >> iscsi.yaml
```

## Dynamic Proxy with [Traefik](https://github.com/traefik/traefik-helm-chart)


Provides **IngressRoute** CRD for dynamic proxy provisioning

## kube-dashboard

Installed VIA helm

## [kube-prometheus-stack](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack)

[values](https://github.com/prometheus-community/helm-charts/blob/main/charts/kube-prometheus-stack/values.yaml)

Installed VIA helm


