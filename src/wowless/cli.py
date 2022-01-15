import click
from progress.spinner import Spinner
import requests
import time
from base64 import urlsafe_b64encode
import sys

url = "https://wowless.dev/api/v1/run"


@click.command()
@click.option(
    "--product",
    "-p",
    required=True,
    type=click.Choice(
        [
            "wow",
            "wowt",
            "wow_classic",
            "wow_classic_ptr",
            "wow_classic_era",
            "wow_classic_era_ptr",
        ]
    ),
)
@click.argument("filename")
def run(product, filename):
    with open(filename, "rb") as f:
        r = requests.post(
            url,
            json={
                "products": [product],
                "zip": urlsafe_b64encode(f.read()).decode("ascii"),
            },
        )
    r.raise_for_status()
    runid = r.json()[product]
    wait = 1.0
    for _ in Spinner(f"waiting for runid {runid} to complete... ").iter(
        range(400)
    ):
        wait = wait * 1.1
        time.sleep(wait)
        r = requests.get(url, params={"runid": runid})
        r.raise_for_status()
        j = r.json()
        if "status" in j and j["status"] == "done":
            for k, v in j["rawlogs"].items():
                print(k)
                print(v, end="")
            return
    print("task never finished", file=sys.stderr)


if __name__ == "__main__":
    run()
