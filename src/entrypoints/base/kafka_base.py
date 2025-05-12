class KafkaBase:
    def close(self) -> None:
        raise NotImplementedError("Close method not implemented")


class ConsumerBase(KafkaBase):
    message_count: int

    def consume(self) -> bool:
        raise NotImplementedError("Consume method not implemented")

    def increment_message_count(self) -> None:
        self.message_count += 1

    def reset_message_count(self) -> None:
        self.message_count = 0


class ProducerBase(KafkaBase):
    def produce(self) -> bool:
        raise NotImplementedError("Produce method not implemented")
