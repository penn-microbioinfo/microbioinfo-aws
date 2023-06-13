#!/bin/bash

# Setup neovim
curl -sL install-node.vercel.app/lts | sudo bash # Install node.js for coc
wget https://github.com/neovim/neovim/releases/download/nightly/nvim.appimage -P $HOME/pkgs/.
chmod u+x $HOME/pkgs/nvim.appimage
sudo mv $HOME/pkgs/nvim.appimage /usr/bin/nvim.appimage
sudo rm /usr/bin/vim
sudo ln -s /usr/bin/nvim.appimage /usr/bin/vim
git clone --depth 1 https://github.com/wbthomason/packer.nvim $HOME/.local/share/nvim/site/pack/packer/start/packer.nvim
git clone https://github.com/penn-microbioinfo/microbioinfo-aws.git $HOME/microbioinfo-aws
mkdir -p $HOME/.config
ln -s $HOME/microbioinfo-aws/setup_instance/config/nvim $HOME/.config/.
