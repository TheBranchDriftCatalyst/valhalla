kubectl -n kubernetes-dashboard create token admin-user
# Status

Currently a refactor of my drogon home lab to utilzie kubernetes + skaffold + helm.  Homelab hyper converged storage cluster.

> This is only partially functional and until V1 is reached will continue to use the old repository drogon (private).


## Roadmap/TOdo

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

# Upgrade and Deployment Checklist

Need to get this repo in a working state once that is done:
  - probably use nfs share mounts for now and move to democratic CSI later

## Persistent Volumes using [Democratic-CSI](https://github.com/democratic-csi/democratic-csi)

**Storage Class Names**
- nfs-persistent
- iscsi-persistent

> The values is kinda a pita to get and can be generated via the following snippet

### Democratic CSI config values

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


# PITA

Skaffold kinda sucks at handling multiple skaffold files.  They dont give you really good options ofr splitting up the files.  The main issue is that skaffold only runs the base most manifests.rawYaml NOT the dependent ones....This is... stupid... and they dont intend to fix it.  Not really sure how to use skaffold properly in the patter i am but for now we will run skaffold X frigging times for every damn service....

runDistro 

ls -a **/skaffold.yaml | sort



