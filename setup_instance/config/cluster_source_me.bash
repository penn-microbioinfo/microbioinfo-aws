CLUSTHOME=/shared-ebs
MBIAWS=$CLUSTHOME/microbioinfo-aws
export PATH=/$CLUSTHOME/bin:/$CLUSTHOME/.local/bin:/opt/slurm/bin:$PATH
export PATH=$PATH:/$CLUSTHOME/build/bowtie2-2.5.2-linux-x86_64
export XDG_CONFIG_HOME=$CLUSTHOME/.config
export XDG_DATA_HOME=$CLUSTHOME/.local/share
export POETRY_VIRTUALENVS_IN_PROJECT=true
source $MBIAWS/setup_instance/config/zshrc
export PATH=/home/ubuntu/.local/bin:$PATH
cd $CLUSTHOME
