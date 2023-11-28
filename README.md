# Container Exporter (cxp)

A resource-friendly, highly efficient and minimal prometheus exporter to track memory & cpu usage of Docker containers along with their lifecycle (uptime)

## How to use

### Before You start
 - Port 8000 must be open
 - Docker & Docker Compose should be installed (optional)
 - presence of git

### Getting started
- clone and enter the repository using the following commands:
```bash
git clone https://github.com/Shayan-Ghani/Container-exporter.git
cd container-exporter
```
- Deploy the docker-compose file that suits you the best for instance :
```bash 
#make the file executable
chmod +x ./start.sh

# with docker compose v1
docker-compose -f container-exporter.yml up -d

# Or using v2
docker compose -f container-exporter.yml up -d
```

#### Can't use Docker? Ok then :
```bash
  # no need if you have done already
  chmod +x ./start.sh

  # install the required python packages
  pip install -r requirements.txt

  # add & at the end to launch in background
  ./start.sh 

``` 

### That is it you are good to go, Enjoy Using CXP! "}"


## Contributions
Welcome to CXP! This project is currently in an experimental yet stable version, and we encourage contributions to enhance its functionality, optimize code, and add new features

Feel free to contribute in any way you can. If you come across a bug or have a suggestion, please don't hesitate to file an issue. Your input is valuable and helps us improve CXP for everyone. We appreciate your contribution to making CXP even better! If you have any questions or need assistance, feel free to reach out. Thank you!

Copyright © 2023 Shayan Ghani shayanghani1384@gmail.com