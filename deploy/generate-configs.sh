#!/bin/bash

set -a
source /opt/.hadoop.env
set +a

HADOOP_CONF_DIR=${HADOOP_CONF_DIR:-/hadoop/etc/hadoop}

echo "Generating config files for ROLE=$ROLE"

mkdir -p $HADOOP_CONF_DIR

envsubst < /opt/templates/core-site.xml.template > $HADOOP_CONF_DIR/core-site.xml
envsubst < /opt/templates/hadoop-env.sh.template > $HADOOP_CONF_DIR/hadoop-env.sh
envsubst < /opt/templates/workers.template > $HADOOP_CONF_DIR/workers

if [[ "$ROLE" == "namenode" ]]; then
  envsubst < /opt/templates/hdfs-site.xml.namenode.template > $HADOOP_CONF_DIR/hdfs-site.xml
else
  envsubst < /opt/templates/hdfs-site.xml.datanode.template > $HADOOP_CONF_DIR/hdfs-site.xml
fi

echo "Configuration files generated in $HADOOP_CONF_DIR"
