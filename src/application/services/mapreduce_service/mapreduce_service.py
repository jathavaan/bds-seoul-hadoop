import logging
import os
import subprocess
import time

from src import Config
from src.application.services.hadoop_service import HdfsService, HdfsDirectoryType


class MapreduceService:
    __logger: logging.Logger
    __hdfs_service: HdfsService

    def __init__(self, logger: logging.Logger, hdfs_service: HdfsService):
        self.__logger = logger
        self.__hdfs_service = hdfs_service

    def run_mapreduce_subprocess(self, game_id: int) -> None:
        self.__logger.info("Running MapReduce job via Hadoop streaming...")
        start_time = time.time()

        mapreduce_command = [
            "hadoop", "jar", Config.HADOOP_STREAMING_JAR_PATH.value,
            "-input", os.path.join(Config.HDFS_INPUT_PATH.value, str(game_id)),
            "-output", os.path.join(Config.HDFS_OUTPUT_PATH.value, str(game_id)),
            "-mapper", f"python3.11 {Config.MAPPER_FILENAME.value}",
            "-reducer", f"python3.11 {Config.REDUCER_FILENAME.value}",
            "-file", Config.MAPPER_PATH.value,
            "-file", Config.REDUCER_PATH.value,
        ]

        try:
            self.__hdfs_service.clear_directory(game_id=game_id, directory_type=HdfsDirectoryType.OUTPUT)

            subprocess.run(mapreduce_command, check=True)
            elapsed_time = time.time() - start_time
            self.__logger.info(
                f"MapReduce job completed in {round(elapsed_time / 60, 2)} minutes" if elapsed_time > 60 else
                f"MapReduce job completed in {round(elapsed_time, 2)} seconds"
            )
        except subprocess.CalledProcessError as e:
            self.__logger.error(f"MapReduce job failed with exit code {e.returncode}")
            self.__logger.error(f"Expected command: {' '.join(mapreduce_command)}")
            self.__logger.error(f"Command: {' '.join(e.cmd)}")
            self.__logger.error(f"Output: {e.output}")
            self.__logger.error(f"Stderr: {e.stderr}")
            raise e

    def get_mapreduce_result(self, game_id: int) -> dict[str, tuple[float, float]]:
        subprocess_result = subprocess.run(
            ["hadoop", "fs", "-cat", os.path.join(Config.HDFS_OUTPUT_PATH.value, str(game_id), "part-*")],
            text=True,
            capture_output=True
        )

        result: dict[str, tuple[float, float]] = {}
        lines = subprocess_result.stdout.strip().split("\n")

        for line in lines:
            time_group, recommended, not_recommended = line.split(",")

            recommended = float(recommended.strip("\t"))
            not_recommended = float(not_recommended.strip("\t"))

            result[time_group] = (recommended, not_recommended)

        return result
