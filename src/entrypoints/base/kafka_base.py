class KafkaBase:
    def close(self) -> None:
        raise NotImplementedError("Close method not implemented")


class ConsumerBase(KafkaBase):
    def consume(self) -> bool:
        raise NotImplementedError("Consume method not implemented")

class ProducerBase(KafkaBase):
    def produce(self) -> bool:
        raise NotImplementedError("Produce method not implemented")
