# Applications

To support this demonstration architecture there are a few different applications that have been made to run various parts of the interaction with hardware and cloud services.

- **GoPro Control** [Python] - Connects to a GoPro's wireless access point, records a video, downloads the video.  Deploys as a Podman container via Quadlet, triggered at `:8181/recordgopro`
- **Drone Control** [Python] - Connects to a DJI Tello's wireless acesss point, streams and records a video...most of the time.  Deploys as a Podman container, triggered at `:8080/scan`
- **S3 Shipper** [Python] - Uploads locally accessible files to an S3 bucket.  Deploys to Microshift, https://s3-shipper-s3-shipper.apps.egd.kemo.edge, path `/upload` with `bucket`, `filename`, `filepath` as POST form data inputs.
- **Symphony** [Python] - A frontend application that will glue the various other workloads in a somewhat nice interface.  Deploys to Microshift, https://symphony-symphony.apps.egd.kemo.edge
- **Wifi Patrol** [Bash] - Uses `nmcli` in order to agressively scan for a list of wireless access points and connect to them.  Has paired Ansible Automation to deploy to a Linux host.

