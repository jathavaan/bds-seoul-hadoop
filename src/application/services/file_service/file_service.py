import datetime
import logging
import os

from src import Config
from src.domain import Review


class FileService:
    __logger: logging.Logger

    def __init__(self, logger: logging.Logger):
        self.__logger = logger

    def write_to_file(self, reviews: list[Review]) -> str:
        game_id = next(map(lambda review: review.game_id, reviews), None)

        filename = f"{datetime.datetime.now().strftime('%Y%m%d')}_{game_id}.txt"
        filepath = os.path.join(Config.TEMP_FILE_STORAGE_DIR.value, filename)
        file_content = ";".join([str(review) for review in reviews])

        self.__logger.info(f"Writing {filepath} to {Config.TEMP_FILE_STORAGE_DIR.value}")
        with open(filepath, encoding="utf-8") as file:
            file.write(file_content)

        return filename

    def get_filepaths(self, game_id: int) -> list[str]:
        return [
            filepath for filepath in os.listdir(Config.TEMP_FILE_STORAGE_DIR.value)
            if filepath.endswith(".txt") and str(game_id) in filepath
        ]

    def delete_file(self, game_id: int) -> bool:
        filepaths = self.get_filepaths(game_id)
        if len(filepaths) == 0:
            self.__logger.info(f"No files for game {game_id} in {Config.TEMP_FILE_STORAGE_DIR.value}")
            return False

        for filepath in filepaths:
            os.remove(filepath)

        self.__logger.info(f"Removed {len(filepaths)} files from {Config.TEMP_FILE_STORAGE_DIR.value}")
        return True
