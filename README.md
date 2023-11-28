# Container Exporter (CXP)

A resource-friendly, highly efficient, and minimal Prometheus exporter to track memory and CPU usage of Docker containers along with their lifecycle (uptime)

## DEV STACK
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=ffdd54) ![Docker](https://img.shields.io/badge/docker-3670A0?style=for-the-badge&logo=docker&logoColor=ffff) ![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=Prometheus&logoColor=white) ![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)

## How to use

### Before You start
 - Port 8000 must be open (default port)
 - Docker & Docker Compose should be installed (optional)
 - The presence of Git and Python3

### Getting started
- clone and enter the repository using the following commands:
```bash
  git clone https://github.com/Shayan-Ghani/Container-exporter.git
  cd container-exporter
```
- Deploy the docker-compose file that suits you the best for instance :
```bash 
# make the file executable
  chmod +x ./start.sh

# with docker compose v1
  docker-compose -f container-exporter.yml up -d

# Or using v2
  docker compose -f container-exporter.yml up -d
```

#### Can't use Docker? Ok then :
```bash
# No need if done already
  chmod +x ./start.sh

# install the required python packages
  pip install -r requirements.txt

# add & at the end to launch in the background
  ./start.sh 

``` 

### Add CXP to Prometheus
- Edit your `prometheus.yml` file and add the address of container-exporter in scrape_configs:

![Prometheus config](./capture/scrape-config.png "Prometheus configuration file")

- Reload or restart your Prometheus server.
### That is it you are good to go, Enjoy Using CXP! "}"


## TO-DO
 - I/O usage 
 - Network Usage

## Contributions
Welcome to CXP! This project is currently in an experimental yet stable version, and we encourage contributions to enhance its functionality, optimize code, and add new features

Feel free to contribute in any way you can. If you come across a bug or have a suggestion, please don't hesitate to file an issue. Your input is valuable and helps us improve CXP for everyone. We appreciate your contribution to making CXP even better! If you have any questions or need assistance, feel free to reach out. Thank you!

Copyright © 2023 Shayan Ghani shayanghani1384@gmail.com
