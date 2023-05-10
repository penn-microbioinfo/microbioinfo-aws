#!/bin/bash

if ! aws --version ; then
	curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
	unzip awscliv2.zip && \
	sudo ./aws/install && \
	rm awscliv2.zip && rm -r aws
fi

mkdir -p $HOME/lib
cd $HOME/lib

git clone git@bitbucket.org:codeforpenn/pennshib.git
git clone git@bitbucket.org:codeforpenn/awsshib.git
git clone git@bitbucket.org:codeforpenn/aws-federated-auth.git

mkdir $HOME/pyenvs
cd $HOME/pyenvs
python3 -m venv pennaws
source pennaws/bin/activate

pip install "python-dateutil<3.0.0,>=2.1"
pip install " urllib3<1.27,>=1.25.4"

cd $HOME/lib

cd pennshib
python3 setup.py develop

cd ../awsshib
python3 setup.py develop

cd ../

#echo "export AWS_PROFILE=445654575720-BushmanLabPostdoc" >> $HOME/.zshrc
if [[ $(grep -c 'alias aws' $HOME/.zshrc) -eq 0 ]]; then
    echo "alias awsenv='source $HOME/pyenvs/pennaws/bin/activate'" >> $HOME/.bashrc
    echo "alias awsauth='awsenv; python ${HOME}/lib/aws-federated-auth/aws-federated-auth.py; export AWS_PROFILE=445654575720-BushmanLabPostdoc'" >> $HOME/.bashrc
fi
