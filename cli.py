import requests
import sys
import time
from base64 import urlsafe_b64encode

url = "https://wowless.dev/api/v1/run"


def run(product, filename):
    with open(filename, "rb") as f:
        r = requests.post(
            url,
            json={
                "products": [product],
                "zip": str(urlsafe_b64encode(f.read())),
            },
        )
    r.raise_for_status()
    runid = r.json()[product]
    wait = 5.0
    for i in range(50):
        wait = wait * 1.1
        time.sleep(wait)
        r = requests.get(url, params={"runid": runid})
        r.raise_for_status()
        logs = r.json()["rawlogs"]
        if logs:
            for k, v in logs.items():
                print(k)
                print(v)
            return


if __name__ == "__main__":
    run("wow_classic_era", sys.argv[1])
