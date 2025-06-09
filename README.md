# RaspberryPi's with Hadoop Distributed File System and MapReduce

This repo contains the MapReduce logic for the Big Data Systems project at Pusan National University. The repos
in this project can be found at below:

- [Client](https://github.com/jathavaan/bds-seoul-client)
- [MariaDB](https://github.com/jathavaan/bds-seoul-mariadb)
- [Hadoop](https://github.com/jathavaan/bds-seoul-hadoop)

The goal of the project is to scrape data from a website, in our case [Steam](https://steampowered.com/) and process the
data in a distributed system. The project is deployed on a cluster of four RaspberryPi's, and this repo holds the source
code for two of them. We have two nodes dedicated to Hadoop, where one is a namenode and datanode, and the other is only
a datanode. The code that can be found in this repo does the following:

- Listen to a Kafka topic from the scraper
- Batch and upload reviews to HDFS
- MapReduce job on the incoming data
- Publishes the results to a Kafka topic

## Dependencies

Ensure that Kafka, Zookeeper, MariaDB and Seq is up and running before starting this Pi. If you are running on a local
machine ensure that the containers in `bds-seoul-mariadb`-repo is up and running.

## Setup

Make sure to add `.env` in the root directory. It should look like this for local development

```dotenv
ROLE=local
NAMENODE_ROLE=namenode
DATANODE_ROLE=datanode
DOCKER_FILE=x86.Dockerfile
HDFS_HOST_IP=namenode
KAFKA_BOOTSTRAP_SERVERS=host.docker.internal
SEQ_SERVER=host.docker.internal
SEQ_PORT=5341
```

and in the folder `hadoop` add `.hadoop.env` which for the local development should look like this

```dotenv
NAMENODE_IP=namenode
DATANODE_IP=datanode

DFS_REPLICATION=2
HDFS_NAMENODE_USER=root
HDFS_DATANODE_USER=root
HDFS_SECONDARYNAMENODE_USER=root
```

For the `.env` file `NAMENODE_ROLE` and `DATANODE_ROLE` should be substituted with `ROLE` which should either have the
value `namenode` or `datanode` when configuring the production environment. In `.hadoop.env` the keys `*_ROLE` should
have the respective IP-addresses as values.

The Python code have to run inside a container. Simply run `docker-compose up -d`.

## Running the code

```powershell
docker-compose start
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