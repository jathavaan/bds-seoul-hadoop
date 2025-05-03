#!/bin/bash

echo "Starting Hadoop entrypoint for ROLE=$ROLE"

echo "Preparing environment..."
set -a
source /opt/.hadoop.env
set +a

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

  echo "Starting Hadoop NameNode (foreground)..."
  hdfs namenode &
  echo "NameNode is running..."
  hdfs datanode &
  echo "DataNode is running..."

  echo "Running Python pipeline"
  pip3.11 install --no-cache-dir -r /app/requirements.txt
  python3.11 /app/main.py &
  wait
elif [[ "$ROLE" == "datanode" ]]; then
  echo "Starting Hadoop DataNode (foreground)..."
  exec hdfs datanode
  echo "DataNode is running..."
else
  echo "Unknown Role=$ROLE"
  exit 1
fi