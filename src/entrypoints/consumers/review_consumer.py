import json
import logging

from confluent_kafka import Consumer

from src import Config
from src.application.services.file_service import FileService
from src.application.services.hadoop_service import HdfsService, HdfsDirectoryType
from src.application.services.mapreduce_service import MapreduceService, MapreduceDto
from src.domain import Review
from src.domain.enums import ProcessType, ProcessStatus
from src.entrypoints.base import ConsumerBase
from src.entrypoints.producers import ProcessStatusProducer


class ReviewConsumer(ConsumerBase):
    __logger: logging.Logger
    __file_service: FileService
    __hdfs_service: HdfsService
    __mapreduce_service: MapreduceService
    __process_status_producer: ProcessStatusProducer

    __consumer: Consumer
    __game_id: int = 0
    __correlation_id: str | None = None
    __messages: list[Review] = []
    __result: MapreduceDto | None = None

    def __init__(
            self,
            logger: logging.Logger,
            file_service: FileService,
            hdfs_service: HdfsService,
            mapreduce_service: MapreduceService,
            process_status_producer: ProcessStatusProducer
    ):
        self.__logger = logger
        self.__file_service = file_service
        self.__hdfs_service = hdfs_service
        self.__mapreduce_service = mapreduce_service
        self.__process_status_producer = process_status_producer

        topics = [Config.KAFKA_REVIEW_TOPIC.value]
        self.__consumer = Consumer({
            "bootstrap.servers": Config.KAFKA_BOOTSTRAP_SERVERS.value,
            "group.id": Config.KAFKA_GROUP_ID.value,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": True,
            "session.timeout.ms": Config.KAFKA_SESSION_TIMEOUT.value,
            "max.poll.interval.ms": Config.KAFKA_MAX_POLL_TIMEOUT.value,
            "heartbeat.interval.ms": Config.KAFKA_HEARTBEAT_INTERVAL.value
        })

        self.__consumer.subscribe(topics)
        self.__logger.info(
            f"Kafka Consumer connected to bootstrap server [{Config.KAFKA_BOOTSTRAP_SERVERS.value}] "
            f"with group ID {Config.KAFKA_GROUP_ID.value}, subscribed to topic(s): {', '.join(topics)}"
        )

    def consume(self) -> tuple[bool, MapreduceDto]:
        is_last_review = False
        while not is_last_review:
            message = self.__consumer.poll(Config.KAFKA_POLL_TIMEOUT.value)

            if not message:
                continue

            if message.error():
                self.__logger.error(message.error())
                continue

            review_data = json.loads(message.value().decode("utf-8"))
            review = Review(**review_data)
            is_last_review = review.is_last_review

            self.__logger.debug(
                f"Received the following message with correlation ID {review.correlation_id}: {review_data}"
            )

            if self.__correlation_id is None:
                self.__correlation_id = review.correlation_id
            elif self.__correlation_id != review.correlation_id:
                self.__logger.warning(
                    f"Correlation ID mismatch expected {self.__correlation_id} but got {review.correlation_id}. Skipping message from producer..."
                )

                continue

            if not self.__game_id or self.__game_id == 0:
                self.__game_id = review.game_id
            elif self.__game_id != review.game_id:
                self.__logger.warning(
                    f"Game ID mismatch expected {self.__game_id} but got {review.game_id}. Skipping message from producer..."
                )

                continue

            self.__messages.append(review)
        else:
            self.__process_status_producer.produce((self.__game_id, ProcessType.MAPREDUCE, ProcessStatus.IN_PROGRESS))
            self.__process_batch()
            result = self.__result
            self.__clean_up_process()
            self.__process_status_producer.produce((self.__game_id, ProcessType.MAPREDUCE, ProcessStatus.COMPLETED))

            return True, result

    def close(self) -> None:
        self.__consumer.close()
        self.__logger.info("Shut down review consumer")

    def get_output(self) -> MapreduceDto:
        self.__logger.info(self.__result)
        return self.__result

    def __process_batch(self) -> None:
        if not self.__messages:
            self.__logger.warning(f"No messages to process for game {self.__game_id}")
            return

        temp_review_filename = self.__file_service.write_to_file(reviews=self.__messages)
        self.__hdfs_service.upload_file_to_hdfs(filename=temp_review_filename, game_id=self.__game_id)

        self.__mapreduce_service.run_mapreduce_subprocess(game_id=self.__game_id)
        result = self.__mapreduce_service.get_mapreduce_result(self.__game_id)
        self.__result = MapreduceDto(
            game_id=self.__game_id,
            correlation_id=self.__correlation_id,
            recommendations=result
        )

        self.__hdfs_service.clear_directory(game_id=self.__game_id, directory_type=HdfsDirectoryType.INPUT)
        self.__hdfs_service.clear_directory(game_id=self.__game_id, directory_type=HdfsDirectoryType.OUTPUT)

    def __clean_up_process(self) -> None:
        self.__game_id = 0
        self.__correlation_id = None
        self.__messages = []
        self.__result = None
