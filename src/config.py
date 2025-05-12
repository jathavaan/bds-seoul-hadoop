import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()


class Config(Enum):
    # Logger
    LOGGER_WIDTH_OFFSET = 75

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
    KAFKA_GROUP_ID = "mariadb_consumer_group"
    KAFKA_TOPICS = ["game_topic"]
    KAFKA_POLL_TIMEOUT = 1.0

    # Hadoop
    HDFS_CONNECTION_STRING = f"http://{os.getenv('HDFS_HOST_IP')}:9870"
    HDFS_USER = "root"

    # Paths
    HDFS_INPUT_PATH = "/input"
    HDFS_OUTPUT_PATH = "/output"
    MAPPER_FILENAME = "mapper.py"
    REDUCER_FILENAME = "reducer.py"
    MAPPER_PATH = os.path.join(".", "src", "mapreduce", MAPPER_FILENAME)
    REDUCER_PATH = os.path.join(".", "src", "mapreduce", REDUCER_FILENAME)
    HADOOP_STREAMING_JAR_PATH = "/opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar"

    # HDFS Streaming command
    HDFS_STREAMING_COMMAND = [
        "hadoop", "jar", HADOOP_STREAMING_JAR_PATH,
        "-input", HDFS_INPUT_PATH,
        "-output", HDFS_OUTPUT_PATH,
        "-mapper", f"python3.11 {MAPPER_FILENAME}",
        "-reducer", f"python3.11 {REDUCER_FILENAME}",
        "-file", MAPPER_PATH,
        "-file", REDUCER_PATH,
    ]

    HDFS_SETUP_TIMEOUT = 30
    HDFS_CONNECT_MAX_RETRIES = 5
