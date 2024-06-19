# On the Energy Consumption of CPython

## What is this?

This repository contains all code and data to reproduce the experiment and results that are described in the paper _"On the Energy Consumption of CPython"_


## Structure of this repository

- Directory [`./data/out`](./data/out) contains per version of CPython ten `xz` compressed CSV files.
  That is the data that we collected in our experiment and that is reported in the paper.
  Sub-directories are called `minitwit<cpython_version>`
- Directory [`./src`](./src) contains all the Python sources and Shell scripts that are required to run the experiment.
  Besides that, it is a [Python Poetry project](https://python-poetry.org/) with all the requirement to execute the experiment from the ``controller` machine and run the analysis Jupyter notebook
  To use it, run `poetry install` and switch to a respective shell
- The Jupyter notebook [Analysis for Paper.ipynb](./src/Analysis for Paper.ipynb) contains all the source code that is used to create the images of the paper and to run the analysis in there.
- The [`./images`](./images) directory is currently empty, all images from above analysis will be stored in there.


## Preparing the SD-cards for the Raspberry Pis

The experiment as described in the paper uses Raspberry Pi's Model B+ V1.2.
The following version is the correct FreeBSD pre-built image for it.

```bash
wget https://download.freebsd.org/ftp/snapshots/arm/armv6/ISO-IMAGES/13.3/FreeBSD-13.3-PRERELEASE-arm-armv6-RPI-B-20240125-5c4e6fd30bbc-257304.img.xz
```

The download link is received from this overview: <https://wiki.freebsd.org/arm/Raspberry%20Pi>

After download, insert SD-card.
In case the card is not read directly, trigger a rescan, e.g., with `sudo lspci -v -nn`.
Finally, write the image to the SD-card

```bash
xzcat ~/Downloads/FreeBSD-13.3-PRERELEASE-arm-armv6-RPI-B-20240125-5c4e6fd30bbc-257304.img.xz | sudo dd bs=2M of=/dev/mmcblk0 status=progress
```

Note, default passwords from FreeBSD on Raspberry Pi images are: `root`: `root`, `freebsd`: `freebsd`.
I do not add other users/passwords for this experiment.


After writing the image, connect the RPI to a network in which can reach the public internet since the provisioner scripts download packages from the internet.
SCP the provision and configuration scripts to it.

```bash
cd src
scp ./provision.sh freebsd@<your_ip>:/home/freebsd
```


In our setup, Raspberry Pis are assigned IPs in the range `192.168.2.*`.
If in doubt, find them as in the following:

```bash
nmap -sn 192.168.1.*
```


### Provision Server

SSH for root is disabled by default on FreeBSD.
Therefore, we navigate via the `freebsd` user.

```bash
cd src
scp provision_root_server.sh freebsd@192.168.2.101:/home/freebsd

ssh freebsd@192.168.2.101
chmod a+x provision_root_server.sh
su -l root -c /home/freebsd/provision_root_server.sh
exit
exit

scp provision.sh freebsd@192.168.2.101:/home/freebsd
ssh freebsd@192.168.2.101
chmod u+x provision.sh
./provision.sh
exit
```

#### Copy `MiniTwit` to Server

```bash
cd src
scp -r minitwit freebsd@192.168.2.101:/home/freebsd
```

### Provision Clients

#### Client 1

```bash
scp provision_root_client1.sh freebsd@192.168.2.100:/home/freebsd
scp provision_client.sh freebsd@192.168.2.100:/home/freebsd
scp -r minitwit_client freebsd@192.168.2.100:/home/freebsd

ssh freebsd@192.168.2.100

chmod a+x provision_root_client2.sh
chmod u+x provision_client.sh

su -l root -c /home/freebsd/provision_root_client1.sh
./provision_client.sh
exit
```


#### Client 2

```bash
scp provision_root_client2.sh freebsd@192.168.2.103:/home/freebsd
scp provision_client.sh freebsd@192.168.2.103:/home/freebsd
scp -r minitwit_client freebsd@192.168.2.103:/home/freebsd

ssh freebsd@192.168.2.103

chmod a+x provision_root_client2.sh
chmod u+x provision_client.sh

su -l root -c /home/freebsd/provision_root_client2.sh
./provision_client.sh
exit
```


#### Client 3

```bash
scp provision_root_client2.sh freebsd@192.168.2.104:/home/freebsd
scp provision_client.sh freebsd@192.168.2.104:/home/freebsd
scp -r minitwit_client freebsd@192.168.2.104:/home/freebsd

ssh freebsd@192.168.2.104

chmod a+x provision_root_client3.sh
chmod u+x provision_client.sh

su -l root -c /home/freebsd/provision_root_client3.sh
./provision_client.sh
exit
```


## Run the Experiment


To run the experiment:

1. Start the OTII 3 application on the host machine (`controller`)
2. Create a new project
3. Power-up the server and the three clients
4. Wait until one can SSH into them
5. On the server, start `MiniTwit` with the respective Python environment (Python 3.8 in the following example):
  ```bash
  cd minitwit38
  source bin/activate
  nohup gunicorn --workers 2 --timeout 120 --bind 0.0.0.0:5000 --chdir $HOME/minitwit/ wsgi:app >> server.log &
  ```
6. On each of the three clients, start the client applications (`scenario`):
  ```bash
  nohup python3 minitwit_client/minitwit_scenario.py >> client.log &
  ```
7. Finally, on the CLI (on `controller`), run the experiment:
  ```bash
  cd src/data_collection
  python run_experiment_from_host.py
  ```
8. After completion of experiment runs:
  - SSH to the server
  - Kill the server application: `pkill gunicorn`
  - Jump to step 5. above and restart with the next Python version
