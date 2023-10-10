# Smart Edge Patterns

This repository will demonstrate how to leverage AI/DS/ML workflows around an Edge architecture.  It consists of:

- An Edge Gateway Device that:
  - Acts as a wireless bridge for a GoPro and/or Drone
  - Runs Microshift and Podman, automated with Ansible
  - Serves the hardware control software
  - Ships video files to an Edge OpenShift instance
- A Single Node OpenShift on Arm instance that:
  - Uses LVM Operator for storage
  - Has automated etcd defragmentation (thank you Gerald Nunn)
  - Is bootstrapped with OpenShift GitOps
  - Runs Red Hat Advanced Cluster Manager, AMQ Streams, NFD+GPU Operators, Minio S3 Object Store, Tekton Pipelines, and Symphony

## Edge Bridge/Gateway Setup

- Install RHEL 8, leave a blank Volume Group to use for Microshift LVM: https://access.redhat.com/documentation/en-us/red_hat_build_of_microshift/4.12/html/installing/microshift-install-rpm#microshift-install-rpm-preparing_microshift-install-rpm
- Subscribe System
- Add non-root user
- Set sudoers to sudo without use of passwords
- Run `ansible-playbook -i inventory playbooks/general-setup.yml`
- Run `ansible-playbook -i inventory playbooks/setup-dns.yml`
- Run `ansible-playbook -i inventory playbooks/setup-microshift.yml`

## Assumptions

- You have some BS router like the Asus RT-ACRH13 that I'm using.
- You have an Edge Gateway Device (EGD) running RHEL that has an Ethernet Port as well as Wifi like the CL250 that I'm using
- You have a server running Single Node OpenShift like the Ampere Altra Development Platform that I'm using
- These 3 devices are connected together via Ethernet
- You have a DJI Tello drone
- You have a GoPro
- The EGD connects to the DJI Tello's broadcasted AP
- Your routed network is `192.168.99.0/24`, DHCP from `.100-254`, DNS domain is `kemo.edge`
- The EGD Ethernet port is set to `192.168.99.10/24` with a hostname of `egd.kemo.edge`
- The SNO instance is using `192.168.99.20/24` at `sno.kemo.edge`
- The EGD runs DNS services via BIND/Named `ansible-playbook -i inventory playbooks/setup-dns.yml`

## Special Thanks

I'm an absolute idiot and I could not have done any of this without the support from these fine folk - be it supporting debugging, guidance, or training content contributions, they were pivotal in putting this all together.  In no particular order, I'd like to thank:

- Raghuram Banda
- James Harmison
- Scott Hamilton
- Richard Hofmeister
- Nicole Ponticorvo
- Brian Kulawiak
- Deb Brubaker
- Sanjay Arora
- Peter Portante
- Tad Stephens
- James Walton
- Brian Addicks
- Dustin Trapani
- Fred Dri
- Devin Cazin

*And probably a few folk I forgot...<3 u all*