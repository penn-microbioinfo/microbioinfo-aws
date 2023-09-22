#!/bin/bash

if [ -z $1 ]; then
	PATH_TO_MBIAWS=$HOME
else
	PATH_TO_MBIAWS=$1
fi

if [ ! -d $HOME/pkgs ]; then
	mkdir $HOME/pkgs
fi

 Install node.js if needed
if ! which node; then
    curl -sL install-node.vercel.app/lts | sudo bash # Install node.js for coc
fi

# Setup neovim
wget https://github.com/neovim/neovim/releases/download/stable/nvim-linux64.tar.gz
mv nvim-linux.tar.gz $HOME/pkgs/.
cd $HOME/pkgs
tar xvf  nvim-linux64.tar.gz
chmod u+x $HOME/pkgs/nvim-linux64/bin/nvim
sudo rm /usr/bin/vim
sudo ln -s /home/ubuntu/pkgs/nvim-linux64/bin/nvim /usr/bin/vim
git clone --depth 1 https://github.com/wbthomason/packer.nvim $HOME/.local/share/nvim/site/pack/packer/start/packer.nvim
#git clone https://github.com/penn-microbioinfo/microbioinfo-aws.git $HOME/microbioinfo-aws
mkdir -p $HOME/.config
ln -s $PATH_TO_MBIAWS/microbioinfo-aws/setup_instance/config/nvim $HOME/.config/.
