# Edge OpenShift Cluster GitOps Bootstrapping

```bash=
# Install OpenShift GitOps
oc apply -k openshift/bootstrap/openshift-gitops/install-operator/

# Configure OpenShift Gitops
oc apply -k openshift/bootstrap/openshift-gitops/operator-init/
```

This will:

- Install the OpenShift GitOps Operator
- Instanciate the Operator with some helpful modifications
- Configure the Operator with:
  - AppProjects
  - Repositories
  - AppOfApps
