#!/bin/bash

if [ -z $1 ]; then
	PATH_TO_MBIAWS=$HOME
else
	PATH_TO_MBIAWS=$1
fi

if [ ! -d $HOME/pkgs ]; then
	mkdir $HOME/pkgs
fi

if [ ! -d $HOME/.config ]; then
    mkdir $HOME/.config
fi

#Install node.js if needed
if ! which node; then
    curl -sL install-node.vercel.app/lts | sudo bash
fi

# Setup neovim
cd $HOME/pkgs
wget https://github.com/neovim/neovim/releases/download/stable/nvim-linux64.tar.gz
tar xvf  nvim-linux64.tar.gz
chmod u+x $HOME/pkgs/nvim-linux64/bin/nvim
sudo rm /usr/bin/vim
sudo ln -sf $HOME/pkgs/nvim-linux64/bin/nvim /usr/bin/vim
ln -sf $PATH_TO_MBIAWS/microbioinfo-aws/setup_instance/config/nvim $HOME/.config/.
