import logging
import os
import subprocess
import time

from src import Config


class MapreduceService:
    __logger: logging.Logger

    def __init__(self, logger: logging.Logger):
        self.__logger = logger

    def run_mapreduce_subprocess(self, filename: str) -> None:
        self.__logger.info("Running MapReduce job via Hadoop streaming...")
        start_time = time.time()
        subprocess.run(Config.HDFS_STREAMING_COMMAND.value, check=True)
        elapsed_time = round((time.time() - start_time) / 60, 2)
        self.__logger.info(f"MapReduce job completed in {elapsed_time} minutes")

    def get_mapreduce_result(self) -> dict[str, tuple[float, float]]:
        self.__logger.info("Displaying results from MapReduce job")
        subprocess_result = subprocess.run(
            ["hadoop", "fs", "-cat", os.path.join(Config.HDFS_OUTPUT_PATH.value, "part-*")],
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
