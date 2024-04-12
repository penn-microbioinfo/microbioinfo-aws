#!/bin/bash

if [ ! $(which zoxide) ]; then
    curl -sS https://raw.githubusercontent.com/ajeetdsouza/zoxide/main/install.sh | bash
else
    echo "zoxide already installed"
fi

if [ ! -f ~/.fzf.zsh ]; then
    git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
    ~/.fzf/install
else
    echo "fzf already installed"
fi

