#!//builds/bin/bash

SHARED_ROOT=/shared-ebs

cat $HOME/.bashrc $SHARED_ROOT/microbioinfo-aws/setup_instance/cluster.bashrc > a && mv a $HOME/.bashrc

#curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
#. ~/.nvm/nvm.sh
#nvm install 16

bash $SHARED_ROOT/microbioinfo-aws/setup_instance/neovim_setup.bash $SHARED_ROOT/microbioinfo-aws
