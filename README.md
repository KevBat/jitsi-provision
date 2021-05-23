# jitsi-provision
This playbook will provision a DO droplet, update the existing DNS A record, and install Jitsi Meet.

Pre-requirements:

1. API key created for your Digital Ocean account

2. SSH key created from the machine you will ssh from

3. Domain that will be the used for the DNS record and to configure Jitsi Meet

4. Precreated DNS records for domain.

5. DNS A record ID that the script will replace with the IP of your new VM

6. An email account for Let's Encrypt certificate generation.

Add in these values to 'run_playbook.sh' and run the script

TODO:

Lock down Jitsi configuration access controls.

Python script creates networking requirements if starting from nothing (currently set up to replace an existing DNS record e.g. you want Jitsi server only online for a few hours then destroyed but don't delete DNS records. VMs cost money y0 $$$)
