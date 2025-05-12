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

    HDFS_SETUP_TIMEOUT = 30
    HDFS_CONNECT_MAX_RETRIES = 5

    # Temp file storage
    TEMP_FILE_STORAGE_DIR = os.path.join(os.getcwd(), "reviews")
