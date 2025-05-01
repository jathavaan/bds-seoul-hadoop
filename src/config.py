import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()


class Config(Enum):
    HDFS_CONNECTION_STRING = f"http://{os.getenv('HOST_IP')}:9870"
    HDFS_USER = "root"
