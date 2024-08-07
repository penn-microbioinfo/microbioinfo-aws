#!/bin/bash

if [ -z $PREFIX ]; then
	PREFIX=$HOME
fi

if [ ! -d $PREFIX ]; then
	mkdir -p $PREFIX
fi

if [ ! -d $PREFIX/pkgs ]; then
	mkdir $PREFIX/pkgs
fi

if [ ! -d $PREFIX/.config ]; then
    mkdir $PREFIX/.config
fi

if [ ! -d $PREFIX/bin ]; then
    mkdir $PREFIX/bin
fi

# Install node.js if needed
if ! which node; then
	curl -sL install-node.vercel.app/lts > install_node.sh
	sudo bash install_node.sh --prefix=${PREFIX}
	rm install_node.sh
fi

# Try to install venv for python (for based-pyright)
. /etc/os-release
case $ID in
    ubuntu) sudo NEEDRESTART_MODE=a apt-get install -y python3-venv
        ;;
esac

# Setup neovim
cd $PREFIX/pkgs
wget https://github.com/neovim/neovim/releases/download/nightly/nvim-linux64.tar.gz
tar xvf  nvim-linux64.tar.gz
chmod u+x $PREFIX/pkgs/nvim-linux64/bin/nvim
ln -sf $PREFIX/pkgs/nvim-linux64/bin/nvim $PREFIX/bin/nvim
git clone https://www.github.com/amsesk/neovim-config.git $PREFIX/.config/nvim
