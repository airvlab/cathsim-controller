# Burt the board

## Download the Arduino

 download from website
 set it as excutable file:

```sh
chmod +x <filepath>
./<filepath>
```

## Release the port

```sh
sudo systemctl stop brltty-udev.service
sudo systemctl mask brltty-udev.service
sudo systemctl stop brltty.service
sudo systemctl disable brltty.service
```

## Get the permission of port

```sh
sudo su
cd /dev/
chown `<username>` ttyUSB0
```

## Create the environment using [conda](https://docs.anaconda.com/miniconda/)

```python
conda create -n controller python=3.10 
conda activate controller
pip install -e .
```

## Troubleshoot

### Be part of `sudo` group

### Port is busy on Ubuntu

Ubuntu uses `brltty`, so we need to uninstall it and stop the services. See more
info [here](https://forum.arduino.cc/t/solved-tools-serial-port-greyed-out-in-ubuntu-22-04-lts/991568/16).

```sh
sudo systemctl stop brltty-udev.service
sudo systemctl mask brltty-udev.service
sudo systemctl stop brltty.service
sudo systemctl disable brltty.service
```
