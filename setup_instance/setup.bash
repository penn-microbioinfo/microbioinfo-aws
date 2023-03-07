#!/bin/bash

mkdir -p $HOME/mnt/general
mkdir -p $HOME/pkgs

# Install ubuntu packages - many of these required by R packages
sudo apt update
sudo apt install -y r-base-core libhdf5-dev tmux libfontconfig1-dev libharfbuzz-dev libfribidi-dev libfreetype6-dev libpng-dev libtiff5-dev libjpeg-dev libxml2-dev zsh sysstat python3.10-venv

# synonymize python with python3
sudo ln -fs /usr/bin/python3 /usr/bin/python

#Change shell to zsh
sudo chsh -s /usr/bin/zsh ubuntu
rm $HOME/.zshrc
ln -s $HOME/microbioinfo-aws/setup_instance/config/zshrc $HOME/.zshrc

# Setup neovim
wget https://github.com/neovim/neovim/releases/download/nightly/nvim-linux64.deb -P $HOME/pkgs/.
sudo apt install $HOME/pkgs/nvim-linux64.deb
sudo rm /usr/bin/vim
sudo ln -s /usr/bin/nvim /usr/bin/vim
git clone --depth 1 https://github.com/wbthomason/packer.nvim $HOME/.local/share/nvim/site/pack/packer/start/packer.nvim
git clone https://github.com/penn-microbioinfo/microbioinfo-aws.git $HOME/.
mkdir -p $HOME/.config
ln -s $HOME/microbioinfo-aws/setup_instance/config/nvim $HOME/.config/.

# Create the expected R_USER_LIBS directory so that 
r_user_libs_path=$(cat /etc/R/Renviron | grep R_LIBS_USER | grep -v '^#' | grep -Eo "['][^']+[']" | sed "s/'//g")
mkdir -p $(echo $r_user_libs_path | sed 's#~#'$HOME'#')

# Install Seurat, tidyverse, and other R dependencies
Rscript install_R_deps.R

echo "Shell has been changed to zsh and config copied to ~/.zshrc - restart session for changes to take effect."
