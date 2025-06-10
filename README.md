# Big Data Systems Team Seoul - Hadoop Namenode and Datanodes

This repository starts the Hadoop namenode and datanode containers, and runs MapReduce jobs implemented in Python. Is
build using Docker and Docker Compose. Since the fourth Raspberry Pi is corrupted, this repository simulates nodes in
the cluster. This way we still have a working cluster with four nodes, but one is simulated.

> [!NOTE]
> Make sure the `bds-seoul-mariadb` project is up and running before starting this project. This is step two in a three
> step startup process. The correct order is:
> 1. [bds-seoul-mariadb](https://github.com/jathavaan/bds-seoul-mariadb)
> 2. [bds-seoul-hadoop](https://github.com/jathavaan/bds-seoul-hadoop)
> 3. [bds-seoul-client](https://github.com/jathavaan/bds-seoul-client)

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Setup](#setup)
    - [Local setup](#local-setup)
    - [Raspberry Pi setup](#raspberry-pi-setup)
    - [Starting the Services](#starting-the-services)

## Prerequisites

- [Docker Desktop](https://docs.docker.com/desktop/)
- [Python 3.11](https://www.python.org/downloads/release/python-3110/)

## Installation

1. Clone the repository:

   ```powershell
   git clone https://github.com/jathavaan/bds-seoul-hadoop.git
   ```

2. Navigate to the project directory:

   ```powershell
    cd bds-seoul-hadoop
    ```

## Setup

There are two different setups for this project: one for local development and one for running on Raspberry Pis.

### Local setup

Create a `.env` file in the root directory with the following content:

```dotenv
ARCHITECTURE=x86
HDFS_HOST_IP=namenode
KAFKA_BOOTSTRAP_SERVERS=host.docker.internal
SEQ_SERVER=host.docker.internal
SEQ_PORT=5341

NAMENODE_IP=namenode
DATANODE_IP=datanode
NAMENODE_ROLE=namenode
DATANODE_ROLE=datanode

DFS_REPLICATION=1
HDFS_NAMENODE_USER=root
HDFS_DATANODE_USER=root
HDFS_SECONDARYNAMENODE_USER=root

JAVA_HOME_PATH=/usr/lib/jvm/java-1.8.0-openjdk-amd64
```

If your local machine is an ARM64 architecture (like Apple Silicon), you have to use `arm.*.dockerfile` instead. Also
change the `JAVA_HOME_PATH` as shown below:

```dotenv
ARCHITECTURE=arm
JAVA_HOME_PATH=/usr/local/openjdk-8
```

See the section about [Starting the Services](#starting-the-services) for information on how to this system.

### Raspberry Pi setup

> [!NOTE]
> This takes over 2 hours depending on your internet connection. It is therefore recommended to run this project
> locally.

The Raspberry Pi setup is more complex and requires multiple Raspberry Pis to be set up. The first step is to identify
the IP-addresses of the Raspberry Pis. Open a terminal on your computer and ssh into the Raspberry Pi:

```powershell
ssh seoul-3@<ip-address-of-raspberry-pi-3>
```

Replace `<ip-address-of-raspberry-pi-3>` with the actual IP-address of the Raspberry Pi, and enter the password
`seoul-3`.

Then change directory into the `bds-seoul-hadoop` directory:

```powershell
cd bds-seoul-hadoop
```

We use `envsubst` to inject the correct IP-addresses when building the docker images. The IP-addresses are set in
`~/.zshrc`. To set the IP-addresses, you can use `nano ~/.zshrc` and add the following lines:

```powershell
export SEOUL_1_IP=<ip-address-of-seoul-1-raspberry-pi>
export SEOUL_2_IP=<ip-address-of-seoul-2-raspberry-pi>
export SEOUL_3_IP=<ip-address-of-seoul-3-raspberry-pi>
export SEOUL_4_IP=<ip-address-of-seoul-4-raspberry-pi>
```

Press `CTRL + X`, then `Y` and `Enter` to save the file. After that, run

```bash
source ~/.zshrc
``` 

to apply the changes. You have now set the IP-addresses for the Raspberry Pis, and you only need to do this if the
IP-addresses of any Raspberry Pi changes.

Using `envsubst`, you can now configure the correct `.env` file. Simply run the following command in the root of
`bds-seoul-mariadb` directory:

```powershell
envsubst < .env.template > .env
```

This will create a `.env` file with the correct IP-addresses for the Raspberry Pis. Run

```bash
cat .env
``` 

to verify that the
environment variables are set correctly. The docker images are now ready to be built. Build and start the containers and
force recreating with the following command:

### Starting the Services

> [!NOTE]
> If you are doing this on a Raspberry Pi, use `sudo docker compose` instead of `docker-compose`.

The next step is to create the containers by running the following command in the root of `bds-seoul-hadoop` directory:

```powershell
docker-compose up -d
```

When the containers are up and running, you can check the logs of the containers by running

```powershell
docker-compose logs -f
```

When you see the logs

```plaintext
[INFO] 2025-06-09 05:29:53 application.services.hadoop_service.hdfs_service:37            Successfully connected to namenode
[INFO] 2025-06-09 05:29:54 application.services.hadoop_service.hdfs_service:70            HDFS is out of safe mode. Proceeding...
[INFO] 2025-06-09 05:29:54 entrypoints.consumers.review_consumer:55                       Kafka Consumer connected to bootstrap server [host.docker.internal:9092] with group ID seoul, subscribed to topic(s): reviews
```

you can be sure that the containers are up and running. You may now run the containers in `bds-seoul-client` to complete
the setup. See the guide in the [repository](https://bds-seoul-client) for more information.
