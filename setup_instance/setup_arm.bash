#!/bin/bash

. SETUP_VARS.bash

mkdir -p $HOME/mnt/general
mkdir -p $HOME/pkgs

# Install ubuntu packages - many of these required by R packages
sudo apt update
sudo apt install -y r-base-core libhdf5-dev tmux libfontconfig1-dev libharfbuzz-dev \
libfribidi-dev libfreetype6-dev libpng-dev libtiff5-dev libjpeg-dev libxml2-dev zsh sysstat \
python3.10-venv libcurl4-openssl-dev neovim

# synonymize python with python3
sudo ln -fs /usr/bin/python3 /usr/bin/python

#Change shell to zsh
sudo chsh -s /usr/bin/zsh ubuntu
rm $HOME/.zshrc
ln -s $HOME/microbioinfo-aws/setup_instance/config/zshrc $HOME/.zshrc

# Install Seurat, tidyverse, and other R dependencies
if [ "$INSTALL_R_DEPS" == "yes" ]; then	
	
    # Create the expected R_USER_LIBS directory so that 
    r_user_libs_path=$(cat /etc/R/Renviron | grep R_LIBS_USER | grep -v '^#' | grep -Eo "['][^']+[']" | sed "s/'//g")
    mkdir -p $(echo $r_user_libs_path | sed 's#~#'$HOME'#')

    Rscript install_R_deps.R
fi
echo "Shell has been changed to zsh and config copied to ~/.zshrc - restart session for changes to take effect."
