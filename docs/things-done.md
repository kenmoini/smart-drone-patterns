# Things that were done to set up this demo

- Install RHEL on an Edge Gateway Device (OnLogic CL250)
- Configure the EGD to run DNS, NTP, disabled firewalld and SELinux (lol)
- Manually fixed DNS on the EGD as mentioned in the README.md Known Issues section
- Install Microshift on that EGD
- Install RHEL on an Arm Edge Server (Ampere Altra Development Platform, 128 Core)
- Install SNO on that Arm Edge Server via Libvirt
- Generate SSL Certificates for the SNO cluster and Microshift, for Microshift added them to `/opt/tls` and `chown 1001:0 /opt/tls/api.egd.kemo.edge.* && chmod ug+r /opt/tls/api.egd.kemo.edge.*` for the apps and the router-certs-defaults Secret as detailed in `patching-microshift-ingress.md`
- Bootstrapped the SNO instance as detailed in `edge-cluster-gitops.md`
- Integrated the Microshift instance with ACM and ArgoCD as detailed in microshift-integration.md