# Known Issues

## EGD DNS Resolution

If running DNS services on the EGD, NetworkManager will likely not set the right DNS configuration.  This can cause issues with resolution of external services as well as issues with Microshift's DNS.

To fix this, make a file `/etc/NetworkManager/conf.d/99-no-dns.conf`:

```
[main]
dns=none
```

Restart NetworkManager `systemctl restart NetworkManager`

Then edit the `/etc/resolv.conf` file to look like this:

```
search kemo.edge
nameserver 192.168.99.10
```

The nameserver IP must be the IP address of the EGD.
