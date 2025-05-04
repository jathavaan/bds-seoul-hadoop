import os
import subprocess
import time

from hdfs import InsecureClient, HdfsError

from src import Config

if __name__ == "__main__":
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

    file_to_upload = os.path.join(os.getcwd(), "airline.csv")

    print(f"Uploading {file_to_upload} to HDFS...")
    client.upload(Config.HDFS_INPUT_PATH.value, file_to_upload, overwrite=True)
    print(f"File uploaded: {client.content(Config.HDFS_INPUT_PATH.value)}")

    # Paths to the Python scripts
    MAPPER_PATH = "./src/mapreduce/mapper.py"
    REDUCER_PATH = "./src/mapreduce/reducer.py"

    # Hadoop streaming jar location
    HADOOP_STREAMING_JAR = "/opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar"

    # HDFS input and output paths
    INPUT_PATH = Config.HDFS_INPUT_PATH.value
    OUTPUT_PATH = Config.HDFS_OUTPUT_PATH.value

    # Remove existing output dir if it exists
    print("Cleaning up old HDFS output directory (if any)...")
    subprocess.run([
        "hadoop", "fs", "-rm", "-r", OUTPUT_PATH
    ], stderr=subprocess.DEVNULL)

    # Extract filenames only for use in -mapper and -reducer arguments
    MAPPER_FILENAME = MAPPER_PATH.split("/")[-1]
    REDUCER_FILENAME = REDUCER_PATH.split("/")[-1]

    # Run Hadoop streaming job
    print("Running MapReduce job via Hadoop streaming...")
    streaming_command = [
        "hadoop", "jar", HADOOP_STREAMING_JAR,
        "-input", INPUT_PATH,
        "-output", OUTPUT_PATH,
        "-mapper", f"python3.11 {MAPPER_FILENAME}",
        "-reducer", f"python3.11 {REDUCER_FILENAME}",
        "-file", MAPPER_PATH,
        "-file", REDUCER_PATH
    ]

    # Optionally print for debugging
    print("Streaming command:\n", " ".join(streaming_command))

    # Execute
    subprocess.run(streaming_command, check=True)

    print("MapReduce job completed.")

    print("Fetching and displaying output from HDFS...")
    result = subprocess.run(
        ["hadoop", "fs", "-cat", os.path.join(OUTPUT_PATH, "part-*")],
        text=True,
        capture_output=True
    )

    print(result.stdout)
