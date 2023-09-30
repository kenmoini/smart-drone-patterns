# MicroShift Integration

This document will cover how to integrate Microshift on the EGD with ArgoCD, ACM, and ACS easily.

## Setup - Log into EGD Microshift

```bash=
## Create the ServiceAccount, Secret Token, and ClusterRoleBinding

cat <<EOF | oc apply -n kube-system  -f -
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: microshift-integration
secrets:
  - name: microshift-integration
---
apiVersion: v1
kind: Secret
metadata:
  name: microshift-integration
  annotations:
    kubernetes.io/service-account.name: microshift-integration
type: kubernetes.io/service-account-token
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: microshift-integration-cluster-admin
subjects:
  - kind: ServiceAccount
    name: microshift-integration
    namespace: kube-system
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
EOF
```

```bash=
## Get the Token & CA
#MICROSHIFT_CA=$(oc get -n kube-system secret/microshift-integration -o jsonpath='{.data.ca\.crt}')

MICROSHIFT_NAME="egd-microshift"
MICROSHIFT_ENDPOINT="https://api.egd.kemo.edge:6443"
MICROSHIFT_TOKEN=$(oc get -n kube-system secret/microshift-integration -o jsonpath='{.data.token}' | base64 -d)

cat > rhacm-importer.yml <<EOF
---
apiVersion: v1
kind: Namespace
metadata:
  name: ${MICROSHIFT_NAME}
---
apiVersion: cluster.open-cluster-management.io/v1
kind: ManagedCluster
metadata:
  name: ${MICROSHIFT_NAME}
  labels:
    name: ${MICROSHIFT_NAME}
    cloud: auto-detect
    vendor: auto-detect
    cluster.open-cluster-management.io/clusterset: microshift
  annotations: {}
spec:
  hubAcceptsClient: true
---
apiVersion: v1
kind: Secret
metadata:
  name: auto-import-secret
  namespace: ${MICROSHIFT_NAME}
data:
  #autoImportRetry: "$(echo 2 | base64)"
  kubeconfig: "$(cat /root/.kube/remote-config | base64 -w0)"
type: Opaque
---
apiVersion: agent.open-cluster-management.io/v1
kind: KlusterletAddonConfig
metadata:
  name: ${MICROSHIFT_NAME}
  namespace: ${MICROSHIFT_NAME}
spec:
  clusterName: ${MICROSHIFT_NAME}
  clusterNamespace: ${MICROSHIFT_NAME}
  clusterLabels:
    name: ${MICROSHIFT_NAME}
    cloud: Edge
    vendor: Microshift
    cluster.open-cluster-management.io/clusterset: microshift
  applicationManager:
    enabled: true
    argocdCluster: true
  policyController:
    enabled: true
  searchCollector:
    enabled: false
  certPolicyController:
    enabled: false
  iamPolicyController:
    enabled: false
EOF

cat > gitops-importer.yml <<EOF
---
apiVersion: v1
kind: Secret
metadata:
  name: ${MICROSHIFT_NAME}-cluster-secret
  namespace: openshift-gitops
  labels:
    argocd.argoproj.io/secret-type: cluster
    clusterId: ${MICROSHIFT_NAME}
type: Opaque
stringData:
  name: ${MICROSHIFT_NAME}
  server: ${MICROSHIFT_ENDPOINT}
  config: |
    {
      "tlsClientConfig": {
        "insecure": true
      },
      "bearerToken": "${MICROSHIFT_TOKEN}"
    }
EOF
```

Next log into the OCP hub and apply those YAML files.