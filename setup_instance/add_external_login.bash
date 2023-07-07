#!/bin/bash

UNAME=humza.hemani
UPLOAD_DIR=julia_car_tcells

useradd -m -d /home/$UPLOAD_DIR $UNAME
passwd $UNAME

sed -i "s/PasswordAuthentication no/PasswordAuthentication yes/" /etc/ssh/sshd_config
systemctl restart sshd
