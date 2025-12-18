# LDAP with modified username and Git author in singleuser server

## Prerequisites

You must have a Kubernetes cluster with a [default ingress controller](https://kubernetes.io/docs/concepts/services-networking/ingress/), and a hostname pointing to the ingress.

## Configuration

Edit [`jupyterhub.yml`](./jupyterhub.yml), replacing `%K8S_HOSTNAME%` with your hostname.

E.g.

```
sed -i 's/%K8S_HOSTNAME%/<k8s-hostname>/g' jupyterhub.yml
```

The main custom configuration in [`jupyterhub.yml` configuration](./jupyterhub.yml) is:

- Extending `LDAPAuthenticator` so that `pre_spawn_start` passes LDAP attributes to the spawned singleuser server using environment variables.
- Disabling the default dynamic user storage which is mounted at `/home/jovyan`, and instead mounting dynamically created volumes at `/home/{username}`

## LDAP server

Install an example OpenLDAP server with test data:

```
helm upgrade --install ldap --repo=https://www.manicstreetpreacher.co.uk/helm-test-openldap/ test-openldap --version=0.2.1 --wait
```

## JupyterHub

Check the [`jupyterhub.yml` configuration](./jupyterhub.yml) to see all the customisations.

Install JupyterHub:

```
helm upgrade --install jupyterhub --repo=https://hub.jupyter.org/helm-chart/ jupyterhub --version=4.3.2 --values jupyterhub.yml --wait
```

Check everything is running:

```
kubectl get pods
```

Login with one of the test LDAP users, e.g. user:`zoidberg` password:`zoidberg`.
Open a Jupyter terminal.
You should see the username is `zoidberg` instead of the default `jovyan`.
If you run `git commit` you should see the author name and email are taken from LDAP.
