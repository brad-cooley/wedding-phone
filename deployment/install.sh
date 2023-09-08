#!/bin/bash
# install.sh

cd ../
sudo apt-get update
sudo apt-get install -y \
        python3-pip \
        libffi-dev \
        libssl-dev \
        portaudio19-dev

pip install --upgrade pip

pip install -r src/requirements.txt
