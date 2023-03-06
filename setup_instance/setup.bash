#!/bin/bash

mkdir -p $HOME/mnt/general
mkdir -p $HOME/pkgs

# Install ubuntu packages - many of these required by R packages
sudo apt update
sudo apt install -y r-base-core libhdf5-dev tmux libfontconfig1-dev libharfbuzz-dev libfribidi-dev libfreetype6-dev libpng-dev libtiff5-dev libjpeg-dev libxml2-dev zsh

#Change shell to zsh
sudo chsh ubuntu /usr/bin/zsh
rm $HOME/.zshrc
ln -s $HOME/microbioinfo-aws/setup_instance/config/zshrc $HOME/.zshrc

# Setup neovim
wget https://github.com/neovim/neovim/releases/download/nightly/nvim-linux64.deb -P $HOME/pkgs/.
sudo apt install $HOME/pkgs/nvim-linux64.deb
sudo rm /usr/bin/vim
ln -s /usr/bin/nvim /usr/bin/vim
git clone --depth 1 https://github.com/wbthomason/packer.nvim\\n $HOME/.local/share/nvim/site/pack/packer/start/packer.nvim
git clone https://github.com/penn-microbioinfo/microbioinfo-aws.git $HOME/.
mkdir -p $HOME/.config
ln -s $HOME/microbioinfo-aws/setup_instance/config/nvim $HOME/.config/nvim
vim "+PackerInstall" "+q" tmp

# Create the expected R_USER_LIBS directory so that 
r_user_libs_path=$(cat /etc/R/Renviron | grep R_LIBS_USER | grep -v '^#' | grep -Eo "['][^']+[']" | sed "s/'//g")
mkdir -p $r_user_libs_path

# Install Seurat, tidyverse, and other R dependencies
Rscript install_R_deps.R

echo "Shell has been changes to zsh and config copied to ~/.zshrc - restart session for changes to take effect."
