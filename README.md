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
