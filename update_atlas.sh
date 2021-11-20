#!/bin/bash

full_path=$(realpath $0)
dir_path=$(dirname $full_path)
venv_path=$dir_path/.frontend_venv


if [ $# -eq 0 ]; then
source $venv_path/bin/activate
cd $dir_path/doorbell/app/frontend/assets/familie &&
python3 -m kivy.atlas familieatlas 482x4800 *.png
cd $dir_path/doorbell/app/frontend/assets/halloween &&
python3 -m kivy.atlas halloweenatlas 802x4800 *.png
fi
