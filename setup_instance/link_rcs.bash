#!/bin/bash
WHEREAMI=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

mkdir -p $HOME/.config/

ln -s $WHEREAMI/config/nvim $HOME/.config/.
ln -s $WHEREAMI/config/zshrc $HOME/.zshrc
