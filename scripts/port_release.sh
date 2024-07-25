#!/bin/bash

sudo su <<HERE
systemctl stop brltty-udev.service
systemctl mask brltty-udev.service
systemctl stop brltty.service
systemctl disable brltty.service
HERE
