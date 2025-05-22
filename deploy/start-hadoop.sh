#!/bin/bash

if [ -f "./.env" ]; then
    echo "Loading environment from ./env"
    set -a
    source ./env
    set +a
else
    echo "ERROR: .env file not found in root directory."
    exit 1
fi

echo "Generating Hadoop config files..."
bash ./deploy/generate-configs.sh

if [[ "$ROLE" == "namenode" ]]; then
    echo "Formatting Namenode (only if not already formatted)..."
    if [ ! -d "/hadoop/dfs/name/current" ]; then
        hdfs namenode -format -force
    else
        echo "Namenode already formatted. Skipping."
    fi

    echo "Starting HDFS: Namenode + Datanodes"
    hdfs namenode &
    hdfs datanode &
else
    echo "Starting Datanode..."
    hdfs datanode
fi
