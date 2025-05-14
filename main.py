from src.entrypoints.consumers.review_consumer import ReviewConsumer
from src.entrypoints.producers import MapreduceReduceResultProducer

if __name__ == "__main__":
    # file_to_upload = os.path.join(os.getcwd(), "airline.csv")
    #
    # print(f"Uploading {file_to_upload} to HDFS...")
    # client.upload(Config.HDFS_INPUT_PATH.value, file_to_upload, overwrite=True)
    # print(f"File uploaded: {client.content(Config.HDFS_INPUT_PATH.value)}")
    #
    # print("Cleaning up old HDFS output directory (if any)...")
    # subprocess.run([
    #     "hadoop", "fs", "-rm", "-r", Config.HDFS_OUTPUT_PATH.value
    # ], stderr=subprocess.DEVNULL)
    #
    # print("Running MapReduce job via Hadoop streaming...")
    # subprocess.run(Config.HDFS_STREAMING_COMMAND.value, check=True)
    # print("MapReduce job completed.")
    #
    # print("Fetching and displaying output from HDFS...")
    # result = subprocess.run(
    #     ["hadoop", "fs", "-cat", os.path.join(Config.HDFS_OUTPUT_PATH.value, "part-*")],
    #     text=True,
    #     capture_output=True
    # )
    #
    # print(result.stdout)
    consumer = ReviewConsumer()
    producer = MapreduceReduceResultProducer()

    try:
        while True:
            if consumer.consume():
                producer.produce()
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
        producer.close()
