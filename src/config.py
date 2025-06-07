import logging
import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()


class Config(Enum):
    # Logger
    LOGGING_LEVEL = logging.INFO
    LOGGER_WIDTH_OFFSET = 90
    SEQ_URL = f"http://{os.getenv('SEQ_SERVER')}:{os.getenv('SEQ_PORT')}"
    SEQ_LOG_BATCH_SIZE = 1

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS = f"{os.getenv('KAFKA_BOOTSTRAP_SERVERS')}:9092"
    KAFKA_GROUP_ID = "seoul"

    KAFKA_REVIEW_TOPIC = "reviews"
    KAFKA_MR_RESULT_TOPIC = "mapreduce_results"
    KAFKA_PROCESS_STATUS_TOPIC = "process_status"

    KAFKA_POLL_TIMEOUT = 0.5
    KAFKA_MAX_POLL_TIMEOUT = 86400000
    KAFKA_HEARTBEAT_INTERVAL = 3000
    KAFKA_SESSION_TIMEOUT = 120000

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
