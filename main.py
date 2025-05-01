import time

import requests
from hdfs import InsecureClient

from src import Config

if __name__ == "__main__":
    print("Sleeping for 30 seconds... Waiting for Hadoop to finish setup")

    time.sleep(30)
    url = Config.HDFS_CONNECTION_STRING.value

    # Wait for Namenode WebHDFS to become available
    max_retries = 30
    for i in range(max_retries):
        try:
            r = requests.get(f"{url}/webhdfs/v1/?op=GETHOMEDIRECTORY", timeout=5)
            if r.status_code == 200:
                print("✅ Namenode is up and responding.")
                break
            else:
                print(f"⚠️ Namenode responded with status {r.status_code}. Retrying...")
        except requests.exceptions.RequestException as e:
            print(f"⏳ Waiting for Namenode... ({i + 1}/{max_retries}) - {e}")
        time.sleep(3)
    else:
        raise RuntimeError("❌ Namenode didn't become available after waiting.")

    client = InsecureClient(url, user=Config.HDFS_USER.value)

    try:
        client.makedirs('/input')
    except Exception as e:
        print(f"ℹ️ Could not create '/input' dir (may already exist): {e}")

    client.upload('/input/', "./airline.csv", overwrite=True)
    print(client.content("/input/"))
