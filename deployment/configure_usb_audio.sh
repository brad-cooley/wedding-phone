#!/bin/bash
# configure_usb_audio.sh
# Configures the Pi to use the USB audio card as a default

echo "Listing audio cards"
aplay -l

CONFIG_PATH=/usr/share/alsa/alsa.conf
sudo cp $CONFIG_PATH $CONFIG_PATH.bak

echo "Setting output defaults for Pi"
sudo sed -i 's/defaults.ctl.card 0/defaults.ctl.card 2/g' $CONFIG_PATH
sudo sed -i 's/defaults.pcm.card 0/defaults.pcm.card 2/g' $CONFIG_PATH