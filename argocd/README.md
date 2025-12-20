# Deploy JupyterHub with ArgoCD

The spins up ArgoCD, and configures it to deploy JupyterHub using the [_app of apps_ pattern](https://argo-cd.readthedocs.io/en/release-3.3/operator-manual/declarative-setup/#app-of-apps):

- A root application is manually added to ArgoCD, which references a Git repository
- ArgoCD continually polls the Git repository and synchronises all Applications, in this case just JupyterHub

## Prerequisites

You must have a Kubernetes cluster with a [default ingress controller](https://kubernetes.io/docs/concepts/services-networking/ingress/), and a hostname pointing to the ingress.

If you are using a default K3s installation you should increase the number of inotify instances/watches:

```sh
sysctl -w fs.inotify.max_user_instances=8192
sysctl -w fs.inotify.max_user_watches=524288
```

## ArgoCD

Install ArgoCD

```sh
helm --namespace=argocd upgrade --create-namespace --install argocd --repo=https://argoproj.github.io/argo-helm argo-cd --version=9.1.9 -f argocd.yml --wait
```

Optionally install the ArgoCD CLI.
This is needed to set parameters without committing changes to Git, you can skip this if you fork this repository and Git commit your ingress host.

```sh
# Lookup the ArgoCD version e.g. v3.2.2 (Helm chart version is different from appVersion)
ARGOCD_VERSION=$(kubectl -nargocd get deploy/argocd-server -ojsonpath='{.metadata.labels.app\.kubernetes\.io/version}')
# Architecture e.g. amd64
CLI_ARCH=$(uname -m | sed -e 's/x86_64/amd64/' -e 's/aarch64/arm64/')

sudo curl -sfSL https://github.com/argoproj/argo-cd/releases/download/$ARGOCD_VERSION/argocd-linux-${CLI_ARCH} -o /usr/local/bin/argocd
sudo chmod a+x /usr/local/bin/argocd
```

## Optional: fork repository

If you want to store _all_ configuration in Git (recommended in production):

1. Fork this repository.
2. Edit [`apps/application-jupyterhub.yaml`](apps/application-jupyterhub.yaml), change `jupyterhub.example.org` to your ingress hostname.
3. Commit and push your changes
4. Edit [`root-application.yaml`](root-application.yaml), change `repoURL: https://github.com/manics/zero-to-jupyterhub-k8s-examples.git` and `targetRevision: main` to your forked repository and branch.

```sh
sed -i -e "s%/manics/zero-to-jupyterhub-k8s-examples%/${GITHUB_REPOSITORY}%" -e "s%main%${GITHUB_REVISION}%" root-application.yaml
git diff
```

## Deploy JupyterHub

Create the root application

```sh
kubectl apply -f root-application.yaml
```

If you did not fork this repository and configure the ingress you can instead [set a parameter](https://argo-cd.readthedocs.io/en/release-3.3/user-guide/commands/argocd_app_set/).
You will need to setup a port-forward to access the ArgoCD service and login.

```sh
kubectl -n argocd port-forward svc/argocd-server 8080:443 &
sleep 1
```

```sh {retry=3}
ARGOCD_PASSWORD=$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)
argocd login localhost:8080 --username=admin --password="$ARGOCD_PASSWORD" --insecure

argocd app set jupyterhub -p ingress.hosts[0]=<k8s-hostname>
```

## Test

Wait for ArgoCD to deploy JupyterHub:

```sh
sleep 20
kubectl -nargocd get applications

kubectl -nargocd wait --for=jsonpath="{.status.health.status}"=Healthy application/jupyterhub --timeout=300s

kubectl -ndefault rollout status deployment/hub
kubectl -ndefault rollout status deployment/proxy
```

Open `http://<k8s-hostname>/` in your browser.
This uses the dummy authenticator, log in with username `demo` and any password.

## Updates

If you forked this repository you can modify your JupyterHub configuration, push it to Git, and ArgoCD should automatically deploy your changes.
