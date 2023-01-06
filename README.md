# microbioinfo-aws
Repo with information on default aws setups.

Setup AWS storage volume:

```
sudo lsblk --output NAME,TYPE,SIZE,FSTYPE,MOUNTPOINT,LABEL
to find the extra space (not sure if always in same space?) and format with:
sudo sudo mkfs -t ext4 /dev/nvme1n1
and mount with:
sudo mount /dev/nvme1n1 mnt
sudo chown ubuntu mnt
```

### Setting up AWS CLI through Penn

1. Contact Penn IT Director James Renphro (jrenfro@isc.upenn.edu) for access to a BitBucket repository containing python scripts for authenticating into Penn Shiboleth (i.e., 2-factor auth) and AWS services.

2. Clone the necessary repositories to your local machine.
