import logging
import os
import subprocess
import time

from src import Config


class MapreduceService:
    __logger: logging.Logger

    def __init__(self, logger: logging.Logger):
        self.__logger = logger

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

        subprocess.run(mapreduce_command, check=True)
        elapsed_time = round((time.time() - start_time) / 60, 2)
        self.__logger.info(f"MapReduce job completed in {elapsed_time} minutes")

    def get_mapreduce_result(self, game_id: int) -> dict[str, tuple[float, float]]:
        self.__logger.info("Displaying results from MapReduce job")
        subprocess_result = subprocess.run(
            ["hadoop", "fs", "-cat", os.path.join(Config.HDFS_OUTPUT_PATH.value, str(game_id), "part-*")],
            text=True,
            capture_output=True
        )

        result = {}
        lines = subprocess_result.stdout.strip().split("\n")

        for line in lines:
            time_group, recommended = line.split()
            recommended = float(recommended)
            not_recommended = float(0)  # TODO: Updated this when MapReduce job is updated

            result[time_group] = (recommended, not_recommended)

        return result
