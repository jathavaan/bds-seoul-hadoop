#!/bin/bash

echo "Starting Hadoop entrypoint for ROLE=$ROLE"

echo "Preparing environment..."
printenv | grep -E "ROLE|NAMENODE_IP|DATANODE[0-9]*_IP|DFS_REPLICATION|JAVA_HOME" > /opt/.hadoop.env

# Generate Hadoop configuration files
echo "Generating Hadoop configuration files..."
bash /opt/generate-configs.sh

# Namenode: format if first time, then start
if [[ "$ROLE" == "namenode" ]]; then
  if [ ! -d "/hadoop/dfs/name/current" ]; then
    echo "Formatting HDFS..."
    hdfs namenode -format -force
  else
    echo "Namenode already formatted."
  fi

  echo "Starting Hadoop DFS (namenode and datanodes)..."
  start-dfs.sh
else
  echo "Starting Hadoop datanode..."
  hdfs datanode
fi

# Keep the container or process alive
tail -f /dev/null
