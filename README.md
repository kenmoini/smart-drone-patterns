# Smart Done Patterns

## Edge Bridge/Gateway Setup

- Install RHEL 8, leave a blank Volume Group to use for Microshift LVM: https://access.redhat.com/documentation/en-us/red_hat_build_of_microshift/4.12/html/installing/microshift-install-rpm#microshift-install-rpm-preparing_microshift-install-rpm
- Subscribe System
- Add non-root user
- Set sudoers to sudo without use of passwords
- Run `ansible-playbook -i inventory playbooks/general-setup.yml`
- Run `ansible-playbook -i inventory playbooks/setup-router.yml`
- Run `ansible-playbook -i inventory playbooks/setup-microshift.yml`
