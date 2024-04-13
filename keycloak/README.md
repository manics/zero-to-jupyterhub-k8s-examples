# Keycloak

## Prerequisites

You must have a Kubernetes cluster with a [default ingress controller](https://kubernetes.io/docs/concepts/services-networking/ingress/), and a hostname pointing to the ingress.

## Configuration

Edit [`jupyterhub.yml`](./jupyterhub.yml) and [`keycloak.yml`](./keycloak.yml), replacing `%K8S_HOSTNAME%` with your hostname.
This host must be reachable inside the cluster as well as outside, as JupyterHub needs to connect to Keycloak using a hostname that matches the hostname used by the client.

E.g.

```
sed -i 's/%K8S_HOSTNAME%/<k8s-hostname>/g' jupyterhub.yml keycloak.yml
```

## Keycloak

Install Keycloak with a default admin user

```
helm upgrade --install keycloak oci://registry-1.docker.io/bitnamicharts/keycloak --version=21.0.0 -f keycloak.yml --wait
```

Use the [python-keycloak](https://github.com/marcospereirampj/python-keycloak) module to create a user and OAuth client.

```
python3 -mvenv ./venv
. ./venv/bin/activate
pip install python-keycloak
python setup-keycloak.py --external-host http://<k8s-hostname>
```

## JupyterHub

Fetch the JupyterHub Helm chart

```
helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
```

Install JupyterHub:

```
helm upgrade --install jupyterhub jupyterhub/jupyterhub --version=3.3.7 --values jupyterhub.yml --wait
```

Check everything is running:

```
kubectl get pods
```

Open `http://<k8s-hostname>/jupyter/` in your browser.
Login with the Keycloak user created by the `setup-keycloak.py` script, e.g. user:`example@example.com` password:`secret`.
