from pathlib import Path
from urllib.request import urlretrieve
import argparse

TABLES = ("customers", "orders", "order_items", "order_payments", "order_reviews", "products", "sellers")
BASE = "https://raw.githubusercontent.com/alexcj10/olist-ecommerce-analytics/main/data/"

def download(destination):
    destination.mkdir(parents=True, exist_ok=True)
    for table in TABLES:
        name = f"olist_{table}_dataset.csv"
        final = destination / name
        if not final.exists():
            partial = destination / (name + ".part")
            urlretrieve(BASE + name, partial)
            partial.replace(final)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("destination", nargs="?", type=Path, default=Path("data"))
    download(parser.parse_args().destination)
