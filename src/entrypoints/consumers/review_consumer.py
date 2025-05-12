import logging
from email.errors import MessageDefect

from confluent_kafka import Consumer, __all__

from src import Config
from src.application import Container
from src.entrypoints.base import ConsumerBase


class ReviewConsumer(ConsumerBase):
    __consumer: Consumer
    __logger: logging.Logger

    def __init__(self):
        container = Container()

        self.__logger = container.logger()
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
        message = self.__consumer.poll(Config.KAFKA_POLL_TIMEOUT.value)
        if not message:
            self.__logger.warning("No message received")
            return False

        if message.error():
            self.__logger.error(message.error())
            return False

        self.increment_message_count()
        self.__logger.info(message.as_string())

        if self.message_count >= 100:
            return True

        return False

    def close(self) -> None:
        self.__consumer.close()
        self.__logger.info("Shut down review consumer")
