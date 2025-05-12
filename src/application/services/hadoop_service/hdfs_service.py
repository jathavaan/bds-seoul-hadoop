import logging
import os
import subprocess
import time
from enum import Enum

from hdfs import InsecureClient, HdfsError

from src import Config


class HdfsDirectoryType(Enum):
    INPUT = 0,
    OUTPUT = 1


class HdfsService:
    __logger: logging.Logger
    __client: InsecureClient

    def __init__(self, logger: logging.Logger):
        self.__logger = logger

        self.__create_hdfs_client()
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

    def __create_hdfs_directories(self, game_id: int) -> None:
        input_path = os.path.join(Config.HDFS_INPUT_PATH.value, str(game_id))
        output_path = os.path.join(Config.HDFS_OUTPUT_PATH.value, str(game_id))

        try:
            status = self.__client.status(input_path)
            if status["type"] == "DIRECTORY":
                print(f"Directory {input_path} already exists")
        except HdfsError:
            print(f"Directory {input_path} does not exist, creating...")
            self.__client.makedirs(input_path)

        try:
            status = self.__client.status(output_path)
            if status["type"] == "DIRECTORY":
                print(f"Directory {output_path} already exists")
        except HdfsError:
            print(f"Directory {output_path} does not exist, creating...")
            self.__client.makedirs(output_path)

    def __exit_safemode(self) -> None:
        while True:
            result = subprocess.run(["hdfs", "dfsadmin", "-safemode", "get"], capture_output=True, text=True)
            if "Safe mode is OFF" in result.stdout:
                self.__logger.info("HDFS is out of safe mode. Proceeding...")
                break
            else:
                self.__logger.info("HDFS is in safe mode. Waiting...")
                time.sleep(5)

    def upload_file_to_hdfs(self, filename: str, game_id: int) -> bool:
        self.__create_hdfs_directories(game_id)

        filepath = os.path.join(Config.TEMP_FILE_STORAGE_DIR.value, filename)
        input_path = os.path.join(Config.HDFS_INPUT_PATH.value, str(game_id))

        self.__client.upload(input_path, filepath)
        self.__logger.info(f"Uploaded {filename} to HDFS")

        return True

    def delete_file_from_hdfs(self, filename: str, game_id: int, directory_type: HdfsDirectoryType) -> bool:
        match directory_type:
            case HdfsDirectoryType.INPUT:
                filepath = os.path.join(Config.HDFS_INPUT_PATH.value, str(game_id), filename)
            case HdfsDirectoryType.OUTPUT:
                filepath = os.path.join(Config.HDFS_OUTPUT_PATH.value, str(game_id), filename)
            case _:
                raise ValueError("Invalid directory type")

        self.__client.delete(filepath)
        self.__logger.info(f"Deleted {filename} from HDFS")
        return True

    def clear_directory(self, game_id: int, directory_type: HdfsDirectoryType) -> bool:
        match directory_type:
            case HdfsDirectoryType.INPUT:
                command = [
                    "hadoop", "fs", "-rm", "-r", os.path.join(Config.HDFS_INPUT_PATH.value, str(game_id))
                ]
            case HdfsDirectoryType.OUTPUT:
                command = [
                    "hadoop", "fs", "-rm", "-r", os.path.join(Config.HDFS_OUTPUT_PATH.value, str(game_id))
                ]
            case _:
                raise ValueError("Invalid directory type")

        self.__logger.info(
            f"Cleaning up old HDFS {'input' if directory_type == HdfsDirectoryType.INPUT else 'output'} directory (if any)"
        )
        subprocess.run(command, stderr=subprocess.DEVNULL)
        self.__logger.info("Directory cleared")

        return True
