import datetime as dt
import json
import os

import requests
from rich import print

from messaging.send_msg import send_whats_app


def file_checks(product_ids: list):
    for product_id in product_ids:
        # Check if today's file exists
        if not os.path.exists(f"outputs/{product_id}/history/"):
            os.makedirs(f"outputs/{product_id}/history/", exist_ok=True)
            print(f"[blue]Made directory: outputs/{product_id}/history/[/blue]")


def read_in_products() -> dict:
    with open("mtg_product/products.json", "r") as f:
        return json.load(f)


def save_products(product_id: str, product_data: dict):
    file_path = f"outputs/{product_id}/{dt.date.today().isoformat()}.json"
    with open(file_path, "w") as f:
        json.dump(product_data, f)
    print(f"[green]Saved product data: {file_path}[/green]")


def save_history(product_id: str, product_data: dict):
    file_path = f"outputs/{product_id}/history/{dt.date.today().isoformat()}.json"
    with open(file_path, "w") as f:
        json.dump(product_data, f)
    print(f"[green]Saved product history: {file_path}[/green]")


def get_number_of_arrows(percent_change: float) -> int:
    int_percent = int(percent_change * 100)
    if int_percent == 0:
        return 0
    if int_percent < 10 and int_percent > -10:
        return 1
    elif percent_change < 0:
        arrows = min(int(int_percent // -10) * -1, -1) - 1
    else:
        arrows = max(int(int_percent // 10), 1) + 1
    print(f"[green]RAW ARROWS: {arrows}")
    abs_arrows = min(abs(arrows), 5)
    print(f"[green]ABS ARROWS: {abs_arrows}")
    return abs_arrows


def determine_change(product_history_data: list, object_to_track: str) -> str:
    """
    Determine if the price went up or down or stayed the same.
    Adjust the price message depending on the comparison
    """
    todays_data = float(product_history_data[0][object_to_track])
    last_data = float(product_history_data[1][object_to_track])
    if last_data == 0:
        percent_change = 0.0
    else:
        percent_change = todays_data / last_data - 1
    print(f"TODAY: {todays_data}")
    print(f"LAST: {last_data}")
    print(f"[green]PERCENT CHANGE: {percent_change}")
    number_of_arrows = get_number_of_arrows(percent_change)
    if todays_data > last_data:
        return f"{todays_data} {'⬆️' * number_of_arrows} {percent_change:.2%}"
    elif todays_data < last_data:
        return f"{todays_data} {'⬇️' * number_of_arrows} {percent_change:.2%}"
    else:
        return f"{todays_data} ➡️ {percent_change:.2%}"


def build_product_url(product_id: str) -> str:
    return f"https://www.tcgplayer.com/product/{product_id}"


def make_tcg_request(product_id: str) -> dict:
    url = f"https://mp-search-api.tcgplayer.com/v2/product/{product_id}/details?range=quarter"
    response = requests.request("GET", url)
    save_products(product_id, response.json())
    return response.json()


def make_tcg_request_history(product_id: str) -> dict:
    url = f"https://infinite-api.tcgplayer.com/price/history/{product_id}/detailed?range=quarter"
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    save_history(product_id, response.json())
    return response.json()


def parse_historical_data(list_of_costs: list):
    parsed_data = []
    for item in list_of_costs:
        parsed_data.append(
            {
                "date": item["bucketStartDate"],
                "marketPrice": item["marketPrice"],
                "quantitySold": item["quantitySold"],
                "transactionCount": item["transactionCount"],
            }
        )
    return parsed_data


def build_message(todays_data: dict, historical_data: dict) -> str:
    product_name = todays_data["productName"]
    price_string = determine_change(
        historical_data["result"][0]["buckets"], "marketPrice"
    )
    transaction_string = determine_change(
        historical_data["result"][0]["buckets"], "transactionCount"
    )
    product_url = build_product_url(int(todays_data["productId"]))
    return f"{product_name}\n• C: ${price_string}\n• T: {transaction_string}\n{product_url}\n\n"


def main():
    products = read_in_products()
    file_checks(products.keys())
    main_msg_title = (
        f"MTG - Market Price Update\n{dt.date.today().isoformat()}\n----------\n"
    )
    for product_id in products.keys():
        todays_costs = make_tcg_request(product_id)
        historical_costs = make_tcg_request_history(product_id)
        msg = build_message(todays_costs, historical_costs)
        msg = main_msg_title + msg
        print(f"[blue]Message to be sent:[/blue]\n{msg}")
        send_whats_app(msg)


if __name__ == "__main__":
    main()
