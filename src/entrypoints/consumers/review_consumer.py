import json
import logging

from confluent_kafka import Consumer

from src import Config
from src.application import Container
from src.application.services.file_service import FileService
from src.application.services.hadoop_service import HdfsService, HdfsDirectoryType
from src.application.services.mapreduce_service import MapreduceService
from src.domain import Review
from src.entrypoints.base import ConsumerBase


class ReviewConsumer(ConsumerBase):
    __logger: logging.Logger
    __file_service: FileService
    __hdfs_service: HdfsService
    __mapreduce_service: MapreduceService

    __consumer: Consumer
    __game_id: int
    __messages: list[Review]
    __result: dict[str, tuple[float, float]]

    def __init__(self):
        container = Container()

        self.__logger = container.logger()
        self.__file_service = container.file_service()
        self.__hdfs_service = container.hdfs_service()
        self.__mapreduce_service = container.mapreduce_service()

        self.__messages = []
        self.__consumer = Consumer({
            "bootstrap.servers": Config.KAFKA_BOOTSTRAP_SERVERS.value,
            "group.id": Config.KAFKA_GROUP_ID.value,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": True
        })

        self.__consumer.subscribe(Config.KAFKA_TOPICS.value)
        self.__logger.info(
            f"Kafka Consumer connected to bootstrap server [{Config.KAFKA_BOOTSTRAP_SERVERS.value}] "
            f"with group ID {Config.KAFKA_GROUP_ID.value}, subscribed to topic(s): {', '.join(Config.KAFKA_TOPICS.value)}"
        )

    def consume(self) -> bool:
        while len(self.__messages) < Config.HADOOP_BATCH_SIZE.value:
            message = self.__consumer.poll(Config.KAFKA_POLL_TIMEOUT.value)
            if not message:
                self.__logger.warning("No message received")
                return False

            if message.error():
                self.__logger.error(message.error())
                return False

            review_data = json.loads(message.value().decode("utf-8"))
            review = Review(**review_data)

            if not self.__game_id or self.__game_id == 0:
                self.__game_id = review.game_id
            elif self.__game_id != review.game_id:
                self.__logger.warning(
                    f"Game ID mismatch expected {self.__game_id} but got {review.game_id}. Skipping message from producer"
                )
                continue

            self.__messages.append(review)
            self.__logger.info(message.as_string())
        else:
            self.__process_batch()
            self.__clean_up_process()
            return True

    def close(self) -> None:
        self.__consumer.close()
        self.__logger.info("Shut down review consumer")

    def get_output(self) -> dict[int, dict[str, tuple[float, float]]]:
        pass

    def __process_batch(self) -> None:
        if not self.__messages:
            self.__logger.warning(f"No messages to process for game {self.__game_id}")
            return

        temp_review_filename = self.__file_service.write_to_file(reviews=self.__messages)
        self.__hdfs_service.upload_file_to_hdfs(filename=temp_review_filename, game_id=self.__game_id)

        self.__mapreduce_service.run_mapreduce_subprocess(game_id=self.__game_id)
        self.__result = self.__mapreduce_service.get_mapreduce_result(self.__game_id)

        self.__hdfs_service.clear_directory(game_id=self.__game_id, directory_type=HdfsDirectoryType.INPUT)
        self.__hdfs_service.clear_directory(game_id=self.__game_id, directory_type=HdfsDirectoryType.OUTPUT)

    def __clean_up_process(self) -> None:
        self.__game_id = 0
        self.__messages = []
        self.__result = {}
