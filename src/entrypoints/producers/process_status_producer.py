import logging

from confluent_kafka import Producer

from src import Config
from src.entrypoints.base import ProducerBase
from src.domain.enums import ProcessStatus, ProcessType


class ProcessStatusProducer(ProducerBase[tuple[int, ProcessType, ProcessStatus]]):
    __logger: logging.Logger
    __producer: Producer

    def __init__(self, logger: logging.Logger):
        self.__logger = logger
        self.__producer = Producer({"bootstrap.servers": Config.KAFKA_BOOTSTRAP_SERVERS.value})

    def produce(self, producer_content: tuple[int, ProcessType, ProcessStatus]) -> None:
        game_id, process_type, status = producer_content
        self.__producer.produce(
            topic=Config.KAFKA_PROCESS_STATUS_TOPIC.value,
            value=f"{game_id},{process_type.value},{status.value}"
        )

    def close(self) -> None:
        self.__producer.flush()
        self.__logger.info("Shutting down Process Status Producer")
