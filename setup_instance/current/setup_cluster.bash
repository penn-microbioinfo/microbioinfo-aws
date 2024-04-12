#!/bin/bash

USER=ubuntu
CLUSTHOME=/shared-ebs
MBIAWS=$CLUSTHOME/microbioinfo-aws

if [ ! -d $MBIAWS ]; then
    git clone git@github.com:penn-microbioinfo/microbioinfo-aws.git $MBIAWS || exit
fi

ln -s $MBIAWS/setup_instance/config/cluster_source_me.bash $CLUSTHOME/source_me.bash

# Does not work with user logged in :/
#sudo usermod -d /shared-ebs $USER

sudo usermod -s /bin/zsh $USER
cat << EOF >> $HOME/.zshrc 
source $CLUSTHOME/source_me.bash
EOF

ln -sf $MBIAWS/setup_instance/config/zshrc $CLUSTHOME/.zshrc
bash $MBIAWS/setup_instance/current/install_cli_tools.bash
