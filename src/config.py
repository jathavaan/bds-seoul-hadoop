import logging
import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()


class Config(Enum):
    # Logger
    LOGGING_LEVEL = logging.INFO
    LOGGER_WIDTH_OFFSET = 90
    SEQ_URL = "http://host.docker.internal:5341"

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
    KAFKA_GROUP_ID = "hadoop_consumer_group"
    KAFKA_REVIEW_TOPIC = "reviews"
    KAFKA_RESULT_TOPIC = "results"
    KAFKA_POLL_TIMEOUT = 0.5

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

    HDFS_SETUP_TIMEOUT = 30
    HDFS_CONNECT_MAX_RETRIES = 5

    HADOOP_BATCH_SIZE = 200

    # Temp file storage
    TEMP_FILE_STORAGE_DIR = os.path.join(os.getcwd(), "reviews")
