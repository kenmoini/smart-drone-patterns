# Patching the Microshift Ingress Certificate

```bash=
oc create secret tls ingress-certificate --cert=api.egd.kemo.edge.bundle.cert.pem --key=api.egd.kemo.edge.key.pem -n openshift-ingress

# set the volume secretName to ingress-certificate from router-default-certificate
oc edit deployment -n openshift-ingress router-default
```