#!/bin/bash

full_path=$(realpath $0)
dir_path=$(dirname $full_path)
venv_path=$2


echo 
echo '---------- install python3.8 and modules -----------'

echo '---------- add repository ppa:deadsnakes/ppa -----------'
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update

echo '---------- install python3.8 -----------'
sudo apt install -y \
    python3.8 \
    python3.8-dev \
    python3.8-venv \
    python3-opengl \
    xclip \
    libmtdev-dev \
    python3-wheel \
    git



python3.8 -m venv $venv_path
source $venv_path/bin/activate
pip install --upgrade pip setuptools
pip install -r $1/doorbell/requirements.dev.txt
deactivate

# sudo mkdir $dir_path/temp
# sudo git clone https://github.com/kivymd/KivyMD.git $dir_path/temp --depth 1

# source $venv_path/bin/activate
# cd $dir_path/temp
# pip install .
# deactivate

# sudo rm -r $dir_path/temp


echo 'export FRONTEND_PREREQ=1' >> ~/.bashrc 
source ~/.bashrc 

exit 0