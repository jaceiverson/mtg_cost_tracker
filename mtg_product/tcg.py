import datetime as dt
import json
import os
from argparse import ArgumentParser

import requests
from rich import print

from messaging.send_msg import send_whats_app


def section_divider() -> None:
    """
    Prints '=' to the screen to separate sections
    """
    print("=" * 40)


def file_checks(product_ids: list) -> None:
    """
    Check if the files exist for a product ID
    outputs
    | {product_id}
    |   |  history/
    |   | {date}.json

    looks for the history directory and will create it and the product directory
    if necessary

    Params
    ------
    product_ids: list: A list of product IDs to check directories for
    """
    for product_id in product_ids:
        # Check if today's file exists
        if not os.path.exists(f"outputs/{product_id}/history/"):
            os.makedirs(f"outputs/{product_id}/history/", exist_ok=True)
            print(f"[blue]Made directory: outputs/{product_id}/history/[/blue]")


def read_in_products() -> dict:
    """
    Reads in the products from the products.json file
    found in the mtg_product directory
    """
    with open("mtg_product/products.json", "r") as f:
        return json.load(f)


def read_products_from_outputs(product_id: str, date: str) -> dict:
    """
    This function allows us to pull data from memory and not make the API
    calls. This helps avoid hitting the API when it isn't necessary

    Params
    ------
    product_id: str: The ID of the product to read data for
    date: str: The date of the product data to read formatted as: dt.date.today().isoformat()
    """
    file_path = f"outputs/{product_id}/{date}.json"
    if not os.path.exists(file_path):
        print(f"[red]File not found:[/red] {file_path}")
        return {}
    with open(file_path, "r") as f:
        return json.load(f)


def read_history_from_outputs(product_id: str, date: str) -> dict:
    """
    This function allows us to pull historical data from memory and not make the API
    calls. This helps avoid hitting the API when it isn't necessary

    Params
    ------
    product_id: str: The ID of the product to read data for
    date: str: The date of the product data to read formatted as: dt.date.today().isoformat()
    """
    file_path = f"outputs/{product_id}/history/{date}.json"
    if not os.path.exists(file_path):
        print(f"[red]File not found:[/red] {file_path}")
        return {}
    with open(file_path, "r") as f:
        return json.load(f)


def save_products(product_id: str, product_data: dict):
    """
    Given a product_id and an API response, save the data to the outputs directory

    Params
    ------
    product_id: str: The ID of the product to save data for
    product_data: dict: API response to save
    """
    file_path = f"outputs/{product_id}/{dt.date.today().isoformat()}.json"
    with open(file_path, "w") as f:
        json.dump(product_data, f)
    print(f"[green]Saved product data: {file_path}[/green]")


def save_history(product_id: str, product_data: dict):
    """
    Given a product_id and an API response, save the historical data to the outputs directory

    Params
    ------
    product_id: str: The ID of the product to save data for
    product_data: dict: historical API response to save
    """
    file_path = f"outputs/{product_id}/history/{dt.date.today().isoformat()}.json"
    with open(file_path, "w") as f:
        json.dump(product_data, f)
    print(f"[green]Saved product history: {file_path}[/green]")


def get_number_of_arrows(percent_change: float) -> int:
    """
    Given the percent_change calculate the number of emoji arrows to show
    We always want to show at least 1 arrow, then for each 10% change we add
    another up to a total of 5 arrows

    Params
    -----
    percent_change: float: The percent change to calculate arrows for

    Returns
    ------
    int: The number of arrows to display
    """
    int_percent = percent_change * 100
    if int_percent == 0:
        return 0
    if int_percent < 10 and int_percent > -10:
        return 1
    elif percent_change < 0:
        arrows = min(int(int_percent // -10) * -1, -1) - 1
    else:
        arrows = max(int(int_percent // 10), 1) + 1
    abs_arrows = min(abs(arrows), 5)
    return abs_arrows


def determine_change(product_history_data: list[dict], object_to_track: str) -> str:
    """
    Determine if the price went up or down or stayed the same.
    Adjust the price message depending on the comparison

    Params
    ------
    product_history_data: list[dict]: The historical data for the product
    object_to_track: str: the key in the dict object we want to track. This is either:
                            "marketPrice" or "transactionCount"

    Returns
    -------
    str: The formatted change message including today's data, last data, percent change, and arrows
    """
    todays_data = float(product_history_data[0][object_to_track])
    last_data = float(product_history_data[1][object_to_track])
    if last_data == 0:
        percent_change = 0.0
    else:
        percent_change = todays_data / last_data - 1
    number_of_arrows = get_number_of_arrows(percent_change)
    print(
        f"{object_to_track:<18} | TODAY: {todays_data:<6} | LAST: {last_data:<6} | %CHANGE: {f'{percent_change:0.2%}':<8} | ARROWS: {number_of_arrows:<4}"
    )
    if todays_data > last_data:
        return f"{todays_data} {'⬆️' * number_of_arrows} {percent_change:.2%}"
    elif todays_data < last_data:
        return f"{todays_data} {'⬇️' * number_of_arrows} {percent_change:.2%}"
    else:
        return f"{todays_data} ➡️ {percent_change:.2%}"


def build_product_url(product_id: str) -> str:
    """
    Given a product_id, build the TCGPlayer product URL

    Params
    ------
    product_id: str: The ID of the product to build the URL for

    Returns
    ------
    str: TCGplayer URL
    """
    return f"https://www.tcgplayer.com/product/{product_id}"


def make_tcg_request(product_id: str) -> dict:
    """
    Given a product_id make the API request to get the live product details

    Params
    ------
    product_id: str: The ID of the product to get details for

    Returns
    -------
    dict: The live product details
    """
    url = f"https://mp-search-api.tcgplayer.com/v2/product/{product_id}/details?range=quarter"
    response = requests.request("GET", url)
    save_products(product_id, response.json())
    return response.json()


def make_tcg_request_history(product_id: str) -> dict:
    """
    Given a product_id make the API request to get the product's historical data

    Params
    ------
    product_id: str: The ID of the product to get details for

    Returns
    -------
    dict: The historical product details
    """
    url = f"https://infinite-api.tcgplayer.com/price/history/{product_id}/detailed?range=quarter"
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    save_history(product_id, response.json())
    return response.json()


def parse_historical_data(list_of_costs: list[dict]) -> list[dict]:
    """
    Parse the historical data from the API response. To extract the information we care about

    Params
    ------
    list_of_costs: list: The list of historical cost data to parse

    Returns
    -------
    list[dict]: The parsed historical data
    """
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
    """
    Combine both today's and historical data to build the message to be sent
    Example output looks like this:

        Icetill Explorer
        • C: $13.25 ⬆️ 4.58%
        • T: 134.0 ⬇️⬇️⬇️⬇️ -33.33%
        https://www.tcgplayer.com/product/644286

    Params
    ------
    todays_data: dict: API response for live details
    historical_data: dict: API response for historical details

    Returns
    ------
    str: formatted message
    """
    product_name = todays_data["productName"]
    print(f"[blue]PRODUCT NAME:[/blue] {product_name}")
    price_string = determine_change(
        historical_data["result"][0]["buckets"], "marketPrice"
    )
    transaction_string = determine_change(
        historical_data["result"][0]["buckets"], "transactionCount"
    )
    product_url = build_product_url(int(todays_data["productId"]))
    return f"{product_name}\n• C: ${price_string}\n• T: {transaction_string}\n{product_url}\n\n"


def process_products(pull_fresh: bool):
    """
    main process for our pipeline. Follows these steps

    1. Read in products we care about
    2. Check to make sure the output directories exist. Create them if not
    3. Get the data to process each product by either:
        a. pulling the data via the API
        b. pulling the data from our output directory -- this requires a pull from today already taking place
    4. Parse the API responses and build a message for each product
    5. Combine the messages with a header and send them via WhatsApp

    Params
    ------
    pull_fresh: bool: Whether to pull fresh data from the API or use cached data
    """
    # 1
    products = read_in_products()
    # 2
    file_checks(products.keys())
    main_msg = f"MTG - Market Price Update\n{dt.date.today().isoformat()}\n----------\n"
    for product_id in products.keys():
        section_divider()
        print(f"[blue]Processing product:[/blue] {product_id}")
        # 3a
        if pull_fresh:
            print("[yellow]Pulling fresh data...[/yellow]")
            todays_costs = make_tcg_request(product_id)
            historical_costs = make_tcg_request_history(product_id)
        # 3b
        else:
            print("[yellow]Using cached data...[/yellow]")
            todays_costs = read_products_from_outputs(
                product_id, dt.date.today().isoformat()
            )
            historical_costs = read_history_from_outputs(
                product_id, dt.date.today().isoformat()
            )
        # 4
        msg = build_message(todays_costs, historical_costs)
        main_msg += msg
        section_divider()
    # 5
    print(f"[green]Message to be sent:[/green]\n{main_msg}")
    send_whats_app(main_msg)


def main():
    """
    script entry point. Accepts 1 argument

    Arguments
    ------
    -f / --pull-fresh | if included we will pull data from the API. not included by default
    """
    args = ArgumentParser()
    args.add_argument("-f", "--pull-fresh", action="store_true")
    parsed_args = args.parse_args()
    process_products(parsed_args.pull_fresh)


if __name__ == "__main__":
    main()
