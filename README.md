# RaspberryPi's with Hadoop Distributed File System and MapReduce

Make sure to add `.env` in the root directory. It should look like this for local development

```dotenv
NAMENODE_ROLE=namenode
DATANODE_ROLE=datanode
```

and in the folder `hadoop` add `.hadoop.env` which for the local development should look like this

```dotenv
NAMENODE_IP=namenode
DATANODE_IP=datanode

DFS_REPLICATION=1
HDFS_NAMENODE_USER=root
HDFS_DATANODE_USER=root
HDFS_SECONDARYNAMENODE_USER=root

JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
```

For the `.env` file `NAMENODE_ROLE` and `DATANODE_ROLE` should be substituted with `ROLE` which should either have the
value `namenode` or `datanode` when configuring the production environment. In `.hadoop.env` the keys `*_ROLE` should
have the respective IP-addresses as values.