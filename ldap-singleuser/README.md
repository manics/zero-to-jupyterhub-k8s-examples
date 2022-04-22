# LDAP with modified username and Git author in singleuser server

Install an example OpenLDAP server with test data:
```
git clone https://github.com/manics/helm-test-openldap
helm upgrade --install ldap ./helm-test-openldap --wait
```

Fetch the JupyterHub Helm chart
```
helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
```

Check the [`jupyterhub.yml` configuration](./jupyterhub.yml) to see how the `LDAPAuthenticator` has been extended so that `pre_spawn_start` passes LDAP attributes to the spawned singleuser server by setting environment variables.

Install JupyterHub:
```
helm upgrade --cleanup-on-fail --install jupyterhub jupyterhub/jupyterhub --version=1.1.3-n423.hae439dba --values jupyterhub.yml --wait
```

Check everything is running:
```
kubectl get pods
```

Login with one of the test LDAP users, e.g. user:`zoidberg` password:`zoidberg`.
Open a Jupyter terminal.
You should see the username is `zoidberg` instead of the default `jovyan`.
If you run `git commit` you should see the author name and email are taken from LDAP.
