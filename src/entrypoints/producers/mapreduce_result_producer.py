import json
import logging

from confluent_kafka import Producer

from src import Config
from src.application import Container
from src.entrypoints.base import ProducerBase


class MapreduceReduceResultProducer(ProducerBase[dict[str, tuple[float, float]]]):
    __logger: logging.Logger
    __producer: Producer

    def __init__(self):
        container = Container()
        self.__logger = container.logger()
        self.__producer = Producer({"bootstrap.servers": Config.KAFKA_BOOTSTRAP_SERVERS.value})

    def produce(self, game_id: int, producer_input: dict[str, tuple[float, float]]) -> bool:
        self.__producer.produce(
            topic=Config.KAFKA_RESULT_TOPIC.value,
            key=str(game_id).encode("utf-8"),
            value=json.dumps(producer_input).encode("utf-8"),
            callback=self.__delivery_report
        )

        self.__producer.flush()
        return True

    def close(self) -> None:
        self.__producer.flush()
        self.__logger.info("Shut down result producer")

    def __delivery_report(self, err, msg):
        if err:
            self.__logger.error(f"Delivery failed: {msg}")
        else:
            self.__logger.debug(f"Delivered to {msg.topic()} [partition {msg.partition()}] @ offset {msg.offset()}")
