from src.entrypoints.consumers.review_consumer import ReviewConsumer
from src.entrypoints.producers import MapreduceReduceResultProducer

if __name__ == "__main__":
    consumer = ReviewConsumer()
    producer = MapreduceReduceResultProducer()

    try:
        while True:
            is_batch_ready, result = consumer.consume()
            if is_batch_ready:
                producer.produce(producer_input=result)
                is_batch_ready = False

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
        producer.close()
