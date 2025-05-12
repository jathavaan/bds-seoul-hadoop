import os
import subprocess
import time

from hdfs import InsecureClient, HdfsError

from src import Config
from src.entrypoints.consumers.review_consumer import ReviewConsumer

if __name__ == "__main__":
    start_time = time.time()
    print("Sleeping for 30 seconds... Waiting for Hadoop to finish setup")
    time.sleep(Config.HDFS_SETUP_TIMEOUT.value)

    max_retries = Config.HDFS_CONNECT_MAX_RETRIES.value
    client = InsecureClient(url=Config.HDFS_CONNECTION_STRING.value, user=Config.HDFS_USER.value)

    for i in range(max_retries):
        try:
            client.status("/")
            print("Successfully connected to namenode")
            break
        except HdfsError as e:
            print(f"Waiting for namenode ({i + 1} / {max_retries})\n\n{e}")
    else:
        raise RuntimeError("Namenode did not become available")

    try:
        status = client.status(Config.HDFS_INPUT_PATH.value)

        if status["type"] == "DIRECTORY":
            print(f"Directory {Config.HDFS_INPUT_PATH.value} already exists")
    except HdfsError:
        print(f"Directory {Config.HDFS_INPUT_PATH.value} does not exist, creating...")
        client.makedirs(Config.HDFS_INPUT_PATH.value)

    while True:
        result = subprocess.run(["hdfs", "dfsadmin", "-safemode", "get"], capture_output=True, text=True)
        if "Safe mode is OFF" in result.stdout:
            print("HDFS is out of safe mode. Proceeding...")
            break
        else:
            print("HDFS is in safe mode. Waiting...")
            time.sleep(5)

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

    end_time = time.time()
    elapsed_time = end_time - start_time

    consumer = ReviewConsumer()

    try:
        while True:
            if consumer.consume():
                break
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
        print(f"Runtime: {elapsed_time / 60:.2f} minutes")
