# LDAP with modified username and Git author in singleuser server

Install an example OpenLDAP server with test data:
```
helm repo add test-openldap https://www.manicstreetpreacher.co.uk/helm-test-openldap/
helm upgrade --install ldap test-openldap/test-openldap --wait
```

Fetch the JupyterHub Helm chart
```
helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
```

Check the [`jupyterhub.yml` configuration](./jupyterhub.yml) to see all the customisations.

Install JupyterHub:
```
helm upgrade --cleanup-on-fail --install jupyterhub jupyterhub/jupyterhub --version=1.1.3-n612.hf25e8f00 --values jupyterhub.yml --set 'ingress.hosts[0]'=<k8s-hostname> --wait
```

Check everything is running:
```
kubectl get pods
```

Login with one of the test LDAP users, e.g. user:`zoidberg` password:`zoidberg`.
Open a Jupyter terminal.
You should see the username is `zoidberg` instead of the default `jovyan`.
If you run `git commit` you should see the author name and email are taken from LDAP.


## Configuration
The main custom configuration in [`jupyterhub.yml` configuration](./jupyterhub.yml) is:
- Extending `LDAPAuthenticator` so that `pre_spawn_start` passes LDAP attributes to the spawned singleuser server using environment variables.
- Disabling the default dynamic user storage which is mounted at `/home/jovyan`, and instead mounting dynamically created volumes at `/home/{username}`
