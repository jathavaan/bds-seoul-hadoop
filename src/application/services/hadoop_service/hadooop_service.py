import logging
import os
import subprocess
import time
from argparse import ArgumentError
from enum import Enum

from hdfs import InsecureClient, HdfsError

from src import Config


class DirectoryType(Enum):
    INPUT = 0,
    OUTPUT = 1


class HadoopService:
    __logger: logging.Logger
    __client: InsecureClient

    def __init__(self, logger: logging.Logger):
        self.__logger = logger

        self.__create_hdfs_client()
        self.__create_hdfs_directories()
        self.__exit_safemode()

    def __create_hdfs_client(self) -> None:
        self.__logger.info("Sleeping for 30 seconds... Waiting for Hadoop to finish setup")
        time.sleep(Config.HDFS_SETUP_TIMEOUT.value)

        max_retries = Config.HDFS_CONNECT_MAX_RETRIES.value
        client = InsecureClient(url=Config.HDFS_CONNECTION_STRING.value, user=Config.HDFS_USER.value)

        for i in range(max_retries):
            try:
                client.status("/")
                self.__logger.info("Successfully connected to namenode")
                break
            except HdfsError as e:
                self.__logger.info(f"Waiting for namenode ({i + 1} / {max_retries})\n\n{e}")
        else:
            raise RuntimeError("Namenode did not become available")

        self.__client = client

    def __create_hdfs_directories(self) -> None:
        try:
            status = self.__client.status(Config.HDFS_INPUT_PATH.value)
            if status["type"] == "DIRECTORY":
                print(f"Directory {Config.HDFS_INPUT_PATH.value} already exists")
        except HdfsError:
            print(f"Directory {Config.HDFS_INPUT_PATH.value} does not exist, creating...")
            self.__client.makedirs(Config.HDFS_INPUT_PATH.value)

        try:
            status = self.__client.status(Config.HDFS_OUTPUT_PATH.value)
            if status["type"] == "DIRECTORY":
                print(f"Directory {Config.HDFS_OUTPUT_PATH.value} already exists")
        except HdfsError:
            print(f"Directory {Config.HDFS_OUTPUT_PATH.value} does not exist, creating...")
            self.__client.makedirs(Config.HDFS_OUTPUT_PATH.value)

    def __exit_safemode(self) -> None:
        while True:
            result = subprocess.run(["hdfs", "dfsadmin", "-safemode", "get"], capture_output=True, text=True)
            if "Safe mode is OFF" in result.stdout:
                self.__logger.info("HDFS is out of safe mode. Proceeding...")
                break
            else:
                self.__logger.info("HDFS is in safe mode. Waiting...")
                time.sleep(5)

    def upload_file_to_hdfs(self, filename: str) -> bool:
        filepath = os.path.join(Config.TEMP_FILE_STORAGE_DIR.value, filename)
        self.__client.upload(Config.HDFS_INPUT_PATH.value, filepath)
        self.__logger.info(f"Uploaded {filename} to HDFS")
        return True

    def delete_file_from_hdfs(self, filename: str, directory_type: DirectoryType) -> bool:
        match directory_type:
            case DirectoryType.INPUT:
                filepath = os.path.join(Config.HDFS_INPUT_PATH.value, filename)
            case DirectoryType.OUTPUT:
                filepath = os.path.join(Config.HDFS_OUTPUT_PATH.value, filename)
            case _:
                raise ValueError("Invalid directory type")

        self.__client.delete(filepath)
        self.__logger.info(f"Deleted {filename} from HDFS")
        return True

    def clear_directory(self, directory_type: DirectoryType) -> bool:
        match directory_type:
            case DirectoryType.INPUT:
                command = [
                    "hadoop", "fs", "-rm", "-r", Config.HDFS_INPUT_PATH.value
                ]
            case DirectoryType.OUTPUT:
                command = [
                    "hadoop", "fs", "-rm", "-r", Config.HDFS_OUTPUT_PATH.value
                ]
            case _:
                raise ValueError("Invalid directory type")

        self.__logger.info(
            f"Cleaning up old HDFS {'input' if directory_type == DirectoryType.INPUT else 'output'} directory (if any)"
        )
        subprocess.run(command, stderr=subprocess.DEVNULL)
        self.__logger.info("Directory cleared")
        return True
