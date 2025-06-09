# Big Data Systems Team Seoul - Hadoop Namenode and Datanodes

This repository starts the Hadoop namenode and datanode containers, and runs MapReduce jobs implemented in Python. Is
build using Docker and Docker Compose. Since the fourth Raspberry Pi is corrupted, this repository simulates nodes in
the cluster. This way we still have a working cluster with four nodes, but one is simulated.

> [!NOTE]
> Make sure the `bds-seoul-mariadb` project is up and running before starting this project. This is step two in a three
> step startup process. The correct order is:
> 1. [bds-seoul-mariadb](https://github.com/jatavaan/bds-seoul-mariadb)
> 2. [bds-seoul-hadoop](https://github.com/jathavaan/bds-seoul-hadoop)
> 3. [bds-seoul-client](https://github.com/jathavaan/bds-seoul-client)

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
    - [Local Setup](#local-setup)
    - [Raspberry Pi Setup](#raspberry-pi-setup)
    - [Starting the Services](#starting-the-services)
    - [Running the MapReduce Job](#running-the-mapreduce-job)
- [Rebuilding Containers](#rebuilding-containers)
- [Logs](#logs)

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

### Local Setup

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

DFS_REPLICATION=2
HDFS_NAMENODE_USER=root
HDFS_DATANODE_USER=root
HDFS_SECONDARYNAMENODE_USER=root

JAVA_HOME_PATH=/usr/lib/jvm/java-1.8.0-openjdk-amd64
```

If your local machine is an ARM64 architecture (like Apple Silicon), you can use the `arm64.Dockerfile` instead:

```dotenv
DOCKER_FILE=arm64.Dockerfile
```

### Raspberry Pi Setup

SSH into the Raspberry Pi and clone the repository:

```bash
git clone https://github.com/jathavaan/bds-seoul-hadoop.git
cd bds-seoul-hadoop
```

Set the IP addresses of the Raspberry Pis in your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
export SEOUL_1_IP=<ip-of-seoul-1>
export SEOUL_2_IP=<ip-of-seoul-2>
export SEOUL_3_IP=<ip-of-seoul-3>
export SEOUL_4_IP=<ip-of-seoul-4>
```

and if you want to rerun with changes in the code

```powershell
docker-compose restart
```

## Rebuilding containers

> [!WARNING] Note that this takes some time (10~20 minutes)

```powershell
docker-compose down -v; docker-compose build --no-cache; docker-compose up -d
```

## Logs

The logs for this node along with the other nodes in the cluster can be viewed
using [Seq](http://host.docker.internal:5341/#/events?range=1d). You have to provide username and password the first
time you open Seq:

- Username: `admin`
- Password: `admin`