#!/bin/bash

full_path=$(realpath $0)
dir_path=$(dirname $full_path)
venv_path=$dir_path/.frontend_venv

# python3.8 -m venv /venv
# PATH=/venv/bin:$PATH

# echo $FRONTEND_PREREQ
# if [[ (! $FRONTEND_PREREQ) || ($1 = "venv") ]]; then
# # if [[ ($1 = "install" ) ]]; then
# $dir_path/install_venv/install_venv.sh $dir_path $venv_path
# fi


if [ $# -eq 0 ]; then
source $venv_path/bin/activate
cd $dir_path/doorbell/app &&
python3 -m main
fi
