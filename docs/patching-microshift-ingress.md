# Patching the Microshift Ingress Certificate

```bash=
# Just replace it because it'll revert on reboot
oc get secret -n openshift-ingress router-certs-default -o yaml > router-certs-default.bak.yml
oc delete secret -n openshift-ingress router-certs-default
oc create secret tls router-certs-default --cert=api.egd.kemo.edge.bundle.cert.pem --key=api.egd.kemo.edge.key.pem -n openshift-ingress

# old method
oc create secret tls ingress-certificate --cert=api.egd.kemo.edge.bundle.cert.pem --key=api.egd.kemo.edge.key.pem -n openshift-ingress
# set the volume secretName to ingress-certificate from router-default-certificate
oc edit deployment -n openshift-ingress router-default
```