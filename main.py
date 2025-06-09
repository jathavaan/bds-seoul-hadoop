from src.application import Container
from src.entrypoints.consumers.review_consumer import ReviewConsumer
from src.entrypoints.producers import MapreduceReduceResultProducer

container = Container()
logger = container.logger()
file_service = container.file_service()
hdfs_service = container.hdfs_service()
mapreduce_service = container.mapreduce_service()
process_status_producer = container.process_status_producer()

if __name__ == "__main__":
    consumer = ReviewConsumer(
        logger=logger,
        file_service=file_service,
        hdfs_service=hdfs_service,
        mapreduce_service=mapreduce_service,
        process_status_producer=process_status_producer
    )
    producer = MapreduceReduceResultProducer(logger=logger)

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
